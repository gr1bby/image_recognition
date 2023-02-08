import redis
from collections import defaultdict
from comparison import get_image_hash


DISCRIPTION = (
    'Something interesting about image1',
    'Something interesting about image2',
    'Something interesting about image3',
    'Something interesting about image4',
    'Something interesting about image5',
    'Something interesting about image6',
    'Something interesting about image7',
    'Something interesting about image8'
)

r = redis.Redis()

hashes = defaultdict()
for i in range(1, 9):
    hashes[get_image_hash(f'faces/face{i}.jpg')] = DISCRIPTION[i - 1]

def setup_db_values():
    r.mset(dict(hashes))
