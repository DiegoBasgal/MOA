from pyModbusTCP.client import ModbusClient
import argparse


def invalid_f():
    print("Invalid nor no function selected.")
    print("READ functions: 1 - READ_COILS")
    print("                2 - READ_DISCRETE_INPUTS")
    print("                3 - READ_HOLDING_REGISTERS")
    print("                4 - READ_INPUT_REGISTERS")
    print("READ functions: 5 - WRITE_SINGLE_COIL")
    print("                6 - WRITE_SINGLE_REGISTER")
    exit()


parser = argparse.ArgumentParser(description="Modbus util")
parser.add_argument("--host", type=str)
parser.add_argument("--port", type=int)
parser.add_argument("--unit_id", type=int)
parser.add_argument("--timeout", type=int)
parser.add_argument("--addr", type=int)
parser.add_argument("--multiple", type=int)
parser.add_argument("--write", action="store_true")
parser.add_argument("--value", type=int)
parser.add_argument("--read", action="store_true")
parser.add_argument("--verbose", action="store_true", help="Enable verbose")
parser.add_argument("--function", type=int)
args = parser.parse_args()

verbose = args.verbose
read = args.read
host = args.host if args.host else "localhost"
port = args.port if args.port else 502
unit_id = args.unit_id if args.unit_id else 1
timeout = args.timeout if args.timeout else 5
verbose = args.verbose
write = True if args.write else False
addr = args.addr if args.addr else 0
multiple = args.multiple if args.multiple else 1
value = args.value if args.value else 0
read = args.read
f = args.function if args.function else 0

if verbose:
    print("verbose = {}".format(verbose))
    print("read = {}".format(read))
    print("host = {}".format(host))
    print("port = {}".format(port))
    print("unit_id = {}".format(unit_id))
    print("timeout = {}".format(timeout))
    print("verbose = {}".format(verbose))
    print("write = {}".format(write))
    print("addr = {}".format(addr))
    print("multiple = {}".format(multiple))
    print("value = {}".format(value))
    print("read = {}".format(read))
    print("function = {}".format(f))

modbus = ModbusClient(
    host, port, unit_id, timeout, debug=verbose, auto_open=True, auto_close=True
)
if read and write:
    print("Cannot read and write at same time.")
    exit()

if write:

    if f == 5:
        f = modbus.write_single_coil
    elif f == 6:
        f = modbus.write_single_register
    else:
        invalid_f()

    if verbose:
        print("Writing {} to addr {}...".format(value, addr))
    response = f(addr, value)
    if verbose:
        print("response = {}".format(response))

if read:

    if f == 1:
        f = modbus.read_coils
    elif f == 2:
        f = modbus.read_discrete_inputs
    elif f == 3:
        f = modbus.read_holding_registers
    elif f == 4:
        f = modbus.read_input_registers
    else:
        invalid_f()

    if verbose:
        print("Reading addr {}...".format(addr))
    response = f(addr, multiple)
    if multiple == 1:
        print("response = {}".format(response))
    else:
        nlines = len(response) // 10
        for line in range(nlines):
            print(
                "{:6d} : {:>6d} {:>6d} {:>6d} {:>6d} {:>6d} {:>6d} {:>6d} {:>6d} {:>6d} {:>6d} : {:<6d} ".format(
                    addr + line * 10,
                    *response[line * 10 : (line + 1) * 10],
                    addr + line * 10 + 9
                )
            )
