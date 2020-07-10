import argparse
import sys
import time
import socket
import select
import struct
import threading
from decimal import Decimal

BUFFER_SIZE = 4096


class SNTP:
    HEADER_FORMAT = ">BBBBII4sQQQQ"
    UTC_OFFSET = 2208988800
    LI = 0
    VN = 4
    MODE = 4
    STRATUM = 1

    def __init__(self, recv_packet, offset):
        self.offset = 0
        self.recv_time = self.get_current_time()
        self.transmit_time = self.get_transmit_time(recv_packet)
        self.offset = offset

    def get_current_time(self):
        time_with_offset = time.time() + self.UTC_OFFSET + self.offset
        return int(Decimal(time_with_offset) * (2 ** 32))

    def get_transmit_time(self, recv_packet):
        return struct.unpack(self.HEADER_FORMAT, recv_packet)[10]

    def build_packet(self):
        return struct.pack(
            self.HEADER_FORMAT,
            self.LI << 6 | self.VN << 3 | self.MODE, self.STRATUM,
            0, 0, 0, 0, b'', 0, self.transmit_time, self.recv_time,
            self.get_current_time()
        )


class WorkerSNTP(threading.Thread):
    def __init__(self, sock, offset):
        super().__init__()
        self.sock = sock
        self.offset = offset
        self.recv_packet = None
        self.addr = None
        self.recv_time = None

    def run(self):
        self.recv_packet, self.addr = self.sock.recvfrom(BUFFER_SIZE)
        print(" : ".join(map(lambda el: str(el), self.addr)))
        packet = SNTP(self.recv_packet, self.offset).build_packet()
        self.sock.sendto(packet, self.addr)


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', type=int, dest='delay', default=0,
                        help='The number of seconds a server should be '
                             'cheating on clients')

    parser.add_argument('-p', '--port', type=int, dest='port',
                        default=123,
                        help='Listening port.')

    return parser.parse_args()


def run_server(port, offset):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', port))
        print("Server is running...")
        while True:
            read_list, _, _ = select.select([sock], [], [], 1)
            if read_list:
                worker = WorkerSNTP(sock, offset)
                worker.start()


if __name__ == '__main__':
    args = parse_arguments()
    try:
        run_server(args.port, args.delay)
    except PermissionError:
        print("Permission error. Use sudo")
        sys.exit(11)
