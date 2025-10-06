# models.py
from pydantic import BaseModel, Field, field_validator, EmailStr


class Contact(BaseModel):
    email: EmailStr
    phone: str | None = None


class Feedback(BaseModel): # I left it just as example

    name: str = Field(min_length=2, max_length=50)
    message: str =  Field(min_length=10, max_length=500)
    contact: Contact


    @field_validator('message')
    def has_bad_words(cls, message: str):
        
        bad_words = [" редиск", " бяк", " козявк", " редисок", " козявок"]
        message2 = ' ' + message.lower()
        for word in bad_words:
            if word in message2:
                raise ValueError("Использование недопустимых слов")
        return message
    

class User(BaseModel):
    username: str
    password: str