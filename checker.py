# -*- coding: utf-8 -*-
import requests
import random
import time
import urllib3
import threading
import logging
from itertools import product

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Sozlash parametrlari
CHARACTERS = ['x', 'z', 'n', 'a', '.', '_']  # Ishlatiladigan belgilar
MIN_LENGTH = 4  # Minimal uzunlik
MAX_LENGTH = 5  # Maksimal uzunlik
REQUEST_DELAY = 1.25  # So'rovlar orasidagi kechikish
BATCH_SIZE = 20  # Har 20 so'rovdan keyin katta kechikish
BATCH_DELAY = 15  # Batch uchun kechikish
MAX_THREADS = 10  # Maksimal parallel threadlar soni

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%H:%M:%S"
)

def generate_usernames():
    """Foydalanuvchi nomlarini generatsiya qilish"""
    usernames = []
    for length in range(MIN_LENGTH, MAX_LENGTH + 1):
        # Barcha mumkin bo'lgan kombinatsiyalarni generatsiya qilish
        for combo in product(CHARACTERS, repeat=length):
            username = ''.join(combo)
            # Qo'shimcha tekshirishlar (masalan, ketma-ket 2 nuqta yoki pastki chiziq)
            if '..' in username or '__' in username:
                continue
            if username.startswith(('.', '_')) or username.endswith(('.', '_')):
                continue
            usernames.append(username)
    return usernames

def check_username(username):
    """Instagramda username mavjudligini tekshirish"""
    try:
        url = f"https://www.instagram.com/{username}"
        response = requests.get(url, verify=False, timeout=10)
        
        if response.status_code == 404:
            # 404 - mavjud emas (band qilinmagan)
            logging.info(f"✅ Band qilinmagan: {username}")
            save_available(username)
            return True
        elif response.status_code == 200:
            # 200 - mavjud (band qilingan)
            logging.info(f"❌ Band qilingan: {username}")
            return False
        else:
            # Boshqa status kodlari
            logging.warning(f"⚠️ Noma'lum javob ({response.status_code}): {username}")
            return False
            
    except Exception as e:
        logging.error(f"🚫 Xatolik ({username}): {str(e)}")
        return False

def save_available(username):
    """Band qilinmagan nomlarni faylga yozish"""
    with open("available.txt", "a") as f:
        f.write(f"{username}\n")

def main():
    # Foydalanuvchi nomlarini generatsiya qilish
    usernames = generate_usernames()
    logging.info(f"Jami {len(usernames)} ta nom generatsiya qilindi")
    
    active_threads = []
    checked_count = 0
    
    for username in usernames:
        # Aktiv threadlar sonini cheklash
        while threading.active_count() > MAX_THREADS:
            time.sleep(0.5)
            
        # Yangi thread yaratish
        t = threading.Thread(
            target=check_username,
            args=(username,),
            daemon=True
        )
        t.start()
        active_threads.append(t)
        
        checked_count += 1
        time.sleep(REQUEST_DELAY)
        
        # Batch tekshiruvlari uchun qo'shimcha kechikish
        if checked_count % BATCH_SIZE == 0:
            logging.info(f"Batch yakunlandi, {BATCH_DELAY} soniya kutilmoqda...")
            time.sleep(BATCH_DELAY)
    
    # Barcha threadlar tugashini kutish
    for t in active_threads:
        t.join()
    
    logging.info("Barcha nomlar tekshirildi!")

if __name__ == "__main__":
    main()
