import socket
import struct
from datetime import datetime
from time import sleep
import pyodbc
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import crc16


def bcd_to_i(i):
    value = (i & 0xF)
    value += ((i >> 4) & 0xF) * 10
    value += ((i >> 8) & 0xF) * 100
    value += ((i >> 12) & 0xF) * 1000
    return value


def addcrc(data):
    crc = hex(crc16(data))
    crc = bytes.fromhex(crc[4] + crc[5] + crc[2] + crc[3])
    return data + crc


def escrever_no_banco(data, medidor, potencia):
    data = data.strftime('%Y-%m-%d %H:%M:%S.000')
    potencia = round(potencia, 3)
    q = "INSERT INTO [dbo].[registros_medidores] VALUES('{}','{}',{});".format(data, medidor, potencia)

    DB_SERVER = "lug-cog"
    DB_DATABASE = "COG_CURITIBA"
    DB_USERNAME = 'sa'
    DB_PASSWORD = 'ctba2020'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + DB_SERVER +
                          ';DATABASE=' + DB_DATABASE + ';UID=' + DB_USERNAME + ';PWD=' + DB_PASSWORD, autocommit=True)
    cursor = cnxn.cursor()
    cursor.execute("SET DATEFORMAT ymd")
    cursor.execute(q)
    print("Escrito no banco")


medidores_NBR = {
    #                IP          PORT  +/- TP    TC  ESCALA
    "SEB_MP": ["192.141.60.208", 8001, -1 * (350) * (20) * (0.001)],
    "SEB_MR": ["192.141.60.208", 8002, -1 * (350) * (20) * (0.001)],
    "POP_MP": ["177.85.112.52", 5001, -1 * (700) * (20) * (0.001)],
    "POP_MR": ["177.85.112.52", 5002, -1 * (700) * (20) * (0.001)],
    "COV_MP": ["177.220.134.10", 5006, -1 * (175) * (20) * (0.001)],
    "COV_MR": ["177.220.134.10", 5005, -1 * (175) * (20) * (0.001)],
}

medidores_MODBUS = {
    "P48_MP": ["138.94.32.11", 8003, 1, 0.1],
    "P48_MR": ["138.94.32.11", 8004, 1, 0.1],
    "XAV_MP": ["177.38.9.166", 7784, 1, 0.1],
    "XAV_MR": ["177.38.9.166", 7785, 1, 0.1],
}

for medidor in medidores_NBR:
    try:
        ip, porta, k = medidores_NBR.get(medidor)
        sock = socket.socket()
        sock.settimeout(5)
        sock.connect((ip, porta))
    except BaseException as e:
        print("COMS-TEST {} FAILLED: {}".format(medidor, e))
    finally:
        sock.close()

while True:
    try:
        resultados = []
        t0 = datetime.now()
        hora = t0.hour
        minuto = t0.minute
        segundo = t0.second
        dia = t0.day
        mes = t0.month
        ano = t0.year
        for medidor in medidores_NBR:
            try:
                ip, porta, k = medidores_NBR.get(medidor)
                sock = socket.socket()
                sock.settimeout(5)
                sock.connect((ip, porta))
                data = bytes.fromhex('019914000001020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
                data = addcrc(data)
                sock.send(data)
                response = sock.recv(1024)
                response = response[1:]
                # hora = bcd_to_i(response[6])
                # minuto = bcd_to_i(response[7])
                # segundo = bcd_to_i(response[8])
                # dia = bcd_to_i(response[9])
                # mes = bcd_to_i(response[10])
                # ano = bcd_to_i(response[11])
                pot_ativa_trifasica = k * struct.unpack('f', response[64:68])[0]
                resultados.append([t0, medidor, pot_ativa_trifasica])
                print(resultados[-1])
                sock.close()

            except socket.timeout:
                print("{} timmed out".format(medidor))
                continue

            except BaseException:
                continue

        for medidor in medidores_MODBUS:
            ip, porta, mode, k = medidores_MODBUS.get(medidor)
            slave = ModbusClient(host=ip, port=porta, timeout=5, unit_id=100, auto_open=False, auto_close=False)
            slave.mode(mode)
            if(slave.open()):
                regs = slave.read_holding_registers(32, 2)
                raw = ((regs[0] << 16) + regs[1])
                if raw > 0b1000000000000000:
                    raw = 0xffffffff - raw
                pot_ativa_trifasica = round(k * raw, 2)
                linha = "{}, {:02d}/{:02d}/20{:02d} {:02d}:{:02d}:{:02d}, {:.2f}".format(medidor, dia, mes, ano, hora, minuto, segundo, pot_ativa_trifasica)
                resultados.append([t0, medidor, pot_ativa_trifasica])
                print(resultados[-1])
            else:
                print(medidor, "failled")
            slave.close()
        for resultado in resultados:
            t0, medidor, pot_ativa_trifasica = resultado
            escrever_no_banco(t0, medidor, pot_ativa_trifasica)

        delta_t = datetime.now() - t0
        sleep(max(30 - delta_t.seconds, 0))

    except BaseException as e:
        print(e)
        continue
"""
sock = socket.socket()
sock.settimeout(5)
sock.connect(('192.141.60.208', 8002))
data = bytes.fromhex(
    '019914000001020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
data = addcrc(data)
sock.send(data)
response = sock.recv(1024)
response = response[1:]
hora = bcd_to_i(response[6])
minuto = bcd_to_i(response[7])
segundo = bcd_to_i(response[8])
dia = bcd_to_i(response[9])
mes = bcd_to_i(response[10])
ano = bcd_to_i(response[11])
pot_ativa_trifasica = -7 * struct.unpack('f', response[64:68])[0]
linha = "{:02d},{:02d},{:02d},{:02d},{:02d},{:02d},{:.2f}".format(dia, mes, ano, hora, minuto, segundo,
                                                                  pot_ativa_trifasica)
print(linha)
with open("out_8002.csv", "+a") as file:
    file.write("{:02d},{:02d},{:02d},{:02d},{:02d},{:02d},{:.2f}\n".format(dia, mes, ano, hora, minuto, segundo,
                                                                           pot_ativa_trifasica))
sock.close()
"""
