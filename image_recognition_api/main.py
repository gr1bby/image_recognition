from base64 import b64decode
from collections import defaultdict

import redis
from fastapi import FastAPI
from pydantic import BaseModel


from fc import get_face
from comparison import get_image_hash, compare_hash
from faces import setup_db_values
from config import FULL_IMG_PATH, FACE_IMG_PATH

# Uncomment this for debug
# import uvicorn


class Item(BaseModel):
    img: str


app = FastAPI()
db = redis.Redis()

# Use it to look this is working
@app.get('/')
async def root():
    return {'message': 'this is working'}


@app.post('/api/recognite_image')
async def recognite_image(item: Item):
    setup_db_values()
    error_response = defaultdict()
    right_response = defaultdict()

    with open(FULL_IMG_PATH, 'wb') as file:
        if item.img:
            decoded = b64decode(item.img)
            file.write(decoded)

    err = get_face(FULL_IMG_PATH, FACE_IMG_PATH)
    
    if err is None:
        results = list()
        right_response['lowest'] = 18
        right_response['text'] = 'unknown'
        face_hash = get_image_hash(FACE_IMG_PATH)

        for key in db.keys():
            result = compare_hash(face_hash, key.decode('utf-8'))
            results.append(str(result))
            if result <= right_response['lowest']:
                right_response['lowest'] = result
                right_response['text'] = db.get(key).decode('utf-8')

        if right_response['text'] == 'unknown':
            right_response['text'] = ', '.join(results)

        if len(right_response) == 0:
            error_response['error'] = "I don't know who is it :("
            return dict(error_response)

        return dict(right_response)

    else:
        error_response['error'] = err
        return dict(error_response)


# Uncomment this for debug
# if __name__ == '__main__':
#     uvicorn.run(app, host='192.168.100.6', port=8000)
