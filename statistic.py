import database
import client

def get_average_time(count_blocks):
    avg_block_time = database.get_average_block_time(count_blocks)
    avg_queue_time = database.get_queue_time() / count_blocks
    work_time = database.get_total_time()
    print(f"{avg_block_time} + {avg_queue_time}")
    total_time = avg_block_time + avg_queue_time
    with open('statstic.txt', "a") as f:
        f.write(f"{count_blocks}:{total_time}:{avg_block_time}:{work_time} \n")

get_average_time(client.TRANSACTION_COUNT)
