from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# 创建Modbus数据存储
store = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0]*100),   # 离散输入
    co = ModbusSequentialDataBlock(0, [0]*100),   # 线圈
    hr = ModbusSequentialDataBlock(0, [0]*100),   # 保持寄存器
    ir = ModbusSequentialDataBlock(0, [0]*100)    # 输入寄存器
)
# 将值10写入保持寄存器地址为4007
store.setValues(3, 4007, [10])
context = ModbusServerContext(slaves=store, single=True)

# 启动Modbus TCP服务器
StartTcpServer(context, address=("192.168.128.9", 502))