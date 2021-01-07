from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from KYTJ_crawl.settings import db_url


class Db:
    def __init__(self):
        engine = create_engine(db_url, 
            connect_args={'check_same_thread': False})
        self.conn = engine.connect()
        self.sess = Session(bind=self.conn)

        sql = """CREATE TABLE IF NOT EXISTS `university` (
                id INTEGER primary key AUTOINCREMENT,
                university_name varchar(32),
                uid varchar(32) unique,
                major varchar(64),
                neirong varchar(128),
                published_date date,
                url varchar(128)
            );"""

        self.conn.execute(sql)
        self.sess.commit()

    def save2db(self, items):
        if not items:
            return
        sql = """insert into university(`university_name`, `uid`, `major`,
        `neirong`, `published_date`, `url`) values('{university_name}','{uid}'
        ,'{major}','{neirong}','{published_date}', '{url}')"""
        for x in items:
            s = sql.format(**x)
            try:
                self.conn.execute(s)
                self.sess.commit()
            except IntegrityError as e:
                self.sess.rollback()
                print(e)

    def get_universities(self):
        sql = "select * from university"
        cursor = self.conn.execute(sql)
        universities = cursor.fetchall()
        return universities

    def get_universities_uids(self):
        sql = "select uid from university;"
        cursor = self.conn.execute(sql)
        university_uids = cursor.fetchall()
        return [x[0] for x in university_uids]


university_db = Db()
