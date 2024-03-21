import argparse
import os
import numpy as np
import openpyxl as op
import pandas as pd
import datetime as dt
import scipy
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from scipy import interpolate
import matplotlib.dates as mdates


def ini_plot(title, fold_name, t, y, color):
    os.makedirs(fold_name, exist_ok=True)
    figure(figsize=(12.8, 9.6))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(t, y, color=color)
    plt.title(f'{title}', fontsize=20)
    plt.setp(plt.gca().xaxis.get_majorticklabels(), 'rotation', 30, 'fontsize', 10)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M:%S'))
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=20)
    plt.savefig(f'{fold_name}/{title}.png')


def time_cost(t1, t2):
    days = (t2 - t1).days
    seconds = (t2 - t1).seconds
    return days * 24 * 60 * 60 + seconds


def get_data(data_path):
    file_list = list(os.walk(data_path))[0][2]
    data_list = []
    for i in file_list:
        path = os.path.join(data_path, i)
        ini_data = pd.read_csv(path, sep=',', header='infer')
        array = ini_data.values[0::, 0::]  # 读取全部行，全部列
        data_list.append(array)

    data = np.vstack(data_list)
    d_data = data[:, 2:].copy()
    f_t = dt.datetime.strptime(data[0][0], "%Y-%m-%d %H:%M:%S")
    e_t = dt.datetime.strptime(data[-1][0], "%Y-%m-%d %H:%M:%S")
    t_c = time_cost(f_t, e_t)
    arr = np.array([row for row in data if sum(~np.isnan(row[1:].astype('float'))) > 0])

    t = np.array([time_cost(f_t, dt.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")) for row in arr])
    ini_plot('原始温度数据', 'analysis', t, arr[:, -3], 'green')
    ini_plot('原始风速数据', 'analysis', t, arr[:, -1], 'red')
    ini_plot('原始风向数据', 'analysis', t, arr[:, -2], 'blue')

    data = arr[:, 2:].astype('float')
    a = data[:, -1] * np.cos(data[:, -2] * 2 * np.pi)
    b = data[:, -1] * np.sin(data[:, -2] * 2 * np.pi)
    data[:, -1] = a
    data[:, -2] = b
    tfit = np.arange(0, t_c + 30, 30)
    t_date = np.array([f_t + dt.timedelta(seconds=int(i)) for i in tfit])

    for i in range(len(data[0])):
        y = data[:, i]
        y_smooth = scipy.signal.savgol_filter(y, 120, 3)
        tck = interpolate.splrep(t, y_smooth, k=3)
        yfit = interpolate.splev(tfit, tck)
        d_data[:, i] = yfit
    ini_plot('处理后温度数据', 'analysis', tfit, d_data[:, -3], 'green')
    ini_plot('处理后wind_x数据', 'analysis', tfit, d_data[:, -1], 'red')
    ini_plot('处理后wind_y数据', 'analysis', tfit, d_data[:, -2], 'blue')
    return tfit, t_date, d_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='datasets')
    parser.add_argument('--output', type=str, default='Seq_LSTM/data/static.npz')
    args = parser.parse_args()

    t, _, data = get_data(args.file)
    np.savez(args.output, t=t, data=data[:, -2:], allow_pickle=True)
    np.savez('analysis/mat_data.npz', tfit=t, d_data=data, allow_pickle=True)
    import scipy.io as io

    io.savemat('analysis/mat_data.mat', mdict=np.load('analysis/mat_data.npz', allow_pickle=True))

    print('Processing completed!')
