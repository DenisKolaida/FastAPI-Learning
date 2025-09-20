# models.py
from pydantic import BaseModel, Field, field_validator, EmailStr, PositiveInt
from pydantic_extra_types.phone_numbers import PhoneNumber


class Contact(BaseModel):
    email: EmailStr
    phone: PhoneNumber = None


class Feedback(BaseModel):

    name: str = Field(min_length=2, max_length=50)
    message: str =  Field(min_length=10, max_length=500)
    contact: Contact


    @field_validator('message')
    @classmethod
    def has_bad_words(cls, message: str):
        
        bad_words = [" редиск", " бяк", " козявк", " редисок", " козявок"]
        message2 = ' ' + message.lower()
        for word in bad_words:
            if word in message2:
                raise ValueError("Использование недопустимых слов")
        return message
    

class UserData(BaseModel):
    username: str
    password: str