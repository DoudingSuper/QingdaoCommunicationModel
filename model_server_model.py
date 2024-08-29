import socket
import struct
import threading

#创建全局变量用于存储从客户发送过来的信息
pending_message = []
pending_message2 = []
pending_message3 = []
old_pending_message = []
old_pending_message2 = []
old_pending_message3 = []
message_lock = threading.Lock()
count = 0
def send_message(client_socket):
    global count
    global pending_message, old_pending_message
    global pending_message2, old_pending_message2
    global pending_message3, old_pending_message3
    while True:
        try:
            if old_pending_message != pending_message:
                # count = count + 1
                # if count % 2 != 0:
                #     message1 = pending_message
                # else:
                #     message2 = pending_message
                #     client_socket.send(message1)
                #     client_socket.send(message2)
                #     print("成功向模型发送消息！！")
                old_pending_message = pending_message
                client_socket.send(pending_message)
                print("成功向模型发送消息！！")
            # if old_pending_message2 != pending_message2:
            #     old_pending_message2 = pending_message2
            #     client_socket.send(pending_message2)
            #     print("成功向模型发送消息！！")
            # if old_pending_message3 != pending_message3:
            #     old_pending_message3 = pending_message3
            #     client_socket.send(pending_message3)
            #     print("成功向模型发送消息！！")
        except ConnectionAbortedError:
            print("连接被中止，尝试重新连接或记录错误信息")
            # 这里可以添加重新连接或记录错误信息的代码

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            hex_data = ' '.join([f'{x:02x}' for x in data])
            print(f"收到消息: {hex_data}")

            # 每个CAN消息的长度和结构
            can_message_length = struct.calcsize('>BI4s4s')
            num_can_messages = len(data) // can_message_length

            # 确保data是一个字节串
            if not isinstance(data, bytes):
                data = bytes(data)

            # 逐个解析每个CAN消息
            for i in range(num_can_messages):
                # 计算当前消息的起始和结束位置
                start_index = i * can_message_length
                end_index = (i + 1) * can_message_length

                # 从数据中提取当前消息的部分
                can_message_data = data[start_index:end_index]

                # 解析CAN消息
                data_length, frame_id, data_bytes1, data_bytes2 = struct.unpack('>BI4s4s', can_message_data)

                # 解包帧ID
                frame_id = hex(frame_id)

                # 解包数据
                data_value = struct.unpack('<I', data_bytes1)[0]

                # 打印解包后的数据
                if frame_id == '0x1a' :
                    print("brakeEnergy:", data_value)
                elif frame_id == '0x1b' :
                    print("totalBrakeEnergy:", data_value)
                elif frame_id == '0x1c' :
                    print("tractionEnergy:", data_value)
                elif frame_id == '0x1d' :
                    print("totalTractionEnergy:", data_value)
        except ConnectionAbortedError:
            print("连接被中止，尝试重新连接或记录错误信息")
            # 这里可以添加重新连接或记录错误信息的代码
        except OSError as e:
            if e.errno == 10038:
                print("客户端连接已关闭")
                break
def receive_messages_from_client():
    # 创建一个UDP套接字来接收从客户发送过来的数据
    command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    command_socket.bind(('127.0.0.1', 8889))#绑定到本地ip和端口
    global pending_message
    while True:
        with message_lock:
            pending_message, _ = command_socket.recvfrom(1024)
            # print("成功从客户得到数据!!")


def receive_commands():
    # 创建一个UDP套接字来接收命令
    command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    command_socket.bind(('127.0.0.1', 8888))
    while True:
        command, _ = command_socket.recvfrom(1024)
        if command.decode() == 'exit':
            break
    # 发送退出命令给主线程
    exit_event.set()

# 创建一个事件，用于在收到退出命令时通知主线程
exit_event = threading.Event()

# 创建一个TCP服务器
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.4.100', 8882))  # 绑定到转换器地址和端口
server_socket.listen(1)  # 最多允许一个客户端连接

print("等待客户端连接...")
client_socket, client_address = server_socket.accept()
print(f"连接来自: {client_address}")

# 启动接收消息的线程
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# 启动接收停止命令的线程
command_thread = threading.Thread(target=receive_commands)
command_thread.start()

# 启动接收客户数据的线程
client_thread = threading.Thread(target=receive_messages_from_client)
client_thread.start()

# 启动发送消息的线程
send_thread = threading.Thread(target=send_message, args=(client_socket,))
send_thread.start()

# 等待接收命令的线程或收到退出命令时退出程序
exit_event.wait()

# 关闭连接
client_socket.close()
server_socket.close()

# 等待接收消息线程结束
receive_thread.join()
send_thread.join()
client_thread.join()
command_thread.join()