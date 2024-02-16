import json
import hashlib
import database
import datetime
import time

def get_hash(block_data):
    return hashlib.sha256(json.dumps(block_data).encode("utf-8")).hexdigest()


def calculate_Merkle_root(hashes_list: list):
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




def get_hash_db(session):
    data_prev_block = database.get_last_block(session)
    data_to_json = json.dumps(
        {'data': data_prev_block[0], 'hash': data_prev_block[1]})
    return hashlib.sha256(data_to_json.encode("utf-8")).hexdigest(), data_prev_block[2]


def write_block(session, data, prev_hash=''):
    prev_hash = ''
    prev_index = 0

    if database.is_database_empty(session) == False:
        data_prev_block, prev_index = database.get_last_block(session)
        prev_hash = get_hash(data_prev_block)
    else:
        first_block = {"data": data, "block_hash": prev_hash}
        prev_hash = get_hash(first_block)
    hash_list = database.get_hashes_list()
    hash_list.append(prev_hash)
    root = calculate_Merkle_root(hash_list)
    timestrap = datetime.datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')

    new_block = {"data": data,
                 "block_hash": prev_hash,
                 "Merklies_root": root,
                 "timestrap": timestrap,
                 "prev_index": prev_index}

    database.add_block(session, new_block)
    # end = time.time()
    # time_to_add = end - start
    # database.add_time(name, time_to_add)


def get_average_time(count_blocks: int):
    _, time_avg = database.get_average_time(count_blocks)

    with open('time.txt', "a") as f:
        f.write(str(count_blocks) + ":" + str(time_avg)+'\n')
