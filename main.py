import telebot
import datetime
import os
from datetime import datetime
from telebot import types
import psycopg2 #БД
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cursor = conn.cursor()
dict = None
dict1 = None
dict2 = None
user = None
@bot.message_handler(commands=['start']) # Команда старт
def start_command(message):
    user_id = message.from_user.id
    global user
    user = user_id
    cursor.execute(f'SELECT "User_Id" FROM "Users" WHERE "User_Id" = {user_id}')
    result = cursor.fetchall()
    if  len(result) == 0:
        print('Есть')
        cursor.execute(f'INSERT INTO "Users" ("User_Id", "User_Balans") VALUES (%s,%s);',(user_id,0))
        cursor.execute(f'INSERT INTO "Basket" ("User_Id") VALUES(%s);',(user_id,))
        conn.commit()
    
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    item_kalen = types.InlineKeyboardButton(text = 'Магазин 🏪', callback_data = 'shop')
    item_racion = types.InlineKeyboardButton(text = 'Личный кабинет 💼', callback_data = 'lc')
    item_mesta = types.InlineKeyboardButton(text = 'Поддержка 💬', callback_data = 'support')
    markup_inline.add(item_kalen, item_racion, item_mesta)
    file = open(r'G:\Diplom\Secret Shop\Bot\\MainMenu.png','rb')
    bot.send_photo(message.chat.id,file,caption=f'Для использования магазина <i>Secret Shop</i> пользуйтесь кнопками снизу' , parse_mode='html',reply_markup=markup_inline ,timeout=2000)
@bot.callback_query_handler(func = lambda call: call.data == 'menu')#Меню
def answer(call):
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    item_kalen = types.InlineKeyboardButton(text = 'Магазин 🏪', callback_data = 'shop')
    item_racion = types.InlineKeyboardButton(text = 'Личный кабинет 💼', callback_data = 'lc')
    item_mesta = types.InlineKeyboardButton(text = 'Поддержка 💬', callback_data = 'support')

    markup_inline.add(item_kalen, item_racion, item_mesta)  
    file = open(r'G:\Diplom\Secret Shop\Bot\\MainMenu.png','rb')
    bot.send_photo(call.message.chat.id,file,caption=f'Для использования магазина <i>Secret Shop</i> пользуйтесь кнопками снизу',parse_mode='html',reply_markup=markup_inline)
@bot.callback_query_handler(func = lambda call: call.data == 'lc' or call.data == 'shop' or call.data == 'support') 
def answer(call):
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    user_id = call.from_user.id
    print(call.message.message_id)
    
    global user
    user = user_id
    if call.data == 'lc':#Личный кабинет
        markup_inline = types.InlineKeyboardMarkup(row_width=2)
        
        cursor.execute(f'SELECT "User_Id" , "User_Balans" FROM "Users" WHERE "User_Id" = {user_id}')
        result = cursor.fetchall()
        item_shop_history = types.InlineKeyboardButton(text='История заказов📜', callback_data = 'history')
        item_use_promo = types.InlineKeyboardButton(text='Активировать промокод🎟️', callback_data = 'use_promo') 
        item_back = types.InlineKeyboardButton(text='В меню⬅️', callback_data = 'menu')
        markup_inline.add(item_shop_history,item_use_promo,item_back)
        file = open(r'G:\Diplom\Secret Shop\Bot\\UserCabinet.png','rb')
        bot.send_photo(call.message.chat.id,file,caption=f'😊Спасибо за то, что вы с нами!😊\nЗдравствуйте:{call.from_user.username}\n🎫Ваш ID:{result[0][0]}🎫\n💵На вашем балансе:{result[0][1]} ₽💵',parse_mode='html',reply_markup=markup_inline)
        
        
    elif call.data == 'shop':#Магазин
        markup_inline = types.InlineKeyboardMarkup(row_width=2)
        cursor.execute(f'SELECT "Categories_Id", "Categories_Name" FROM "Categories"')
        result = cursor.fetchall()
        data = []
        for resul in result:
            data.append(resul[1])
            
        for test in data:
            markup_inline.add(types.InlineKeyboardButton(text=test,callback_data=test+'_category'))
        item1 = types.InlineKeyboardButton(text='В меню⬅️',callback_data='menu')
        item2 = types.InlineKeyboardButton(text='Корзина',callback_data='basket')
        markup_inline.add(item1,item2)
        file = open(r'G:\Diplom\Secret Shop\Bot\\Shop.png','rb')
        bot.send_photo(call.message.chat.id,file,caption=f'Добро пожаловать магазин, выбирай все что угодно!',parse_mode='html',reply_markup=markup_inline)
        
    elif call.data == 'support':
        markup_inline = types.InlineKeyboardMarkup(row_width=2)
        bot.send_message(call.message.chat.id, 'Заглушка для общей инфы')
    
    cursor.execute(f'SELECT "Categories_Id", "Categories_Name" FROM "Categories"')
    result = cursor.fetchall()
    data = []
    for resul in result:
        data.append(resul[1])

def check_data_categories(test, data):#Проверка call_back
    return any(map(lambda x: test == x+'_category', data))

@bot.callback_query_handler(func = lambda call:check_data_categories(call.data, data) ) #Категории
def answer(call):
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    text = call.data
    text = "'"+'_'.join(text.split('_')[:-1])+"'"
    global dict 
    dict = text
    
    cursor.execute(f'SELECT "Categories_Id" FROM "Categories" WHERE "Categories_Name" = {text}')
    result = cursor.fetchone()
    cursor.execute(f'SELECT "Product_Categories_Name","Categories_Id" FROM "Product_Categories" WHERE "Categories_Id" = {result[0]}')
    result_2 = cursor.fetchall()
    dat = []
    num = 0
    while num != len(result_2):
        for res in result_2[num]:
            dat.append(res)
        markup_inline.add(types.InlineKeyboardButton(text=dat[0],callback_data=dat[0]+'_'+str(dat[1])))
        num+=1
        dat.clear()
    item1 = types.InlineKeyboardButton(text='В меню⬅️',callback_data='menu')
    item2 = types.InlineKeyboardButton(text='Назад', callback_data='shop')
    item3 = types.InlineKeyboardButton(text='Корзина',callback_data='basket')
    markup_inline.add(item1,item2,item3)
    file = open(r'G:\Diplom\Secret Shop\Bot\\Shop.png','rb')
    bot.send_photo(call.message.chat.id,file,caption=f'Вы видите категории деталей для {text}',parse_mode='html',reply_markup=markup_inline)

def check_data_subcategories(test):#Проверка call_back
    if dict == None:
        return None
    cursor.execute(f'SELECT "Categories_Id" FROM "Categories" WHERE "Categories_Name" = {dict}')
    result = cursor.fetchone()
    
    cursor.execute(f'SELECT "Product_Categories_Name","Product_Categories_Id" FROM "Product_Categories" WHERE "Categories_Id" = {result[0]}')
    result_2 = cursor.fetchall()
    for te in result_2:
        if test == te[0]+"_"+str(te[1]): 
            return True

@bot.callback_query_handler(func = lambda call:check_data_subcategories(call.data))#Подкатегории
def answer(call):
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    global dict1
    text = call.data
    print(text)
    text = text.split("_")
    print(text)
    dict1 = int(text[1])
    cursor.execute(f'SELECT "Product_Categories_Image" FROM "Product_Categories" WHERE "Product_Categories_Id" = {int(text[1])}')
    resultat = cursor.fetchone()
    cursor.execute(f'SELECT "Product_Id","Product_Name" FROM "Product" WHERE "Product_Categories_Id" = {int(text[1])}')
    result = cursor.fetchall()
    print(result)
    for res in result:
        markup_inline.add(types.InlineKeyboardButton(text = res[1],callback_data=str(res[0])+'_product'))
    item1 = types.InlineKeyboardButton(text='В меню⬅️',callback_data='menu')
    item2 = types.InlineKeyboardButton(text='Назад', callback_data='shop')
    item3 = types.InlineKeyboardButton(text='Корзина',callback_data='basket')
    markup_inline.add(item1,item2,item3)
    file = open(rf'G:\Diplom\Secret Shop\Bot\{resultat[0]}','rb')
    bot.send_photo(call.message.chat.id,file,caption=f'Присутствующий на складе товар:',parse_mode='html',reply_markup=markup_inline)

def check_data_tovar(test):#Проверка call_back
    if dict1 == None:
        return None
    cursor.execute(f'SELECT "Product_Id","Product_Name" FROM "Product" WHERE "Product_Categories_Id" = {dict1}')
    result = cursor.fetchall()
    for te in result:
        if test == str(te[0])+'_product':
            return True

@bot.callback_query_handler(func = lambda call:check_data_tovar(call.data)) #Товар
def answer(call):
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    text = call.data
    text = text.split("_")
    global dict2
    dict2 = int(text[0]) 
    cursor.execute(f'SELECT "Product_Name","Product_Price","Product_Text" FROM "Product" WHERE "Product_Id" = {int(text[0])}')
    result = cursor.fetchone()
    item1 = types.InlineKeyboardButton(text='В меню⬅️',callback_data='menu')
    item2 = types.InlineKeyboardButton(text='Назад', callback_data='shop')
    item3 = types.InlineKeyboardButton(text='Добавить в корзину',callback_data='addbasket') 
    item4 = types.InlineKeyboardButton(text='Корзина',callback_data='basket')
    markup_inline.add(item1,item2,item3,item4)
    bot.send_message(call.message.chat.id , f'Название:{result[0]}\nЦена:{result[1]} ₽\nОписание:{result[2]}',parse_mode='html', reply_markup = markup_inline)


@bot.callback_query_handler(func= lambda call:call.data =='addbasket')#Добавление в корзину
def answer(call):  
    cursor.execute(f'SELECT "Product_Name","Product_Price","Product_Text" FROM "Product" WHERE "Product_Id" = {dict2}')
    result = cursor.fetchone()
    user_id = call.from_user.id
    cursor.execute(f'SELECT "Basket_Id" FROM "Basket" WHERE "User_Id" = {user_id}')
    result_basket = cursor.fetchone()
    cursor.execute(f'INSERT INTO "Basket_Content" ("Basket_Id","Product_Id","Product_Name","Product_Price") VALUES(%s,%s,%s,%s)',(result_basket[0],dict2,result[0],result[1]))
    conn.commit()
    bot.send_message(call.message.chat.id, 'Товар успешно добавлен!',parse_mode='html')
@bot.callback_query_handler(func = lambda call:call.data == 'basket')#Корзина
def answer(call):
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    user_id = call.from_user.id
    global user
    user = user_id
    cursor.execute(f'SELECT "Basket_Id" FROM "Basket" WHERE "User_Id" = {user_id}')
    result = cursor.fetchone()
    cursor.execute(f'SELECT "Basket_Content_Id","Product_Name","Product_Price" FROM "Basket_Content" WHERE "Basket_Id" = {result[0]}')
    result_2 = cursor.fetchall()
    if len(result_2) == 0:
        item1 = types.InlineKeyboardButton(text='В меню⬅️',callback_data='menu')
        item2 = types.InlineKeyboardButton(text='Назад', callback_data='shop')
        markup_inline.add(item1,item2)
        file = open(r'G:\Diplom\Secret Shop\Bot\\Basket.png','rb')
        bot.send_photo(call.message.chat.id,file,caption=f'Ваша корзина пуста',parse_mode='html',reply_markup=markup_inline)
    else:

        print(result_2)
        total_summ = 0
        for te in result_2:
            total_summ +=te[2]
            markup_inline.add(types.InlineKeyboardButton(text=te[1]+'-'+str(te[2])+'₽',callback_data=str(te[0])+'_basketitem'))
        item1 = types.InlineKeyboardButton(text='Оформить заказ',callback_data='zakaz')
        item2 = types.InlineKeyboardButton(text='Очистить корзину',callback_data='basketclear')
        item3 = types.InlineKeyboardButton(text='В меню⬅️',callback_data='menu')
        item4 = types.InlineKeyboardButton(text='Назад', callback_data='shop')
        markup_inline.add(item1,item2,item3,item4)
        file = open(r'G:\Diplom\Secret Shop\Bot\\Basket.png','rb')
        bot.send_photo(call.message.chat.id,file,caption=f'Для удаления товара из корзины нажмите по нему\nОбщая стоимость товара:{total_summ}₽',parse_mode='html',reply_markup=markup_inline)

def check_data(test):#Удаление товара
    cursor.execute(f'SELECT "Basket_Id" FROM "Basket" WHERE "User_Id" = {user}')
    result = cursor.fetchone()
    cursor.execute(f'SELECT "Basket_Content_Id","Product_Name","Product_Price" FROM "Basket_Content" WHERE "Basket_Id" = {result[0]}')
    result_2 = cursor.fetchall()
    for te in result_2:
        if test == str(te[0])+'_basketitem':
            return True


@bot.callback_query_handler(func=lambda call:check_data(call.data))#Удаление товара
def anser(call):
    test = call.data
    text = test.split("_")
    cursor.execute(f'DELETE FROM "Basket_Content" WHERE "Basket_Content_Id" = {text[0]}')
    conn.commit()
    

@bot.callback_query_handler(func = lambda call:call.data == 'basketclear')#Очистка корзины
def answer(call):
    user_id = call.from_user.id
    cursor.execute(f'SELECT "Basket_Id" FROM "Basket" WHERE "User_Id" = {user_id}')
    result = cursor.fetchone()
    cursor.execute(f'DELETE FROM "Basket_Content" WHERE "Basket_Id" = {result[0]}')
    conn.commit()
   

    bot.send_message(call.message.chat.id, 'Корзина успешно очищена!',parse_mode='html')

@bot.callback_query_handler(func = lambda call:call.data == 'zakaz')#Подтверждение заказа
def answer(call):
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(text='Да',callback_data='zakazNext')
    item2 = types.InlineKeyboardButton(text='Нет',callback_data='menu')
    markup_inline.add(item1,item2)
    bot.send_message(call.message.chat.id, 'Вы уверены, что хотите продолжить?',parse_mode='html',reply_markup=markup_inline)

@bot.callback_query_handler(func = lambda call:call.data == 'zakazNext')#Подтверждение заказа
def answer(call):
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    cursor.execute(f'SELECT "Basket_Id" FROM "Basket" WHERE "User_Id" = {user}')
    result = cursor.fetchone()
    cursor.execute(f'SELECT "Basket_Content_Id","Product_Name","Product_Price","Product_Id" FROM "Basket_Content" WHERE "Basket_Id" = {result[0]}')
    result_2 = cursor.fetchall()
    total_sum = 0
    for item in result_2:
        total_sum += int(item[2])
    cursor.execute(f'SELECT "User_Balans" FROM "Users" WHERE "User_Id" = {user}')
    result_3 = cursor.fetchone()
    if total_sum > int(result_3[0]):
        item1 = types.InlineKeyboardButton(text='В меню⬅️',callback_data='menu')
        markup_inline.add(item1)
        bot.send_message(call.message.chat.id, f'На вашем балансе недостаточно средств\nОбщая стоимость:{total_sum}₽\nНа вашем счету:{result_3[0]}₽\nВам нужно пополнить баланс на:{total_sum-result_3[0]}₽ чтобы совершить покупку',parse_mode='html',reply_markup=markup_inline)
    else:
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(f'UPDATE "Users" SET "User_Balans" = "User_Balans" - {total_sum} WHERE "User_Id" = {user}')
        conn.commit()
        cursor.execute(f'INSERT INTO "Order_Hystory" ("User_Id","Order_Hystory_Status","Order_Hystory_Date") VALUES(%s,%s,%s);',(user,'В обработке',time))
        conn.commit()
        cursor.execute(f'SELECT "Order_Hystory_Id" FROM "Order_Hystory" WHERE "User_Id" = {user} AND "Order_Hystory_Date" = {"'"+time+"'"}')
        result_4 = cursor.fetchone()
        for item in result_2:
            cursor.execute(f'INSERT INTO "Order_Content" ("Order_Hystory_Id","Product_Id","Product_Name","Product_Price") VALUES(%s,%s,%s,%s)',(result_4[0],item[3],item[1],item[2]))
            conn.commit()
            cursor.execute(f'SELECT "Basket_Id" FROM "Basket" WHERE "User_Id" = {user}')
            result = cursor.fetchone()
            cursor.execute(f'DELETE FROM "Basket_Content" WHERE "Basket_Id" = {result[0]}')
            conn.commit()

        item1 = types.InlineKeyboardButton(text='В меню⬅️',callback_data='menu')
        markup_inline.add(item1)
        bot.send_message(call.message.chat.id, 'Заказ успешно завершен!',parse_mode='html',reply_markup=markup_inline)

@bot.callback_query_handler(func = lambda call:call.data == 'history')#История заказов
def answer(call):
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    cursor.execute(f'SELECT "Order_Hystory_Id","Order_Hystory_Status","Order_Hystory_Date" FROM "Order_Hystory" WHERE "User_Id" = {user}')
    result = cursor.fetchall()
    for item in result:
        markup_inline.add(types.InlineKeyboardButton(text=str(item[2])+' '+item[1], callback_data = str(item[0])+'_order'))
        markup_inline.add(types.InlineKeyboardButton(text='Назад',callback_data='lc'))
    file = open(r'G:\Diplom\Secret Shop\Bot\\ShopHistory.png','rb')
    bot.send_photo(call.message.chat.id,file,caption=f'Ваши заказы:',parse_mode='html',reply_markup=markup_inline)

def checkorder_data(test):#call_back
    cursor.execute(f'SELECT "Order_Hystory_Id","Order_Hystory_Status","Order_Hystory_Date" FROM "Order_Hystory" WHERE "User_Id" = {user}')
    result = cursor.fetchall()
    for te in result:
        if test == str(te[0])+'_order':
            return True

@bot.callback_query_handler(func=lambda call:checkorder_data(call.data))#Содержимое заказа
def anser(call):
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    text = call.data
    text = text.split("_")
    cursor.execute(f'SELECT "Product_Name","Product_Price" FROM "Order_Content" WHERE "Order_Hystory_Id" = {text[0]}')
    result = cursor.fetchall()
    for te in result:
        markup_inline.add(types.InlineKeyboardButton(text=te[0]+'-'+str(te[1])+'₽',callback_data='nothing'))
    markup_inline.add(types.InlineKeyboardButton(text='Назад',callback_data='lc'))
    file = open(r'G:\Diplom\Secret Shop\Bot\\ShopHistory.png','rb')
    bot.send_photo(call.message.chat.id,file,caption=f'Содержимое заказа:',parse_mode='html',reply_markup=markup_inline)
        
@bot.callback_query_handler(func = lambda call: call.data == 'use_promo') #Использование промокода
def answer(call):
    msg = bot.send_message(call.message.chat.id, f'Пожалуйста введите промокод:', parse_mode='html')
    bot.register_next_step_handler(msg, promo_check)
    
def promo_check(message): #Функция проверки промокода
    promo  = "'" +str(message.text) + "'"
    promo1 = message.text
    cursor.execute(f'SELECT "Promo_Id","Promo_Text","Promo_Type","Promo_Count","Promo_Prize" FROM "Promo" WHERE "Promo_Text" = {promo}')
    promo_table = cursor.fetchall()
    user_id = message.from_user.id
    cursor.execute(f'SELECT "Used_Promo_Id","User_Id","Promo_Id","Used_Promo_Promo_Text","Used_Promo_Promo_Prizeo","Used_Promo_Using" FROM "Used_Promo" WHERE "User_Id" = {user_id}')
    promo_used_table = cursor.fetchall()
    check_promo_used_table = 0
    try:
        if len(promo_used_table) == 0:
            number = len(promo_used_table)
        else:
            number = len(promo_used_table)-1
        while number != -1:
            print(number)
            check = promo_used_table[number].count(promo1)
            print(check)
            if check == 1:
                print("Завершен")
                check_promo_used_table = 1
                break
            number = number - 1
            print("Нету")
    except:
        print("Нету")
    if len(promo_table) == 0:
        bot.send_message(message.chat.id, 'Данного промокода не существует')
    elif promo_table[0][3] == 0:
        bot.send_message(message.chat.id, 'Промокод недействителен')
    elif check_promo_used_table == 1:
        bot.send_message(message.chat.id,'Вы уже активировали этот промокод')
    else:
        cursor.execute(f'INSERT INTO "Used_Promo" ("User_Id", "Promo_Id","Used_Promo_Promo_Text","Used_Promo_Promo_Prizeo","Used_Promo_Using") VALUES (%s,%s,%s,%s,%s);',(user_id,promo_table[0][0],promo_table[0][1],promo_table[0][4],'True'))
        conn.commit()
        cursor.execute(f'SELECT "User_Id","User_Balans" FROM "Users" WHERE "User_Id" = {user_id}')
        user_ac = cursor.fetchall()
        cursor.execute(f'UPDATE "Users" SET "User_Balans" = %s WHERE "User_Id" = %s',(promo_table[0][4] + user_ac[0][1],user_id))
        conn.commit()
        cursor.execute(f'UPDATE "Promo" SET "Promo_Count" = %s WHERE "Promo_Id" = %s',(promo_table[0][3]-1,promo_table[0][0]))
        conn.commit()
        bot.send_message(message.chat.id, 'Промокод успешно активирован😊')
    pass

bot.infinity_polling(none_stop=True)