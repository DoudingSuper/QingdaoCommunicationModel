import socket

# 创建一个UDP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 发送消息到指定地址和端口
client_socket.sendto(b'exit', ('127.0.0.1', 8888))
print("stop!!")
# 关闭套接字
client_socket.close()