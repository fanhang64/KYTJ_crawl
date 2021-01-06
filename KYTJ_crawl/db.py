from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, MetaData

from KYTJ_crawl.settings import db_url


class Db:
    def __init__(self):
        engine = create_engine(db_url)
        self.conn = engine.connect()
        

    def save2db(self):
        pass

    def execute_sql(self):
        pass

    def get_universities(self):
        pass
