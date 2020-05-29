# CSI_Authentication

### 使用说明：

将Pi_Script文件夹移至树莓派中

对三个树莓派均执行：

`prepare.sh`

`python send_csi.py`

选择一个树莓派执行：`python detect_connection.py`

然后在主机执行`python main.py`

注意：需要先在两个py文件的头部及parameter.py中自行修改IP、端口等配置

### 文件说明：

- main.py：核心代码，控制整个运行流程
- test.py：跑测试集，获得通过率和不通过率
- parameter.py： 存放所有参数
- get_fingerprint.py：将向树莓派请求CSI信息和预处理封装为get_fingerprint()函数
- detect：调用model对指纹进行识别
- model.py：神经网络模型
- local_illegal：本实验的非法设备指纹测试集，包含九个点
- local_legal：本实验的合法设备指纹测试集，包含九个点
- temp：每次进行认证时会保留指纹到此文件夹
- train文件夹：
  - CNN_pytorch.py：CNN模型训练
  - parse_pcap.py：将本地pcap文件预处理为指纹
  - data文件夹：预处理后的训练数据
  - data_pcap文件夹：原始数据
  - model文件夹：模型文件夹
    - MAC-1：设备1的模型
- assets：图片资源
