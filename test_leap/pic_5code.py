# coding: utf-8

import glob
from pathlib import Path
import sys

import matplotlib
import pandas as pd
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from qar_common import configure_matplotlib, read_qar_csv

configure_matplotlib(plt)

## PITCH CAPT CMD POSITION 替换为 N1 ACTUAL (LOW ROTOR SPEED) SYS. 1
## ROLL CAPT CMD POSITION 替换为 N1 ACTUAL (LOW ROTOR SPEED) SYS. 1
## PITCH CAPT CMD POSITION 替换为 N1 ACTUAL (LOW ROTOR SPEED) SYS. 1
## PITCH CAPT CMD POSITION 替换为 N1 ACTUAL (LOW ROTOR SPEED) SYS. 1
## PITCH CAPT CMD POSITION 替换为 N1 ACTUAL (LOW ROTOR SPEED) SYS. 1
## PITCH CAPT CMD POSITION 替换为 N1 ACTUAL (LOW ROTOR SPEED) SYS. 1





def more_pic(paths=None, output_path="big_pic.png"):
    data1 = []
    paths = sorted(paths) if paths is not None else sorted(glob.glob("datas/*"))
    for path in paths:
        data = read_qar_csv(path).drop(
            index=0).reset_index(drop=True)
        data1.append(data)
    if not data1:
        raise ValueError("没有可分析的 LEAP CSV 文件")
    plt.figure(figsize=(50, 30))
    for dat1 in data1:
        ############################# 图1 ####################################

        N_U = [
            "PITCH CAPT CMD POSITION_58",
            "PITCH CAPT CMD POSITION_186",
            "PITCH CAPT CMD POSITION_314",
            "PITCH CAPT CMD POSITION_442",
            "PITCH CAPT CMD POSITION_570",
            "PITCH CAPT CMD POSITION_698",
            "PITCH CAPT CMD POSITION_826",
            "PITCH CAPT CMD POSITION_954",
        ]

        V_AC = [
            "ROLL CAPT CMD POSITION_46",
            "ROLL CAPT CMD POSITION_174",
            "ROLL CAPT CMD POSITION_302",
            "ROLL CAPT CMD POSITION_430",
            "ROLL CAPT CMD POSITION_558",
            "ROLL CAPT CMD POSITION_686",
            "ROLL CAPT CMD POSITION_814",
            "ROLL CAPT CMD POSITION_942"
        ]

        AQ = [
            "N1 ACTUAL (LOW ROTOR SPEED) SYS. 1"
        ]

        M = [
            "RADIO ALTITUDE SYS. 1_5"
        ]

        # 提取第一个条件大于等于50的索引

        con1 = dat1[AQ] >= 50
        sel1 = dat1.iloc[con1.values, :]

        # 提取全部N_U为负的值
        con2 = (((sel1[N_U] < 0).values).sum(axis=1) > 0)
        sel2 = sel1.iloc[con2, :]

        index1 = []

        for i in (sel2[M] > 50).index:
            index1.append(i)
            if sel2.loc[i, M].values > 50:
                break

        # 保存筛选后的数据
        pic1 = dat1.iloc[index1, :]

        y = pic1[N_U]
        x = pic1[V_AC]

        plt.subplot(241)
        # #去掉边框
        plt.gca().spines['right'].set_color('none')
        plt.gca().spines['top'].set_color('none')
        # 指定x与y轴
        plt.gca().xaxis.set_ticks_position('bottom')
        plt.gca().yaxis.set_ticks_position('left')
        # #设置x与y轴的位置
        plt.gca().spines['bottom'].set_position(('data', 0))
        plt.gca().spines['left'].set_position(('data', 0))  # 设置为(0,0)显示
        for i, j in zip(x.columns, y.columns):
            plt_x = x[i].astype(float)
            plt_y = y[j].astype(float)
            plt.scatter(plt_x * -1, plt_y * -1, alpha=0.15,
                        c='b',
                        s=15,
                        marker='o')

        plt.plot([-10, -10], [-10, 10], 'r')
        plt.plot([10, 10], [10, -10], 'r')
        plt.xticks(np.linspace(20, -20, 11),
                   list(np.linspace(-20, 20, 11).astype(int).astype(str)),
                   size=12)
        plt.yticks(np.linspace(16, -16, 8),
                   list(np.linspace(-16, 16, 8).astype(int).astype(str)),
                   size=12)
        plt.title("起飞50英尺以下杆量", size=15)
        ############################# 图2 ####################################
        plt.subplot(242)
        AD_AG = [
            "NOSE LANDING GEAR COMPRESSED SYS. 1_49",
            "NOSE LANDING GEAR COMPRESSED SYS. 1_305",
            "NOSE LANDING GEAR COMPRESSED SYS. 1_561",
            "NOSE LANDING GEAR COMPRESSED SYS. 1_817"
        ]

        BA_BD = [
            "PITCH ATTITUDE CAPT_44",
            "PITCH ATTITUDE CAPT_172",
            "PITCH ATTITUDE CAPT_300",
            "PITCH ATTITUDE CAPT_428",
            "PITCH ATTITUDE CAPT_556",
            "PITCH ATTITUDE CAPT_684",
            "PITCH ATTITUDE CAPT_812",
            "PITCH ATTITUDE CAPT_940",
        ]

        L = ["RADIO ALTITUDE SYS. 1_5"]

        E_H = [
            "GROUND FLIGHT BOOLEAN BSOL_26",
            "GROUND FLIGHT BOOLEAN BSOL_282",
            "GROUND FLIGHT BOOLEAN BSOL_538",
            "GROUND FLIGHT BOOLEAN BSOL_794"
        ]

        # 条件1
        con1 = (dat1[AD_AG] == "NOFALT").sum(axis=1) > 0

        for i in range(len(con1)):
            if con1[i]:
                i = i - 3
                break

        # 提取停止条件
        con2 = (dat1[L] > 50).values.flatten()

        for i2, c2 in enumerate(con2):
            if c2:
                break

        # 提取条件1数据
        pic2_data = dat1.loc[i:i2, BA_BD]

        # 标记点
        bjd = (dat1.loc[i:i2, E_H] == "NOACT").sum(axis=1) > 0

        bjd_index = np.where(bjd)[0][0]

        plt.plot(pic2_data.values.flatten())
        plt.plot(bjd_index * 4, pic2_data.values.flatten()[bjd_index * 4], 'o')
        plt.title('离地姿态')
        ############################# 图3 ####################################

        plt.subplot(243)
        I_M = [
            "RADIO ALTITUDE SYS. 1_1",
            "RADIO ALTITUDE SYS. 1_2",
            "RADIO ALTITUDE SYS. 1_3",
            "RADIO ALTITUDE SYS. 1_4",
            "RADIO ALTITUDE SYS. 1_5"
        ]

        N_U = [
            "PITCH CAPT CMD POSITION_58",
            "PITCH CAPT CMD POSITION_186",
            "PITCH CAPT CMD POSITION_314",
            "PITCH CAPT CMD POSITION_442",
            "PITCH CAPT CMD POSITION_570",
            "PITCH CAPT CMD POSITION_698",
            "PITCH CAPT CMD POSITION_826",
            "PITCH CAPT CMD POSITION_954"
        ]

        V_AC = [
            "ROLL CAPT CMD POSITION_46",
            "ROLL CAPT CMD POSITION_174",
            "ROLL CAPT CMD POSITION_302",
            "ROLL CAPT CMD POSITION_430",
            "ROLL CAPT CMD POSITION_558",
            "ROLL CAPT CMD POSITION_686",
            "ROLL CAPT CMD POSITION_814",
            "ROLL CAPT CMD POSITION_942"
        ]

        # 取第一个变化的值
        d1 = dat1[E_H] == 'ACTIVE'
        con1 = d1.sum(axis=1) < 4

        index1 = np.where(con1)[0][0]
        # 取出目标列所有的最大值
        max_data = dat1[I_M].max(axis=1)
        # 获取满足条件的索引
        index_list = []

        for i in reversed(max_data.index):
            if max_data[i] < 1000 and max_data[i] > 100:
                index_list.append(i)
            elif max_data[i] > 1000:
                break

        x = dat1.loc[index_list, V_AC].values.flatten()
        y = dat1.loc[index_list, N_U].values.flatten()

        # #去掉边框
        plt.gca().spines['right'].set_color('none')
        plt.gca().spines['top'].set_color('none')
        # 指定x与y轴
        plt.gca().xaxis.set_ticks_position('bottom')
        plt.gca().yaxis.set_ticks_position('left')
        # #设置x与y轴的位置
        plt.gca().spines['bottom'].set_position(('data', 0))
        plt.gca().spines['left'].set_position(('data', 0))  # 设置为(0,0)显示

        plt.scatter(x * -1, y * -1, alpha=0.15,
                    c='b',
                    s=15,
                    marker='o')
        plt.plot([-10, -10], [-10, 10], 'r')
        plt.plot([10, 10], [10, -10], 'r')

        plt.xticks(np.linspace(20, -20, 11),
                   list(np.linspace(-20, 20, 11).astype(int).astype(str)),
                   size=12)
        plt.yticks(np.linspace(16, -16, 8),
                   list(np.linspace(-16, 16, 8).astype(int).astype(str)),
                   size=12)
        plt.title("进近1000-100英尺杆量", size=15)
        ############################# 图4 ####################################
        plt.subplot(244, projection='polar')
        AU = [
            "WIND DIRECTION - TRUE"
        ]

        AP = [
            "RUNWAY HEADING (TAKE-OFF OR LANDING)"
        ]

        AV = [
            "WIND SPEED"
        ]

        pic4_data = dat1.iloc[index_list, :]

        theta = pic4_data[AU].dropna() - pic4_data[AP].dropna().values[0, 0]

        # 半径
        radii = pic4_data[AV].dropna().values.flatten()

        plt.bar(theta.values.flatten(), radii, width=0.02)
        plt.bar(0, max(radii), color='red', width=0.02)
        plt.title('进近1000-100英尺风向风速')
        ############################# 图5 ####################################
        plt.subplot(245)
        # 取第一个变化的值
        d1 = dat1[E_H] == 'ACTIVE'
        con1 = d1.sum(axis=1) < 4

        index1 = np.where(con1)[0][0]
        # 取出目标列所有的最大值
        max_data = dat1[I_M].max(axis=1)
        # 获取满足条件的索引
        index_list = []

        for i in reversed(max_data.index):
            if max_data[i] < 100 and max_data[i] > 0:
                index_list.append(i)
            elif max_data[i] > 100:
                break

        x = dat1.loc[index_list, V_AC].values.flatten()
        y = dat1.loc[index_list, N_U].values.flatten()

        # #去掉边框
        plt.gca().spines['right'].set_color('none')
        plt.gca().spines['top'].set_color('none')
        # 指定x与y轴
        plt.gca().xaxis.set_ticks_position('bottom')
        plt.gca().yaxis.set_ticks_position('left')
        # #设置x与y轴的位置
        plt.gca().spines['bottom'].set_position(('data', 0))
        plt.gca().spines['left'].set_position(('data', 0))  # 设置为(0,0)显示

        plt.scatter(x * -1, y * -1, alpha=0.15,
                    c='b',
                    s=15,
                    marker='o')
        plt.plot([-10, -10], [-10, 10], 'r')
        plt.plot([10, 10], [10, -10], 'r')

        plt.xticks(np.linspace(20, -20, 11),
                   list(np.linspace(-20, 20, 11).astype(int).astype(str)),
                   size=12)
        plt.yticks(np.linspace(16, -16, 8),
                   list(np.linspace(-16, 16, 8).astype(int).astype(str)),
                   size=12)
        plt.title("落地100英尺以下杆量", size=15)

        ############################# 图6 ####################################
        plt.subplot(246, projection='polar')
        # 取第一个变化的值
        d1 = dat1[E_H] == 'ACTIVE'
        con1 = d1.sum(axis=1) < 4

        index1 = np.where(con1)[0][0]
        # 取出目标列所有的最大值
        max_data = dat1[I_M].max(axis=1)
        # 获取满足条件的索引
        index_list = []

        for i in reversed(max_data.index):
            if max_data[i] < 100 and max_data[i] > 0:
                index_list.append(i)
            elif max_data[i] > 100:
                break

        pic6_data = dat1.iloc[index_list, :]

        theta = pic6_data[AU].dropna() - pic6_data[AP].dropna().values[0, 0]

        # 半径
        radii = pic6_data[AV].dropna().values.flatten()

        plt.bar(theta.values.flatten(), radii, width=0.02)
        plt.bar(0, max(radii), color='red', width=0.02)
        plt.title('100英尺以下风向风速')
        ############################# 图7 ####################################
        plt.subplot(247)
        AW_AZ = [
            "ROLL ANGLE SYS. 1_109",
            "ROLL ANGLE SYS. 1_237",
            # "ROLL ATTITUDE CAPT_568",
            # "ROLL ATTITUDE CAPT_824"
        ]

        # 取第一个变化的值
        d1 = dat1[E_H] == 'ACTIVE'
        con1 = d1.sum(axis=1) < 4

        index1 = np.where(con1)[0][0]
        # 取出目标列所有的最大值
        max_data = dat1[I_M].max(axis=1)
        # 获取满足条件的索引
        index_list = []

        for i in reversed(max_data.index):
            if max_data[i] < 50 and max_data[i] > 0:
                index_list.append(i)
            elif max_data[i] > 50:
                break

        pic7_data = dat1.iloc[index_list, :]

        y = -pic7_data[AW_AZ].values
        x = pic7_data[AW_AZ].values

        # 固定Y值
        for i in range(len(y.flatten())):
            plt.plot([-y.flatten()[i], y.flatten()[i]])

        plt.yticks(np.linspace(5, -5, 8),
                   size=12)
        plt.title("50英尺以下坡度")
        ############################# 图8 ####################################
        plt.subplot(248)

        J_M = [
            "RADIO ALTITUDE SYS. 1_1",
            "RADIO ALTITUDE SYS. 1_2",
            "RADIO ALTITUDE SYS. 1_3",
            "RADIO ALTITUDE SYS. 1_4",
            "RADIO ALTITUDE SYS. 1_5"
        ]

        AS = [
            "THRUST LEVER ANGLE POS SYS. 1"
        ]

        max_data = dat1[J_M].max(axis=1)

        index_list = []
        started = False
        for i in reversed(max_data.index):
            if dat1.loc[i, E_H[0]] == "NOACT" and dat1.loc[i, E_H[1]] == "NOACT" and dat1.loc[i, E_H[2]] == "NOACT" and \
                    dat1.loc[i, E_H[3]] == "NOACT":
                started = True
            if started and max_data[i] < 50 and max_data[i] > 0:
                index_list.append(i)
            elif started and max_data[i] > 50:
                break

        sort_value = pd.Series(index_list).sort_values(ascending=True).values

        indexs = dat1.loc[sort_value, J_M].index
        data8 = dat1.loc[sort_value, I_M].values

        data8 = np.array([sorted(i, reverse=True) for i in data8]).flatten()
        dt = dat1.loc[indexs, AS].values

        for d in range(len(dt)):
            if dt[d] < 0:
                break

        plt.plot(data8)
        plt.plot(d * 4 + 1, data8[d * 4 + 1], 'o')
        plt.xticks(
            np.linspace(0, len(data8), 4),
            list((np.linspace(0, len(data8), 4) / 4).astype(int).astype(str)),
            size=12)
        plt.title("收油门高度")


    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()


if __name__ == "__main__":
    more_pic()
