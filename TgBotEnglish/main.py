import random

from telebot import StateMemoryStorage, TeleBot, types
from telebot.states import StatesGroup, State

from ADDword import set_default_words, set_new_pair_words
from DBCreator import session
from DeleteWords import delete_user_word
from GETwords import get_all_general_words, get_all_rus_from_user, get_translate_to_english, \
    get_all_eng_words_for_other, get_users_words
from SETuser import check_user, set_new_user
from def_words import default_words

print('Start telegram bot...')

class Command:
    LEARNING = 'Начать'
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'

class MyStates(StatesGroup):
    target_word = State()
    russian_word = State()
    another_words = State()

state_storage = StateMemoryStorage()
token_bot = ''
bot = TeleBot(token_bot, state_storage=state_storage)

def show_target(data):
    return f"{data['target_word']} -> {data['russian_word']}"

def show_hint(*lines):
    return '\n'.join(lines)

buttons = []
rusword = []
engword = []

def get_random_russian_word(user):
    def_words = get_all_general_words()
    russian_words_collection = get_all_rus_from_user(user)
    random.shuffle(def_words)
    if russian_words_collection:
        random.shuffle(russian_words_collection)
        result = [russian_words_collection[0], def_words[0]]
        random.shuffle(result)
        return result[0]
    else:
        return def_words[0]

def set_start():
    buttons.clear()
    learning_btn = types.KeyboardButton(Command.LEARNING)
    return learning_btn

def set_buttons(target_word, other_words):
    buttons.clear()
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    other_words_buttons = [types.KeyboardButton(word) for word in other_words]
    buttons.extend(other_words_buttons)
    random.shuffle(buttons)
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])
    return buttons

def set_command_buttons():
    buttons.clear()
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])
    return buttons

@bot.message_handler(commands=['cards', 'start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    if not check_user(message.from_user.id):
        set_new_user(message.from_user.id)
    markup.add(set_start())
    bot.send_message(message.chat.id, 'Привет, здесь ты можешь попрактиковаться в английском языке) \n'
                                      'Тренировки можешь проходить в удобном для себя темпе. \n'
                                      'Можешь использовать меня как конструктор, добавляй слова, которые хочешь запомнить.\n'
                                      'Для этого воспрользуйся инструментами:\n'
                                      '- добавить слово ➕,\n'
                                      '- удалить слово 🔙.\n'
                                      'Тебе будут попадаться как твои слова, так и слова из общей базы.\n'
                                      'Ну что, начнём ⬇️', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == Command.LEARNING)
def start_learning(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    russian_word = get_random_russian_word(message.from_user.id)
    target_word = get_translate_to_english(russian_word)
    other_words = get_all_eng_words_for_other(target_word)
    markup.add(*set_buttons(target_word, other_words))
    bot.send_message(message.chat.id, f'Угадай слово {russian_word}', reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['russian_word'] = russian_word
        data['other_words'] = other_words


@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    start_learning(message)

@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    set_command_buttons()
    markup.add(*buttons)
    users_words = get_users_words(message.from_user.id)
    if not users_words:
        bot.send_message(message.chat.id, 'В твоей коллекции ещё нет слов. Ты не можешь ничего удалить)'
                                          '\n Сначала добавьте слово')
    else:
        english_word = bot.send_message(message.chat.id,
                                        f'Введи слово, которое хочешь удалить \n Вот слова из твоей коллекции: \n {users_words}')
        bot.register_next_step_handler(english_word, delete_input_word)

def delete_input_word(message):
    hint = delete_user_word(message.from_user.id, message.text)
    bot.send_message(message.chat.id, hint)
    users_words = get_users_words(message.from_user.id)
    if not users_words:
        bot.send_message(message.chat.id, f'В твоей коллекции нет слов')
    else:
        bot.send_message(message.chat.id, f'Вот слова из твоей коллекции: \n {users_words}')


@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_my_word(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    set_command_buttons()
    markup.add(*buttons)
    rus = bot.send_message(message.chat.id, 'Введи слово на русском')
    bot.register_next_step_handler(rus, add_rus_word)

def add_rus_word(message):
    rusword.clear()
    rusword.append(message.text)
    eng = bot.send_message(message.chat.id, 'Введи слово на английском')
    bot.register_next_step_handler(eng, add_eng_word)

def add_eng_word(message):
    engword.clear()
    engword.append(message.text)
    result = set_new_pair_words(message.from_user.id, rusword[0].lower(), engword[0].lower())
    if result:
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, 'Слово добавлено в коллекцию')
    users_words = get_users_words(message.from_user.id)
    bot.send_message(message.chat.id, f'Слова в твоей коллекции: \n {users_words}')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    m_text = message.text
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']
        if m_text == target_word:
            hint = show_target(data)
            hint_text = ['Отлично!', hint]
            set_command_buttons()
            hint = show_hint(*hint_text)
        else:
            for btn in buttons:
                if btn.text == m_text:
                    btn.text = m_text + '❌'
                    break
            hint = show_hint("Допущена ошибка!",
                                 f"Попробуй ещё раз вспомнить слово 🇷🇺{data['russian_word']}")
    markup.add(*buttons)
    bot.send_message(message.chat.id, hint, reply_markup=markup)


if __name__ == '__main__':
    set_default_words(default_words)
    bot.polling()
    session.close()


























