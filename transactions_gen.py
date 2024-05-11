import random
import string
import secrets

def get_random_string(length: int)-> str:
    """
    Генерирует случайную строку длиной length бит.


            Параметры:
                    length (int) : длина сгенерированной строки 
            
                    
            Возвращаемое значение: строка в виде случайного набора символов

    """
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(length)) 


def generate_transactuins_list(count_transactions: int, transactions_size: int) -> list:
    """
    Генерирует список транзакций.


            Параметры:
                    count_transactions (int) : количество транзакций
                    transactions_size (int) : размер транзакции 
            
                    
            Возвращаемое значение: список транзакций длиной count_transactions

    """
    transactions_list = []
    for _ in range(count_transactions):
        transactions_list.append(get_random_string(transactions_size))
    return transactions_list