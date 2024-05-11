class MyQueue:
    def __init__(self):
        self.queue = []


    def push(self, item):
        """
        Добавляет новый элемент в очередь


            Параметры:
                       self (__main__.MyQueue) : объект класса.
                       item (любой тип) : данные единицы списка.
                

        """
        self.queue.append(item)



    def pop(self):
        """
        Удаляет первый элемент очереди и возвращает его.


                Параметры:
                        self (__main__.MyQueue) : объект класса.
                
                        
                Возвращаемое значение: первый элемент очереди

        """
        if len(self.queue) == 0:
            return None
        removed = self.queue.pop(0)
        return removed
    

    def len_queue(self):
        """
        Удаляет первый элемент очереди и возвращает его.


                Параметры:
                        self (__main__.MyQueue) : объект класса.
                
                        
                Возвращаемое значение: первый элемент очереди

        """
        return len(self.queue)
    

