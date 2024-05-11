from sqlalchemy import create_engine, DateTime, delete
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.functions import sum as sum_string
from sqlalchemy.sql.expression import desc

engine = create_engine(
    'postgresql+psycopg2://postgres:12345678@25.18.233.38:5432/postgres')


def create_session()->scoped_session:
    """
    Создает курсор для запросов в базу данных.


            Возвращаемое значение: курсор для запросов к базе данных.
            

    """
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine))


Base = declarative_base()


def init_db():
    """
    Создает новое соединение. В случае, если таблицы не были созданы, создает их.         
    """
    session = create_session()
    Base.query = session.query_property()
    Base.metadata.create_all(bind=engine)
    session.commit()


def get_hashes_list() -> list:
    """
    Возвращает список всех хэшей блокчейна, связывающих блоки.


            Возвращаемое значение: список хэшей.
    """
    session = create_session()
    all_hashes_response = session.query(Block.block_hash).all()
    session.commit()
    for i in range(len(all_hashes_response)):
        all_hashes_response[i] = all_hashes_response[i][0]
    return all_hashes_response


def add_block(new_block:dict):
    """
    Добавляет сформированный блок в базу данных.


            Параметры:
                    new_block (dict) : данные нового блока.
            

    """
    session = create_session()
    b = Block(new_block['data'], new_block['block_hash'],
              new_block['Merklies_root'], new_block['timestrap'],
              new_block['prev_index'])
    
    check_list = []

    while len(check_list) == 0:
        session.add(b)
        session.commit()
        check_list += session.query(Block.number_id).select_from(Block).where(
            Block.data == new_block['data']).where(Block.block_hash == new_block['block_hash']).all()   


def get_last_block()->dict:
    """
    Возвращает данные последнего блока.


            Возвращаемое значение: словарь с данными последнего блока.
    """
    session = create_session()
    response = session.query(Block.data, Block.block_hash,
                                Block.number_id).select_from(Block).order_by(desc(Block.number_id)).limit(1).all()
    session.commit()
    return {"data": response[0][0], "block_hash": response[0][1]}, response[0][2]


def get_queue_time()->float:
    """
    Возвращает время разблра очереди.


            Возвращаемое значение: время разбора очереди.
    """
    session = create_session()
    response = session.query(Statistic.queue_time).select_from(Statistic).order_by(desc(Statistic.n_id)).limit(1).all()
    session.commit()
    return response[0][0]


def get_total_time()->float:
    """
    Возвращает время работы системы.


            Возвращаемое значение: время работы системы.
    """
    session = create_session()
    response = session.query(Statistic.total_time).select_from(Statistic).order_by(desc(Statistic.n_id)).limit(1).all()
    session.commit()
    return response[0][0]


def get_average_block_time(count_blocks:int)-> float:
    """
    Возвращает среднее время пребывания заявки в очереди.


            Параметры:
                    count_blocks (int) : количество блоков, по которому рассчитывается время.
            
                    
            Возвращаемое значение: среднее время пребывания заявки в очереди.

    """
    session = create_session()
    last_id = session.query(Statistic.n_id).select_from(Statistic).order_by(desc(Statistic.n_id)).limit(1).all()[0][0]
    sum = session.query(sum_string(Statistic.block_time)).where(Statistic.n_id >= last_id - count_blocks + 1).all()[0][0]
    session.commit()
    return sum / count_blocks


def is_database_empty()->bool:
    """
    Возвращает информацию о том, пустая ли в данный момент база данных.


            Возвращаемое значение: логическое значение пустоты базы данных.
    """
    session = create_session()
    logic_result = session.query(count(Block.number_id)).all()[0][0] == 0
    session.commit()
    return logic_result


def get_block_id(data:str)->int:
    """
    Возвращает номер блока с транзакцией data.


            Параметры:
                    data (str) : данные блока.
            
                    
            Возвращаемое значение: номер блока.

    """
    session = create_session()
    block_id = session.query(Block.number_id).where(Block.data == data).all()[0][0]
    session.commit()
    return block_id



def add_statistic(data:str, stat_element:dict):
    """
    Добавляет статистику в базу данных.


            Параметры:
                    data (str) : данные блока;
                    stat_element (dict): статистика.
            

    """
    db_session = create_session()
    n_id = get_block_id(data)
    s = Statistic(n_id, stat_element["create_time"], stat_element["queue_time"], stat_element["total_time"], stat_element["order"])
    db_session.add(s)
    db_session.commit()


def get_block_data(count_blocks:int)->list:
    """
    Возвращает информацию о блокчейн-цепи.


            Параметры:
                    count_blocks (int) : количество блоков.
            
                    
            Возвращаемое значение: список блоков и их связей.

    """
    session = create_session()
    data = session.query(Block.number_id, Block.prev_index).where(Block.number_id <= count_blocks).all()
    for i in range (len(data)):
        data[i] = tuple(data[i])
    session.commit()
    return list(data)


def get_count_block()->int:
    """
    Возвращает количество блоков.

                
            Возвращаемое значение: количество блоков.

    """
    session = create_session()
    count_elements = session.query(count(Block.number_id)).all()[0][0]
    session.commit()
    return count_elements
    

class Block(Base):
    __tablename__ = 'blocks'
    number_id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String(100000), nullable=True)
    block_hash = Column(String(100), nullable=True)
    Merklies_root = Column(String(100), nullable=True)
    timestrap = Column(String(100), nullable=True)
    prev_index = Column(Integer)

    def __init__(self, data, hash_, root, timestamp, prev_index):
        self.data = data
        self.block_hash = hash_
        self.Merklies_root = root
        self.timestrap = timestamp
        self.prev_index = prev_index


class Statistic(Base):
    __tablename__ = 'statistic'
    n_id = Column(Integer, primary_key=True)
    block_time = Column(Float)
    queue_time = Column(Float)
    total_time = Column(Float)
    order = Column(Integer)

    def __init__(self, n_id, b_time, q_time, t_time, order):
        self.n_id = n_id
        self.block_time = b_time
        self.queue_time = q_time
        self.total_time = t_time
        self.order = order



