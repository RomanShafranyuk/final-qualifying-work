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
add_time = 0

def handle_client(sock:socket.socket):
    global transactuin_queue, transactuin_queue_lock, add_time, COUNT_TRANSACTION
    while True:
        command = network.receive_command(sock)
        if command == "SERV":
            transactions = network.receive_message(sock)
            transactuin_queue_lock.acquire()
            for i in range(len(transactions)):
                if hashlib.sha256(transactions[i][0].encode("utf-8")).hexdigest() == transactions[i][1]:
                    time_to_add = time.time()
                    transactuin_queue.push({"data": transactions[i][0], "order": i, "add_time": time_to_add})
            transactuin_queue_lock.release()
        elif command == "STAT":
            count = int.from_bytes(sock.recv(4), 'little')
            stat = json.dumps(statistic.get_average_time(count))
            sock.send(stat.encode("utf-8"))
        elif command == "DRAW":
            count_elements = database.get_count_block()
            data = database.get_block_data(count_elements)
            network.send_message(sock, data)
        elif command == "EXIT":
            break
    sock.close()


def mining():
    global transactuin_queue, transactuin_queue_lock
    statistic_element = {} 
    while True:
        transactuin_queue_lock.acquire()
        
        if transactuin_queue.len_queue() !=0:
            print(transactuin_queue.len_queue())
            this_transaction = transactuin_queue.pop()
            # print(this_transaction)
            pop_time = time.time()
            queue_time = pop_time - this_transaction["add_time"]
            statistic_element["queue_time"] = queue_time
            statistic_element["order"] = this_transaction["order"]

            start_create_block = time.time()
            block.write_block(this_transaction["data"])
            # print("Блок добавлен")
            end_create_block = time.time()
            create_time = end_create_block - start_create_block
            statistic_element["create_time"] = create_time
            statistic_element["total_time"] = create_time + queue_time
            database.add_statistic(this_transaction["data"], statistic_element)
        transactuin_queue_lock.release()




#session = database.create_session()
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

