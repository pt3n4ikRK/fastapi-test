from pydantic import BaseModel, Field


class Person(BaseModel):
    user_name: str
    age: int = Field(description="Age of user", ge=0)