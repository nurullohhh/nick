import requests
import random
import time
import urllib3
import threading
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Log sozlamasi
logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S")

# Faylni ochish
with open("5_letter_combinations.csv", "r") as f:
    lines = f.readlines()[1:]  # birinchi qatorda sarlavha bor

# Foydali listga aylantirish
usernames = [line.strip().split(",")[0] for line in lines]

# Mavjud threadlar
active_threads = []

# Tekshirish funksiyasi
def check(un, index):
    time.sleep(random.uniform(0.5, 1.5))
    url = f"https://www.instagram.com/{un}"
    try:
        x = requests.get(url, verify=False)
        if x.status_code == 200:
            logging.info(f"[{index}] ❌ Taken - {un}")
        else:
            logging.info(f"[{index}] ✅ Available - {un} ({x.status_code})")
            with open("available.txt", "a") as f2:
                f2.write(un + "\n")
    except Exception as e:
        logging.warning(f"[{index}] ⚠️ Error for {un}: {e}")

# Har bir foydalanuvchini tekshirish
for idx, un in enumerate(usernames):
    thread = threading.Thread(target=check, args=(un, idx), daemon=True)
    thread.start()
    active_threads.append(thread)
    time.sleep(1.2)
    if idx % 20 == 0:
        time.sleep(10)
