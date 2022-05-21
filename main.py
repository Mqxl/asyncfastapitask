from fastapi import FastAPI
from sqlalchemy import select, insert
import models
import random
import secrets
from settings import session, redis
app = FastAPI()


@app.post("/device/insert", status_code=201)
async def insert_device(
    count: int
):
    device_types = tuple(('emeter', 'zigbee', 'lora', 'gsm'))
    values_tuple = []
    for i in range(count):
        values_tuple.append({
            'dev_id': secrets.token_hex(48),
            'dev_type': random.choice(device_types)
        })
    insert_stmt = insert(
        models.Device
    ).values(
        values_tuple
    ).returning(models.Device)
    result = (await session.execute(insert_stmt)).all()
    values_tuple = []
    count = 0
    for i in result:
        if count >= 5:
            continue
        values_tuple.append({
            'device_id': i.id,
        })
        count += 1

    endpoint_stmt = insert(
        models.EndPoints
    ).values(
        values_tuple
    )
    await session.execute(endpoint_stmt)
    await session.commit()
    return result


@app.post("/check/")
async def check_anagram(
    first_string: str,
    second_string: str
):
    anagram = sorted(first_string) == sorted(second_string)
    count = await redis.get('anagram_count')

    if anagram is True:
        if count is None:
            count = 0
        await redis.set('anagram_count', int(count) + 1)
    count = await redis.get('anagram_count')
    return {
        "Is anagram": anagram,
        "anagram count": count
    }


@app.get('/list/')
async def device_list():
    stmt = select(models.EndPoints.device_id)
    select_stmt = select(
        models.Device
    ).where(
        models.Device.id.notin_(stmt)
    ).group_by(
        models.Device.id
    )
    try:
        return (await session.execute(select_stmt)).all()
    except:
        return None

