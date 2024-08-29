def pack_can_message(can_id, data):
    # 构造CAN消息
    can_id_bytes = can_id.to_bytes(4, byteorder='big')  # 将CAN标识符转换为4字节的大端字节序
    dlc = len(data)  # 数据长度码为数据的长度
    dlc_byte = dlc.to_bytes(1, byteorder='big')  # 将DLC转换为1字节的大端字节序
    data_bytes = bytes(data)  # 将数据转换为字节类型

    # 拼接CAN消息
    can_message = can_id_bytes + dlc_byte + data_bytes

    return can_message

# 示例数据
can_id = 0x123
data = [0x01, 0x02, 0x03, 0x04]

# 将数据打包成CAN消息
can_message = pack_can_message(can_id, data)
print(can_message)

import struct

# 定义 CAN 标识符
can_id = 0x123

# 将 CAN 标识符打包为 4 个字节的大端字节序
can_id_packed = struct.pack('>I', can_id)

# 打印打包后的结果
print("CAN标识符打包后的字节序列：", can_id_packed)

import struct

# 定义要转换的十进制小数
decimal_number = 3.14

# 将十进制小数转换为小端字节序
decimal_packed = struct.pack('<f', decimal_number)

# 打印打包后的结果
print("十进制小数打包后的小端字节序列：", decimal_packed)
data = ' '.join([f'{x:02x}' for x in decimal_packed])
print(data)



# 从小端字节序中解包出十进制数
decimal_number = struct.unpack('<f', decimal_packed)[0]

# 打印解包后的十进制数
print("解包后的十进制数：", decimal_number)


# 数据
data_length = 8  # 数据长度为8字节
frame_id = 0x12345678  # 帧ID为0x12345678
data = 123.45  # 示例小数数据

# 将小数转换为字节表示，假设小数为双精度浮点数（64位）
data_bytes = struct.pack('<d', data)

# 打包CAN消息
can_message = struct.pack('>BI8s', data_length, frame_id, data_bytes)

# 打印打包后的CAN消息
print("打包后的CAN消息:", can_message)

data = ' '.join([f'{x:02x}' for x in can_message])
print(data)

# 解包CAN消息
data_length, frame_id, data_bytes = struct.unpack('>BI8s', can_message)

# 解包帧ID
frame_id = hex(frame_id)

# 解包数据
data = struct.unpack('<d', data_bytes)[0]

# 打印解包后的数据
print("数据长度:", data_length)
print("帧ID:", frame_id)
print("数据:", data)