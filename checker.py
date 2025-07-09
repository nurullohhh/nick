#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import requests
import time
import random
import sys

# SSL ogohlantirishlarini o'chirish
requests.packages.urllib3.disable_warnings()

# Sozlamalar
DELAY = 5.0  # So'rovlar orasidagi kechikishni oshirish
TIMEOUT = 20
RETRY_COUNT = 3
INPUT_FILE = "5_harfli_undosh_niklar.csv"
OUTPUT_FILE = "mavjud_emas_niklar.txt"
ERROR_FILE = "xatolar_logi.txt"

# User-Agentlar ro'yxati
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36",
    "Instagram 219.0.0.12.117 Android"
]

def get_random_agent():
    return random.choice(USER_AGENTS)

def log_error(nik, error):
    with open(ERROR_FILE, "a", encoding='utf-8') as f:
        f.write(f"{nik}: {error}\n")

def read_niks_from_csv():
    try:
        with open(INPUT_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader if row and len(row[0]) == 5]
    except Exception as e:
        print(f"Xatolik: {INPUT_FILE} faylini o'qib bo'lmadi. Sabab: {e}")
        sys.exit(1)

def check_nik_availability(nik):
    headers = {
        'User-Agent': get_random_agent(),
        'Accept-Language': 'en-US,en;q=0.9'
    }
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
                return False  # Band
            elif response.status_code == 404:
                return True  # Bo'sh
            elif response.status_code == 429:
                wait_time = 60  # 1 daqiqa kutish
                print(f"\nRate limit: {wait_time} soniya kutamiz...")
                time.sleep(wait_time)
                continue
                
        except requests.exceptions.RequestException as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            log_error(nik, error_msg)
            time.sleep(DELAY * (attempt + 1))
            continue
        
    return None  # Xatolik

def save_available_nik(nik):
    with open(OUTPUT_FILE, "a", encoding='utf-8') as f:
        f.write(nik + "\n")

def main():
    print("\n5 Harfli Undosh Niklar Tekshirgichi")
    print(f"Fayl: {INPUT_FILE}\n")
    
    niks = read_niks_from_csv()
    
    if not niks:
        print("Faylda hech qanday 5 harfli nik topilmadi!")
        return
    
    print(f"Jami {len(niks)} ta nik topildi")
    print(f"Tekshiruv taxminan {len(niks)*DELAY/60:.1f} daqiqa davom etadi\n")
    
    available_count = 0
    error_count = 0
    
    for i, nik in enumerate(niks, 1):
        print(f"\rTekshirilmoqda: {i}/{len(niks)} | Bo'sh: {available_count} | Xatolar: {error_count}", end='')
        
        result = check_nik_availability(nik)
        
        if result is True:
            print(f"\n✅ Bo'sh: {nik}")
            save_available_nik(nik)
            available_count += 1
        elif result is False:
            print(f"\n❌ Band: {nik}", end='')
        else:
            print(f"\n⚠️ Xato: {nik} (qayta urinishlar tugadi)", end='')
            error_count += 1
        
        time.sleep(DELAY)
    
    print("\n\n" + "="*50)
    print(f"Tekshiruv yakunlandi!")
    print(f"Bo'sh niklar: {available_count} ta")
    print(f"Xatolar: {error_count} ta")
    print(f"Natijalar '{OUTPUT_FILE}' fayliga yozildi")
    print(f"Xatolar '{ERROR_FILE}' fayliga yozildi")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDastur to'xtatildi")
        sys.exit(0)
    except Exception as e:
        print(f"\nKutilmagan xatolik: {e}")
        sys.exit(1)
