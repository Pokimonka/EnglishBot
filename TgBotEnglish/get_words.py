import random

from db_creator import session
from model import WordsPair, UsersWordsPair, User


def get_all_eng_words_for_other(word):
    result = (session.query(WordsPair.english_word).select_from(WordsPair)
              .filter(WordsPair.english_word != word)
              ).all()
    res = []
    for r in result:
        res.append(r[0])
    random.shuffle(res)
    return res[:3]


def get_all_general_words():
    res = []
    result = (session.query(WordsPair.russian_word).select_from(WordsPair)
              .filter(WordsPair.default_word == True)).all()
    for r in result:
        res.append(r[0])
    return res

def get_all_rus_from_user(user_id):
    result = (session.query(WordsPair.russian_word).select_from(WordsPair)
              .join(UsersWordsPair).filter(UsersWordsPair.pair_id == WordsPair.id)
              .join(User).filter(User.id == UsersWordsPair.user_id)
              .filter(User.user_id == user_id)
              ).all()
    res = []
    for r in result:
        res.append(r[0])
    return res

def get_translate_to_english(rus_word):
    result = (session.query(WordsPair.english_word).select_from(WordsPair)
              .filter(WordsPair.russian_word == rus_word)
              ).all()
    return result[0][0]


def get_users_words(user_id):
    result = (session.query(WordsPair.russian_word, WordsPair.english_word).select_from(WordsPair)
              .join(UsersWordsPair).filter(UsersWordsPair.pair_id == WordsPair.id)
              .join(User).filter(User.id == UsersWordsPair.user_id)
              .filter(User.user_id == user_id)).all()
    words = []
    if result:
        for res in result:
            words.append(f'{res[0]} -> {res[1]}')
    line = '\n'.join(words)
    return line