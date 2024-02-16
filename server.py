import socket
import database
from MyQueue import Queue
import block
import threading

transactuin_queue = Queue()
transactuin_queue_lock = threading.Lock()

def handle_client(sock):
    global transactuin_queue, transactuin_queue_lock
    data_from = sock.recv(100)
    data = data_from.decode("utf-8")
    #print(f"Получены данные: {data}")
    transactuin_queue_lock.acquire()
    transactuin_queue.push(data)
    transactuin_queue_lock.release()

def create_new_block():
    count_blocks = 0
    global transactuin_queue, transactuin_queue_lock 
    while True:
        transactuin_queue_lock.acquire()
        if transactuin_queue.len_queue() !=0:
            this_transaction = transactuin_queue.pop()
            block.write_block(session, this_transaction)
            count_blocks += 1
            print(count_blocks)
        transactuin_queue_lock.release()



session = database.create_session()
database.init_db(session)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(10)
print("Сервер запущен и ожидает подключений...")
 


try:
    thread1 = threading.Thread(target=create_new_block)
    thread1.start()
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            #print(f"Подключение установлено с {client_address}")
            tmp_thread = threading.Thread(target=handle_client, args=[client_socket])
            tmp_thread.start()
        except Exception:
            pass
except:
    pass
 
# Получаем данные от клиента

# Закрываем соединения
server_socket.close()

