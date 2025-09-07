from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    name: str
    age: int


class Feedback(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    message: str =  Field(min_length=10, max_length=200)
    @field_validator('message')
    @classmethod
    def has_bad_words(cls, message: str):
        
        bad_words = [" редиск", " бяк", " козявк", " редисок", " козявок"]
        message2 = ' ' + message.lower()
        for word in bad_words:
            if word in message2:
                raise ValueError("Использование недопустимых слов")
        return message