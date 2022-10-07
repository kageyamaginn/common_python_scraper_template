#from array import list
from datetime import date


class Agency:
    phone:str
    name:str

class Lease:
    available_date:date
    available_period:int

class Roomate:
    name:str
    work:str
    checkin_time:int

class Uptown:
    name:str
    position:list(float)
    decade:int
    builing_type:str
    heating_type:str
    realty_management_company:str

class Room:
    def __init__(self) -> None:
        pass
    link:str
    name:str
    pics:list(bytes)
    price:int
    tags:list(str)
    square:float
    direction: str
    room_type:str
    location:str
    floor:list(int)
    has_elevator:bool
    year_of_construction:int
    heating_type:str
    agency:Agency

