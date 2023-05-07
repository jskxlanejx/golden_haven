from config import *
from testsql import *
from telethon import TelegramClient, events
from telethon import Button
import threading
import emoji
import random
import asyncio


bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=API_TOKEN)

@bot.on(events.NewMessage(pattern='/locations'))
async def locations_handler(event):
    user_id = event.sender_id
    username = get_username_from_database(user_id)

    locations_buttons = [
        Button.inline("Озеро", b"ozero"),
    ]

    response = f"Это меню локаций, {username}🔥!"
    await event.respond(response, buttons=locations_buttons)

@bot.on(events.CallbackQuery(data=b"ozero_random"))
async def start_fishing_handler(event):
    sender_id = event.sender_id
    fish = get_fish_from_database(sender_id)
    rand_fish = random.randint(0, 2)
    update_user_fish(sender_id, fish + rand_fish)

    await event.respond("🎣(30 секунд...)")

    await asyncio.sleep(30)

    response = f"Вы поймали {rand_fish} рыб(ы)! Теперь у вас {fish + rand_fish} рыб(ы)!"
    
    await event.respond(response)

@bot.on(events.CallbackQuery())
async def locations_callback_handler(event):
    sender_id = event.sender_id
    horse = get_horse_from_database(sender_id)
    fish = get_fish_from_database(sender_id)

    if event.data == b"ozero":
        if not horse:
            await event.respond("У вас нет лошади, чтобы добраться до озера!")
            return
        
        # анимация поездки
        response1 = "🐎"
        await event.respond(response1)
        await asyncio.sleep(3)

        ozero_buttons = [
            Button.inline("Да!", b"ozero_random"),
            Button.inline("Меню", b"menub"),
        ]
        response = f"Вы приехали к \"озеру\" для ловли рыбы, хотите начать рыбачить?\n\n🐟: {fish}"
        await event.respond(response, buttons=ozero_buttons)

    # обработчик для кнопки "Да!"
    if event.data == "ozero_random":
        rand_fish = random.randint(0, 2)
        update_user_fish(sender_id, fish + rand_fish)
        response = f"Вы поймали {rand_fish} рыб(ы)! Теперь у вас {fish + rand_fish} рыб(ы)!"
        await event.respond(response)
    

@bot.on(events.NewMessage(pattern='/quests'))
async def quests_handler(event):
    user_id = event.sender_id
    username = get_username_from_database(user_id)

    quest_buttons = [
        Button.inline("2 🐓", b"Quest_1"),
    ]

    # Формируем ответ
    response = (
        f"👋🏻Привет {username}, это меню квестов🔥!"
    )
    await event.respond(response, buttons=quest_buttons)

@bot.on(events.CallbackQuery())
async def quests_callback_handler(event):
    sender_id = event.sender_id

    if event.data == b"Quest_1":
        # Получаем текущий баланс пользователя из базы данных
        chickens = get_chickens_from_database(sender_id)
        balance = get_balance_from_database(sender_id)
        quest1 = get_quest1(sender_id)

        if quest1 == 1:
            await event.answer("Вы уже выполняли 1 квест😡!")

        elif chickens >= 2:
            update_user_balance(sender_id, balance + 500)
            update_user_exp(sender_id, get_exp_from_database(sender_id) + 5)
            update_user_quest1(sender_id, quest1 + 1)
            await event.answer("Вы выполнили 1 квест🎉!")
        else:
            await event.answer("Недостаточно куриц🐔")
    

# Обработчик команды /profile
@bot.on(events.NewMessage(pattern='/profile'))
async def profile_handler(event):
    sender_id = event.sender_id
    username = get_username_from_database(sender_id)
    if not username:
        response = "Сначала представьтесь, набрав команду /start"
        await event.respond(response)
        return

    # Получаем текущий баланс пользователя из базы данных
    balance = get_balance_from_database(sender_id)

    # Получаем количество коров пользователя из базы данных
    cows = get_cows_from_database(sender_id)

    # Получаем количество коз пользователя из базы данных
    goats = get_goats_from_database(sender_id)

    # Получаем количество молока пользователя из базы данных
    milk = get_milk_from_database(sender_id)

    egg = get_egg_from_database(sender_id)

    chicken = get_chickens_from_database(sender_id)

    horse = get_horse_from_database(sender_id)

    meat = get_meat_from_database(sender_id)

    exp = get_exp_from_database(sender_id)

    lvl = get_lvl_from_database(sender_id)

    fish = get_fish_from_database(sender_id)


    # Формируем ответ
    response = (
        f"👨‍🌾Профиль: @{username} lvl:{lvl}👩‍🌾\n\n"
        f"--------------------~~~--------------------\n"
        f"💰Текущий баланс: {balance}$\n\n"
        f"Ваши животные:\n"
        f"🐄: {cows} 🐎: {horse}\n"
        f"🐐: {goats} 🐓: {chicken}\n\n"
        f"Ваши ресурсы:\n"
        f"🥚: {egg} 🥩: {meat}\n"
        f"🥛: {milk} 🐟: {fish}\n\n"
        f"🌾: {exp} \n\n"
        f"By @shinogizxc1 🫧"
    )

    # Создаем список кнопок для клавиатуры
    menu_buttons = [
        Button.url("Открыть канал", url="https://t.me/jesshigashikata")
    ]
 # Создаем клавиатуру из списка кнопок
    menu_keyboard = [menu_buttons]

    # Проверяем, есть ли кнопки в клавиатуре
    if menu_buttons:
        # Отправляем пользователю сообщение с клавиатурой меню
        await event.respond(response, buttons=menu_keyboard)
    else:
        # Отправляем пользователю сообщение без клавиатуры
        await event.respond(response)

# Обработчик команды /shop
@bot.on(events.NewMessage(pattern='/shop'))
async def shop_handler(event):
    sender_id = event.sender_id
    username = get_username_from_database(sender_id)
    if not username:
        response = "Сначала представьтесь, набрав команду /start"
        await event.respond(response)
        return

    # Получаем текущий баланс пользователя из базы данных
    balance = get_balance_from_database(sender_id)

    # Получаем количество коров пользователя из базы данных
    cows = get_cows_from_database(sender_id)

    # Получаем количество коз пользователя из базы данных
    goats = get_goats_from_database(sender_id)

    # Получаем количество лошадей пользователя из базы данных
    horse = get_horse_from_database(sender_id)

    # Получаем количество кур пользователя из базы данных
    chickens = get_chickens_from_database(sender_id)

    # Создаем список кнопок для клавиатуры
    shop_buttons = [
        Button.inline(" 🐄 (1200$)", b"buy_cow"),
        Button.inline("🐐 (650$)", b"buy_goat"),
        Button.inline(" 🐎 (5000$)", b"buy_horse"),
        Button.inline("🐓 (200$)", b"buy_chicken"), # Добавляем кнопку для покупки кур
        Button.inline("🔚Меню", b"menub")
    ]

    # Создаем клавиатуру из списка кнопок
    shop_keyboard = [shop_buttons[i:i+2] for i in range(0, len(shop_buttons), 2)]

    # Отправляем пользователю сообщение с клавиатурой магазина
    response = (
        f"--------------------------------------------------------------\n"
        f"💎Ваш баланс: {balance}$\n\n"
        f"🐄: 2 молока в сутки(за 1)🥛\n"
        f"🐐: 1 молока в сутки(за 1)🥛\n"
        f"🐎: Coming soon\n"
        f"🐓: 4 яйцо в сутки(за 1 курицу 2 яйца в пол дня)🥚\n\n"
        "🛒Что вы хотите купить?"
    )
    await event.respond(response, buttons=shop_keyboard)

# Обработчик нажатий на кнопки меню магазина
@bot.on(events.CallbackQuery())
async def shop_callback_handler(event):
    sender_id = event.sender_id

    # Обработчик покупки коровы
    if event.data == b"buy_cow":
        # Получаем текущий баланс пользователя из базы данных
        balance = get_balance_from_database(sender_id)

        # Проверяем, хватает ли у пользователя денег на покупку коровы
        if balance >= 1200:
            # Если хватает, то списываем стоимость коровы с баланса пользователя и добавляем ему корову
            update_user_balance(sender_id, balance - 1200)
            update_user_cows(sender_id, get_cows_from_database(sender_id) + 1)
            await event.answer("Вы купили корову!")
        else:
            await event.answer("У вас недостаточно монет для покупки коровы")

    # Обработчик покупки лошадей
    elif event.data == b"buy_horse":
      # Получаем текущий баланс пользователя из базы данных
        balance = get_balance_from_database(sender_id)

        # Проверяем, хватает ли у пользователя денег на покупку лошади
        if balance >= 5000:
            # Если хватает, то списываем стоимость лошадь с баланса пользователя и добавляем ему лошадь
            update_user_balance(sender_id, balance - 5000)
            update_user_horse(sender_id, get_chickens_from_database(sender_id) + 1)
            await event.answer("Вы купили лошадь!")
        else:
            await event.answer("У вас недостаточно монет для покупки лошади")

    # Обработчик покупки кур
    elif event.data == b"buy_chicken":
      # Получаем текущий баланс пользователя из базы данных
        balance = get_balance_from_database(sender_id)

        # Проверяем, хватает ли у пользователя денег на покупку кур
        if balance >= 200:
            # Если хватает, то списываем стоимость кур с баланса пользователя и добавляем ему кур
            update_user_balance(sender_id, balance - 200)
            update_user_chickens(sender_id, get_chickens_from_database(sender_id) + 1)
            await event.answer("Вы купили курицу!")
        else:
            await event.answer("У вас недостаточно монет для покупки кур")

    # Обработчик покупки козы
    elif event.data == b"buy_goat":
        # Получаем текущий баланс пользователя из базы данных
        balance = get_balance_from_database(sender_id)

        # Проверяем, хватает ли у пользователя денег на покупку козы
        if balance >= 650:
            # Если хватает, то списываем стоимость козы с баланса пользователя и добавляем ему козу
            update_user_balance(sender_id, balance - 650)
            update_user_goats(sender_id, get_goats_from_database(sender_id) + 1)
            await event.answer("Вы купили козу!")
        else:
            await event.answer("У вас недостаточно монет для покупки козы")

    # Обработчик кнопки "Вернуться в главное меню"
    elif event.data == b"menub":
        await menu_handler(event)
        return

    # Обновляем сообщение с клавиатурой магазина после покупки
    #await shop_handler(event)

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    sender_id = event.sender_id
    username = get_username_from_database(sender_id)
    if not username:
        response = "👋🏻Привет!\n\n ⚠️/help"
        await event.respond(response)
        return
    balance = get_balance_from_database(sender_id)
    response = f"👋🏻Привет, @{username}!\n\n⚠️/help"
    await event.respond(response)

@bot.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
     response = (
        f"👋🏻Привет! Я помогу тебе с командами: \n\n"
        f"💀/start - ты уже жмякал, она нужна для старта(удивительно)\n\n"
        f"⚠️/help - помощь по командам\n\n"
        f"🕋/menu - меню\n\n"
        f"🏬/shop - магазин\n\n"
        f"🛍/sell - продать молочко и яйца\n\n"
        f"🌽/profile - профиль\n\n\n"
        f"Приятного времяпровождения!"
    )
     await event.respond(response)

@bot.on(events.NewMessage(pattern='/menu'))
async def menu_handler(event):
    user_id = event.sender_id
    menu_buttons = [
        Button.inline('Профиль', b'profile_b'),
        Button.inline('Магазин', b'shop_b'),
        Button.inline('Продать', b'sell_b'),
        Button.inline('Квесты', b'quest_b'),
        Button.inline('Локации', b'locations_b')
    ]
    response = 'Меню\n\nЭто поле нужно для мобильности! Тут ты можешь быстрой перейти в свой профиль или магазин.\n\nУдачи, фермер😊!'
    await event.respond(response, buttons=menu_buttons)


async def button_handler(event, handler_function):
    response = await handler_function(event)
    if response:
        menu_buttons = [
            Button.inline('Магазин', b'shop_b'),
            Button.inline('Продать', b'sell_b')
        ]
        await event.respond(response, buttons=menu_buttons)
    else:
        pass
        #await event.respond(Произошла ошибка при обработке вашего запроса)


@bot.on(events.CallbackQuery(pattern=b'profile_b'))
async def profile_button_handler(event):
    await button_handler(event, profile_handler)


@bot.on(events.CallbackQuery(pattern=b'shop_b'))
async def shop_button_handler(event):
    await button_handler(event, shop_handler)


@bot.on(events.CallbackQuery(pattern=b'sell_b'))
async def sell_button_handler(event):
    await button_handler(event, sell_handler)


@bot.on(events.CallbackQuery(pattern=b'quest_b'))
async def quest_button_handler(event):
    await button_handler(event, quests_handler)


@bot.on(events.CallbackQuery(pattern=b'locations_b'))
async def locations_button_handler(event):
    await button_handler(event, locations_handler) 

@bot.on(events.NewMessage(pattern='/sell'))
async def sell_handler(event):
    # Получаем id пользователя, который отправил запрос
    user_id = event.sender_id

    # Отправляем пользователю кнопки для выбора
    sell_buttons = [
        Button.inline('🥚', b'sell_egg'),
        Button.inline('🥛', b'sell_milk'),
        Button.inline('🥩', b'sell_meat'),
        Button.inline('🐟', b'sell_fish')
    ]
    await event.respond('👨‍🌾Что бы вы хотели продать?\n\n 📊Текущий курс:\n\n🥚 - 0.5$\n🥛 - 1$\n🥩 - 1$\n🐟 - 0.3$\n\n⚠️Продается сразу все!!', buttons=sell_buttons)

@bot.on(events.CallbackQuery(pattern=b'sell_egg'))
async def sell_eggs_handler(event):
    # Получаем id пользователя, который отправил запрос
    user_id = event.sender_id

    # Получаем количество яиц, которое нужно продать
    am = get_egg_from_database(user_id)

    # Вызываем функцию sell_egg
    res = sell_egg(user_id, am)

    # Проверяем, что callback_query.data соответствует 'sell_eggs'
    if event.data.decode() == 'sell_egg':
        # Отправляем ответ пользователю с результатом выполнения функции
        await event.respond(res)

@bot.on(events.CallbackQuery(pattern=b'sell_meat'))
async def sell_meat_handler(event):
    # Получаем id пользователя, который отправил запрос
    user_id = event.sender_id

    # Получаем количество яиц, которое нужно продать
    am = get_meat_from_database(user_id)

    # Вызываем функцию sell_egg
    res = sell_meat(user_id, am)

    # Проверяем, что callback_query.data соответствует 'sell_eggs'
    if event.data.decode() == 'sell_meat':
        # Отправляем ответ пользователю с результатом выполнения функции
        await event.respond(res)

@bot.on(events.CallbackQuery(pattern=b'sell_milk'))
async def sell_milk_handler(event):
    # Получаем id пользователя, который отправил запрос
    user_id = event.sender_id

    # Получаем количество молока, которое нужно продать
    amount = get_milk_from_database(user_id)

    # Вызываем функцию sell_milk
    result = sell_milk(user_id, amount)

    # Проверяем, что callback_query.data соответствует 'sell_milk'
    if event.data.decode() == 'sell_milk':
        # Отправляем ответ пользователю с результатом выполнения функции
        await event.respond(result)

@bot.on(events.CallbackQuery(pattern=b'sell_fish'))
async def sell_fish_handler(event):
    # Получаем id пользователя, который отправил запрос
    user_id = event.sender_id

    # Получаем количество молока, которое нужно продать
    amount = get_fish_from_database(user_id)

    # Вызываем функцию sell_milk
    result = sell_fish(user_id, amount)

    if event.data.decode() == 'sell_fish':
        # Отправляем ответ пользователю с результатом выполнения функции
        await event.respond(result)

@bot.on(events.NewMessage())
async def normal_handler(event):
    sender_id = event.sender_id
    user = await event.get_sender()
    exp = get_exp_from_database(sender_id)
    username = user.username if user.username is not None else user.first_name + ' ' + user.last_name
    add_user_to_database(sender_id, username)

    # Получаем текущий баланс пользователя из базы данных
    balance = get_balance_from_database(sender_id)

    # Обновляем баланс текущего пользователя
    update_user_balance(sender_id, balance)
    update_level(sender_id, exp)

def main():
    #update_thread = threading.Thread(target=update_db)
    #update_thread.start()
    #если надо изменить колонки null на 0, редач эту функцию
    meat_thread = threading.Thread(target=farm_meat)
    meat_thread.start()
    egg_thread = threading.Thread(target=farm_egg)
    egg_thread.start()
    milk_thread = threading.Thread(target=farm_milk)  # создаем новый поток для функции farm_milk
    milk_thread.start()  # запускаем поток с функцией
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()