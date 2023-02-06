# backend-fastapi-assignment

Suppose that you have a hotel and you want to create an API for your customer to make a reservation.  

***Assumption***
 - Your restaurant has a total of 10 rooms.
 - All customers can make reservations regardless that day has passed.

## API Description

### 1. `GET` Get the reservation by name
Use `get` method to retrieve the details of the reservation by name of booker.

### 2. `GET` Get the all the reservation in one room.
Use `get` method to retrieve all the reservation in that room.

### 3. `POST` Make a reservation.
Use `post` method to make a reservation.

### 4. `Put` Update the reservation
Use `put` method to update the specific reservation.

### 5. `Delete` Cancel the reservation
Use `delete` method to cancel the specific reservation.

Conditions:
 - Error handling (e.g., the start date must come before the end date)
 - date format must be ("YYYY-MM-DD")
 - "2017-07-3 != 2017-07-03"
 - The booking time must not overlap with other people's bookings. (including updated reservations)
 - room_id must be in the range 1 to 10
 - raise HTTPException 400, when the result was unsuccessful

## Test procedure
1. Set variable in test/fastapi_test.py
2. run `uvicorn main:app --reload`
3. run `python test/fastapi_test.py`
