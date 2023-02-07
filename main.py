from fastapi import FastAPI, HTTPException, Body
from datetime import date
from pymongo import MongoClient
from pydantic import BaseModel

DATABASE_NAME = "exceed11"
COLLECTION_NAME = "reservation_min"
MONGO_DB_URL = "mongodb://exceed11:sRS47gYL@mongo.exceed19.online"
MONGO_DB_PORT = 8443


class Reservation(BaseModel):
    name : str
    start_date: date
    end_date: date
    room_id: int


client = MongoClient(f"{MONGO_DB_URL}:{MONGO_DB_PORT}")

db = client[DATABASE_NAME]

collection = db[COLLECTION_NAME]

app = FastAPI()

def find_reservation(reservation: Reservation):
    return collection.find_one({
        "name": reservation.name,
        "start_date": str(reservation.start_date).replace(":", "-"),
        "end_date": str(reservation.end_date).replace(":", "-"),
        "room_id": reservation.room_id
    })
    
def insert_reservation(reservation: Reservation):
    return collection.insert_one({
        "name": reservation.name,
        "start_date": str(reservation.start_date).replace(":", "-"),
        "end_date": str(reservation.end_date).replace(":", "-"),
        "room_id": reservation.room_id
    })

def delete_reservation(reservation: Reservation):
    return collection.delete_one({
        "name": reservation.name,
        "start_date": str(reservation.start_date).replace(":", "-"),
        "end_date": str(reservation.end_date).replace(":", "-"),
        "room_id": reservation.room_id
    })

def room_avaliable(room_id: int, start_date: date, end_date: date):
    start_date = str(start_date).replace(":", "-")
    end_date = str(end_date).replace(":", "-")
    query={"room_id": room_id,
           "$or": 
                [{"$and": [{"start_date": {"$lte": start_date}}, {"end_date": {"$gte": start_date}}]},
                 {"$and": [{"start_date": {"$lte": end_date}}, {"end_date": {"$gte": end_date}}]},
                 {"$and": [{"start_date": {"$gte": start_date}}, {"end_date": {"$lte": end_date}}]}]
            }
    
    result = collection.find(query, {"_id": 0})
    list_cursor = list(result)

    return not len(list_cursor) > 0


@app.get("/reservation/by-name/{name}", status_code=200)
def get_reservation_by_name(name:str):
    res = collection.find_one({"name": name}, {"_id": 0})
    if res is None:
        res = []
    else:
        res["start_date"] = str(res["start_date"])
        res["end_date"] = str(res["end_date"])
        res = [res]
    return {"result": res}

@app.get("/reservation/by-room/{room_id}", status_code=200)
def get_reservation_by_room(room_id: int):
    if room_id not in range(1, 11):
        raise HTTPException(status_code=400, detail="Room id must be between 1 and 10")
    res = collection.find_one({"room_id": room_id}, {"_id": 0})
    if res is None:
        res = []
    else:
        res["start_date"] = str(res["start_date"])
        res["end_date"] = str(res["end_date"])
        res = [res]
    return {"result": res}

@app.post("/reservation", status_code=200)
def reserve(reservation : Reservation):
    
    if reservation.room_id not in range(1, 11):
        raise HTTPException(status_code=400, detail="Room id must be between 1 and 10")
    
    if reservation.start_date > reservation.end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    if not room_avaliable(reservation.room_id, reservation.start_date, reservation.end_date):
        raise HTTPException(status_code=400, detail="Room not avaliable")
    
    if find_reservation(reservation) is not None:
        raise HTTPException(status_code=400, detail="Reservation already exists")

    insert_reservation(reservation)
    
    return {"msg": "Reservation created"}

@app.put("/reservation/update", status_code=200)
def update_reservation(reservation: Reservation, new_start_date: date = Body(), new_end_date: date = Body()):
    
    if reservation.room_id not in range(1, 11):
        raise HTTPException(status_code=400, detail="Room id must be between 1 and 10") 
    
    if new_start_date > new_end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    if find_reservation(reservation) is None:
        raise HTTPException(status_code=400, detail="Reservation not found")
    
    # delete_reservation(reservation)
    
    if not room_avaliable(reservation.room_id, new_start_date, new_end_date):
        # insert_reservation(reservation)
        raise HTTPException(status_code=400, detail="Room not avaliable")
    
    collection.update_one(
        {
            "name": reservation.name,
            "start_date": str(reservation.start_date).replace(":", "-"),
            "end_date": str(reservation.end_date).replace(":", "-"),
            "room_id": reservation.room_id    
        },
        {
            "$set":{
                "start_date": str(new_start_date).replace(":", "-"),
                "end_date": str(new_end_date).replace(":", "-")
            }
        }
    )
    
    return {"msg": "Reservation updated"}
        

@app.delete("/reservation/delete", status_code=200)
def cancel_reservation(reservation: Reservation): 
    if reservation.room_id not in range(1, 11):
        raise HTTPException(status_code=400, detail="Room id must be between 1 and 10")
    
    if reservation.start_date > reservation.end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    if find_reservation(reservation) is None:
        raise HTTPException(status_code=400, detail="Reservation not found")
    
    delete_reservation(reservation)
    return {"msg": "Reservation  deleted"}