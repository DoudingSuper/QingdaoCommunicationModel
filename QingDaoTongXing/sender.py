import socket
import csv
import sys
import struct

def read_csv(filename):
    """读取CSV文件"""
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # 将CSV中的每一行数据作为一组数据
            data.append(row)
    return data

def hex_convert(data):
    """将数据转换为16进制表示"""
    return struct.unpack('<I', struct.pack('<data', data))[0]

def generate_frame_ids(num_columns):
    """根据列数生成帧ID列表"""
    return [f"00 00 00 {i:02}" for i in range(num_columns)]

def convert_csv_to_can(csv_filename):
    """将CSV文件转换为CAN数据"""
    can_data = []

    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        
        # 获取列数并生成帧ID列表
        num_columns = len(next(reader))
        frame_ids = generate_frame_ids(num_columns)
        
        # 逐行处理数据
        for row in reader:
            # 每一行数据对应一个帧ID
            for frame_id, data in zip(frame_ids, row):
                # 将数据转换为16进制表示
                hex_data = hex_convert(int(data))
                
                # 组织CAN消息格式
                can_message = f"{'{:02X}'.format(len(data))} {' '.join(frame_id.split())} {hex_data}"
                
                # 添加到CAN数据列表
                can_data.append(can_message)
    
    return can_data

def send_data(can_data, host, port):
    """发送数据到转换装置"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # 逐行发送数据
        can_data_str = [str(item) for item in can_data]
        for data in can_data_str:
            # 发送数据
            s.sendall(data.encode())
            # 打印已发送的数据
            print("已发送数据:", data)
            # # 检查用户是否输入了终止命令
            # if input("按下 'q' 键并回车终止程序，或者按回车键继续发送数据：").strip().lower() == 'q':
            #     print("用户终止了程序。")
            #     sys.exit()  # 终止程序
        print("数据已发送到", (host, port))

if __name__ == "__main__":
    # 读取CSV文件
    csv_filename = 'test_data.csv'
    csv_data = read_csv(csv_filename)
    # can_data = convert_csv_to_can('test_data.csv')
    # 设置转换装置的主机和端口
    converter_host = '192.168.4.101'#转换器IP地址
    converter_port = 8882
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((converter_host, converter_port))
        data = '04 00 00 00 02 35 85 01 00 00 00 00 00'
        s.sendall(data.encode())
        print("发送成功")
    # 发送数据到转换装置
    # send_data(csv_data, converter_host, converter_port)
