import getpass
import socket
import argparse
import os
import sys
import re


class FTP:
    BUFFER_SIZE = 4096

    def __init__(self, server, port, filename, socket_timeout=2):
        self.server = server
        self.port = port
        self.filename = filename
        self.login = None
        self.password = None

        socket.setdefaulttimeout(socket_timeout)
        self.server_socket = socket.socket()
        self.data_socket = socket.socket()

    def send(self, data, sock=None, log=True):
        if not data.endswith(b'\r\n'):
            data += b'\r\n'
        if not sock:
            sock = self.server_socket

        try:
            sock.send(data)
        except socket.error:
            return

        if log:
            print(data.decode('utf8', errors='ignore'))

        return True

    def receive(self, sock=None, log=True):
        if not sock:
            sock = self.server_socket

        data = b''
        try:
            while True:
                chunk = sock.recv(self.BUFFER_SIZE)
                data += chunk
                if len(chunk) <= self.BUFFER_SIZE:
                    break
        except socket.timeout:
            pass
        except socket.error:
            return

        if log:
            print(data.decode('utf8', errors='ignore'))

        return data

    def start(self):
        try:
            self.server_socket.connect((self.server, self.port))
        except socket.error:
            print('Error occurred while connecting to server')
            return

        try:
            data = self.server_socket.recv(1024)
            if b'FTP' not in data:
                print(f'<{self.server}:{self.port}> is not a FTP Server')
                return
        except socket.error as e:
            print(f'<{self.server}:{self.port}> is not a FTP Server')
            return

        print(f'Connection to {self.server}:{self.port} established')

        if not self.authorization():
            return
        print(f'User {self.login} is authorized')

        self.send('HELP'.encode())
        data = self.receive()
        self.send('EPSV'.encode() if b'EPSV' in data else 'PASV'.encode())

        port_regexp = re.compile(r'\(\|\|\|(\d+)\|\)')
        data = self.receive().decode('utf8', errors='ignore')
        port = port_regexp.search(data)
        if not port:
            print('Unable to send file. Port is not defined')
            return
        port = int(port.group(1))

        self.data_socket.connect((self.server, port))
        print(f'Established passive connection through port: {port}')

        self.send(f'STOR {os.path.basename(self.filename)}'.encode())
        with open(self.filename, 'rb') as f:
            content = f.read()
        if self.send(content, sock=self.data_socket, log=False):
            print(f'File {self.filename} uploaded')
        else:
            print(f'Cannot send file {self.filename}')
        self.data_socket.close()
        self.receive()

    def authorization(self):
        self.login = input('Enter login: ')
        self.password = getpass.getpass('Enter password: ')

        if not self.send(f'USER {self.login}'.encode()):
            return
        data = self.receive()
        if not data or not data.startswith(b'3'):
            message = data.decode("utf8") if data else "-"
            print(f'Cannot authorize:   {message}')
            return

        if not self.send(f'PASS {self.password}'.encode()):
            return
        data = self.receive()
        if not data or not data.startswith(b'2'):
            message = data.decode("utf8") if data else "-"
            print(f'Cannot authorize:   {message}')
            return

        return True

    def close(self):
        self.server_socket.close()
        self.data_socket.close()


def main(server, port, filename):
    ftp = FTP(server, port, filename)
    try:
        ftp.start()
    finally:
        ftp.close()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', action='store', required=True,
                        help='FTP Server')
    parser.add_argument('-p', '--port', action='store', type=int, default=21,
                        help='FTP Port, 21 by default')
    parser.add_argument('filename', action='store',
                        help='File to upload')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    if not os.path.exists(args.filename):
        print(f'File <{args.filename}> does not exist')
        sys.exit(10)
    if not os.path.isfile(args.filename):
        print(f'<{args.filename}> is not a file')
        sys.exit(11)

    main(args.server, args.port, args.filename)
