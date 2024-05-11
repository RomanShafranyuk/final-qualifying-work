import socket
from tqdm import tqdm 
import json
import sys

PACKAGE_SIZE = 1024
def send_command(socket: socket.socket, command:str):
    """
    Отправляет на сервер команду от клиента.


            Параметры:
                    socket (socket.socket) : сокет связи 
                    command (str) : команда от клиента для обращения к сервису 
    """
    socket.send(command.encode("utf-8"))


def receive_command(socket:socket.socket):
    """
    Принимает команду от клиента


            Параметры:
                    socket (socket.socket) : сокет связи 
    """
    return socket.recv(4).decode("utf-8")


def send_message(socket: socket.socket, message: list):
    """
    Отправляет сообщение в виде списка по протоколу TCP.


            Параметры:
                    socket (socket.socket) : сокет связи 
                    transactions (list) : сообщение 
    """
    global PACKAGE_SIZE
    data_to_send = json.dumps(message) 
    message_size = sys.getsizeof(data_to_send)
    socket.send(message_size.to_bytes(4, 'little'))
    print(socket.recv(PACKAGE_SIZE).decode("utf-8")) 
    bar = tqdm(range(message_size), f"Отправка транзакций {message_size} байт")

    ind = 0
    while True:
        if ind + PACKAGE_SIZE >= message_size:
            pack_size = message_size - ind
        else:
            pack_size = PACKAGE_SIZE
        package = data_to_send[ind:ind+pack_size]
        try:
            socket.send(package.encode("utf-8"))
        except TimeoutError:
            print("Send: timeout")

        try:
            socket.recv(PACKAGE_SIZE).decode("utf-8")
        except TimeoutError:
            print("Recv: timeout")
        bar.update(len(package))
        ind += pack_size
        if ind >= message_size:
            break
    socket.send("END".encode("utf-8"))
    print(f"{message_size}, {ind}\n Сообщение  успешно отправлено")

def receive_message(socket: socket.socket):
    """
    Получает сообщение по протоколу TCP.


            Параметры:
                    socket (socket.socket) : сокет связи 
            
                    
            Возвращаемое значение: список транзакций, подписанных хэшем SHA-256

    """
    global PACKAGE_SIZE
    len_packages = []
    message = bytearray()
    msg_size = int.from_bytes(socket.recv(4), 'little')
    socket.send(f"Получен размер файла, {msg_size} байт".encode("utf-8"))
    bar = tqdm(range(msg_size), f"Отправка транзакций {msg_size} байт")
    while True:
        package = socket.recv(PACKAGE_SIZE)
        if package.decode("utf-8") == "END": 
            bar.update(len(package))
            break
        len_packages.append(len(package))
        message.extend(package)
        socket.send("Получено сообщение".encode("utf-8"))
        bar.update(len(package))
    
    
    return json.loads(message.decode("utf-8"))