import socket
from tqdm import tqdm 
import json
import sys

PACKAGE_SIZE = 1024

def send_message(sock: socket.socket, transactions: list):
    """
    Отправляет набор транзакций по протоколу TCP.


            Параметры:
                    sock (socket.socket) : сокет связи 
                    transactions (list) : список транзакций для отправки
    """
    global PACKAGE_SIZE
    message = json.dumps(transactions)
    message_size = sys.getsizeof(message)
    sock.send(str(message_size).encode("utf-8"))
    print(sock.recv(PACKAGE_SIZE).decode("utf-8"))
    bar = tqdm(range(message_size), f"Отправка транзакций {message_size} байт", unit="B", unit_scale=True, unit_divisor=PACKAGE_SIZE)
    start_msg = 0
    end_msg = PACKAGE_SIZE

    while True:
        data = message[start_msg:end_msg]
        if not data:
            break
        sock.send(data.encode("utf-8"))
        sock.recv(PACKAGE_SIZE).decode("utf-8")
        bar.update(len(data))
        start_msg += PACKAGE_SIZE
        end_msg += PACKAGE_SIZE
    print("Транзакции успешно отправлены")

def receive_message(sock: socket.socket):
    """
    Получает сообщение по протоколу TCP.


            Параметры:
                    sock (socket.socket) : сокет связи 
            
                    
            Возвращаемое значение: список транзакций, подписанных хэшем SHA-256

    """
    global PACKAGE_SIZE
    message = ""
    msg_size = int(sock.recv(4).decode("utf-8"))
    sock.send(f"Получен размер файла, {msg_size} байт".encode("utf-8"))
    bar = tqdm(range(msg_size), f"Отправка транзакций {msg_size} байт", unit="B", unit_scale=True, unit_divisor=PACKAGE_SIZE)
    while len(message) != msg_size:
        data = sock.recv(PACKAGE_SIZE).decode("utf-8")

        if not data:
            break
        message += data
        sock.send("Получено сообщение".encode("utf-8"))
        bar.update(len(data))
    return json.loads(message)


    
