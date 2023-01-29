from datetime import datetime
import enum

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey,
                        DateTime, Enum, Time, Float, Boolean, Text)
import psycopg2

from utils import get_environment_variable

POSTGRES_USER = get_environment_variable('POSTGRES_USER')
POSTGRES_PASSWORD = get_environment_variable('POSTGRES_PASSWORD')
POSTGRES_HOST = get_environment_variable('POSTGRES_HOST')
POSTGRES_DB = get_environment_variable('POSTGRES_DB')


engine = create_engine(f'postgresql+psycopg2://{POSTGRES_USER}:'
                       f'{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}')

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    habits = relationship('Habit')

    def __repr__(self):
        return f'User(id={self.id})'


class HabitRepeatType(enum.Enum):
    DAILY = 'Daily'
    EVERY_OTHER_DAY = 'Every other day'
    WEEKDAYS = 'Weekdays'
    WEEKEND = 'Weekend'
    WEEKLY = 'Weekly'
    BIWEEKLY = 'Biweekly'
    MONTHLY = 'Monthly'


class Habit(Base):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    repeat_type = Column(Enum(HabitRepeatType))
    repeat_time = Column(Time)
    user = Column(Integer, ForeignKey('users.id'))
    habit_parameters = relationship('HabitParameter')
    habit_records = relationship('HabitRecord')
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (f'Habit(id={self.id}, name={self.name},'
                f' repeat_type={self.repeat_type},'
                f' repeat_time={self.repeat_time}, user={self.user})')


class HabitParameter(Base):
    __tablename__ = 'habit_parameters'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    habit = Column(Integer, ForeignKey('habits.id'))

    def __repr__(self):
        return (f'HabitParameter(id={self.id}, name={self.name},'
                f' habit={self.habit})')


class HabitRecord(Base):
    __tablename__ = 'habit_records'
    id = Column(Integer, primary_key=True)
    habit = Column(Integer, ForeignKey('habits.id'))
    result = Column(Boolean)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (f'HabitRecord(id={self.id}, result={self.result},'
                f' habit={self.habit}, comment={self.comment})')


class HabitParameterRecord(Base):
    __tablename__ = 'habit_parameter_records'
    id = Column(Integer, primary_key=True)
    habit_parameter = Column(Integer, ForeignKey('habit_parameters.id'))
    value = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (f'HabitRecord(id={self.id}, value={self.value},'
                f' habit_parameter={self.habit_parameter})')


if __name__ == '__main__':
    ans = input('Recreate tables? All data will be lost. (y/n) ')
    if ans == 'y':
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
