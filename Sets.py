import io
import json
from difflib import get_close_matches

print('=' * 10,"- Словарь сетов gamepe.me v-1.0, by @azfdagg -",'=' * 10,)
print('=' * 10,"! Сеты с минусом работают только на 1.18+ !",'=' * 10,)
print("""
""")
help ="""
h - Вывод справки
q - Выход
s - Вывод всего словаря
"""

data = json.load(open("data.json",'r',encoding='utf-8'))
data_json = io.open("data.json", 'r', encoding='utf-8').read()

def retrive_definition(word):
    word = word.lower()

    if word in data:
        return data[word]
    elif word.title() in data:
        return data[word.title()]
    elif word.upper() in data:
        return data[word.upper()]
    elif len(get_close_matches(word, data.keys())) > 0:
        action = input("Возможно вы имели ввиду %s ? [y или n]: " % get_close_matches(word, data.keys())[0])
        if (action == "y"):
            return data[get_close_matches(word, data.keys())[0]]
        elif (action == "n"):
            return ("Этого слова не существует")
        else:
            return ("Мы не поняли Вашего запроса, извиняемся.")


word_user = ""
while word_user != "q":
    word_user = input("Введите слово или команду (h -> справка): ")
    output = retrive_definition(word_user)
    if type(output) == list:
        for item in output:
            print("-", item)
    elif word_user == "help":
        print(help)
    elif word_user == "s":
        print(data_json)
    else:
       print("- Неверная команда или блок -", output)
#    if choice == "s":
#      print(data_json)
#    elif choice == "h":
#        print(help)


