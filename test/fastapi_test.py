from pymongo import MongoClient
import unittest
import requests

# TODO change IP and PORT to your fastapi deployment
# TODO set DATABASE_NAME, COLLECTION_NAME, MONGO_DB_URL, and MONGO_DB_PORT (same as main.py)

IP = "127.0.0.1"       # default: 127.0.0.1
PORT = "8000"          # default: 8000

DATABASE_NAME = "hotel"
COLLECTION_NAME = "reservation"
MONGO_DB_URL = f"mongodb://localhost"   # mongodb://localhost
MONGO_DB_PORT = 27017                   # 27017      

BASE_URL = f"http://{IP}:{PORT}"


# Mocking
mock_name = "JohnDoe"
mock_name1 = "John Doe"


def connect_mongodb():
    client = MongoClient(f"{MONGO_DB_URL}:{MONGO_DB_PORT}")
    global db; db = client[DATABASE_NAME]
    global collection; collection = db[COLLECTION_NAME]

    collection.delete_many({})

    print("MongoClient connected\n")


class TestApi(unittest.TestCase):
    def setUp(self):
        collection.delete_many({})

    def test_get_empty_by_name(self):
        res = requests.get(BASE_URL + f"/reservation/by-name/{mock_name}")
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {
            "result": []
        })

    def test_get_empty_by_room(self):
        res = requests.get(BASE_URL + f"/reservation/by-room/10")
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {
            "result": []
        })

    def test_get_by_name(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-09",
            "room_id": 9
        }

        myobj1 = {
            "name": mock_name1,
            "start_date": "2017-02-10",
            "end_date": "2017-02-15",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj1)))

        res = requests.get(BASE_URL + f"/reservation/by-name/{mock_name}")
        self.assertEqual(res.json(), {
            "result": [myobj]
        })

    def test_get_by_room(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-09",
            "room_id": 9
        }

        myobj1 = {
            "name": mock_name1,
            "start_date": "2017-02-10",
            "end_date": "2017-02-15",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj1)))

        res = requests.get(BASE_URL + "/reservation/by-room/10")
        self.assertEqual(res.json(), {
            "result": [myobj1]
        })

    def test_post_proper_body(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-01",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

    def test_post_with_space_in_name(self):
        myobj = {
            "name": mock_name1,
            "start_date": "2017-01-01",
            "end_date": "2017-01-01",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

    def test_post_room_id_int_in_str_form(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-01",
            "room_id": "10"
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

    def test_post_room_id_int_in_str_form(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-01",
            "room_id": "10"
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(
            {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-01",
            "room_id": 10
        }
        )))

    def test_post_room_id_str_in_str_form(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-01",
            "room_id": mock_name
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(list(collection.find(myobj)))

    def test_post_start_day_improper_format(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-1",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(
            {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-15",
            "room_id": 10
        }
        )))

    def test_post_end_day_improper_format(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-9",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(
            {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-09",
            "room_id": 10
        }
        )))

    def test_post_start_month_improper_format(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-1-01",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(
            {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-15",
            "room_id": 10
        }
        )))

    def test_post_end_month_improper_format(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-1-09",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(
            {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-09",
            "room_id": 10
        }
        )))

    def test_post_start_date_come_after_end_date(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-09",
            "end_date": "2017-01-01",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj)))

    def test_post_room_id_out_of_range(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-09",
            "room_id": -1
        }

        myobj1 = {
            "name": mock_name,
            "start_date": "2017-02-01",
            "end_date": "2017-02-09",
            "room_id": 11
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj1)))

    def test_post_date_out_of_range(self):
        myobj = {
            "name": mock_name,
            "start_date": "10000-01-01",
            "end_date": "2017-01-09",
            "room_id": 8
        }

        myobj1 = {
            "name": mock_name,
            "start_date": "2017-13-01",
            "end_date": "2017-01-09",
            "room_id": 9
        }

        myobj2 = {
            "name": mock_name,
            "start_date": "2017-01-32",
            "end_date": "2017-01-09",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(list(collection.find(myobj1)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj2)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(list(collection.find(myobj2)))

    def test_post_date_cover_other_reservation(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        myobj1 = {
            "name": mock_name,
            "start_date": "2017-01-09",
            "end_date": "2017-01-16",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj1)))

    def test_post_date_in_between_other_reservation(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        myobj1 = {
            "name": mock_name,
            "start_date": "2017-01-11",
            "end_date": "2017-01-14",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj1)))

    def test_post_start_date_overlap_in_other_reservation(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        myobj1 = {
            "name": mock_name,
            "start_date": "2017-01-12",
            "end_date": "2017-01-16",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj1)))

    def test_post_end_date_overlap_in_other_reservation(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        myobj1 = {
            "name": mock_name,
            "start_date": "2017-01-09",
            "end_date": "2017-01-14",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj1)))

    def test_post_start_date_overlap_at_other_reservation_start_date(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        myobj1 = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-16",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj1)))

    def test_post_start_date_overlap_at_other_reservation_end_date(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        myobj1 = {
            "name": mock_name,
            "start_date": "2017-01-15",
            "end_date": "2017-01-16",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj1)))

    def test_post_end_date_overlap_at_other_reservation_start_date(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        myobj1 = {
            "name": mock_name,
            "start_date": "2017-01-05",
            "end_date": "2017-01-10",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj1)))

    def test_post_end_date_overlap_at_other_reservation_end_date(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        myobj1 = {
            "name": mock_name,
            "start_date": "2017-01-05",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.post(BASE_URL + f"/reservation", json=myobj1)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(list(collection.find(myobj1)))

    def test_put_proper_body(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-16"
        new_end_date = "2017-01-20"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 200)
        self.assertFalse(list(collection.find(myobj)))
        self.assertTrue(list(collection.find(new_obj)))

    def test_put_new_start_day_improper_format(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-6"
        new_end_date = "2017-01-09"

        new_obj = {
            "name": mock_name,
            "start_date": "2017-01-06",
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 200)
        self.assertFalse(list(collection.find(myobj)))
        self.assertTrue(list(collection.find(new_obj)))

    def test_put_new_end_day_improper_format(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-01"
        new_end_date = "2017-01-9"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": "2017-01-09",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 200)
        self.assertFalse(list(collection.find(myobj)))
        self.assertTrue(list(collection.find(new_obj)))

    def test_put_new_start_month_improper_format(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-1-16"
        new_end_date = "2017-01-20"

        new_obj = {
            "name": mock_name,
            "start_date": "2017-01-16",
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 200)
        self.assertFalse(list(collection.find(myobj)))
        self.assertTrue(list(collection.find(new_obj)))

    def test_put_new_end_month_improper_format(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-16"
        new_end_date = "2017-1-20"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": "2017-01-20",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 200)
        self.assertFalse(list(collection.find(myobj)))
        self.assertTrue(list(collection.find(new_obj)))

    def test_put_start_date_come_after_end_date(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-20"
        new_end_date = "2017-01-16"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 400)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

    def test_put_date_out_of_range(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-32"
        new_end_date = "2017-01-31"

        new_start_date1 = "2017-13-16"
        new_end_date1 = "2017-12-20"

        new_start_date2 = "10000-01-16"
        new_end_date2 = "2017-01-20"

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 422)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find({
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "room_id": 10
        })))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date1,
            "new_end_date": new_end_date1
        })
        
        self.assertEqual(res.status_code, 422)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find({
            "name": mock_name,
            "start_date": new_start_date1,
            "end_date": new_end_date1,
            "room_id": 10
        })))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date2,
            "new_end_date": new_end_date2
        })
        
        self.assertEqual(res.status_code, 422)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find({
            "name": mock_name,
            "start_date": new_start_date2,
            "end_date": new_end_date2,
            "room_id": 10
        })))

    def test_put_date_in_between_other_reservation(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-11"
        new_end_date = "2017-01-14"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 400)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

    def test_put_start_date_overlap_in_other_reservation(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-11"
        new_end_date = "2017-01-16"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 400)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

    def test_put_end_date_overlap_in_other_reservation(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-09"
        new_end_date = "2017-01-14"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 400)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

    def test_put_start_date_overlap_at_other_reservation_start_date(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-10"
        new_end_date = "2017-01-20"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 400)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))
        
    def test_put_start_date_overlap_at_other_reservation_end_date(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-15"
        new_end_date = "2017-01-20"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 400)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

    def test_put_end_date_overlap_at_other_reservation_start_date(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-05"
        new_end_date = "2017-01-10"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 400)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

    def test_put_end_date_overlap_at_other_reservation_end_date(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-10",
            "end_date": "2017-01-15",
            "room_id": 10
        }

        new_start_date = "2017-01-09"
        new_end_date = "2017-01-15"

        new_obj = {
            "name": mock_name,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

        res = requests.put(BASE_URL + f"/reservation/update", json={
            "reservation": myobj,
            "new_start_date": new_start_date,
            "new_end_date": new_end_date
        })
        
        self.assertEqual(res.status_code, 400)
        self.assertTrue(list(collection.find(myobj)))
        self.assertFalse(list(collection.find(new_obj)))

    def test_delete(self):
        myobj = {
            "name": mock_name,
            "start_date": "2017-01-01",
            "end_date": "2017-01-01",
            "room_id": 10
        }

        res = requests.post(BASE_URL + f"/reservation", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(list(collection.find(myobj)))

        res = requests.delete(BASE_URL + f"/reservation/delete", json=myobj)
        
        self.assertEqual(res.status_code, 200)
        self.assertFalse(list(collection.find(myobj)))
        

    
if __name__ == "__main__":
    connect_mongodb()
    unittest.main(verbosity=2, exit=False)