import socket
import database
from MyQueue import MyQueue
import block
import threading
import time
import hashlib
import network
import statistic
import json
transactuin_queue = MyQueue()

transactuin_queue_lock = threading.Lock()

def handle_client(client_socket:socket.socket):
    """
    Функция обработчик клиентского подключения. В зависисомсти от запроса клиента обращается ктому или иному сервису.


            Параметры:
                    client_socket (socket.socket) : сокет для связи с подключенным клиентом
            

    """
    global transactuin_queue, transactuin_queue_lock
    while True:
        command = network.receive_command(client_socket)
        if command == "SERV":
            transactions = network.receive_message(client_socket)
            transactuin_queue_lock.acquire()
            for i in range(len(transactions)):
                if hashlib.sha256(transactions[i][0].encode("utf-8")).hexdigest() == transactions[i][1]:
                    time_to_add = time.time()
                    transactuin_queue.push({"data": transactions[i][0], "order": i, "add_time": time_to_add})
            transactuin_queue_lock.release()
        elif command == "STAT":
            count = int.from_bytes(client_socket.recv(4), 'little')
            stat = json.dumps(statistic.get_average_queue_time(count))
            client_socket.send(stat.encode("utf-8"))
        elif command == "DRAW":
            count_elements = database.get_count_block()
            data = database.get_block_data(count_elements)
            network.send_message(client_socket, data)
        elif command == "EXIT":
            break
    client_socket.close()


def mining():
    """
    Функция отправляет транзакции из очереди на сервис формирования блоков
    """
    global transactuin_queue, transactuin_queue_lock
    statistic_element = {} 
    while True:
        transactuin_queue_lock.acquire()
        
        if transactuin_queue.len_queue() !=0:
            this_transaction = transactuin_queue.pop()
            pop_time = time.time()
            queue_time = pop_time - this_transaction["add_time"]
            statistic_element["queue_time"] = queue_time
            statistic_element["order"] = this_transaction["order"]
            start_create_block = time.time()
            block.write_block(this_transaction["data"])
            end_create_block = time.time()
            create_time = end_create_block - start_create_block
            statistic_element["create_time"] = create_time
            statistic_element["total_time"] = create_time + queue_time
            database.add_statistic(this_transaction["data"], statistic_element)
        transactuin_queue_lock.release()


database.init_db()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('25.18.233.38', 7001))
server_socket.listen(10)
print("Сервер запущен и ожидает подключений...")
 


try:
    thread1 = threading.Thread(target=mining)
    thread1.start()
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Подключение установлено с {client_address}")
            tmp_thread = threading.Thread(target=handle_client, args=[client_socket])
            tmp_thread.start()
        except Exception:
            pass
except:
    pass
 

server_socket.close()

