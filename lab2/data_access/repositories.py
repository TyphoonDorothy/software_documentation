import csv
from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from .models import Base


class IRepository(ABC):
    @abstractmethod
    def read_csv(self, file_path: str) -> list:
        pass

    @abstractmethod
    def save_entities(self, objects: list):
        pass

class SqlAlchemyRepository(IRepository):
    def __init__(self, db_url=""):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def read_csv(self, file_path: str):
        data = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def save_entities(self, objects: list):
        session = self.Session()
        try:
            session.add_all(objects)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()