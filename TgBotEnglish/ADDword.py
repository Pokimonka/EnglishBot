from DBCreator import session
from def_words import default_words
from model import  User, WordsPair, UsersWordsPair

def get_user_pair_id(user_id, rus, eng):
    pid = (session.query(WordsPair.id).select_from(WordsPair)
           .filter(WordsPair.russian_word == rus)
           .filter(WordsPair.english_word == eng)
           .filter(WordsPair.default_word == False)).all()
    p_id = pid[0][0]
    uid = (session.query(User.id).select_from(User)
           .filter(User.user_id == user_id)).all()
    us_id = uid[0][0]
    return [p_id, us_id]

def check_and_add_words(rus, eng):
    word = (session.query(WordsPair.id).select_from(WordsPair)
            .filter(WordsPair.russian_word == rus)
            .filter(WordsPair.english_word == eng)
            .filter(WordsPair.default_word == False)).all()
    if not word:
        new_pair = WordsPair(russian_word = rus, english_word = eng, default_word = False)
        session.add(new_pair)
        session.commit()

def set_new_pair_words(user_id, rus, eng):
    check_and_add_words(rus, eng)
    pair_user = get_user_pair_id(user_id, rus, eng)
    uwid = (session.query(UsersWordsPair.id).select_from(UsersWordsPair)
           .filter(UsersWordsPair.user_id == pair_user[1]).filter(UsersWordsPair.pair_id == pair_user[0])).all()
    if uwid:
        return 'Это слово уже добавлено'
    else:
        new_u_p = UsersWordsPair(user_id=pair_user[1], pair_id=pair_user[0])
        session.add(new_u_p)
        session.commit()
        return ''

def set_default_words(words):
    for eng, rus in words.items():
        new_pair = WordsPair(russian_word = rus, english_word = eng, default_word = True)
        session.add(new_pair)
        session.commit()
