import database
import client

def get_average_time(count_blocks):
    session = database.create_session()
    avg_block_time = database.get_average_block_time(count_blocks, session)
    avg_queue_time = database.get_queue_time(session)
    total_time = avg_block_time + avg_queue_time
    with open('statstic.txt', "a") as f:
        f.write(str(count_blocks) + ":" + str(total_time)+'\n')

get_average_time(client.TRANSACTION_COUNT)
