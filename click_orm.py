import os
from configparser import ConfigParser

from sqlalchemy import Column, String, INTEGER, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


cp = ConfigParser()
cp.read(os.path.abspath('settings.conf'))
username = cp.get("database", "username")
password = cp.get("database", "password")
port = cp.get("database", "port")
db_name = cp.get("database", "db_name")


# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost:{port}/{db_name}")
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# 定义User对象:
class File(Base):
    # 表的名字:
    __tablename__ = 'files'

    # 表的结构:
    id = Column(INTEGER, primary_key=True)
    name = Column(String(100))
    filetype = Column(String(20))
    path = Column(String(100))
    en_text = Column(String(100))
    count = Column(INTEGER)

    def __repr__(self):
        return f"<File id: {self.id} name: {self.name} filetype: {self.filetype} path: {self.path} en_text: {self.en_text} count: {self.count}>"


# 装饰器，不需要每次创建session并提交，关闭了
def need_commit(func):
    def wrapper(*args):
        db_session = DBSession()
        ret = func(db_session, *args)
        db_session.commit()
        db_session.close()
        return ret
    return wrapper

def not_commit(func):
    def wrapper(*args):
        db_session = DBSession()
        ret = func(db_session, *args)
        db_session.close()
        return ret
    return wrapper


def init_db(): #初始化表
    Base.metadata.create_all(engine)

def drop_db():  #删除表
    Base.metadata.drop_all(engine)

@need_commit
def create(db_session, data):
    file1 = File(**data)
    db_session.add(file1)
    db_session.flush()
    row_num = file1.id
    return row_num

@need_commit
def update(db_session, condition, new_value):
    res = db_session.query(File).filter(condition).update(new_value)
    return res

@not_commit
def retrieve(db_session, condition):
    db_session = DBSession()
    return db_session.query(File).filter(condition)

@need_commit
def delete(db_session, condition):
    res = db_session.query(File).filter(condition).delete()
    return res


if __name__ == '__main__':

    drop_db()
    init_db()

    # data = {
    #     "name": "haaha",
    #     "filetype": "txt",
    #     "path": "~/Desktop",
    #     "en_text": "dsjaioemJIO@",
    #     "count": 3
    # }
    # print(create(data))
    

    # results = retrieve(File.id > 0).first()
    # print(results)

    # print(update(File.id == 6, {"count": File.count - 1}))

    # results = retrieve(File.id == 6).one_or_none()
    # print(results)


    # print(delete(File.id < 6))

    # results = retrieve(File.id > 0).all()
    # for result in results:
    #     print(result)












































