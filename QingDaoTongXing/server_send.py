import socket
import struct
# 创建一个TCP服务器
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.4.100', 8882))  # 绑定到本地地址和端口
server_socket.listen(1)  # 最多允许一个客户端连接

print("等待客户端连接...")
client_socket, client_address = server_socket.accept()
print(f"连接来自: {client_address}")

# 向客户端发送消息
# 数据
data_length = 4  # 数据长度为8字节
frame_id = 0x01  # 帧ID为0x12345678
data = 500 # 示例小数数据
data2 = 10  # 示例小数数据

# 将小数转换为字节表示，假设小数为双精度浮点数（64位）
data_bytes1 = struct.pack('<I', data)
data_bytes2 = struct.pack('<I', data2)

# 打包CAN消息
can_message = struct.pack('>BI4s4s', data_length, frame_id, data_bytes1, data_bytes2)

# 打印打包后的CAN消息 
print("打包后的CAN消息:", can_message)

client_socket.send(can_message)


# 关闭连接
client_socket.close()
server_socket.close()