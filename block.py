import json
import hashlib
import database
import datetime


def get_hash(block_data: dict) -> str:
    """
    Формирует связывающий хэш.


            Параметры:
                    block_data (dict) : данные предыдущего блока
            
                    
            Возвращаемое значение: строка хэщ-код предыдущего блока

    """
    return hashlib.sha256(json.dumps(block_data).encode("utf-8")).hexdigest()


def calculate_Merklie_root(hashes_list: list) -> str:
    """
    Рассчитывается корень дерева Меркла текущей цепи блокчейна.


            Параметры:
                    hashes_list (list) : список хэшей текущей блокчейн-цепи
            
                    
            Возвращаемое значение: строка хэщ-код корня Меркла

    """
    while len(hashes_list) > 1:
        tmp = []
        if len(hashes_list) % 2 != 0:
            hashes_list.append(hashes_list[len(hashes_list) - 1])
        for i in range(0, len(hashes_list) - 1, 2):
            tmp.append(hashlib.sha256(
                hashes_list[i].encode("utf-8") + hashes_list[i + 1].encode("utf-8")).hexdigest())
        hashes_list.clear()
        hashes_list += tmp

    return hashes_list[0]


def write_block(data: str):
    """
    Формирует новый блок и добавляет его в существующую блокчейн-цепь в базу данных.


            Параметры:
                    session (sqlalchemy.orm.scoping.scoped_session) : курсор для запроса к базе данных
                    data (str) : текущая транзакция
            

    """
    prev_hash = ''
    prev_index = 0

    if database.is_database_empty() == False:
        data_prev_block, prev_index = database.get_last_block()
        prev_hash = get_hash(data_prev_block)
    else:
        first_block = {"data": data, "block_hash": prev_hash}
        prev_hash = get_hash(first_block)
    hash_list = database.get_hashes_list()
    hash_list.append(prev_hash)
    root = calculate_Merklie_root(hash_list)
    timestrap = datetime.datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')

    new_block = {"data": data,
                 "block_hash": prev_hash,
                 "Merklies_root": root,
                 "timestrap": timestrap,
                 "prev_index": prev_index}

    database.add_block(new_block)