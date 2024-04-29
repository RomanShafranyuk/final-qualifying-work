from sqlalchemy import create_engine, DateTime, delete
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.functions import sum as sum_string
from sqlalchemy.sql.expression import desc

engine = create_engine(
    'postgresql+psycopg2://postgres:12345678@25.18.233.38:5432/postgres')


def create_session():
    """
    Создает курсор для запросов в базу данных.


            Возвращаемое значение: курсор для запросов к базе данных
            

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
    Возвращает список всех хэшей блокчейна, связывающих блоки


            Возвращаемое значение: список хэшей
    """
    session = create_session()
    all_hashes_response = session.query(Block.block_hash).all()
    session.commit()
    for i in range(len(all_hashes_response)):
        all_hashes_response[i] = all_hashes_response[i][0]
    return all_hashes_response


def add_block(new_block):
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
    


def get_last_block():
    session = create_session()
    response = session.query(Block.data, Block.block_hash,
                                Block.number_id).select_from(Block).order_by(desc(Block.number_id)).limit(1).all()
    session.close()
    return {"data": response[0][0], "block_hash": response[0][1]}, response[0][2]


def get_queue_time():
    session = create_session()
    response = session.query(Statistic.queue_time).select_from(Statistic).order_by(desc(Statistic.n_id)).limit(1).all()
    session.close()
    return response[0][0]

def get_total_time():
    session = create_session()
    response = session.query(Statistic.total_time).select_from(Statistic).order_by(desc(Statistic.n_id)).limit(1).all()
    session.close()
    return response[0][0]

def get_average_block_time(count_blocks):
    session = create_session()
    last_id = session.query(Statistic.n_id).select_from(Statistic).order_by(desc(Statistic.n_id)).limit(1).all()[0][0]
    sum = session.query(sum_string(Statistic.block_time)).where(Statistic.n_id >= last_id - count_blocks + 1).all()[0][0]
    session.close()
    return sum / count_blocks


def is_database_empty():
    session = create_session()
    logic_result = session.query(count(Block.number_id)).all()[0][0] == 0
    session.close()
    return logic_result


def get_block_id(data):
    session = create_session()
    block_id = session.query(Block.number_id).where(Block.data == data).all()[0][0]
    session.close()
    return block_id


def add_statistic(data, stat_element):
    db_session = create_session()
    n_id = get_block_id(data)
    s = Statistic(n_id, stat_element["create_time"], stat_element["queue_time"], stat_element["total_time"], stat_element["order"])
    db_session.add(s)
    db_session.commit()
    db_session.close()


def get_block_data(count_blocls):
    session = create_session()
    data = session.query(Block.number_id, Block.prev_index).where(Block.number_id <= count_blocls).all()
    session.close()
    return data
    

class Block(Base):
    __tablename__ = 'blocks'
    number_id = Column(Integer, primary_key=True)
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


# session = create_session()
# print(type(session))
# init_db(session)
# clear_tables(session)
