# 风场短期预测

### 将风场数据分解成x、y方向风矢量，然后进行滤波、插值、多元线性回归分析和预测

### 预测模型和方法参考子项目：[guoX66/Seq_LSTM (github.com)](https://github.com/guoX66/Seq_LSTM)

### 训练过程损失（以wind_y为例）：

![image](https://github.com/guoX66/wind_prediction/blob/main/assets/loss.jpg)

### 预测过程图（以wind_y为例）：

![image](https://github.com/guoX66/wind_prediction/blob/main/assets/pre.jpg)



### 预测误差如下表：

| model-output    | MSE(10e-6) | RMSE    | MAE     | R2     | MAPE(%) | SMAPE(%) |
| --------------- | ---------- | ------- | ------- | ------ | ------- | -------- |
| LSTM-wind_x     | 2.371      | 0.00154 | 0.00117 | 0.9973 | 21.142  | 13.386   |
| CNN_LSTM-wind_x | 2.347      | 0.00153 | 0.00117 | 0.9972 | 20.817  | 13.021   |
| Seq2Seq-wind_x  | 2.305      | 0.00152 | 0.00116 | 0.9973 | 20.977  | 13.584   |
| LSTM-wind_y     | 3.578      | 0.00189 | 0.00152 | 0.9993 | 6.406   | 5.647    |
| CNN_LSTM-wind_y | 3.259      | 0.00181 | 0.00143 | 0.9993 | 5.997   | 5.230    |
| Seq2Seq-wind_x  | 2.379      | 0.00154 | 0.00118 | 0.9995 | 5.512   | 4.730    |



# 1、 环境部署

### 用git命令将子项目一并拉取 , 或将子项目下载后放入本项目中

    git clone --recurse-submodules https://github.com/guoX66/Seq_LSTM.git

### 安装 python>=3.10.2，并安装依赖

    pip install -r requirements

### 然后参考[子项目](https://github.com/guoX66/Seq_LSTM)进行环境部署



# 2、数据处理

### 数据已经保存在release中，数据来源：https://www.industrial-bigdata.com

### 将解压后的datasets文件夹放到项目目录下

```
--wind_prediction
    --database
        --2019-01-01.csv
        --2019-01-02.csv
        ...
        --2019-01-10.csv
```

运行数据处理程序，处理过程保存在analysis文件夹中，处理后的数据将保存在analysis-data.npz中

```bash
python deal.py --file datasets --output Seq_LSTM/data/static.npz
```



## 多元线性回归分析

经过数据处理步骤，用matlab运行Linear.m文件即可,处理后的结果保存在analysis文件夹中



# 3、训练与预测

### 进入子项目,按照子项目步骤进行

```bash
cd Seq_LSTM
```
