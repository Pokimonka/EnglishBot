from db_creator import session
from model import User


def check_user(user_id):
    uid = (session.query(User.id).select_from(User)
           .filter(User.user_id == user_id)).all()
    if uid:
        return True
    else:
        return False

def set_new_user(user_id):
    new_user = User(user_id=user_id)
    session.add(new_user)
    session.commit()