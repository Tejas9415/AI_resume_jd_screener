"""
mini_api.py
-----------
Ek CHHOTA practice FastAPI app - kal wale recruitment screener se alag.
Yahan sirf FastAPI ka core pattern samajhna hai: route, GET, POST,
path param, Pydantic body.
"""

from fastapi import FastAPI
# FastAPI -> humara main app class, isi se poora server banega

from pydantic import BaseModel
# BaseModel -> request body ka shape/validation define karne ke liye


app = FastAPI()
# ^ ye "app" object hamara poora web server represent karta hai -
#   isi mein hum routes (endpoints) register karenge neeche


class Item(BaseModel):
    # Ye class define karti hai POST request mein JSON body kaisi dikhni chahiye
    name: str
    # ^ "name" field hona ZAROORI hai, aur wo string honi chahiye
    price: float
    # ^ "price" field hona zaroori hai, float type mein
    # (agar client galat type bheje - jaise price ki jagah text - to
    #  FastAPI khud hi automatic 422 error de dega, humein manually
    #  check karne ki zaroorat nahi)


@app.get("/")
# @app.get(...) -> "decorator" jo batata hai ye function GET request
# handle karega is path ("/") par
def home():
    # function ka naam kuch bhi ho sakta hai, FastAPI ko farak nahi padta
    return {"message": "Hello from FastAPI"}
    # jo bhi dict return karoge, wo automatically JSON ban ke client ko jaayega


@app.get("/greet/{name}")
# {name} -> path parameter, URL ke andar hi ek variable slot
def greet(name: str):
    # ^ function parameter ka naam URL ke {name} se EXACTLY match karna
    #   chahiye - FastAPI automatically wahan se value nikaal ke yahan de dega
    return {"greeting": f"Hello {name}"}


@app.post("/items")
# POST -> client naya data server ko BHEJ raha hai (GET sirf maangta hai)
def create_item(item: Item):
    # ^ jaise hi function parameter ka type "Item" (humara Pydantic model)
    #   hai, FastAPI khud samajh jaata hai: "iska matlab request BODY se
    #   JSON parse karke Item object banao" - hume manually JSON parse
    #   karne, validate karne, kuch nahi karna padta
    return {"received": item, "total_with_tax": round(item.price * 1.18, 2)}
    # item ek proper Python object hai yahan, item.price seedha use ho raha hai