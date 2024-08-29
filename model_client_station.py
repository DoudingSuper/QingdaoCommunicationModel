import socket
import time
import struct

# 创建一个UDP套接字来发送消息到服务器
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 8889)  # 服务器的地址和端口

# 十对不同的数据
data_pairs = [(1000, 10), (2000, 200), (3000, 300), (4000, 640), (5000, 1150), 
              (6000, 60), (7000, 70), (8000, 80), (9000, 90), (10000, 100)]

# 以一定的间隔循环发送数据
while True:
    for data1, data2 in data_pairs:
        # 数据长度为8字节
        data_length = 4
        # 帧ID为0x01
        frame_id = 0x01
        # 将小数转换为字节表示，假设小数为双精度浮点数（64位）
        data_bytes1 = struct.pack('<I', data1)
        data_bytes2 = struct.pack('<I', data2)
        # 打包CAN消息
        can_message = struct.pack('>BI4s4s', data_length, frame_id, data_bytes1, data_bytes2)

        # 打印打包后的CAN消息
        print("打包后的CAN消息:", can_message)

        # 发送消息
        client_socket.sendto(can_message, server_address)
        print("发送成功！！")

        # 设置发送间隔为1秒
        time.sleep(1)

# 关闭套接字
client_socket.close()

# 发送完成后关闭套接字
client_socket.close()
