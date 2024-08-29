import socket
import struct
import threading
from pymodbus.client import ModbusTcpClient
import time

# Modbus TCP服务器信息
MODBUS_SERVER_IP = '192.168.50.198'  # Modbus服务器的IP
MODBUS_SERVER_PORT = 504          # 通常Modbus TCP使用502端口

# Modbus保持寄存器地址
HOLDING_REGISTER_VOLTAGE_ADDRESS1 = 40005 - 40001  # 从0开始索引
HOLDING_REGISTER_VOLTAGE_ADDRESS2 = 40006 - 40001  # 从0开始索引
HOLDING_REGISTER_VOLTAGE_ADDRESS3 = 40007 - 40001  # 从0开始索引

# 创建Modbus TCP客户端
    #速度差
client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)
while True:
    # 尝试连接到Modbus服务器
    if client.connect():
        address = 40006  # 寄存器地址
        value = 12   # 要写入的值
        result = client.write_register(HOLDING_REGISTER_VOLTAGE_ADDRESS2, value, unit=1)
        if not result.isError():
            print("写入成功")
        else:
            print("写入失败", result)
        # 读取保持寄存器中的数据
        #速度
        response1 = client.read_holding_registers(HOLDING_REGISTER_VOLTAGE_ADDRESS1, count=1, unit=1)
        #乘客
        response2 = client.read_holding_registers(HOLDING_REGISTER_VOLTAGE_ADDRESS2, count=1, unit=1)
        response3 = client.read_holding_registers(HOLDING_REGISTER_VOLTAGE_ADDRESS3, count=1, unit=1)
        if response1.isError() or response2.isError() or response3.isError():
            print(f"读取寄存器地址{40007}的电压值失败: {response3}")
        else:
            # 获取寄存器中的原始数值
            value1 = response1.registers[0]
            value2 = response2.registers[0]
            value3 = response3.registers[0]
        print(value2)