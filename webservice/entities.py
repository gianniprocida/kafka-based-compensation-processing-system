from pydantic import BaseModel


class Employee(BaseModel):
  name: str
  transport: str
  distance: str
  office_days: str


class Compensation(BaseModel):
  bike: dict
  bus: dict 
  train: dict
  car: dict
