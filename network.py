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
    message = json.dumps(transactions) # msg string
    message_size = sys.getsizeof(message)
    sock.send(message_size.to_bytes(4, 'little')) # send message size
    print(sock.recv(PACKAGE_SIZE).decode("utf-8")) # recv system message
    bar = tqdm(range(message_size), f"Отправка транзакций {message_size} байт")#, unit="B", unit_scale=True, unit_divisor=PACKAGE_SIZE)

    ind = 0
    while True:
        if ind + PACKAGE_SIZE >= message_size:
            pack_size = message_size - ind
        else:
            pack_size = PACKAGE_SIZE
        data = message[ind:ind+pack_size]
        print(ind, "pack size", pack_size)
        try:
            sock.send(data.encode("utf-8"))
        except TimeoutError:
            print("Send: timeout")

        print("Data sent, waiting for reply...")
        try:
            print(sock.recv(PACKAGE_SIZE).decode("utf-8"))
        except TimeoutError:
            print("Recv: timeout")
        bar.update(len(data))
        ind += pack_size
        if ind >= message_size:
            break
    
    print(f"{message_size}, {ind}\n Транзакции успешно отправлены")

def receive_message(sock: socket.socket):
    """
    Получает сообщение по протоколу TCP.


            Параметры:
                    sock (socket.socket) : сокет связи 
            
                    
            Возвращаемое значение: список транзакций, подписанных хэшем SHA-256

    """
    global PACKAGE_SIZE
    len_packages = []
    message = bytearray()
    msg_size = int.from_bytes(sock.recv(4), 'little')
    sock.send(f"Получен размер файла, {msg_size} байт".encode("utf-8"))
    bar = tqdm(range(msg_size), f"Отправка транзакций {msg_size} байт")
    while True:
        data = sock.recv(PACKAGE_SIZE)
        #print(len(data))
        if not data:
            break
        len_packages.append(len(data))
        message.extend(data)
        sock.send("Получено сообщение".encode("utf-8"))
        bar.update(len(data))
    
    #print(f"\n{sys.getsizeof(message)} байт\n")
    #print(len_packages)
    return json.loads(message.decode("utf-8"))