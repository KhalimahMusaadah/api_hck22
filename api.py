#LIbraries
from fastapi import FastAPI, HTTPException, Header
import uvicorn 
import pandas as pd

#bikin instance untuk menangkap REST API (Fast API)
khalim = FastAPI()

###############################LOAD FROM JSON###############################
#Endpoint utama
@khalim.get("/")
def home():
    return {"message": "Hello World! This is my first API",
            "menu": {1: "/students",
                     2: "/horses",
                     3: "/shopping_cart"}}
    
students_data = {
    "Joni":{
        "shoe_size": 44,
        "color": "black"
    },
    "Salsa":{
        "shoe_size": 39,
        "color": "white"
    },
    "Dewa":{
        "shoe_size": 42,
        "color": "green"
    }
}

#endpoint_student
@khalim.get("/students") #setara dengan http://127.0.0.1:8000 atau localhost:800
def students():
    return {"message": "ini merupakan API untuk menampilkan, menambah, menghapus students",
            "menu":{
                1: "/data",
                2: "/find_students/{name}",
                3: "add_students",
                4: "/update_students/{name}",
                5: "/delete_students/{name}"
            }}
    
#Endpoint untuk menampilkan semua data
@khalim.get("/students/data")
def std_data():
    return students_data

#Endpoint mencari siswa
@khalim.get("/students/find_students/{name}")
def find_student(name:str):
    #conditional pengecekan apakah nama siswa ada
    if name in students_data.keys():
        return students_data[name]
    else:
        raise HTTPException(status_code = 404, detail = "status not found")
    
#Endpoint menambah data siswa
@khalim.post("/students/add_students")
def add_std(student_data:dict):
    #untuk menambahkan print pesan dalam terminal
    print(f"student data: {student_data}")
    #untuk menangkap masukan
    student_name = student_data["name"]
    student_shoe_size = student_data["shoe_size"]
    student_color = student_data["color"]
    students_data[student_name] = {
        "shoe_size" : student_shoe_size,
        "color" : student_color
    }
    #untuk menambah tampilan ke dalam API
    return{"message": f"student {student_name} successfully added"}

#Endpoint untuk update/edit data
@khalim.put("/students/update_students/{name}")
def put_std(name:str, student_data:dict):
    #conditional pengecekan apakah nama ada dalam data
    if name not in students_data.keys():
        raise HTTPException(status_code = 404, detail = f"student {name} bot found")
    else:
        #assign variabel value dari hasil slicing dictionary students_data dalam student_data
        students_data[name] = student_data
        #menampilkan pesan dalam api
        return{"message": f"students data {name} has been update"}

#Endpoint untuk hapus data siswa
@khalim.delete("/students/delete_students/{name}")
def del_std(name:str):
    if name in students_data.keys():
        del students_data[name]
        return{"message" : f"student_data {name} has been delete"}
    else:
        raise HTTPException(status_code = 404, detail = f"student {name} bot found")


################################LOAD FROM CSV###############################
#load data disimpan dalam variabel horse
horse = pd.read_csv('horse_clean.csv')

#endpoint horse home
@khalim.get('/horses')
def kandang():
    return {"message" : "selamat datang di submenu perkudaan hewan paling keren",
            "menu": {
                1 : "get all horses (/horses/data)",
                2 : "filter by surgery ('horses/surgery/{surg})",
                3 : "filter by outcome ('horses/outcome/{out})",
                4 : "delete horses data by unamed: 0 *sad :'((/horses/del/{id}))"
            }
            }
    
#Endpoint show horses data
@khalim.get("/horses/data")
def kuda():
    return horse.to_dict(orient = "records")

#Endpoint filter by surgery
@khalim.get("/horses/surgery/{surgery_type}")
def operasi(surgery_type:str):
    #menyimpan hasil slicing dalam variabel baru
    horse_surgery = horse[horse["surgery"] == surgery_type]
    #return hasil slicing
    return horse_surgery.to_dict(orient = "records")


#Endpoint filter by outcome
@khalim.get("/horses/outcome/{outcome_type}")
def idup(outcome_type:str):
    #menyimpan hasil slicing dalam variabel baru
    horse_outcome = horse[horse["outcome"] == outcome_type]
    #return hasil slicing
    return horse_outcome.to_dict(orient = "records")

#API KEY (password)
API_KEY = "admin1234"

# Endpoint untuk hapus data menggunakan akses API Key
@khalim.delete("/horses/del/{id}")
def apus(id:int, api_key:str=Header(None)): # Memasang API Key dalam Header dengan default value None
    # Menunjukkan value api_key dalam terminal
    print(api_key)
    # Conditional pengecekan API Key
    if api_key is None or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key masih kosong atau salah")
    # Kalo API Key bener
    else:
        # Pengecekan apakah id ada dalam kolom unnamed: 0
        if id not in horse["Unnamed: 0"].values:
            raise HTTPException(status_code=404, detail=f"Horse with id {id} did not found!")
        # Kalo ketemu / ada
        else: 
            horse.drop(horse[horse["Unnamed: 0"]==id].index, inplace=True)
            return {"message":f"Horse with id {id} succesfully deleted!"}
        




################################SHOPPING CART###############################
from fastapi import FastAPI, HTTPException, Header

app = FastAPI()

API_KEY = "phase0h8"

data = {"name":"shopping cart",
        "columns":["prod_name","price","num_items"],
        "items":{}}

@app.get("/")
def root():
    return {"message":"Welcome to Toko H8 Shopping Cart! There are some features that you can explore",
            "menu":{1:"See shopping cart (/data)",
                    2:"Add item (/add) - You may need request",
                    3:"Edit shopping cart (/edit/id)",
                    4:"Delete item from shopping cart (/del/id)"}}

@app.get("/cart")
def show():
    return data

@app.post("/add")
def add_item(added_item:dict, api_key: str = Header(None)):
    if api_key is None or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key. You are not allowed to add data!")
    else:
        id = len(data["items"].keys())+1
        data["items"][id] = added_item
        return f"Item successfully added into your cart with ID {id}"

@app.put("/edit/{id}")
def update_cart(id:int,updated_cart:dict, api_key: str = Header(None)):
    if id not in data['items'].keys():
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")
    else:
        if api_key is None or api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API Key. You are not allowed to edit data!")
        else:
            data["items"][id].update(updated_cart)
            return {"message": f"Item with ID {id} has been updated successfully."}

@app.delete("/del/{id}")
def remove_row(id:int, api_key: str = Header(None)):
    if id not in data['items'].keys():
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")
    else:
        if api_key is None or api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API Key. You are not allowed to delete data!")
        else:
            data["items"].pop(id)
            return {"message": f"Item with ID {id} has been deleted successfully."}
        
cart = {"name": "shopping cart",
        "columns": ["prod_name", "price", "num_items"],
        "items": {}}


@khalim.get("/shopping_cart")
def root():
    return {"message": "Welcome to Toko H8 Shopping Cart! There are some features that you can explore",
            "menu": {1: "See shopping cart (/shopping_cart/cart)",
                     2: "Add item (/shopping_cart/add)",
                     3: "Edit shopping cart (/shopping_cart/edit/{id})",
                     4: "Delete item from shopping cart (/shopping_cart/del/{id})",
                     5: "Calculate total price (/shopping_cart/total)",
                     6: "Exit (/shopping_cart/exit)"}
            }


@khalim.get("/shopping_cart/cart")
def show():
    return cart


@khalim.post("/shopping_cart/add")
def add_item(added_item: dict):
    id = len(cart["items"].keys()) + 1
    cart["items"][id] = added_item
    return f"Item successfully added into your cart with ID {id}"


@khalim.put("/shopping_cart/edit/{id}")
def update_cart(id: int, updated_cart: dict):
    if id not in cart['items'].keys():
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")
    else:
        cart["items"][id].update(updated_cart)
        return {"message": f"Item with ID {id} has been updated successfully."}


@khalim.delete("/shopping_cart/del/{id}")
def remove_row(id: int):
    if id not in cart['items'].keys():
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")
    else:
        cart["items"].pop(id)
        return {"message": f"Item with ID {id} has been deleted successfully."}


@khalim.get("/shopping_cart/total")
def get_total():
    total_price = sum(item["price"] * item["num_items"] for item in cart["items"].values())
    return {"total_price": total_price}


@khalim.get("/shopping_cart/exit")
def exit():
    return {"message": "Thank you for using Toko H8 Shopping Cart! See you next time."}
        
if __name__ == "__main__":
    uvicorn.run("api:khalim", host = "127.0.0.1", port = 8000, reload = True)