from config import TOKEN
import telebot
from telebot.types import Message, ReplyKeyboardMarkup as Rkm, InlineKeyboardMarkup as Ikm, InlineKeyboardButton as Ikb,\
    CallbackQuery
import databases

bot = telebot.TeleBot(TOKEN)
users = {}

@bot.message_handler(commands=['start'])
def start(m: Message):
    bot.send_message(m.chat.id, f"привет {m.from_user.username}")


@bot.message_handler(commands=['help'])
def help_bot(m: Message):
    kb = Rkm(resize_keyboard=True, one_time_keyboard=True)
    kb.row('список команд', 'контакты')
    kb.row('справка')
    bot.send_message(m.chat.id, "чем я могу помочь?", reply_markup=kb)


@bot.message_handler(commands=['sign_up'])
def sign_up(m: Message):
    users[m.chat.id] = {}
    bot.send_message(m.chat.id, 'напиши юзернейм:')
    bot.register_next_step_handler(m,reg1)


@bot.message_handler(commands=['inline'])
def inline(m: Message):
    kb = Ikm()
    kb.row(Ikb(text='Google', url='google.com'), Ikb(text='Яндекс', url='yandex.ru'))
    kb.row(Ikb(text='ВКонтакте', url='vk.com'), Ikb(text='Telegram', url='telegram.org'))
    kb.row(Ikb(text='действие 1', callback_data='d1'))
    kb.row(Ikb(text='уведомление',callback_data='notice'))
    bot.send_message(m.chat.id, "выбери сайт:", reply_markup=kb)


@bot.message_handler(commands=['menu'])
def menu_bot(m: Message):
    kb = Rkm(resize_keyboard=True, one_time_keyboard=True)
    kb.row('отправить фото', 'дать описание питомцу')
    kb.row('указать место пропажи')
    bot.send_message(m.chat.id, 'что вы хотите сделать?', reply_markup=kb)


def reg1(m: Message):
    username = m.text
    users[m.chat.id]['username'] = username
    bot.send_message(m.chat.id,f'твой выбранный юзернейм - {username}, как тебя зовут?')
    bot.register_next_step_handler(m,reg2,username)


def reg2(m: Message,username):
    name = m.text
    users[m.chat.id]['name'] = name
    bot.send_message(m.chat.id,f'твое имя - {name}, username - {username}, сколько тебе лет?')
    bot.register_next_step_handler(m,reg3,name,username)


def reg3(m: Message,name,username):
    age = m.text
    users[m.chat.id]['age'] = age
    bot.send_message(m.chat.id,f'{username}, {name}: твой возраст-{age}, из какого ты города?')
    bot.register_next_step_handler(m, reg4)


def reg4(m: Message):
    city = m.text
    users[m.chat.id]['city'] = city
    bot.send_message(m.chat.id,f'твой город-{city}, из какой ты страны?')
    bot.register_next_step_handler(m, reg5)


def reg5(m: Message):
    country = m.text
    users[m.chat.id]['country'] = country
    bot.send_message(m.chat.id,f'проверь свои данные: {users[m.chat.id]}')
    databases.write_row(users,m.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def inline_handler(call: CallbackQuery ):
    print(call.data)
    if call.data == 'd1':
        bot.send_message(call.message.chat.id,'действие 1 работает')
        bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id)
    elif call.data == 'notice':
        bot.answer_callback_query(call.id,'это всплывающее уведомление',False)
        bot.send_message(call.message.chat.id,'уведомление получено')


@bot.message_handler(
    func=lambda m: m.text == 'указать место пропажи')  # lambda-синтаксис для создания анонимных функций
def set_location(m: Message):
    kb_loc = Rkm(resize_keyboard=True, one_time_keyboard=True)
    kb_loc.row('отправить геолокацию', 'ввести адрес вручную')
    bot.send_message(m.chat.id, "как вы хотите указать место пропажи?", reply_markup=kb_loc)


@bot.message_handler(func=lambda m: m.text == 'ввести адрес вручную')  # lambda-синтаксис для создания анонимных функций
def input_address(m: Message):
    bot.send_message(m.chat.id, "пожалуйста, введите адрес пропажи (например, ул. Пушкина, 10).")


# @bot.message_handler(func=lambda m: m.text != '' and m.chat.id == m.chat.id)  #обрабатываем текст после ввода адреса
# def confirm_address(m: Message):
#     address = m.text
#     bot.send_message(m.chat.id, f"адрес сохранён: {address}. спасибо!")

@bot.message_handler(content_types=['location'])
def handle_location(m: Message):  # функция создана для уточнения гео координат
    lat = m.location.latitude  # долгота
    lon = m.location.longitude  # широта
    bot.send_message(m.chat.id, f"место сохранено: {lat}, {lon}. спасибо!")


@bot.message_handler(func=lambda m: m.text == 'отправить фото')
def send_photo(m: Message):
    bot.send_message(m.chat.id, "пожалуйста, отправьте фото питомца.")


@bot.message_handler(func=lambda m: m.text == 'дать описание питомцу')
def describe_pet(m: Message):
    bot.send_message(m.chat.id, "пожалуйста, опишите питомца (порода, окрас, возраст, особые приметы).")


@bot.message_handler(content_types=['text'])
def text_handler(m: Message):
    print(m.text)
    msg = m.text.lower()
    if msg == 'привет':
        bot.send_message(m.chat.id, 'о привет!')
    elif 'hello' in msg:
        bot.reply_to(m, 'I see your hello😎')
    elif msg == 'список команд':
        bot.send_message(m.chat.id, f"список команд:\n\n/start - в начало\n/help - помощь")
    elif msg == 'справка':
        bot.send_message(m.chat.id, 'здесь будет справка')
    elif msg == 'контакты':
        bot.send_message(m.chat.id, 'контакты для связи: тел:+79128673662')
    elif msg == 'отправить геолокацию':
        bot.send_message(m.chat.id, 'отправьте свою текущую геолокацию')


bot.infinity_polling()
