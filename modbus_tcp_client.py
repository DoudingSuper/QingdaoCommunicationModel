from pymodbus.client import ModbusTcpClient
import time
# Modbus TCP服务器信息
MODBUS_SERVER_IP = '192.168.3.5'  # Modbus服务器的IP
MODBUS_SERVER_PORT = 502          # 通常Modbus TCP使用502端口

# Modbus保持寄存器地址
HOLDING_REGISTER_VOLTAGE_ADDRESS = 40007 - 40001  # 从0开始索引

# 创建Modbus TCP客户端
client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)
while True:
    # 尝试连接到Modbus服务器
    if client.connect():
        # 读取保持寄存器中的数据
        response = client.read_holding_registers(HOLDING_REGISTER_VOLTAGE_ADDRESS, count=1, unit=1)
        if response.isError():
            print(f"读取寄存器地址{40007}的电压值失败: {response}")
        else:
            # 获取寄存器中的原始数值
            raw_voltage_value = response.registers[0]
            # 将原始数值转换为实际电压值（传递值 = 实际值 * 10）
            actual_voltage_value = raw_voltage_value / 10.0
            print(f"读取寄存器地址{40007}的电压值实际值: {actual_voltage_value} V")
        
        # 断开客户端连接
        client.close()
    else:
        print(f"无法连接到Modbus服务器 {MODBUS_SERVER_IP}:{MODBUS_SERVER_PORT}")
    time.sleep(0.1)