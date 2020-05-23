# CSI_Authentication

### 文件说明：

- parameter.py： 存放所有参数，方便后期调试。
- main.py：核心代码，控制整个运行流程
- get_fingerprint：请求和获取CSI信息，将CSI信息加工成指纹
- detect：调用model对指纹进行识别
- train文件夹：
  - data文件夹：处理后的训练数据
  - data_pcap文件夹：原始数据
  - model文件夹：模型文件夹
    - MAC-n：某MAC地址对应C(3, 3) + C(3, 2) + C(3, 1)种（树莓派正常与否）情况的模型



### 运行流程：

略，等pcr作图
