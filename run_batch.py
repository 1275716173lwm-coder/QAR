# coding: utf-8

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import traceback


ROOT_DIR = Path(__file__).resolve().parent
PICS_DIR = ROOT_DIR / "pics"


@dataclass
class AnalysisTask:
    person: str
    aircraft: str
    paths: list
    output_path: Path


AIRCRAFT_DIRS = {
    "cfm": "CFM",
    "leap": "LEAP",
    "pw": "PW",
}

MODULE_PATHS = {
    "CFM": ROOT_DIR / "test_cfm" / "pic_code.py",
    "LEAP": ROOT_DIR / "test_leap" / "pic_5code.py",
    "PW": ROOT_DIR / "test_pw" / "pic_code.py",
}


def classify_csv(path):
    name = path.name.lower()
    has_qlzlly = "qlzlly" in name
    has_qlz = "qlz" in name
    has_lly = "lly" in name

    if has_qlzlly:
        return "LEAP"
    if has_qlz:
        return "CFM"
    if has_lly:
        return "PW"
    return None


def unique_output_path(person, aircraft):
    PICS_DIR.mkdir(parents=True, exist_ok=True)
    base = PICS_DIR / f"{person}_{aircraft}.png"
    if not base.exists():
        return base

    index = 1
    while True:
        candidate = PICS_DIR / f"{person}_{aircraft}_{index}.png"
        if not candidate.exists():
            return candidate
        index += 1


def scan_data_root(data_root):
    tasks = []
    skipped = []
    errors = []

    for person_dir in sorted((p for p in data_root.iterdir() if p.is_dir()), key=lambda p: p.name.lower()):
        aircraft_dirs = {}
        for child in person_dir.iterdir():
            if child.is_dir() and child.name.lower() in AIRCRAFT_DIRS:
                aircraft_dirs[child.name.lower()] = child

        for dir_key in ("cfm", "leap", "pw"):
            aircraft = AIRCRAFT_DIRS[dir_key]
            aircraft_dir = aircraft_dirs.get(dir_key)
            if aircraft_dir is None:
                skipped.append((person_dir.name, aircraft, "缺少机型文件夹"))
                continue

            csv_paths = sorted(aircraft_dir.glob("*.csv"), key=lambda p: p.name.lower())
            if not csv_paths:
                skipped.append((person_dir.name, aircraft, "没有 CSV 文件"))
                continue

            wrong_paths = [path for path in csv_paths if classify_csv(path) != aircraft]
            if wrong_paths:
                bad_names = "、".join(path.name for path in wrong_paths[:5])
                if len(wrong_paths) > 5:
                    bad_names += f" 等 {len(wrong_paths)} 个文件"
                errors.append((person_dir.name, aircraft, f"{person_dir.name} 的 {aircraft} 数据错误：{bad_names}"))
                continue

            tasks.append(
                AnalysisTask(
                    person=person_dir.name,
                    aircraft=aircraft,
                    paths=csv_paths,
                    output_path=unique_output_path(person_dir.name, aircraft),
                )
            )

    return tasks, skipped, errors


def load_analysis_modules():
    modules = {}
    for aircraft, module_path in MODULE_PATHS.items():
        spec = importlib.util.spec_from_file_location(f"qar_{aircraft.lower()}_analysis", module_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"无法加载 {aircraft} 分析模块：{module_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules[aircraft] = module
    return modules


class ProgressWindow:
    def __init__(self, root, total):
        self.root = root
        self.total = total
        self.done = 0

        root.title("QAR 批量分析进度")
        root.geometry("520x210")
        root.resizable(False, False)

        self.person_var = tk.StringVar(value="当前人员：等待开始")
        self.aircraft_var = tk.StringVar(value="当前机型：-")
        self.progress_var = tk.StringVar(value=f"进度：0 / {total}")
        self.status_var = tk.StringVar(value="当前状态：正在准备")

        frame = ttk.Frame(root, padding=18)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, textvariable=self.person_var).pack(anchor="w", pady=(0, 6))
        ttk.Label(frame, textvariable=self.aircraft_var).pack(anchor="w", pady=(0, 6))
        ttk.Label(frame, textvariable=self.progress_var).pack(anchor="w", pady=(0, 10))

        self.progress = ttk.Progressbar(frame, maximum=max(total, 1), mode="determinate")
        self.progress.pack(fill="x", pady=(0, 12))

        ttk.Label(frame, textvariable=self.status_var, wraplength=470).pack(anchor="w")

    def update_status(self, person=None, aircraft=None, status=None, done=None):
        if person is not None:
            self.person_var.set(f"当前人员：{person}")
        if aircraft is not None:
            self.aircraft_var.set(f"当前机型：{aircraft}")
        if status is not None:
            self.status_var.set(f"当前状态：{status}")
        if done is not None:
            self.done = done
            self.progress["value"] = done
            self.progress_var.set(f"进度：{done} / {self.total}")


def worker(tasks, modules, events):
    completed = 0
    failures = []
    total = len(tasks)

    for index, task in enumerate(tasks, start=1):
        events.put(("status", task.person, task.aircraft, "正在读取 CSV", completed))
        try:
            events.put(("status", task.person, task.aircraft, "正在生成图片", completed))
            modules[task.aircraft].more_pic(
                [str(path) for path in task.paths],
                str(task.output_path),
            )
            completed += 1
            events.put(("status", task.person, task.aircraft, f"已生成：{task.output_path.name}", completed))
        except Exception as exc:
            failures.append((task.person, task.aircraft, str(exc), traceback.format_exc()))
            completed += 1
            events.put(("status", task.person, task.aircraft, "分析失败，已继续后续任务", completed))

    events.put(("done", total - len(failures), failures))


def show_initial_errors(errors):
    if not errors:
        return
    lines = [message for _, _, message in errors[:10]]
    if len(errors) > 10:
        lines.append(f"还有 {len(errors) - 10} 条错误未显示。")
    messagebox.showwarning("数据校验错误", "\n".join(lines))


def run_progress_window(tasks, skipped, validation_errors):
    root = tk.Tk()
    progress_window = ProgressWindow(root, len(tasks))
    events = queue.Queue()

    try:
        modules = load_analysis_modules()
    except Exception as exc:
        messagebox.showerror("加载失败", f"分析模块加载失败：\n{exc}")
        root.destroy()
        return

    thread = threading.Thread(target=worker, args=(tasks, modules, events), daemon=True)
    thread.start()

    def poll_events():
        try:
            while True:
                event = events.get_nowait()
                if event[0] == "status":
                    _, person, aircraft, status, done = event
                    progress_window.update_status(person, aircraft, status, done)
                elif event[0] == "done":
                    _, completed, failures = event
                    progress_window.update_status(status="全部任务处理完成", done=len(tasks))
                    total_errors = len(validation_errors) + len(failures)
                    summary = (
                        f"批量分析完成。\n\n"
                        f"成功：{completed}\n"
                        f"跳过：{len(skipped)}\n"
                        f"错误：{total_errors}\n\n"
                        f"图片目录：{PICS_DIR}"
                    )
                    if failures:
                        first_failure = failures[0]
                        summary += f"\n\n首个分析失败：{first_failure[0]} {first_failure[1]}：{first_failure[2]}"
                    messagebox.showinfo("完成", summary)
                    root.destroy()
                    return
        except queue.Empty:
            pass
        root.after(150, poll_events)

    root.after(150, poll_events)
    root.mainloop()


def main():
    selector = tk.Tk()
    selector.withdraw()
    selector.update()
    selected = filedialog.askdirectory(title="请选择数据文件夹", initialdir=str(ROOT_DIR / "data"))
    selector.destroy()

    if not selected:
        return

    data_root = Path(selected)
    if not data_root.exists() or not data_root.is_dir():
        messagebox.showerror("路径错误", "选择的数据文件夹不存在。")
        return

    tasks, skipped, validation_errors = scan_data_root(data_root)
    show_initial_errors(validation_errors)

    if not tasks:
        messagebox.showinfo(
            "没有可分析数据",
            f"没有找到可分析的人员机型数据。\n\n跳过：{len(skipped)}\n错误：{len(validation_errors)}",
        )
        return

    run_progress_window(tasks, skipped, validation_errors)


if __name__ == "__main__":
    main()
