from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///ORM_base.sqlite')
Base = declarative_base(bind=engine)
Session = sessionmaker()

class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    vacancy = Column(String(50), index=True)
    count = Column(Float, default=0)
    up = Column(Float, default=0)
    down = Column(Float, default=0)
    area_id = Column(Integer, ForeignKey('area.id'))

class Skills(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)

class VacancySkill(Base):
    __tablename__ = 'Vacancy_skills'
    id = Column(Integer, primary_key=True)
    id_vacancy = Column(Integer, ForeignKey('vacancy.id'))
    id_skill = Column(Integer, ForeignKey('skills.id'))
    count = Column(Float, default=0)
    percent = Column(Float, default=0)

    def __str__(self):
        return f'{self.id}) {self.id_vacancy} | {self.id_skill} | {self.count} | {self.percent} |'

class Area(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, index=True)

    def __str__(self):
        return f'{self.id}) {self.name} |'

    def __repr__(self):
        return f'{self.id} - {self.name} '


Base.metadata.create_all()
