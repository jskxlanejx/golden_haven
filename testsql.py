import sqlite3
import os
import time
import threading


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database")

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Создаем таблицу пользователей, если ее еще нет
c.execute('''CREATE TABLE IF NOT EXISTS users 
               (id INTEGER PRIMARY KEY, username TEXT, balance INTEGER DEFAULT 650, cows INTEGER DEFAULT 0, goats INTEGER DEFAULT 0, milk INTEGER DEFAULT 0, chickens INTEGER DEFAULT 0, egg INTEGER DEFAULT 0, horse INTEGER DEFAULT 0, meat INTEGER DEFAULT 0, lvl INTEGER DEFAULT 0, exp INTEGER DEFAULT 0, quest1 INTEGER DEFAULT 0, fish INTEGER DEFAULT 0)''')


def add_user_to_database(user_id, username):
    c.execute("INSERT OR IGNORE INTO users (id, username, balance, cows, goats, milk, chickens, egg, horse, meat, lvl, exp, quest1, fish) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, username, 650, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    conn.commit()

def update_level(user_id, exp):
    lvl = exp // 5
    c.execute("UPDATE users SET lvl=?, exp=? WHERE id=?", (lvl, exp, user_id))

    return lvl

"""
def update_db():
    while True:
        time.sleep(2)
        conn = sqlite3.connect('database')
        c = conn.cursor()
        c.execute("UPDATE users SET exp = 0 WHERE exp IS NULL")
        conn.commit()
        conn.close()
#"""

def update_user_fish(user_id, amount):
    c.execute("UPDATE users SET fish = ? WHERE id = ?", (amount, user_id))
    conn.commit()

def get_fish_from_database(user_id):
    c.execute("SELECT fish FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def get_lvl_from_database(user_id):
    c.execute("SELECT lvl FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def update_user_balance(user_id, amount):
    c.execute("UPDATE users SET balance = ? WHERE id = ?", (amount, user_id))
    conn.commit()

def update_user_quest1(user_id, amount):
    c.execute("UPDATE users SET quest1 = ? WHERE id = ?", (amount, user_id))
    conn.commit()

def get_quest1(user_id):
    c.execute("SELECT quest1 FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def update_user_exp(user_id, exp):
    c.execute("UPDATE users SET exp = ? WHERE id = ?", (exp, user_id))
    conn.commit()

def get_exp_from_database(user_id):
    c.execute("SELECT exp FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def get_username_from_database(user_id):
    c.execute("SELECT username FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else None

def get_balance_from_database(user_id):
    c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def get_cows_from_database(user_id):
    c.execute("SELECT cows FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def update_user_cows(user_id, cows):
    c.execute("UPDATE users SET cows = ? WHERE id = ?", (cows, user_id))
    conn.commit()

def get_horse_from_database(user_id):
    c.execute("SELECT horse FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def update_user_horse(user_id, horse):
    c.execute("UPDATE users SET horse = ? WHERE id = ?", (horse, user_id))
    conn.commit()

def get_chickens_from_database(user_id):
    c.execute("SELECT chickens FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def update_user_chickens(user_id, chickens):
    c.execute("UPDATE users SET chickens = ? WHERE id = ?", (chickens, user_id))
    conn.commit()

def get_goats_from_database(user_id):
    c.execute("SELECT goats FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def update_user_goats(user_id, goats):
    c.execute("UPDATE users SET goats = ? WHERE id = ?", (goats, user_id))
    conn.commit()

def get_milk_from_database(user_id):
    c.execute("SELECT milk FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def get_egg_from_database(user_id):
    c.execute("SELECT egg FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def update_user_milk(user_id, milk):
    c.execute("UPDATE users SET milk = ? WHERE id = ?", (milk, user_id))
    conn.commit()

def update_user_meat(user_id, meat):
    c.execute("UPDATE users SET meat = ? WHERE id = ?", (meat, user_id))
    conn.commit()

def get_meat_from_database(user_id):
    c.execute("SELECT meat FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    return result[0] if (result is not None) and (result[0] is not None) else 0

def sell_milk(user_id, amount):
    current_balance = get_balance_from_database(user_id)
    current_milk = get_milk_from_database(user_id)
    price = 1.0 # in dollars
    new_balance = current_balance + (amount * price)
    new_milk = current_milk - amount
    update_user_balance(user_id, new_balance)
    update_user_milk(user_id, new_milk)
    return f"Ты продал {amount} 🥛 за {amount*price} $. 💰 Твой баланс: {new_balance}."

def sell_fish(user_id, amount):
    current_balance = get_balance_from_database(user_id)
    current_fish = get_fish_from_database(user_id)
    price = 0.3 # in dollars
    new_balance = current_balance + (amount * price)
    new_fish = current_fish - amount
    update_user_balance(user_id, new_balance)
    update_user_fish(user_id, new_fish)
    return f"Ты продал {amount} 🐟 за {amount*price} $. 💰 Твой баланс: {new_balance}."

def update_user_egg(user_id, egg):
    c.execute("UPDATE users SET egg = ? WHERE id = ?", (egg, user_id))
    conn.commit()

def sell_egg(user_id, amount):
    current_balance = get_balance_from_database(user_id)
    current_egg = get_egg_from_database(user_id)
    
    if current_egg < amount:
        return "У вас недостаточно яиц для продажи."
    
    price = 0.5 # in dollars
    new_balance = current_balance + (amount * price)
    new_egg = current_egg - amount
    
    update_user_balance(user_id, new_balance)
    update_user_egg(user_id, new_egg)
    
    return f"Ты продал {amount} 🥚 за {amount*price} $. 💰 Твой баланс: {new_balance}."

def sell_meat(user_id, amount):
    current_balance = get_balance_from_database(user_id)
    current_meat = get_meat_from_database(user_id)
    
    if current_meat < amount:
        return "У вас недостаточно мяса для продажи."
    
    price = 1.0 # in dollars
    new_balance = current_balance + (amount * price)
    new_meat = current_meat - amount
    
    update_user_balance(user_id, new_balance)
    update_user_meat(user_id, new_meat)
    
    return f"Ты продал {amount} 🥩 за {amount*price} $. 💰 Твой баланс: {new_balance}."
    

def farm_milk():
    while True:
        time.sleep(86400)
        conn = sqlite3.connect('database')
        cursor = conn.cursor()
    
        # выбираем всех коров и добавляем +2 молока за каждую
        cursor.execute("SELECT * FROM users WHERE cows > 0")
        for row in cursor.fetchall():
            cows = row[3]  # количество коров в текущей записи
            cursor.execute(f"UPDATE users SET milk=milk+2*{cows} WHERE id={row[0]}")
    
        # выбираем всех коз и добавляем +1 молока за каждую
        cursor.execute("SELECT * FROM users WHERE goats > 0")
        for row in cursor.fetchall():
            goats = row[4]  # количество коз в текущей записи
            cursor.execute(f"UPDATE users SET milk=milk+1*{goats} WHERE id={row[0]}")
    
        conn.commit()
        conn.close()

def farm_egg():
    while True:
        time.sleep(43200)
        conn = sqlite3.connect('database')
        cursor = conn.cursor()
        # выбираем всех кур и добавляем +2 яйца за каждую
        cursor.execute("SELECT * FROM users WHERE chickens > 0")
        for row in cursor.fetchall():
            chicken = row[6]  # количество кур в текущей записи
            cursor.execute(f"UPDATE users SET egg=egg+2*{chicken} WHERE id={row[0]}")
    
        conn.commit()
        conn.close()

def farm_meat():
    while True:
        time.sleep(172800)
        conn = sqlite3.connect('database')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE cows > 1 OR goats > 1 OR chickens > 1")
        # выбираем всех пользователей, у которых больше одного коровы, козы или курицы
        for row in cursor.fetchall():
            meat = 0
            if row[3] > 1:  # если коров больше одной, добавляем +1 мясо за каждую
                meat += row[3]
            if row[4] > 1:  # если коз больше одной, добавляем +1 мясо за каждую
                meat += row[4]
            if row[6] > 1:  # если кур больше одной, добавляем +1 мясо за каждую
                meat += row[6]
            cursor.execute(f"UPDATE users SET meat=meat+{meat} WHERE id={row[0]}")
    
        conn.commit()
        conn.close()