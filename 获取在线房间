import socket
outime = float(input('设置间隔(单位秒):'))
start_port = 54002
end_port = 54999
sum = 0
print('请稍等,查询的时间根据你设置间隔以及到服务器的延迟决定...')
for port in range(start_port, end_port + 1):
    try:
        # 创建一个套接字对象m
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间
        s.settimeout(outime)
        # 尝试连接端口
        result = s.connect_ex(('lmbaka.top', port))  # 这里的'localhost'可以替换成你要测试的主机名或IP地址
        if result == 0:
            sum+=1
            print('frp.lmbaka.top:'+str(port))
        s.close()
    except socket.error:
        pass
print(f'当前有{sum}个房间在线')
input('按任意键退出')
