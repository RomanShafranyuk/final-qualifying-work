import database

def get_average_queue_time(count_blocks: int) -> dict:
    """
    Рассчитывает время пребывания заявки в очереди.


            Параметры:
                    count_blocks (int) : количество транзакций.
            
                    
            Возвращаемое значение: строка со статистическими данными

    """
    avg_block_time = database.get_average_block_time(count_blocks)
    avg_queue_time = database.get_queue_time() / count_blocks
    work_time = database.get_total_time()
    total_time = avg_block_time + avg_queue_time
    return {"N": count_blocks, "Tоч": total_time, "tобсл_ср": avg_block_time, "t": work_time}


