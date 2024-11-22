import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.BigInteger, unique=True, nullable=False)

    def __str__(self):
        return f'User {self.id}: {self.user_id}'

class WordsPair(Base):
    __tablename__ = "words_pair"

    id = sq.Column(sq.Integer, primary_key=True)
    russian_word = sq.Column(sq.String(length=40), nullable=False)
    english_word = sq.Column(sq.String(length=40), nullable=False)
    default_word = sq.Column(sq.Boolean, nullable=False)

    def __str__(self):
        return f'Pair {self.russian_word}: {self.english_word}'


class UsersWordsPair(Base):
    __tablename__ = "users_words_pair"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)
    pair_id = sq.Column(sq.Integer, sq.ForeignKey("words_pair.id"), nullable=False)

    user = relationship(User, backref="users_words_pair")
    pair = relationship(WordsPair, backref="users_words_pair")

    def __str__(self):
        return f'UsersWords_pair {self.id}: ({self.user_id}, {self.pair_id})'




def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)