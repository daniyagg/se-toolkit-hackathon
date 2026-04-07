from pydantic import BaseModel


class WaterResponse(BaseModel):
    cups: int
    goal: int = 8


class DrinkResponse(BaseModel):
    cups: int
    goal: int = 8
    date: str
