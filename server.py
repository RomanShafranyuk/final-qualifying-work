import socket
import database
from MyQueue import Queue
import block
import threading
import time
import hashlib
import json

transactuin_queue = Queue()

transactuin_queue_lock = threading.Lock()
add_time = 0


def handle_client(sock):
    global transactuin_queue, transactuin_queue_lock, add_time
    data_from = sock.recv(100000000)
    transactions: list = json.loads(data_from.decode("utf-8"))
    for i in range(len(transactions)):
        if hashlib.sha256(transactions[i][0].encode("utf-8")).hexdigest() == transactions[i][1]:
            time_to_add = time.time()
            transactuin_queue_lock.acquire()
            transactuin_queue.push({"data": transactions[i][0], "order": i, "add_time": time_to_add})
            transactuin_queue_lock.release()

        
    sock.close()

def mining():
    global transactuin_queue, transactuin_queue_lock, start_time, start_time_lock,end_time, end_time_lock
    statistic_element = {} 
    while True:
        transactuin_queue_lock.acquire()

        if transactuin_queue.len_queue() !=0:
           
            this_transaction = transactuin_queue.pop()
            print(this_transaction)
            pop_time = time.time()
            queue_time = pop_time - this_transaction["add_time"]
            statistic_element["queue_time"] = queue_time
            statistic_element["order"] = this_transaction["order"]

            start_create_block = time.time()
            block.write_block(session, this_transaction["data"])
            print("Блок добавлен")
            end_create_block = time.time()
            create_time = end_create_block - start_create_block
            statistic_element["create_time"] = create_time
            statistic_element["total_time"] = create_time + queue_time
            database.add_statistic(this_transaction["data"], statistic_element)
        transactuin_queue_lock.release()




session = database.create_session()
database.init_db(session)

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
 
# Получаем данные от клиента

# Закрываем соединения
server_socket.close()

