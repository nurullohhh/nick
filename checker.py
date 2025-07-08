# -*- coding: utf-8 -*-
"""
Instagram username checker for 4 and 5 letter usernames
Muallif: Nurulloh uchun to‘liq optimallashtirilgan
"""

import requests
import random
import time
import urllib3
import threading
import logging

# SSL ogohlantirishlarini o‘chirish
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Log sozlamalari
logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S")

# 4 va 5 harfli fayllarni o‘qish funksiyasi
def load_usernames(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()[1:] if line.strip()]

usernames_5 = load_usernames("5_letter_usernames_only.csv")
usernames_4 = load_usernames("4_letter_usernames_only.csv")
usernames = usernames_4 + usernames_5

# Bo‘sh username’lar ro‘yxati
available_list = []

# Tekshiruvchi funksiya
def check(username, index):
    time.sleep(random.uniform(0.5, 1.5))
    url = f"https://www.instagram.com/{username}"
    try:
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            logging.info(f"[{index}] ❌ Taken - {username}")
        else:
            logging.info(f"[{index}] ✅ Available - {username} ({response.status_code})")
            available_list.append(username)
            with open("available.txt", "a") as f2:
                f2.write(username + "\n")
    except Exception as e:
        logging.warning(f"[{index}] ⚠️ Error for {username}: {e}")

# Threadlarni ishga tushirish
threads = []
for idx, username in enumerate(usernames):
    t = threading.Thread(target=check, args=(username, idx), daemon=True)
    t.start()
    threads.append(t)
    time.sleep(1.2)
    if idx % 20 == 0:
        time.sleep(10)

# Tugashini kutamiz
for t in threads:
    t.join()

# Yakuniy natijani chiqarish
print("\n✅ Tekshiruv tugadi. Bo'sh (available) username'lar:")
for name in available_list:
    print(" -", name)
print(f"\nJami topildi: {len(available_list)} ta.")
