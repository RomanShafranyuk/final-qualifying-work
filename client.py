import socket
import hashlib
import transactions_gen
import network
import paint
import json

from consolemenu import prompt_utils, ConsoleMenu, SelectionMenu, Screen
from consolemenu.items import FunctionItem
socket.setdefaulttimeout(2)
SERVER_ADDRESS = ('25.18.233.38',7001)
TRANSACTION_SIZE = 1024

def send_transactions(server_socket:socket.socket):
    """
    Генерирует список транзакций и отправляет их на сервер.


            Параметры:
                    server_socket (socket.socket) : сокет для связи с сервером.
            

    """
    transactions_count = int(input("Введите количество транзакций\n>>> "))
    network.send_command(server_socket, "SERV")
    print("Начата генерация транзакций")
    transactions = transactions_gen.generate_transactuins_list(transactions_count, TRANSACTION_SIZE)
    for i in range(len(transactions)):
        signature = hashlib.sha256(transactions[i].encode("utf-8")).hexdigest()
        transactions[i] = (transactions[i], signature)
    print("Транзакции сформированы")
    notsend_prompt = prompt_utils.PromptUtils(Screen())
    network.send_message(server_socket, transactions)
    notsend_prompt.enter_to_continue()


def get_statistic(socket: socket.socket):
    """
    Запрашивает статистические данные у сервера и записывает их в файл формата txt.


            Параметры:
                    socket (socket.socket) : сокет для связи с сервером.
            

    """
    transactions_count = int(input("Введите количество транзакций\n>>> "))
    network.send_command(socket, "STAT")
    socket.send(transactions_count.to_bytes(4, 'little'))
    stat = socket.recv(1024).decode("utf-8")
    notsend_prompt = prompt_utils.PromptUtils(Screen())
    print("Получена статистика.")
    notsend_prompt.enter_to_continue()
    with open("statistic.txt", "a") as f:
        f.write(stat + '\n')


def print_blockchain(socket: socket.socket):
    """
    Запрашивает данные о блокчейн-цепи у сервера, выводит иллюстрацию блокчейн-цепи и сохраняет ее в картинку формата png.


            Параметры:
                    socket (socket.socket) : сокет для связи с сервером.
            

    """
    network.send_command(socket, "DRAW")
    data = network.receive_message(socket)
    paint.get_graph(data)


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    print("Клиент подключился к серверу ")
    menu = ConsoleMenu(f"CLIENT: {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}")
    item1 = FunctionItem("Отправить транзакции", send_transactions, [client_socket])
    item2 = FunctionItem("Посчитать статистику", get_statistic, [client_socket])
    item3 = FunctionItem("Вывести блокчейн", print_blockchain, [client_socket])
    menu.append_item(item1)
    menu.append_item(item2)
    menu.append_item(item3)
    menu.show()
    network.send_command(client_socket, "EXIT")
    client_socket.close()
