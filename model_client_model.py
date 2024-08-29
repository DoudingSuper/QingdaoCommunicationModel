import socket
import time
import struct

# 创建一个UDP套接字来发送消息到服务器
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 8889)  # 服务器的地址和端口

# 十对不同的数据
# data_pairs = [(8, 1000,46), (10, 200, 31), (16, 300,40), (10, 640,90), (7, 1150, 86), 
#               (12, 600,110), (15, 700,112), (20, 1000,130), (18, 1000,40), (13, 1000,40)]
data_pairs = [(1, 2,112),(3, 4, 31),(30, 40, 48)]
# data_pairs = [(8, 1000,101), (9, 200, 102), (10, 300,103), (11, 640,104), (12, 1150, 105), 
#               (15, 600,110), (17, 700,112), (18, 1000,140), (20, 1000,120), (30, 1000,40)]
# data_pairs = [(9, 100,80, 100)]

# 以一定的间隔循环发送数据S
while True:
    for data1, data2, data3 in data_pairs:
        # 数据长度为8字节
        data_length = 4
        # 帧ID为0x01
        frame_id1 = 0x01
        frame_id2 = 0x02
        frame_id3 = 0x03
        # 将数转换为字节表示
        data_bytes1 = struct.pack('<I', data1)
        data_bytes2 = struct.pack('<I', data2)
        data_bytes3 = struct.pack('<I', data3)
        data_bytes4 = struct.pack('<I', 0)
        data_bytes5 = struct.pack('<I', 0)
        data_bytes6 = struct.pack('<I', 0)
        # 打包CAN消息
        can_message1 = struct.pack('>BI4s4s', data_length, frame_id1, data_bytes1, data_bytes4)
        can_message2 = struct.pack('>BI4s4s', data_length, frame_id2, data_bytes2, data_bytes5)
        can_message3 = struct.pack('>BI4s4s', data_length, frame_id3, data_bytes3, data_bytes6)
        hex_data = ' '.join([f'{x:02x}' for x in can_message2])
        # 打印打包后的CAN消息
        print("打包后的CAN消息:", hex_data)

        # 发送消息
        client_socket.sendto(can_message1, server_address)
        time.sleep(0.1)
        client_socket.sendto(can_message2, server_address)
        time.sleep(0.1)
        client_socket.sendto(can_message3, server_address)

        print("发送成功！！")

        # 设置发送间隔为1秒
        time.sleep(1)

# 关闭套接字
client_socket.close()

# 发送完成后关闭套接字
client_socket.close()
