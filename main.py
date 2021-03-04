from typing import Optional
from fastapi import FastAPI
import hashlib
import os

herokuEnv = os.getenv("HEROKU_ENV", "live")

if herokuEnv == 'live':
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q:Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/hash/{hashType}")
def getHash(hashType:str, inp:Optional[str]):
    # TODO : input 값을 parameter로 사용하지 않도록 해야함.
    hashTypeLower = hashType.lower()

    result = {}

    result['type'] = hashTypeLower
    result['input'] = inp

    encInp = inp.encode('utf-8')
    enc = None
    
    if hashTypeLower == 'md5':
        enc = hashlib.md5()
    elif hashTypeLower == 'sha1':
        enc = hashlib.sha1()
    elif hashTypeLower == 'sha256':
        enc = hashlib.sha256()
    elif hashTypeLower == 'sha512':
        enc = hashlib.sha512()

    try:
        enc.update(encInp)
        result['output'] = enc.hexdigest()
        result['hash'] = inp
    except Exception as ex:
        result['exception'] = str(ex)

    return result