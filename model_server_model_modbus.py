import socket
import struct
import threading
from pymodbus.client import ModbusTcpClient
import time
#创建全局变量用于存储从客户发送过来的信息
pending_message = []
pending_message1 = []
pending_message2 = []
pending_message3 = []
old_pending_message = []
old_pending_message1 = []
old_pending_message2 = []
old_pending_message3 = []
message_lock = threading.Lock()
count = 0
def send_message(client_socket):
    global pending_message, old_pending_message
    global pending_message1, old_pending_message1
    global pending_message2, old_pending_message2
    global pending_message3, old_pending_message3
    while True:
        try:
            # if old_pending_message1 != pending_message1:
            #     # count = count + 1
            #     # if count % 2 != 0:
            #     #     message1 = pending_message
            #     # else:
            #     #     message2 = pending_message
            #     #     client_socket.send(message1)
            #     #     client_socket.send(message2)
            #     #     print("成功向模型发送消息！！")
            #     old_pending_message1 = pending_message1
            #     client_socket.send(pending_message1)
            #     print("*************成功向模型发送消息1！！")
            # time.sleep(0.5)
            # if old_pending_message2 != pending_message2:
            #     old_pending_message2 = pending_message2
            #     client_socket.send(pending_message2)
            #     print("********************成功向模型发送消息2！！") 
            # time.sleep(0.5)
            # if old_pending_message3 != pending_message3:
            #     old_pending_message3 = pending_message3
            #     client_socket.send(pending_message3)
            #     print("*****************************成功向模型发送消息3！！") 
            # time.sleep(0.5)
            if old_pending_message != pending_message:
                old_pending_message = pending_message
                client_socket.send(pending_message)
                print("*****************************成功向模型发送消息！！") 
            time.sleep(0.5)
        except ConnectionAbortedError:
            print("连接被中止，尝试重新连接或记录错误信息")
            # 这里可以添加重新连接或记录错误信息的代码

def receive_messages(client_socket):
    client = ModbusTcpClient('192.168.50.198', port=504)
    client.connect()
    unit_id = 1    # 单元标识符，通常为1
    client.close()
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
                    address = 40007  # 寄存器地址
                    value = data_value   # 要写入的值
                    result = client.write_register(address, value, unit=unit_id)
                    if not result.isError():
                        print("写入成功")
                    else:
                        print("写入失败", result)
                elif frame_id == '0x1b' :
                    print("totalBrakeEnergy:", data_value)
                    address = 40008  # 寄存器地址
                    value = data_value   # 要写入的值
                    result = client.write_register(address, value, unit=unit_id)
                    if not result.isError():
                        print("写入成功")
                    else:
                        print("写入失败", result)
                elif frame_id == '0x1c' :
                    print("tractionEnergy:", data_value)
                    address = 40009  # 寄存器地址
                    value = data_value   # 要写入的值
                    result = client.write_register(address, value, unit=unit_id)
                    if not result.isError():
                        print("写入成功")
                    else:
                        print("写入失败", result)
                elif frame_id == '0x1d' :
                    print("totalTractionEnergy:", data_value)
                    address = 40010  # 寄存器地址
                    value = data_value   # 要写入的值
                    result = client.write_register(address, value, unit=unit_id)
                    if not result.isError():
                        print("写入成功")
                    else:
                        print("写入失败", result)
        except ConnectionAbortedError:
            print("连接被中止，尝试重新连接或记录错误信息")
            # 这里可以添加重新连接或记录错误信息的代码
        except OSError as e:
            if e.errno == 10038:
                print("客户端连接已关闭")
                break
def receive_messages_from_client():
    # Modbus TCP服务器信息
    MODBUS_SERVER_IP = '192.168.50.198'  # Modbus服务器的IP
    MODBUS_SERVER_PORT = 504          # 通常Modbus TCP使用502端口

    # Modbus保持寄存器地址
    HOLDING_REGISTER_VOLTAGE_ADDRESS1 = 40005 - 40001  # 从0开始索引
    HOLDING_REGISTER_VOLTAGE_ADDRESS2 = 40006 - 40001  # 从0开始索引
    HOLDING_REGISTER_VOLTAGE_ADDRESS3 = 40007 - 40001  # 从0开始索引

    # 创建Modbus TCP客户端
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)
    while True:
        # 尝试连接到Modbus服务器
        if client.connect():
            # 读取保持寄存器中的数据
            #速度
            response1 = client.read_holding_registers(HOLDING_REGISTER_VOLTAGE_ADDRESS1, count=1, unit=1)
            #乘客
            response2 = client.read_holding_registers(HOLDING_REGISTER_VOLTAGE_ADDRESS2, count=1, unit=1)
            #速度差
            response3 = client.read_holding_registers(HOLDING_REGISTER_VOLTAGE_ADDRESS3, count=1, unit=1)
            if response1.isError() or response2.isError() or response3.isError():
                print(f"读取寄存器地址{40007}的电压值失败: {response3}")
            else:
                # 获取寄存器中的原始数值
                value1 = response1.registers[0]
                value2 = response2.registers[0]
                value3 = response3.registers[0]
                # print(f"读取寄存器地址{40007}的数值: {value3}")

                # 将其打包为CAN数据帧的格式
                # 数据长度为8字节
                data_length = 4
                # 帧ID为0x01
                frame_id1 = 0x01
                frame_id2 = 0x02
                frame_id3 = 0x03
                # 将数转换为字节表示
                data_bytes1 = struct.pack('<I', value1)
                data_bytes2 = struct.pack('<I', value2)
                data_bytes3 = struct.pack('<I', value3)
                data_bytes4 = struct.pack('<I', 0)
                # 打包CAN消息
                can_message1 = struct.pack('>BI4s4s', data_length, frame_id1, data_bytes1, data_bytes4)
                can_message2 = struct.pack('>BI4s4s', data_length, frame_id2, data_bytes2, data_bytes4)
                can_message3 = struct.pack('>BI4s4s', data_length, frame_id3, data_bytes3, data_bytes4)
                # # 
                global pending_message 
                pending_message = can_message1
                time.sleep(0.5)
                pending_message = can_message2
                time.sleep(0.5)
                pending_message = can_message3
                time.sleep(0.5)
                # global pending_message1 
                # pending_message1 = can_message1
                # time.sleep(0.5)
                # global pending_message2 
                # pending_message2 = can_message2
                # time.sleep(0.5)
                # global pending_message3 
                # pending_message3 = can_message3
                # time.sleep(0.5)

        else:
            print(f"无法连接到Modbus服务器 {MODBUS_SERVER_IP}:{MODBUS_SERVER_PORT}")
        time.sleep(0.1)


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