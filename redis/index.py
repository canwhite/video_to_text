import asyncio
import redis.asyncio as redis

async def main():
    r = redis.Redis(host='localhost', port=6379, db=0)
    await r.set('my-key', 'value')
    value = await r.get('my-key')
    print(value)
    await r.aclose()

asyncio.run(main())