from sqlalchemy import or_
from DBCreator import session
from model import WordsPair, User, UsersWordsPair


def delete_user_word(user_id, word):
    pid = (session.query(WordsPair.id).select_from(WordsPair)
           .filter(WordsPair.default_word == False)
           .filter(or_(WordsPair.english_word == word.lower(), WordsPair.russian_word == word.lower()))
           ).all()
    if pid:
        p_id = pid[0][0]
        uid = (session.query(User.id).select_from(User)
               .filter(User.user_id == user_id)).all()
        us_id = uid[0][0]
        uw_id = (session.query(UsersWordsPair.id).select_from(UsersWordsPair)
               .filter(UsersWordsPair.pair_id == p_id)
               .filter(UsersWordsPair.user_id == us_id)).all()
        if uw_id:
            iduw = uw_id[0][0]
            UWP = session.query(UsersWordsPair).filter(UsersWordsPair.id == iduw).first()
            session.delete(UWP)
            session.commit()
            WP = session.query(WordsPair).filter(WordsPair.id == p_id).first()
            session.delete(WP)
            session.commit()
            return 'Слово успешно удалено из твоей коллекции'
        else:
            return 'В твоей коллекции нет такого слова'
    else:
        return 'Ты не можешь удалить это слово'