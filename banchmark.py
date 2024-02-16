from client import *
from multiprocessing import Pool
import data_gen

if __name__ == "__main__":
        transaction_list = data_gen.generate_block_data(10, 100)
        with Pool(4) as p:
            p.map(send_transaction, transaction_list)