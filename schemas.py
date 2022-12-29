from fastapi import Form, File, UploadFile
from pydantic import BaseModel, EmailStr
from typing import Union


class Item(BaseModel):
    task: str


class UserIn(BaseModel):
    name: str
    email: str
    password: str
    username: str
    phone: int

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            email: str = Form(...),
            phone: str = Form(...),
            username: str = Form(...),
            password: str = Form(...),
    ):
        return cls(
            name=name,
            email=email,
            phone=phone,
            username=username,
            password=password
        )


class UserOut(BaseModel):
    name: str
    email: str
    password: str
    username: str
    phone: int

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            email: str = Form(...),
            phone: str = Form(...),
            username: str = Form(...),
            password: str = Form(...),
    ):
        return cls(
            name=name,
            email=email,
            phone=phone,
            username=username,
            password=password
        )


class LoginForm(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(
            cls,
            username: str = Form(...),
            password: str = Form(...)
    ):
        return cls(
            username=username,
            password=password
        )



class BookForm(BaseModel):
    book_name: str
    author: str
    prize: int
    description : str


    @classmethod
    def as_form(
            cls,
            book_name: str = Form(...),
            author: str = Form(...),
            prize: int = Form(...),
            description: str = Form(...),

    ):
        return cls(
            book_name=book_name,
            author=author,
            prize=prize,
            description=description,

        )


class BookEdit(BaseModel):
    book_name: str
    author: str
    prize: int
    description : str