# TODO Перевод в обратную сторону.
# def get_translate_to_russian(eng_word):
#     result = (session.query(WordsPair.russian_word).select_from(WordsPair)
#               .filter(WordsPair.english_word == eng_word)
#               ).all()
#     return result[0][0]
#
# def get_all_eng_from_user(user_id):
#     result = (session.query(WordsPair.english_word).select_from(WordsPair)
#               .join(UsersWordsPair).filter(UsersWordsPair.pair_id == WordsPair.id)
#               .join(User).filter(User.id == UsersWordsPair.user_id)
#               .filter(User.user_id == user_id)
#               ).all()
#     res = []
#     for r in result:
#         res.append(r[0])
#     return res
#
#
# def get_all_rus_words_for_other(word):
#     result = (session.query(WordsPair.russian_word).select_from(WordsPair)
#               .filter(WordsPair.russian_word != word)
#               ).all()
#     res = []
#     for r in result:
#         res.append(r[0])
#     return res[:3]