2020-05-15 11:44

修复：

- tlist无法存入时间戳问题
- process无法传入数据问题

bug：

- 插值无法正确插入

优化：

- 用CUDA跑数据



2020-05-14 23:26

修复：

- 修复middleman传输CSI信息大小不对的问题（count）
- 将middleman改为UDP传出，解决了包大小不对及传输延迟高的问题。
- 优化了middleman的输出信息

bug：

- tlist无法正确存放时间戳，插值算法因此未测试
- process的data无法正确输入

优化：

- 用CUDA跑数据

------

2020-05-13 11:32

修复：

- 修改了collect_data.sh的参数，测试好数据收集的部分

- 调整了参数设置，以及将get_data改为适用两个树莓派
- 设置一个连接数量的变量，确保未全部连接上时不对缓冲区进行数据操作
- 将model用CPU再训练，解决model在CPU的pytorch上无法使用的问题

bug：

- middleman传出的包大小不对，无法正确解析出CSI
- 树莓派1正确连接，树莓派2无法连接

待优化：

- middleman的输出信息需要改一下
- 使用CUDA训练和测试数据