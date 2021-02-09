import socket
from datetime import datetime
from MySQLdb import _mysql
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import DataBank


class Usina:

    status_moa = 0          # Menor que 10 é bom

    emergencia_elipse_acionada = False
    emergencia_django_acionada = False
    modo_manual_elipse_acionado = False
    estado_anterior_modo_manual_elipse = False
    modo_autonomo = True
    aguardando_reservatorio = False
    clp_online = False
    clp_ip = ''
    clp_porta = 0
    modbus_server_ip = ''
    modbus_server_porta = 0
    kp = 0
    ki = 0
    kd = 0
    kie = 0
    margem_pot_critica = 0
    n_movel_L = 0
    n_movel_R = 0
    nv_alvo = 0
    nv_maximo = 0
    nv_minimo = 0
    nv_montante = 0
    nv_religamento = 0
    posicao_comporta = 0
    pot_minima = 0
    pot_nominal = 0
    pot_nominal_ug = 2.5
    pot_disp = 0
    timer_erro = 0
    ug1_disp = 0
    ug1_pot = 0
    ug1_setpot = 0
    ug1_sinc = False
    ug1_tempo = 0
    ug2_disp = 0
    ug2_pot = 0
    ug2_setpot = 0
    ug2_sinc = False
    ug2_tempo = 0
    valor_ie_inicial = 0.3
    mysql_config = {
        'host': "localhost",
        'user': "root",
        'passwd': "11Marco2020@",
        'db': "django_db",
        'charset': 'utf8'
    }

    def __init__(self):
        self.modbus_server_ip = get_ip_local()
        self.atualizar_valores_locais()
        self.status_moa = 7

    def atualizar_valores_locais(self):

        # Atualiza ip local
        self.modbus_server_ip = get_ip_local()

        # Lê do banco
        db = _mysql.connect(**self.mysql_config)
        db.query("""SELECT *
                    FROM parametros_moa_parametrosusina
                    WHERE id = 1""")
        r = db.store_result()
        parametros = r.fetch_row(maxrows=1, how=2)[0]
        for parametro in parametros:
            parametros[parametro] = parametros[parametro].decode('utf-8')

        self.modo_autonomo = True if int(parametros['parametros_moa_parametrosusina.modo_autonomo']) > 0 else False
        self.emergencia_django_acionada = int(parametros['parametros_moa_parametrosusina.emergencia_django_acionada'])
        self.clp_ip = parametros['parametros_moa_parametrosusina.clp_ip']
        self.clp_porta = int(parametros['parametros_moa_parametrosusina.clp_porta'])
        self.modbus_server_porta = int(parametros['parametros_moa_parametrosusina.modbus_server_porta'])
        self.kp = float(parametros['parametros_moa_parametrosusina.kp'])
        self.ki = float(parametros['parametros_moa_parametrosusina.ki'])
        self.kd = float(parametros['parametros_moa_parametrosusina.kd'])
        self.kie = float(parametros['parametros_moa_parametrosusina.kie'])
        self.margem_pot_critica = float(parametros['parametros_moa_parametrosusina.margem_pot_critica'])
        self.n_movel_L = int(parametros['parametros_moa_parametrosusina.n_movel_L'])
        self.n_movel_R = int(parametros['parametros_moa_parametrosusina.n_movel_R'])
        self.nv_alvo = float(parametros['parametros_moa_parametrosusina.nv_alvo'])
        self.nv_maximo = float(parametros['parametros_moa_parametrosusina.nv_maximo'])
        self.nv_minimo = float(parametros['parametros_moa_parametrosusina.nv_minimo'])
        self.nv_religamento = float(parametros['parametros_moa_parametrosusina.nv_religamento'])
        self.pot_minima = float(parametros['parametros_moa_parametrosusina.pot_minima'])
        self.pot_nominal = float(parametros['parametros_moa_parametrosusina.pot_nominal'])
        self.pot_nominal_ug = float(parametros['parametros_moa_parametrosusina.pot_nominal_ug'])
        self.timer_erro = int(parametros['parametros_moa_parametrosusina.timer_erro'])

        # Comunicação modbus
        # LEITURA nv montante = 0
        # LEITURA disp = 2 e 4
        # LEITURA pot real 8 e 9
        client = ModbusClient(host=self.clp_ip, port=self.clp_porta, timeout=5, unit_id=1)
        if client.open():

            regs = client.read_holding_registers(0, 100)
            client.close()

            if regs is None:
                raise ConnectionError

            self.nv_montante = round((regs[0] * 0.001) + 620, 2)
            self.ug1_disp = False if regs[2] else True
            self.ug2_disp = False if regs[4] else True
            self.ug1_pot = regs[8] / 1000
            self.ug2_pot = regs[9] / 1000
            self.ug1_sinc = True if self.ug1_pot > 0 else False
            self.ug2_sinc = True if self.ug2_pot > 0 else False
            self.ug1_tempo = regs[10]
            self.ug2_tempo = regs[11]
            self.clp_online = True

        else:
            self.clp_online = False
        self.pot_disp = 0
        if self.ug1_disp:
            self.pot_disp += 2.5
        if self.ug2_disp:
            self.pot_disp += 2.5

        self.emergencia_elipse_acionada = DataBank.get_words(1000, 1)[0]

        estado_anterior_modo_manual_elipse = self.modo_manual_elipse_acionado
        self.modo_manual_elipse_acionado = True if DataBank.get_words(1001, 1)[0] > 0 else False

        # se mudou de estado, atualiza
        if not (self.modo_manual_elipse_acionado == estado_anterior_modo_manual_elipse):
            self.modo_autonomo = not self.modo_manual_elipse_acionado
            # atualiza no banco tbm
            q = """UPDATE parametros_moa_parametrosusina
                   SET modo_autonomo = '{}'
                   WHERE id = 1; """.format(1 if self.modo_autonomo else 0)
            db = _mysql.connect(**self.mysql_config)
            db.query(q)
            db.commit()

    def atualizar_valores_remotos(self):

        # Escreve no banco
        q = """UPDATE parametros_moa_parametrosusina
                   SET
                   timestamp = '{}',
                   status_moa = '{}',
                   emergencia_elipse_acionada = {},
                   aguardando_reservatorio = {},
                   clp_online = {},
                   nv_montante = {},
                   posicao_comporta = {},
                   pot_disp = {},
                   ug1_disp = {},
                   ug1_pot = {},
                   ug1_setpot = {},
                   ug1_sinc = {},
                   ug1_tempo = {},
                   ug2_disp = {},
                   ug2_pot = {},
                   ug2_setpot = {},
                   ug2_sinc = {},
                   ug2_tempo = {}
                   WHERE id = 1; 
                     """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                self.status_moa,
                                self.emergencia_elipse_acionada,
                                1 if self.aguardando_reservatorio else 0,
                                1 if self.clp_online else 0,
                                self.nv_montante,
                                self.posicao_comporta,
                                self.pot_disp,
                                1 if self.ug1_disp else 0,
                                self.ug1_pot,
                                self.ug1_setpot,
                                1 if self.ug1_sinc else 0,
                                self.ug1_tempo,
                                1 if self.ug2_disp else 0,
                                self.ug2_pot,
                                self.ug2_setpot,
                                1 if self.ug2_sinc else 0,
                                self.ug2_tempo)

        db = _mysql.connect(**self.mysql_config)
        db.query(q)
        db.commit()

        # Comunicação modbus
        # ESCRITA set pot = 1 e 3
        client = ModbusClient(host=self.clp_ip, port=self.clp_porta, timeout=5, unit_id=1)
        if client.open():
            client.write_single_register(1, int(self.ug1_setpot * 1000))
            client.write_single_register(3, int(self.ug2_setpot * 1000))
            client.close()
        else:
            self.clp_online = False
            raise ConnectionError

    def acionar_emergerncia_clp(self):

        self.ug1_setpot = 0
        self.ug1_disp = 0
        self.ug2_setpot = 0
        self.ug2_disp = 0

        client = ModbusClient(host=self.clp_ip, port=self.clp_porta, timeout=5, unit_id=1)
        if client.open():
            client.write_single_register(1, int(0))
            client.write_single_register(2, int(1))
            client.write_single_register(3, int(0))
            client.write_single_register(4, int(1))
            client.close()
        else:
            self.clp_online = False
            raise ConnectionError

    def remover_emergencia_clp(self):

        client = ModbusClient(host=self.clp_ip, port=self.clp_porta, timeout=5, unit_id=1)
        if client.open():
            client.write_single_register(2, int(0))
            client.write_single_register(4, int(0))
            client.close()
        else:
            self.clp_online = False
            raise ConnectionError


def get_ip_local():
    s = 0
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        temp = s.getsockname()[0]
    except Exception:
        temp = 'localhost'
    finally:
        s.close()
    return temp
