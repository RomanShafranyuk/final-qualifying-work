class Queue:
    def __init__(self):
        self.queue = []


    def push(self, item):
        self.queue.append(item)

    def add_blocks(self, blocks):
        self.queue += blocks

    def pop(self):
        if len(self.queue) == 0:
            return None
        removed = self.queue.pop(0)
        return removed
    

    def print_queue(self):
        print(self.queue)

    def len_queue(self):
        return len(self.queue)