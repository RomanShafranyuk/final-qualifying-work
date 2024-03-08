import socket
from tqdm import tqdm 

SIZE = 512

def send_message(msg: str, sock: socket.socket, size:int):
    global SIZE
    sock.send(str(size).encode("utf-8"))
    print(sock.recv(SIZE).decode("utf-8"))
    bar = tqdm(range(size), f"Отправка транзакций {size} байт", unit="B", unit_scale=True, unit_divisor=SIZE)
    start_msg = 0
    end_msg = SIZE

    while True:
        data = msg[start_msg:end_msg]
        if not data:
            break
        sock.send(data.encode("utf-8"))
        sock.recv(SIZE).decode("utf-8")
        bar.update(len(data))
        start_msg += SIZE
        end_msg += SIZE
    print("Транзакции успешно отправлены")

def receive_message(sock: socket.socket):
    global SIZE
    message = ""
    msg_size = int(sock.recv(4).decode("utf-8"))
    sock.send(f"Получен размер файла, {msg_size} байт")
    bar = tqdm(range(msg_size), f"Отправка транзакций {msg_size} байт", unit="B", unit_scale=True, unit_divisor=SIZE)
    while len(message) != msg_size:
        data = sock.recv(SIZE).decode("utf-8")

        if not data:
            break
        message += data
        sock.send("Получено сообщение".encode("utf-8"))
        bar.update(len(data))
    return message


    
