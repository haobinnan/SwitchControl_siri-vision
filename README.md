# Sirivision（希力）交换机端口状态控制

由于Sirivision（希力）官网未提供交换机二次开发的API接口，对于想实现自动控制或将控制方法嵌入到自己的程序中来就比较不友好了，本Python脚本可以通过远程方式控制交换机端口的状态，从而达到限制设备是否可以上网。

## 命令行参数说明
1. **IP** 交换机IP地址

2. **User** 交换机用户名

3. **Password** 交换机密码

4. **ShowAllPort** 查看所有端口状态

5. **PortStatistics** 查看端口统计信息

6. **ShowPortState** 查看指定端口状态

    参数：**PortNumber** (1,2,3,....) 端口号

7. **SetPortState** 设置指定端口状态

    参数：**PortNumber** (1,2,3,....) 端口号 | **State** (0,1) 端口状态 【0：禁止 1：开启】

8. **ShowSystemInfo** 查看系统信息

9. **Reboot** 重启交换机

10. **Save** 保存交换机配置





目前对SR_8808MNB_8G（千兆版）、及2.5G交换机型号进行过测试。
推荐淘宝店铺：https://xiliweishi.tmall.com/
