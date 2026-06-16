# QAR 飞机起降数据批量分析工具

本项目用于批量分析三种发动机型号飞机的起降数据：CFM、LEAP、PW。程序会按人员和机型遍历 CSV 数据，分别调用对应机型的分析脚本生成图像，并将结果保存到主目录下的 `pics` 文件夹。

## 目录结构

```text
F:\qar_test
├── data/              # 人员数据目录
│   ├── 人员姓名/
│   │   ├── cfm/       # CFM 数据
│   │   ├── leap/      # LEAP 数据
│   │   └── pw/        # PW 数据
├── test_cfm/          # CFM 分析脚本
├── test_leap/         # LEAP 分析脚本
├── test_pw/           # PW 分析脚本
├── pics/              # 输出图片目录
├── run_batch.py       # 批量分析入口
├── qar_common.py      # 公共 CSV 读取和绘图配置
└── AGENTS.md          # 项目任务和数据规则说明
```

## 数据命名规则

- 文件名包含 `qlzlly`：LEAP 数据。
- 文件名包含 `qlz` 且不包含 `qlzlly`：CFM 数据。
- 文件名包含 `lly` 且不包含 `qlzlly`：PW 数据。

如果某个人员的机型文件夹中出现不匹配的数据文件，程序会弹窗提示该人员对应机型的数据错误，并跳过该机型分析。

## 启动方式

在 PowerShell 中进入项目目录：

```powershell
cd F:\qar_test
python run_batch.py
```

如果 `python` 命令不可用，可尝试：

```powershell
py run_batch.py
```

启动后选择数据根目录，例如：

```text
F:\qar_test\data
```

程序会显示进度窗口，包括当前人员、当前机型、当前进度和当前处理状态。

## 输出规则

分析结果保存到：

```text
F:\qar_test\pics
```

图片命名格式为：

```text
人员姓名_机型.png
```

例如：

```text
黄骏_CFM.png
黄骏_LEAP.png
黄骏_PW.png
```

如果同名图片已存在，程序会自动追加编号，避免覆盖旧结果，例如 `黄骏_CFM_1.png`。

## 编码说明

项目 Python 源码使用 UTF-8 编码。CSV 读取时会依次尝试 `utf-8`、`utf-8-sig`、`gb18030`、`cp936`，以兼容不同来源的数据文件并减少中文乱码问题。
