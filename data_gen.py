import random
import string
import secrets

def get_random_string(length: int)-> list:
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(length)) 
def generate_block_data(count_blocks: int, data_size: int) -> list:
    result = []
    for _ in range(count_blocks):
        result.append(get_random_string(data_size))
    return result