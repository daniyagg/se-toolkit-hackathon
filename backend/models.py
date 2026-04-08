from pydantic import BaseModel
from typing import List, Optional


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    user_id: str
    message: str


class WaterResponse(BaseModel):
    cups: int
    goal: int = 8


class DrinkResponse(BaseModel):
    cups: int
    goal: int = 8
    date: str


class HistoryEntry(BaseModel):
    date: str
    cups: int


class HistoryResponse(BaseModel):
    goal: int = 8
    history: List[HistoryEntry]
