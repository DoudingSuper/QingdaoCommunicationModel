import socket
import struct
# 创建一个TCP服务器
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.4.100', 8882))  # 绑定到本地地址和端口
server_socket.listen(1)  # 最多允许一个客户端连接

print("等待客户端连接...")
client_socket, client_address = server_socket.accept()
print(f"连接来自: {client_address}")


# 接收客户端发送的消息
while True:
    data = client_socket.recv(1024)
    print(type(data))
    if not data:
        break
    # hex_data = binascii.hexlify(data).decode('utf-8')
    hex_data = ' '.join([f'{x:02x}' for x in data])
    print(f"收到消息: {hex_data}")
    # 解包CAN消息
    data_length, frame_id, data_bytes1, data_bytes2 = struct.unpack('>BI4s4s', data)

    # 解包帧ID
    frame_id = hex(frame_id)

    # 解包数据
    data = struct.unpack('<I', data_bytes1)[0]

    # 打印解包后的数据
    print("数据长度:", data_length)
    print("帧ID:", frame_id)
    print(":", data)
# 关闭连接
client_socket.close()
server_socket.close()