import psutil
import subprocess
import os
import pyperclip
import random
import requests

def get(url, *args, **kwargs):
    try:
        return requests.get(url, *args, **kwargs)
    except Exception as e:
        print('请求失败: {}'.format(e))
        return None

print('公告信息')
print('--------------------------------------------------------')
url = 'http://api.lmbaka.top:114/frp/information'
response = get(url)
if response and response.status_code == 200:
    print(response.text)
else:
    print('请求失败，无法获取公告信息')
print('--------------------------------------------------------')
print('正在寻找Minecraft开放的端口...')
def get_open_ports():
    all_processes = psutil.process_iter()
    open_ports = set()  # 集合存端口

    for process in all_processes:
        try:
            if process.name() == "javaw.exe":
                process_connections = process.connections()

                for conn in process_connections:
                    if conn.status == 'LISTEN':
                        open_ports.add(conn.laddr.port)  # 防重

        except (psutil.Error, psutil.NoSuchProcess):
            pass

    return open_ports

def input_port(desc: str, error_desc: str, start: int=0, end: int=65535, empty_random: bool=False):
    while (True):
        try:
            port = input(desc)
            if (empty_random and len(port) <= 0):
                return random.randint(start, end)
            port = int(port)
            if not (start <= port <= end):
                print(error_desc)
                continue
            return port
        except ValueError:  # 输入内容无法转为 int
            print(error_desc)
            continue

def start_frpc(minecraft_port, external_port):
    # 清除 frpc.ini 文件内容
    with open("frpc.ini", mode="w") as f:
        f.write("[common]\n")
        f.write("server_addr = gyfrp.lmbaka.top\n")
        f.write("server_port = 54001\n")

    name = "tunnel" + str(os.urandom(4).hex().upper())

    # 构建 frpc.ini 配置文件内容
    frpc_ini = f"""[tunnel_{name}]
type = tcp
local_ip = 127.0.0.1
local_port = {minecraft_port}
remote_port = {external_port}
"""

    with open("frpc.ini", mode="a") as f:
        f.write(frpc_ini)

    # 启动 frpc
    frpc_process = subprocess.Popen(
        ["frpc", "-c", "frpc.ini"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    target_address = f"frp.lmbaka.top:{external_port}"
    print('__________________________________________________________')
    print('IP:'+target_address+' 已复制到剪贴板')
    print(f"使用 frp.lmbaka.top:{external_port} 登入房间")
    pyperclip.copy(target_address)
    # 输出日志信息到控制台
    for line in iter(frpc_process.stdout.readline, b''):
        print(line.decode('utf-8').strip())

def main():
    open_ports = get_open_ports()

    if len(open_ports) == 1:
        for port in open_ports:
            print('检测到Minecraft开放端口:'+str(port))
            external_port = input_port("请输入外部端口号, 应当为 54000-55000 的整数 (直接回车以随机)：", "您输入的端口号有误, 请重新输入", 54000, 55000, True)
            start_frpc(port, external_port)
    else:
        print("未找到Minecraft的开放端口或者有多个不同端口,你需要手动输入端口号")
        minecraft_port = input_port("请输入 Minecraft 端口号：", "您输入的端口号有误, 请重新输入")
        external_port = input_port("请输入外部端口号, 应当为 54000-55000 的整数 (直接回车以随机)：", "您输入的端口号有误, 请重新输入", 54000, 55000, True)
        start_frpc(minecraft_port, external_port)

if __name__ == '__main__':
    main()
