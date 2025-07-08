import itertools
import csv

# Belgilar to'plami
chars = ['q', 'z', 'x', '.', '_']

# 5 xonali kombinatsiyalar
combinations_5 = itertools.product(chars, repeat=5)

# 4 xonali kombinatsiyalar
combinations_4 = itertools.product(chars, repeat=4)

# CSV fayliga yozish
with open('kombinatsiyalar.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # CSV fayl uchun sarlavha
    writer.writerow(['Kombinatsiya', 'Uzunlik'])
    
    # 5 xonali kombinatsiyalarni yozish
    for combo in combinations_5:
        combo_str = ''.join(combo)
        writer.writerow([combo_str, 5])
    
    # 4 xonali kombinatsiyalarni yozish
    for combo in combinations_4:
        combo_str = ''.join(combo)
        writer.writerow([combo_str, 4])

print("Kombinatsiyalar kombinatsiyalar.csv fayliga yozildi.")
