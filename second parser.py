import requests
import json
import time
import os
import pandas


def getPage(text, page, area):    #Запрашивает одну страницу с данными по фильтрам
    params = {
        'text': text,           # текст запроса
        #'area': area,          # Поиск в зоне
        'page': page,           # Номер страницы
        'per_page': 100,        # Кол-во вакансий на 1 странице

    }
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.json()
    req.close()
    return data                         # Возвращает json файл с вакансиями одной страницы


def Sbor_str(page, text, derectory):    # запускает функцию getPage  в цикле для запроса множества страниц с карточками
    for i in range(page):               #делает запрос на 'page' страниц поочередно перебирая их range(n) где n - число нужных страниц
        try:
            data = getPage(text, i, 1)
            time.sleep(1.5)
            with open(f'{derectory}/result{i}.json', 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file)           #Сохраняет в выбранную директорию страницы поиска (20 файлов по 100 вакансий)
            print(f"страница {i+1} загруженна")
        except:
            print('я сохранил все которые нашел, их оказалось меньше чем ты предполагал ;)')

def Zapros_kartochek(derectory, derectory_vacancy):           # пробегается по страницам с вакансиями и сохряняет на pc сами вакансии (1 файл- 1 карточка вакансии)
    i = 0
    for fl in os.listdir(derectory):
        with open(f'{derectory}/{fl}', encoding='utf-8') as file:
            jsonText = file.read()
            jsonObj = json.loads(jsonText)
            for v in jsonObj['items']:
                req = requests.get(v['url'])
                data = req.json()
                req.close()
                i += 1
                with open(f'{derectory_vacancy}/vacancy{i}.json', 'w', encoding="utf-8") as json_file:
                    json.dump(data, json_file)
                time.sleep(0.25)
                print(f'все идет по плану, сохранен файл : {i}')


class SkillCount:     #Класс для подсчета скилов
    def __init__(self):
        self.skills = {}

    def clear_slills(self):  # очистить список скилов
        self.skills = {}

    def __call__(self, x):
        for i in x:
            if i not in self.skills:   # Если скила нет в списке то он добавляется со значением 1
                self.skills[i] = 1
            else:
                self.skills[i] = self.skills.get(i) + 1     # Если скил есть в списке то он увеличивает значение на 1

    def __str__(self):
        lst = tuple([x for x in self.skills.items()])         #Создаем кортеж из нашего словаря
        ret = [':'.join(list(map(str, x)))+'\n' for x in sorted(lst, key=lambda x: x[1], reverse=True)]   #преобразуем в текст и сортируем по убыванию значения
        return f"{''.join(ret)}"    #сращиваем все в одну строку и возвращаем чтобы выглядело не в строчку



def make_doc(derectory_vacancy):    # Проходит по всем карточкам собирая в списки интересеющую нас информацию из карточек для дальнейшей записи в exel файл или посчета скилов
    skill_list = SkillCount()  # Обьект посчетов определенных скилов
    data = []
    for art in os.listdir(derectory_vacancy):
        with open(f"{derectory_vacancy}/{art}", "r", encoding="utf-8") as file:
            jsonObj = json.loads(file.read())
            dic_attr = {'name': ['name'], 'salary_from': ['salary', 'from'], 'salary_to': ['salary', 'to'],
                        'currency': ['salary', 'currency'], 'experience': ['experience', 'name'], 'schedule': ['schedule','name'],
                        'alternate_url': ['alternate_url']
                        }      #ключи храним в списках для универсализации. в случае когда нужно добраться до более глубокого значения
            for key, value in dic_attr.items():
                if len(value) == 1:
                    dic_attr[key] = jsonObj.get(*value, None)
                if len(value) ==2:
                    try:
                        dic_attr[key] = jsonObj[value[0]].get(value[1], None)
                    except:
                        dic_attr[key] = None
            try:
                key_skills = [x['name'] for x in jsonObj['key_skills']]
            except:
                key_skills = [None]
            skill_list(key_skills)      #Каждую итерацию сюда поступает список скилов
            data.append([dic_attr['name'], dic_attr['salary_from'], dic_attr['salary_to'], dic_attr['currency'],
                         dic_attr['experience'], dic_attr['schedule'], dic_attr['alternate_url'] ])

    print(skill_list)
    return data

page = 1                                          # сколько страниц запрашиваем
text = 'Python'                                   # текст поиска как в поиске hh
derectory = './dict_hh'                           # Дерриктория куда будут сохраняться страницы с карточками
derectory_vacancy = './vacancy_hh'                # дерриктория куда будут сохраняться карточки

Sbor_str(page, text, derectory)                   #собирает список страниц на котором представленна урезанная карточка по профессии
Zapros_kartochek(derectory, derectory_vacancy)    # Выполняет функцию по сбору самих карточек и сохраняет их в отдельные файлы

header = ['name', 'salary_from', 'salary_to', 'currency', 'experience', 'schedule', 'alternate_url']
data = make_doc(derectory_vacancy)
df = pandas.DataFrame(data, columns=header)
df.to_csv('C:/Users/user/Desktop/Auto_Parser/data1.csv', sep=';', encoding='utf8')
