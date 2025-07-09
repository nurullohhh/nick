#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import requests
import time
import random
import sys
from tqdm import tqdm

# SSL ogohlantirishlarini o'chirish
requests.packages.urllib3.disable_warnings()

# Asosiy sozlamalar
DELAY = 3.0  # Har bir so'rov orasidagi minimal vaqt
TIMEOUT = 15  # So'rov uchun maksimal kutish vaqti
RETRY_COUNT = 2  # Qayta urinishlar soni
INPUT_FILE = "5_harfli_undosh_niklar.csv"  # Kirish fayli
OUTPUT_FILE = "mavjud_emas_niklar.txt"  # Natijalar fayli

# User-Agentlar ro'yxati
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36",
    "Instagram 219.0.0.12.117 Android"
]

def get_random_agent():
    """Tasodifiy User-Agent tanlash"""
    return random.choice(USER_AGENTS)

def read_niks_from_csv():
    """CSV fayldan niklar ro'yxatini o'qish"""
    try:
        with open(INPUT_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Fayldagi barcha qatorlarni o'qiymiz (sarlavha qatorini qo'shmasdan)
            return [row[0] for row in reader if row and len(row[0]) == 5]
    except Exception as e:
        print(f"Xatolik: {INPUT_FILE} faylini o'qib bo'lmadi. Sabab: {e}")
        sys.exit(1)

def check_nik_availability(nik):
    """Nikning mavjudligini tekshirish"""
    headers = {'User-Agent': get_random_agent()}
    url = f"https://www.instagram.com/{nik}/"
    
    for attempt in range(RETRY_COUNT):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT,
                verify=False,
                allow_redirects=False
            )
            
            if response.status_code == 200:
                return False  # Nik band
            elif response.status_code == 404:
                return True  # Nik bo'sh
            elif response.status_code == 429:
                time.sleep(30)  # Limit qo'yilganda 30 soniya kutish
                continue
                
        except Exception as e:
            time.sleep(DELAY * 2)
            continue
        
        time.sleep(DELAY)
    
    return None  # Xatolik yuz berdi

def save_available_nik(nik):
    """Bo'sh nikni faylga yozish"""
    with open(OUTPUT_FILE, "a", encoding='utf-8') as f:
        f.write(nik + "\n")

def main():
    print("\n5 Harfli Undosh Niklar Tekshirgichi")
    print(f"Fayl: {INPUT_FILE}\n")
    
    # Niklarni fayldan o'qish
    niks = read_niks_from_csv()
    
    if not niks:
        print("Faylda hech qanday 5 harfli nik topilmadi!")
        return
    
    print(f"Jami {len(niks)} ta nik topildi")
    print(f"Tekshiruv taxminan {len(niks)*DELAY/60:.1f} daqiqa davom etadi\n")
    
    # Progress bar bilan tekshirish
    available_count = 0
    pbar = tqdm(niks, desc="Tekshirilmoqda", unit="nik")
    
    for nik in pbar:
        result = check_nik_availability(nik)
        
        if result is True:
            pbar.write(f"✅ Bo'sh: {nik}")
            save_available_nik(nik)
            available_count += 1
        elif result is False:
            pbar.write(f"❌ Band: {nik}")
        else:
            pbar.write(f"⚠️ Xato: {nik}")
        
        time.sleep(DELAY)
    
    # Natijalarni ko'rsatish
    print("\n" + "="*50)
    print(f"Tekshiruv yakunlandi! Jami {available_count} ta bo'sh nik topildi")
    print(f"Natijalar {OUTPUT_FILE} fayliga yozildi")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDastur to'xtatildi")
        sys.exit(0)
    except Exception as e:
        print(f"\nKutilmagan xatolik: {e}")
        sys.exit(1)
