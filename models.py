from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    task = Column(String(255))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(Integer, unique=True)
    username = Column(String, unique=True)
    admin_user = Column(Boolean, default=False)
    password = Column(String)



class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    book_name = Column(String)
    author = Column(String)
    prize = Column(Integer)
    description = Column(String)



class UserBook(Base):
    __tablename__ = 'userbooks'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="userbooks")
    returned = Column(Boolean, default=False)
    borrowed_date = Column(Date)
    user = Column(String)

Book.userbooks = relationship("UserBook", order_by=UserBook.id, back_populates="book")