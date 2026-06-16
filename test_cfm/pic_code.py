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

from qar_common import configure_matplotlib, numeric_array, numeric_columns, read_qar_csv

configure_matplotlib(plt)


#解决中文显示问题


def pic_main(path):
    data = read_qar_csv(path).drop(index=0).reset_index(drop=True)

    DS = 'N1 Actual Eng 1'
    F = 'Radio Height 1_1'

    BD_BK = ['Capt Pitch Command Positi_1',
             'Capt Pitch Command Positi_2',
             'Capt Pitch Command Positi_3',
             'Capt Pitch Command Positi_4',
             'Capt Pitch Command Positi_5',
             'Capt Pitch Command Positi_6',
             'Capt Pitch Command Positi_7',
             'Capt Pitch Command Positi_8']

    BL_BS = ['Capt Roll Command Positio_1',
             'Capt Roll Command Positio_2',
             'Capt Roll Command Positio_3',
             'Capt Roll Command Positio_4',
             'Capt Roll Command Positio_5',
             'Capt Roll Command Positio_6',
             'Capt Roll Command Positio_7',
             'Capt Roll Command Positio_8'
             ]

    data1 = data.copy()

    DS = 'N1 Actual Eng 1'
    F = 'Radio Height 1_1'

    BD_BK = ['Capt Pitch Command Positi_1',
             'Capt Pitch Command Positi_2',
             'Capt Pitch Command Positi_3',
             'Capt Pitch Command Positi_4',
             'Capt Pitch Command Positi_5',
             'Capt Pitch Command Positi_6',
             'Capt Pitch Command Positi_7',
             'Capt Pitch Command Positi_8']

    BL_BS = ['Capt Roll Command Positio_1',
             'Capt Roll Command Positio_2',
             'Capt Roll Command Positio_3',
             'Capt Roll Command Positio_4',
             'Capt Roll Command Positio_5',
             'Capt Roll Command Positio_6',
             'Capt Roll Command Positio_7',
             'Capt Roll Command Positio_8'
             ]

    data_F = data1[data1[F].astype(float) > 10].index
    df_F = data1.iloc[data_F, :]
    df_DS = df_F[df_F[DS].astype(float) >= 50]

    x = df_DS[BL_BS]
    y = df_DS[BD_BK]

    # 图1

    fig = plt.figure(figsize=(8, 6))
    ax = plt.gca()
    # #去掉边框
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    # 指定x与y轴
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    # #设置x与y轴的位置
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))  # 设置为(0,0)显示

    plt.title("pic_1 RA_10", size=15)
    for i, j in zip(x.columns, y.columns):
        plt_x = x[i].astype(float)
        plt_y = y[j].astype(float)

        plt.scatter(plt_x, plt_y * -1, alpha=0.8,
                    c='b',
                    s=15,
                    marker='o')

    plt.plot([-10, -10], [-10, 10], 'r')
    # plt.plot([-5,5], [5,5], 'r')
    plt.plot([10, 10], [10, -10], 'r')
    # plt.plot([5,-5], [-5,-5], 'r')
    plt.xticks(np.linspace(20, -20, 11), size=12)
    plt.yticks(np.linspace(16, -16, 8),
               list(np.linspace(-16, 16, 8).astype(int).astype(str)),
               size=12)
    plt.show()

    # X轴大于10 标记红色

    # 图2
    D_E = [
        'AIRCRAFT ON GROUND (CFM)_592',
        'AIRCRAFT ON GROUND (CFM)_599'
    ]

    EX_FA = [
        'LANDING GEAR NOSE_1',
        'LANDING GEAR NOSE_2',
        'LANDING GEAR NOSE_3',
        'LANDING GEAR NOSE_4',
    ]

    X_AD = [
        'Pitch attitude CA_1',
        'Pitch attitude CA_2',
        'Pitch attitude CA_3',
        'Pitch attitude CA_4',
        'Pitch attitude CA_5',
        'Pitch attitude CA_6',
        'Pitch attitude CA_7',
    ]

    F_M = [
        'Radio Height 1_1',
        'Radio Height 1_2',
        'Radio Height 1_3',
        'Radio Height 1_4',
        'Radio Height 2_1',
        'Radio Height 2_2',
        'Radio Height 2_3',
        'Radio Height 2_4',
    ]

    # EX_FA

    fil2_data = data[(data[EX_FA] == 'AIR').sum(axis=1) > 0]

    ea_index = (data[EX_FA] == 'AIR').sum(axis=1)

    index_list = []

    for i in ea_index.index:
        if ea_index[i] > 0:
            index_list.append(ea_index.index[i])
            index_list.append(ea_index.index[i] - 1)
            index_list.append(ea_index.index[i] - 2)
            index_list.append(ea_index.index[i] - 3)

    save_index1 = np.unique(index_list)

    index1 = pd.DataFrame({'index': save_index1})

    # 特征筛选2

    indexs2 = data[F_M].max(axis=1)

    for i in range(len(indexs2)):
        if indexs2[i] > 50:
            break

    save_index2 = indexs2[:i].index

    index2 = pd.DataFrame({'index': save_index2})

    # 合并索引

    save_index = pd.merge(index1, index2, how='inner')

    # save_df = fil2_data[fil2_data[F_M].max(axis=1) < 50]

    pic2_df = data.loc[save_index.values.flatten(), :]
    # 条件1筛选
    d1 = (pic2_df[D_E[1]] == 'NO').astype(int)
    d2 = (pic2_df[D_E[0]] == 'YES').astype(int)
    select_yn = d1 - d2 > 0

    index_list = []

    for i in select_yn.index:

        if select_yn[i] == True:
            index_list.append(i)
            break

    num = np.where(select_yn.index == index_list[0])[0]

    plt_x = pic2_df.loc[:, X_AD].values.flatten().astype(float)
    plt.figure(figsize=(10, 6))
    plt.plot(plt_x)
    plt.xticks(
        np.linspace(0, len(plt_x), 8),
        list((np.linspace(0, len(plt_x), 8) / 8).astype(int).astype(str)),
        size=12)

    line_plot = pic2_df.loc[index_list[0], X_AD].values.flatten().astype(float)[0]
    plt.plot(num * 7, line_plot, 'o')
    plt.title('图2')
    plt.show()

    #  YES变NO 标红  打点

    F_M = [
        'Radio Height 1_1',
        'Radio Height 1_2',
        'Radio Height 1_3',
        'Radio Height 1_4',
        'Radio Height 2_1',
        'Radio Height 2_2',
        'Radio Height 2_3',
        'Radio Height 2_4',
    ]

    BD_BK = ['Capt Pitch Command Positi_1',
             'Capt Pitch Command Positi_2',
             'Capt Pitch Command Positi_3',
             'Capt Pitch Command Positi_4',
             'Capt Pitch Command Positi_5',
             'Capt Pitch Command Positi_6',
             'Capt Pitch Command Positi_7',
             'Capt Pitch Command Positi_8'
             ]

    BL_BS = ['Capt Roll Command Positio_1',
             'Capt Roll Command Positio_2',
             'Capt Roll Command Positio_3',
             'Capt Roll Command Positio_4',
             'Capt Roll Command Positio_5',
             'Capt Roll Command Positio_6',
             'Capt Roll Command Positio_7',
             'Capt Roll Command Positio_8'
             ]

    # 条件1筛选
    d1 = (data[D_E[1]] == 'NO').astype(int)
    d2 = (data[D_E[0]] == 'YES').astype(int)
    select_yn = d1 - d2 > 0

    D_E_index = data[:][select_yn].index.values
    # index_list = [i for i in range(D_E_index[0])]

    # 条件2 通过阈值筛选数据

    # 提取每一列最大最

    max_data = data[F_M].max(axis=1)

    # 将所有满足条件的索引添加进来
    index_list = []

    for i in reversed(max_data.index):
        if max_data[i] < 1000 and max_data[i] > 100:
            index_list.append(i)
        elif max_data[i] > 1000:
            break

    # up_fm = (data[F_M].astype(float)>100).max(axis=1)
    # down_fm = (data[F_M].astype(float)<1500).max(axis=1)
    # merge_fm = up_fm + down_fm > 0

    x = data.loc[index_list, BD_BK].values.flatten()
    y = data.loc[index_list, BL_BS].values.flatten()

    fig = plt.figure(figsize=(8, 6))
    ax = plt.gca()
    # #去掉边框
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    # 指定x与y轴
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    # #设置x与y轴的位置
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))  # 设置为(0,0)显示

    plt.title("pic_3", size=15)

    # for i,j in zip(x.columns,y.columns):
    #     plt_x = x[i].astype(float)
    #     plt_y = y[j].astype(float)

    #     plt.scatter(plt_x, plt_y*-1, alpha=0.8,
    #                 c='b',
    #                 s=15,
    #                 marker='o')

    plt.scatter(x, y * -1, alpha=0.8,
                c='b',
                s=15,
                marker='o')
    plt.plot([-10, -10], [-10, 10], 'r')
    # plt.plot([-5,5], [5,5], 'r')
    plt.plot([10, 10], [10, -10], 'r')
    # plt.plot([5,-5], [-5,-5], 'r')

    plt.xticks(np.linspace(20, -20, 11), size=12)
    plt.yticks(np.linspace(16, -16, 8),
               list(np.linspace(-16, 16, 8).astype(int).astype(str)),
               size=12)
    plt.show()

    ## X 轴大于10标记红色

    ## 图4

    FR = [
        'RUNWAY HEADING'
    ]

    DL = [
        'Wind direction true'
    ]

    DM = [
        'Wind speed'
    ]

    index_list = []

    for i in reversed(max_data.index):
        if max_data[i] < 1000 and max_data[i] > 100:
            index_list.append(i)
        elif max_data[i] > 1000:
            break

    pic4_data = data.iloc[index_list, :]

    FR_values = np.unique(pic4_data[FR].dropna().values)[0]

    theta = (pic4_data[DL].values - FR_values).flatten()

    # 半径
    radii = pic4_data[DM].values.flatten()

    plt.figure(figsize=(6, 6))
    plt.subplot(projection='polar')

    plt.bar(theta, radii, width=0.01)
    plt.bar(FR_values, max(radii), color='red', width=0.01)  # 给FR标记一个其他颜色

    plt.title('图4')
    plt.show()

    # 图5

    # 将所有满足条件的索引添加进来
    index_list = []

    for i in reversed(max_data.index):
        if max_data[i] < 100 and max_data[i] > 0:
            index_list.append(i)
        elif max_data[i] > 100:
            break

    # up_fm = (data[F_M].astype(float)>100).max(axis=1)
    # down_fm = (data[F_M].astype(float)<1500).max(axis=1)
    # merge_fm = up_fm + down_fm > 0

    y = data.loc[index_list, BD_BK]
    x = data.loc[index_list, BL_BS]

    fig = plt.figure(figsize=(8, 6))
    ax = plt.gca()
    # #去掉边框
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    # 指定x与y轴
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    # #设置x与y轴的位置
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))  # 设置为(0,0)显示

    plt.title("pic_5", size=15)

    for i, j in zip(x.columns, y.columns):
        plt_x = x[i].astype(float)
        plt_y = y[j].astype(float)

        plt.scatter(plt_x, plt_y * -1, alpha=0.8,
                    c='b',
                    s=15,
                    marker='o')
    plt.plot([-10, -10], [-5, 5], 'r')
    plt.plot([-10, 10], [5, 5], 'r')
    plt.plot([10, 10], [5, -5], 'r')
    plt.plot([-10, 10], [-5, -5], 'r')

    plt.xticks(np.linspace(20, -20, 11), size=12)
    plt.yticks(np.linspace(16, -16, 8),
               list(np.linspace(-16, 16, 8).astype(int).astype(str)),
               size=12)
    plt.show()

    # 图6

    # 将所有满足条件的索引添加进来
    index_list = []

    for i in reversed(max_data.index):
        if max_data[i] < 100 and max_data[i] > 0:
            index_list.append(i)
        elif max_data[i] > 100:
            break

    pic6_data = data.iloc[index_list, :]

    theta = (pic6_data[DL].values - np.unique(pic6_data[FR].dropna().values)[0]).flatten()

    # 半径
    radii = pic6_data[DM].values.flatten()

    plt.figure(figsize=(6, 6))
    plt.subplot(projection='polar')

    plt.bar(theta, radii, width=0.01)
    plt.bar(FR_values, max(radii), color='red', width=0.01)  # 给FR标记一个其他颜色
    plt.title('图6')
    plt.show()

    # 图7

    AN_AR = [
        'Roll attitude CA_1',
        'Roll attitude CA_2',
        'Roll attitude CA_3',
        'Roll attitude CA_4',
    ]

    # 将所有满足条件的索引添加进来
    index_list = []

    for i in reversed(max_data.index):
        if max_data[i] < 100 and max_data[i] > 0:
            index_list.append(i)
        elif max_data[i] > 100:
            break

    pic7_data = data.iloc[index_list, :]

    y = -pic7_data[AN_AR].values
    x = pic7_data[AN_AR].values

    # 固定Y值
    for i in range(len(y.flatten())):
        plt.plot([-y.flatten()[i], y.flatten()[i]])

    plt.yticks(np.linspace(5, -5, 8),
               size=12)
    plt.show()

    CN = [
        'Throttle lever angle Eng1_1'
    ]

    F_I = [
        'Radio Height 1_1',
        'Radio Height 1_2',
        'Radio Height 1_3',
        'Radio Height 1_4',
    ]

    sort_value = pd.Series(index_list).sort_values(ascending=True).values

    plt.figure(figsize=(10, 8))

    indexs = data.loc[sort_value, F_I].index
    data8 = data.loc[sort_value, F_I].values.flatten()
    plt_x8 = data8[data8 < 50]
    dt = data.loc[indexs, CN].values

    for d in range(len(dt)):
        if dt[d] < 0:
            break

    plt.plot(plt_x8)
    plt.plot(len(data8) - len(plt_x8), data8[d * 4], 'o')
    plt.xticks(
        np.linspace(0, len(plt_x8), 4),
        list((np.linspace(0, len(plt_x8), 4) / 4).astype(int).astype(str)),
        size=12)
    plt.show()


def big_main(path, output_path="big_pic.png"):

    data = read_qar_csv(path).drop(
        index=0).reset_index(drop=True)

    data1 = data.copy()

    DY = 'N1 Actual Eng 1'

    F = 'RADIO HEIGHT (R/A1) SYS. 1_1'

    BJ_BQ = ['Capt Pitch Command Positi_1',
             'Capt Pitch Command Positi_2',
             'Capt Pitch Command Positi_3',
             'Capt Pitch Command Positi_4',
             'Capt Pitch Command Positi_5',
             'Capt Pitch Command Positi_6',
             'Capt Pitch Command Positi_7',
             'Capt Pitch Command Positi_8',]

    BD_BK = ['Capt Pitch Command Positi_1',
             'Capt Pitch Command Positi_2',
             'Capt Pitch Command Positi_3',
             'Capt Pitch Command Positi_4',
             'Capt Pitch Command Positi_5',
             'Capt Pitch Command Positi_6',
             'Capt Pitch Command Positi_7',
             'Capt Pitch Command Positi_8']

    BL_BS = ['Capt Roll Command Positio_1',
             'Capt Roll Command Positio_2',
             'Capt Roll Command Positio_3',
             'Capt Roll Command Positio_4',
             'Capt Roll Command Positio_5',
             'Capt Roll Command Positio_6',
             'Capt Roll Command Positio_7',
             'Capt Roll Command Positio_8'
             ]

    data_F = data1[data1[F].astype(float) < 50].index
    df_F = data1.iloc[data_F, :]

    df_DS = df_F[df_F[DY].astype(float) >= 50]

    for i in range(1, len(df_DS[BD_BK].index)):
        if df_DS[BD_BK].index[i] - df_DS[BD_BK].index[i - 1] > 2:
            break

    indexs = df_DS[BD_BK].index[:i - 1].values

    df_DS_select = df_DS.loc[indexs, BD_BK][(df_DS.loc[indexs, BD_BK].astype(float) >= 0).sum(axis=1) == 0].index

    x = df_DS.loc[df_DS_select, BL_BS]
    y = df_DS.loc[df_DS_select, BD_BK]

    plt.figure(figsize=(30, 14))
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

    plt.title("起飞50英尺以下杆量", size=15)
    for i, j in zip(x.columns, y.columns):
        plt_x = x[i].astype(float)
        plt_y = y[j].astype(float)
        plt.scatter(plt_x, plt_y * -1, alpha=0.15,
                    c='b',
                    s=15,
                    marker='o')

    plt.plot([-10, -10], [-10, 10], 'r')
    # plt.plot([-5,5], [5,5], 'r')
    plt.plot([10, 10], [10, -10], 'r')
    # plt.plot([5,-5], [-5,-5], 'r')
    plt.xticks(np.linspace(20, -20, 11), size=12)
    plt.yticks(np.linspace(16, -16, 8),
               list(np.linspace(-16, 16, 8).astype(int).astype(str)),
               size=12)
    # plt.show()

    plt.subplot(242)
    # 图2
    D_E = [
        'AIRCRAFT ON GROUND (CFM)_592',
        'AIRCRAFT ON GROUND (CFM)_599'
    ]

    EX_FA = [
        'LANDING GEAR NOSE_1',
        'LANDING GEAR NOSE_2',
        'LANDING GEAR NOSE_3',
        'LANDING GEAR NOSE_4',
    ]

    X_AD = [
        'Pitch attitude CA_1',
        'Pitch attitude CA_2',
        'Pitch attitude CA_3',
        'Pitch attitude CA_4',
        'Pitch attitude CA_5',
        'Pitch attitude CA_6',
        'Pitch attitude CA_7',
    ]

    F_M = [
        'RADIO HEIGHT (R/A1) SYS. 1_1',
        'RADIO HEIGHT (R/A1) SYS. 1_2',
        'RADIO HEIGHT (R/A1) SYS. 1_3',
        'RADIO HEIGHT (R/A1) SYS. 1_4',
        'RADIO HEIGHT (R/A1) SYS. 2_1',
        'RADIO HEIGHT (R/A1) SYS. 2_2',
        'RADIO HEIGHT (R/A1) SYS. 2_3',
        'RADIO HEIGHT (R/A1) SYS. 2_4',
    ]

    # EX_FA

    fil2_data = data[(data[EX_FA] == 'AIR').sum(axis=1) > 0]

    ea_index = (data[EX_FA] == 'AIR').sum(axis=1)

    index_list = []

    for i in ea_index.index:
        if ea_index[i] > 0:
            index_list.append(ea_index.index[i])
            index_list.append(ea_index.index[i] - 1)
            index_list.append(ea_index.index[i] - 2)
            index_list.append(ea_index.index[i] - 3)

    save_index1 = np.unique(index_list)

    index1 = pd.DataFrame({'index': save_index1})

    # 特征筛选2

    indexs2 = data[F_M].max(axis=1)

    for i in range(len(indexs2)):
        if indexs2[i] > 50:
            break

    save_index2 = indexs2[:i].index

    index2 = pd.DataFrame({'index': save_index2})

    # 合并索引

    save_index = pd.merge(index1, index2, how='inner')

    # save_df = fil2_data[fil2_data[F_M].max(axis=1) < 50]

    pic2_df = data.loc[save_index.values.flatten(), :]
    # 条件1筛选
    d1 = (pic2_df[D_E[1]] == 'NO').astype(int)
    d2 = (pic2_df[D_E[0]] == 'YES').astype(int)
    select_yn = d1 - d2 > 0

    index_list = []

    for i in select_yn.index:

        if select_yn[i] == True:
            index_list.append(i)
            break

    num = np.where(select_yn.index == index_list[0])[0]

    plt_x = pic2_df.loc[:, X_AD].values.flatten().astype(float)
    plt.plot(plt_x)
    plt.xticks(
        np.linspace(0, len(plt_x), 8),
        list((np.linspace(0, len(plt_x), 8) / 8).astype(int).astype(str)),
        size=12)

    line_plot = pic2_df.loc[index_list[0], X_AD].values.flatten().astype(float)[0]
    plt.plot(num * 7, line_plot, 'o')

    plt.title('离地姿态')

    plt.subplot(243)

    F_M = [
        'RADIO HEIGHT (R/A1) SYS. 1_1',
        'RADIO HEIGHT (R/A1) SYS. 1_2',
        'RADIO HEIGHT (R/A1) SYS. 1_3',
        'RADIO HEIGHT (R/A1) SYS. 1_4',
        'RADIO HEIGHT (R/A1) SYS. 2_1',
        'RADIO HEIGHT (R/A1) SYS. 2_2',
        'RADIO HEIGHT (R/A1) SYS. 2_3',
        'RADIO HEIGHT (R/A1) SYS. 2_4',
    ]

    BD_BK = ['Capt Pitch Command Positi_1',
             'Capt Pitch Command Positi_2',
             'Capt Pitch Command Positi_3',
             'Capt Pitch Command Positi_4',
             'Capt Pitch Command Positi_5',
             'Capt Pitch Command Positi_6',
             'Capt Pitch Command Positi_7',
             'Capt Pitch Command Positi_8'
             ]

    BL_BS = ['Capt Roll Command Positio_1',
             'Capt Roll Command Positio_2',
             'Capt Roll Command Positio_3',
             'Capt Roll Command Positio_4',
             'Capt Roll Command Positio_5',
             'Capt Roll Command Positio_6',
             'Capt Roll Command Positio_7',
             'Capt Roll Command Positio_8'
             ]

    # 条件1筛选
    d1 = (data[D_E[1]] == 'NO').astype(int)
    d2 = (data[D_E[0]] == 'YES').astype(int)
    select_yn = d1 - d2 > 0

    D_E_index = data[:][select_yn].index.values
    # 条件2 通过阈值筛选数据

    # 提取每一列最大最

    max_data = data[F_M].max(axis=1)

    # 将所有满足条件的索引添加进来
    index_list = []

    for i in reversed(max_data.index):
        if max_data[i] < 1000 and max_data[i] > 100:
            index_list.append(i)
        elif max_data[i] > 1000:
            break

    x = data.loc[index_list, BD_BK].values.flatten()
    y = data.loc[index_list, BL_BS].values.flatten()

    # #去掉边框
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    # 指定x与y轴
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.gca().yaxis.set_ticks_position('left')
    # #设置x与y轴的位置
    plt.gca().spines['bottom'].set_position(('data', 0))
    plt.gca().spines['left'].set_position(('data', 0))  # 设置为(0,0)显示

    plt.scatter(y, -x, alpha=0.15,
                c='b',
                s=15,
                marker='o')
    plt.plot([-10, -10], [-10, 10], 'r')
    plt.plot([10, 10], [10, -10], 'r')

    plt.xticks(np.linspace(20, -20, 11), size=12)
    plt.yticks(np.linspace(16, -16, 8),
               list(np.linspace(-16, 16, 8).astype(int).astype(str)),
               size=12)
    plt.title("进近1000-100英尺杆量")

    ## X 轴大于10标记红色
    plt.subplot(244, projection='polar')
    ## 图4

    FR = [
        'RUNWAY HEADING'
    ]

    DL = [
        'Wind direction true'
    ]

    DM = [
        'Wind speed'
    ]

    index_list = []

    for i in reversed(max_data.index):
        if max_data[i] < 1000 and max_data[i] > 100:
            index_list.append(i)
        elif max_data[i] > 1000:
            break

    pic4_data = data.iloc[index_list, :]

    FR_values = np.unique(pic4_data[FR].dropna().values)[0]

    theta = (pic4_data[DL].values.astype(float) - float(FR_values)).flatten()

    # 半径
    radii = pic4_data[DM].values.flatten()

    plt.bar(theta, radii, width=0.01)
    plt.bar(0, max(radii), color='red', width=0.01)  # 给FR标记一个其他颜色
    plt.title('进近1000-100英尺风向风速')
    plt.subplot(245)

    # 图5

    # 将所有满足条件的索引添加进来
    index_list = []

    for i in reversed(max_data.index):
        if max_data[i] < 100 and max_data[i] > 0:
            index_list.append(i)
        elif max_data[i] > 100:
            break

    y = data.loc[index_list, BD_BK]
    x = data.loc[index_list, BL_BS]

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

        plt.scatter(plt_x, plt_y * -1, alpha=0.15,
                    c='b',
                    s=15,
                    marker='o')
    plt.plot([-10, -10], [-5, 5], 'r')
    plt.plot([-10, 10], [5, 5], 'r')
    plt.plot([10, 10], [5, -5], 'r')
    plt.plot([-10, 10], [-5, -5], 'r')

    plt.xticks(np.linspace(20, -20, 11), size=12)
    plt.yticks(np.linspace(16, -16, 8),
               list(np.linspace(-16, 16, 8).astype(int).astype(str)),
               size=12)
    plt.title("落地100英尺以下杆量")
    # plt.show()
    plt.subplot(246, projection='polar')

    # 图6

    # 将所有满足条件的索引添加进来
    index_list = []

    for i in reversed(max_data.index):
        if max_data[i] < 100 and max_data[i] > 0:
            index_list.append(i)
        elif max_data[i] > 100:
            break
    pic6_data = data.iloc[index_list, :]

    theta = (pic6_data[DL].values.astype(float) - float(np.unique(pic6_data[FR].dropna().values)[0])).flatten()

    # 半径
    radii = pic6_data[DM].values.flatten()

    plt.bar(theta, radii, width=0.01)
    plt.bar(0, max(radii), color='red', width=0.01)  # 给FR标记一个其他颜色
    plt.title('100英尺以下风向风速')

    plt.subplot(247)

    # 图7

    AN_AR = [
        'Roll attitude CA_1',
        'Roll attitude CA_2',
        'Roll attitude CA_3',
        'Roll attitude CA_4',
    ]

    # 将所有满足条件的索引添加进来
    index_list = []

    for i in reversed(max_data.index):
        if max_data[i] < 100 and max_data[i] > 0:
            index_list.append(i)
        elif max_data[i] > 100:
            break

    pic7_data = data.iloc[index_list, :]
    y = -pic7_data[AN_AR].values.astype(float)
    x = pic7_data[AN_AR].values

    # 固定Y值
    for i in range(len(y.flatten())):
        plt.plot([-y.flatten()[i], y.flatten()[i]])

    plt.yticks(np.linspace(5, -5, 8),
               size=12)
    plt.title("50英尺以下坡度")

    plt.subplot(248)
    # 图8

    CN = [
        'Throttle lever angle Eng1_1'
    ]

    F_I = [
        'RADIO HEIGHT (R/A1) SYS. 1_1',
        'RADIO HEIGHT (R/A1) SYS. 1_2',
        'RADIO HEIGHT (R/A1) SYS. 1_3',
        'RADIO HEIGHT (R/A1) SYS. 1_4',
    ]

    sort_value = pd.Series(index_list).sort_values(ascending=True).values

    indexs = data.loc[sort_value, F_I].index
    data8 = data.loc[sort_value, F_I].values.flatten().astype(float)
    plt_x8 = data8[data8 < 50]
    end_index = np.where(plt_x8 < 1)[0][0]

    plt8 = []
    for p8 in plt_x8:
        if p8 < 0:
            break
        else:
            plt8.append(p8)
    plt_x8 = np.array(plt8)

    dt = data.loc[indexs, CN].values.astype(float)

    for d in range(len(dt)):
        if dt[d] < 0:
            break

    plt.plot(plt_x8[:end_index])
    plt.plot(np.where(plt_x8[:end_index] == data8[d * 4])[0], data8[d * 4], 'o')
    plt.xticks(
        np.linspace(0, len(plt_x8[:end_index]), 4),
        list((np.linspace(0, len(plt_x8[:end_index]), 4) / 4).astype(int).astype(str)),
        size=12)
    plt.title("收油门高度")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()


def more_pic(paths=None, output_path="big_pic.png"):
    data1 = []
    paths = sorted(paths) if paths is not None else sorted(glob.glob("datas/*"))
    for path in paths:
        data = read_qar_csv(path).drop(
            index=0).reset_index(drop=True)
        data1.append(data)
    if not data1:
        raise ValueError("没有可分析的 CFM CSV 文件")
    plt.figure(figsize=(30, 14))
    for dat1 in data1:

        DY = 'N1 Actual Eng 1'

        F = 'RADIO HEIGHT (R/A1) SYS. 1_1'

        BJ_BQ = ['Capt Pitch Command Positi_1',
                 'Capt Pitch Command Positi_2',
                 'Capt Pitch Command Positi_3',
                 'Capt Pitch Command Positi_4',
                 'Capt Pitch Command Positi_5',
                 'Capt Pitch Command Positi_6',
                 'Capt Pitch Command Positi_7',
                 'Capt Pitch Command Positi_8', ]

        BD_BK = ['Capt Pitch Command Positi_1',
                 'Capt Pitch Command Positi_2',
                 'Capt Pitch Command Positi_3',
                 'Capt Pitch Command Positi_4',
                 'Capt Pitch Command Positi_5',
                 'Capt Pitch Command Positi_6',
                 'Capt Pitch Command Positi_7',
                 'Capt Pitch Command Positi_8']

        BL_BS = ['Capt Roll Command Positio_1',
                 'Capt Roll Command Positio_2',
                 'Capt Roll Command Positio_3',
                 'Capt Roll Command Positio_4',
                 'Capt Roll Command Positio_5',
                 'Capt Roll Command Positio_6',
                 'Capt Roll Command Positio_7',
                 'Capt Roll Command Positio_8'
                 ]

        data_F = dat1[dat1[F].astype(float) < 50].index
        df_F = dat1.iloc[data_F, :]

        df_DS = df_F[df_F[DY].astype(float) >= 50]

        for i in range(1, len(df_DS[BD_BK].index)):
            if df_DS[BD_BK].index[i] - df_DS[BD_BK].index[i - 1] > 2:
                break

        indexs = df_DS[BD_BK].index[:i - 1].values

        df_DS_select = df_DS.loc[indexs, BD_BK][(df_DS.loc[indexs, BD_BK].astype(float) >= 0).sum(axis=1) == 0].index

        x = df_DS.loc[df_DS_select, BL_BS]
        y = df_DS.loc[df_DS_select, BD_BK]
        plt.subplot(241)
        # 去掉边框
        plt.gca().spines['right'].set_color('none')
        plt.gca().spines['top'].set_color('none')
        # 指定x与y轴
        plt.gca().xaxis.set_ticks_position('bottom')
        plt.gca().yaxis.set_ticks_position('left')
        # #设置x与y轴的位置
        plt.gca().spines['bottom'].set_position(('data', 0))
        plt.gca().spines['left'].set_position(('data', 0))  # 设置为(0,0)显示

        plt.title("起飞50英尺以下杆量", size=15)
        for i, j in zip(x.columns, y.columns):
            plt_x = x[i].astype(float)
            plt_y = y[j].astype(float)
            plt.scatter(plt_x, plt_y * -1, alpha=0.15,
                        c='b',
                        s=15,
                        marker='o')

        plt.plot([-10, -10], [-10, 10], 'r')
        plt.plot([10, 10], [10, -10], 'r')

        plt.xticks(np.linspace(20, -20, 11), size=12)
        plt.yticks(np.linspace(16, -16, 8),
                   list(np.linspace(-16, 16, 8).astype(int).astype(str)),
                   size=12)

        plt.subplot(242)
        # 图2
        D_E = [
            'AIRCRAFT ON GROUND (CFM)_592',
            'AIRCRAFT ON GROUND (CFM)_599'
        ]

        EX_FA = [
            'LANDING GEAR NOSE_1',
            'LANDING GEAR NOSE_2',
            'LANDING GEAR NOSE_3',
            'LANDING GEAR NOSE_4',
        ]

        X_AD = [
            'Pitch attitude CA_1',
            'Pitch attitude CA_2',
            'Pitch attitude CA_3',
            'Pitch attitude CA_4',
            'Pitch attitude CA_5',
            'Pitch attitude CA_6',
            'Pitch attitude CA_7',
        ]

        F_M = [
            'RADIO HEIGHT (R/A1) SYS. 1_1',
            'RADIO HEIGHT (R/A1) SYS. 1_2',
            'RADIO HEIGHT (R/A1) SYS. 1_3',
            'RADIO HEIGHT (R/A1) SYS. 1_4',
            'RADIO HEIGHT (R/A1) SYS. 2_1',
            'RADIO HEIGHT (R/A1) SYS. 2_2',
            'RADIO HEIGHT (R/A1) SYS. 2_3',
            'RADIO HEIGHT (R/A1) SYS. 2_4',
        ]

        # EX_FA

        fil2_data = dat1[(dat1[EX_FA] == 'AIR').sum(axis=1) > 0]

        ea_index = (dat1[EX_FA] == 'AIR').sum(axis=1)

        index_list = []

        for i in ea_index.index:
            if ea_index[i] > 0:
                index_list.append(ea_index.index[i])
                index_list.append(ea_index.index[i] - 1)
                index_list.append(ea_index.index[i] - 2)
                index_list.append(ea_index.index[i] - 3)

        save_index1 = np.unique(index_list)

        index1 = pd.DataFrame({'index': save_index1})

        # 特征筛选2

        indexs2 = numeric_columns(dat1, F_M).max(axis=1)

        for i in range(len(indexs2)):
            if indexs2[i] > 50:
                break

        save_index2 = indexs2[:i].index

        index2 = pd.DataFrame({'index': save_index2})

        # 合并索引

        save_index = pd.merge(index1, index2, how='inner')

        pic2_df = dat1.loc[save_index.values.flatten(), :]
        # 条件1筛选
        d1 = (pic2_df[D_E[1]] == 'NO').astype(int)
        d2 = (pic2_df[D_E[0]] == 'YES').astype(int)
        select_yn = d1 - d2 > 0

        index_list = []

        for i in select_yn.index:

            if select_yn[i] == True:
                index_list.append(i)
                break

        num = np.where(select_yn.index == index_list[0])[0]

        plt_x = numeric_array(pic2_df, X_AD).reshape(-1)
        plt.plot(plt_x)
        plt.xticks(
            np.linspace(0, len(plt_x), 8),
            list((np.linspace(0, len(plt_x), 8) / 8).astype(int).astype(str)),
            size=12)

        line_plot = pd.to_numeric(
            pic2_df.loc[index_list[0], X_AD], errors="coerce"
        ).to_numpy()[0]
        plt.plot(num * 7, line_plot, 'o')

        plt.title('离地姿态')

        plt.subplot(243)

        F_M = [
            'RADIO HEIGHT (R/A1) SYS. 1_1',
            'RADIO HEIGHT (R/A1) SYS. 1_2',
            'RADIO HEIGHT (R/A1) SYS. 1_3',
            'RADIO HEIGHT (R/A1) SYS. 1_4',
            'RADIO HEIGHT (R/A1) SYS. 2_1',
            'RADIO HEIGHT (R/A1) SYS. 2_2',
            'RADIO HEIGHT (R/A1) SYS. 2_3',
            'RADIO HEIGHT (R/A1) SYS. 2_4',
        ]

        BD_BK = ['Capt Pitch Command Positi_1',
                 'Capt Pitch Command Positi_2',
                 'Capt Pitch Command Positi_3',
                 'Capt Pitch Command Positi_4',
                 'Capt Pitch Command Positi_5',
                 'Capt Pitch Command Positi_6',
                 'Capt Pitch Command Positi_7',
                 'Capt Pitch Command Positi_8'
                 ]

        BL_BS = ['Capt Roll Command Positio_1',
                 'Capt Roll Command Positio_2',
                 'Capt Roll Command Positio_3',
                 'Capt Roll Command Positio_4',
                 'Capt Roll Command Positio_5',
                 'Capt Roll Command Positio_6',
                 'Capt Roll Command Positio_7',
                 'Capt Roll Command Positio_8'
                 ]

        # 条件1筛选
        d1 = (dat1[D_E[1]] == 'NO').astype(int)
        d2 = (dat1[D_E[0]] == 'YES').astype(int)
        select_yn = d1 - d2 > 0

        D_E_index = dat1[:][select_yn].index.values
        # 条件2 通过阈值筛选数据

        # 提取每一列最大最

        max_data = numeric_columns(dat1, F_M).max(axis=1)

        # 将所有满足条件的索引添加进来
        index_list = []

        for i in reversed(max_data.index):
            if max_data[i] < 1000 and max_data[i] > 100:
                index_list.append(i)
            elif max_data[i] > 1000:
                break

        x = numeric_array(dat1.loc[index_list], BD_BK).reshape(-1)
        y = numeric_array(dat1.loc[index_list], BL_BS).reshape(-1)
        # #去掉边框
        plt.gca().spines['right'].set_color('none')
        plt.gca().spines['top'].set_color('none')
        # 指定x与y轴
        plt.gca().xaxis.set_ticks_position('bottom')
        plt.gca().yaxis.set_ticks_position('left')
        # #设置x与y轴的位置
        plt.gca().spines['bottom'].set_position(('data', 0))
        plt.gca().spines['left'].set_position(('data', 0))  # 设置为(0,0)显示

        plt.title("进近1000-100英尺杆量", size=15)

        plt.scatter(y, -x.astype(float), alpha=0.15,
                    c='b',
                    s=15,
                    marker='o')
        plt.plot([-10, -10], [-10, 10], 'r')
        plt.plot([10, 10], [10, -10], 'r')

        plt.xticks(np.linspace(20, -20, 11),
                   list(np.linspace(20, -20, 11).astype(int).astype(str)), size=12)
        plt.yticks(np.linspace(16, -16, 8),
                   list(np.linspace(-16, 16, 8).astype(int).astype(str)), size=12)

        ## X 轴大于10标记红色
        plt.subplot(244, projection='polar')
        ## 图4

        FR = [
            'RUNWAY HEADING'
        ]

        DL = [
            'Wind direction true'
        ]

        DM = [
            'Wind speed'
        ]

        index_list = []

        for i in reversed(max_data.index):
            if max_data[i] < 1000 and max_data[i] > 100:
                index_list.append(i)
            elif max_data[i] > 1000:
                break

        pic4_data = dat1.iloc[index_list, :]

        FR_values = np.unique(numeric_array(pic4_data.dropna(subset=FR), FR).reshape(-1))[0]
        theta = numeric_array(pic4_data, DL).reshape(-1) - float(FR_values)

        # 半径
        radii = numeric_array(pic4_data, DM).reshape(-1)
        plt.bar(theta, radii, width=0.01)
        plt.bar(0, max(radii), color='red', width=0.01)  # 给FR标记一个其他颜色
        plt.title('进近1000-100英尺风向风速')
        plt.subplot(245)

        # 图5

        # 将所有满足条件的索引添加进来
        index_list = []

        for i in reversed(max_data.index):
            if max_data[i] < 100 and max_data[i] > 0:
                index_list.append(i)
            elif max_data[i] > 100:
                break

        y = dat1.loc[index_list, BD_BK]
        x = dat1.loc[index_list, BL_BS]

        # #去掉边框
        plt.gca().spines['right'].set_color('none')
        plt.gca().spines['top'].set_color('none')
        # 指定x与y轴
        plt.gca().xaxis.set_ticks_position('bottom')
        plt.gca().yaxis.set_ticks_position('left')
        # #设置x与y轴的位置
        plt.gca().spines['bottom'].set_position(('data', 0))
        plt.gca().spines['left'].set_position(('data', 0))  # 设置为(0,0)显示

        plt.title("落地100英尺以下杆量", size=15)

        for i, j in zip(x.columns, y.columns):
            plt_x = x[i].astype(float)
            plt_y = y[j].astype(float)

            plt.scatter(plt_x, plt_y * -1, alpha=0.15,
                        c='b',
                        s=15,
                        marker='o')
        plt.plot([-10, -10], [-5, 5], 'r')
        plt.plot([-10, 10], [5, 5], 'r')
        plt.plot([10, 10], [5, -5], 'r')
        plt.plot([-10, 10], [-5, -5], 'r')

        plt.xticks(np.linspace(20, -20, 11), size=12)
        plt.yticks(np.linspace(16, -16, 8),
                   list(np.linspace(-16, 16, 8).astype(int).astype(str)),
                   size=12)

        plt.subplot(246, projection='polar').grid(True)

        # 图6

        # 将所有满足条件的索引添加进来
        index_list = []

        for i in reversed(max_data.index):
            if max_data[i] < 100 and max_data[i] > 0:
                index_list.append(i)
            elif max_data[i] > 100:
                break
        pic6_data = dat1.iloc[index_list, :]

        FR_values = np.unique(numeric_array(pic6_data.dropna(subset=FR), FR).reshape(-1))[0]
        # 半径
        radii = numeric_array(pic6_data, DM).reshape(-1)
        theta = numeric_array(pic6_data, DL).reshape(-1) - float(FR_values)

        plt.bar(theta, np.array(radii), width=0.01)
        plt.bar(0, max(radii), color='red', width=0.01)  # 给FR标记一个其他颜色

        plt.title('100英尺以下风向风速')

        plt.subplot(247)

        # 图7

        AN_AR = [
            'Roll attitude CA_1',
            'Roll attitude CA_2',
            'Roll attitude CA_3',
            'Roll attitude CA_4',
        ]

        # 将所有满足条件的索引添加进来
        index_list = []

        for i in reversed(max_data.index):
            if max_data[i] < 100 and max_data[i] > 0:
                index_list.append(i)
            elif max_data[i] > 100:
                break

        pic7_data = dat1.iloc[index_list, :]
        y = -numeric_array(pic7_data, AN_AR)
        x = pic7_data[AN_AR].to_numpy()

        # 固定Y值
        for i in range(len(y.flatten())):
            plt.plot([-y.flatten()[i], y.flatten()[i]])

        plt.yticks(np.linspace(5, -5, 8),
                   size=12)
        plt.title("50英尺以下坡度")

        plt.subplot(248)
        # 图8

        CN = [
            'Throttle lever angle Eng1_1'
        ]

        F_I = [
            'RADIO HEIGHT (R/A1) SYS. 1_1',
            'RADIO HEIGHT (R/A1) SYS. 1_2',
            'RADIO HEIGHT (R/A1) SYS. 1_3',
            'RADIO HEIGHT (R/A1) SYS. 1_4',
        ]

        sort_value = pd.Series(index_list).sort_values(ascending=True).values

        indexs = dat1.loc[sort_value, F_I].index
        data8 = numeric_array(dat1.loc[sort_value], F_I).reshape(-1)
        plt_x8 = data8[data8 < 50]
        # end_index = np.where(plt_x8 < 1)[0][0]
        # print(plt_x8)
        plt8 = []
        for p8 in plt_x8:
            if p8 <= 0:
                break
            else:
                plt8.append(p8)

        plt_x8 = np.array(plt8)

        dt = numeric_array(dat1.loc[indexs], CN).reshape(-1)
        plt_window = plt_x8[:44]

        marker_index = None
        marker_value = None
        for d in range(len(dt)):
            if dt[d] < 0:
                marker_pos = d * 4
                if marker_pos < len(data8) and len(plt_window) > 0:
                    marker_value = data8[marker_pos]
                    matched_index = np.where(plt_window == marker_value)[0]
                    if len(matched_index) > 0:
                        marker_index = int(matched_index[0])
                    else:
                        # The sampled altitude may fall outside the truncated window
                        # or differ slightly after numeric conversion.
                        marker_index = int(np.abs(plt_window - marker_value).argmin())
                break

        plt.plot(plt_window)
        if marker_index is not None and marker_value is not None:
            plt.plot(marker_index, marker_value, 'o')
        plt.xticks(
            np.linspace(0, len(plt_window), 4),
            list((np.linspace(0, len(plt_window), 4) / 4).astype(int).astype(str)),
            size=12)
        plt.title("收油门高度")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()
