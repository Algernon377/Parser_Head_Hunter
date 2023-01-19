import requests
import json
import time
import os
import pandas


def getPage(page, area): #Запрашивает одну страницу с данными по фильтрам
    params = {
        'text': 'Python',  # текст запроса
        # 'area': area,         # Поиск в зоне
        'page': page,         # Номер страницы
        'per_page': 100,     # Кол-во вакансий на 1 странице

    }
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.json()
    req.close()
    return data          # Возвращает json файл с вакансиями одной страницы


def Sbor_str():
    for i in range(20):           #делает запрос на 20 страниц поочередно перебирая их
        data = getPage(i, 1)
        time.sleep(3)
        with open(f'dict_hh/result{i}.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file)           #Сохраняет в выбранную директорию страницы поиска (20 файлов по 100 вакансий)
        print(f"страница {i+1} загруженна")
# Sbor_str() #Запуск двух  верхних функций
lst_api = []
def Zapros_kartochek():
    i = 0
    for fl in os.listdir('./dict_hh'):
        with open(f'./dict_hh/{fl}', encoding='utf-8') as file:
            jsonText = file.read()
            jsonObj = json.loads(jsonText)
            for v in jsonObj['items']:
                req = requests.get(v['url'])
                data = req.json()
                req.close()
                i+=1
                with open(f'./vacancy_hh/vacancy{i}.json', 'w', encoding="utf-8") as json_file:
                    json.dump(data, json_file)
                time.sleep(0.25)
                print(f'все идет по плану, сохранен файл : {i}')
# Zapros_kartochek()    # Выполняет функцию по сбору самих карточек и сохраняет их в отдельные файлы


data = []
header = ['name', 'salary_from', 'salary_to', 'currency' ,'experience', 'schedule', 'schedule']+[0]*30
for art in os.listdir('./vacancy_hh'):
    with open(f"C:/Users/user/Desktop/Auto_Parser/vacancy_hh/{art}", "r", encoding="utf-8") as file:
        jsonObj = json.loads(file.read())
        try:
            name = jsonObj['name']
        except:
            name = None
        try:
            salary_from = jsonObj['salary']['from']
        except:
            salary_from = None
        try:
            salary_to = jsonObj['salary']['to']
        except:
            salary_to = None
        try:
            currency = jsonObj['salary']['currency']
        except:
            currency = None
        try:
            experience = jsonObj['experience']['name']
        except:
            experience = None

        try:
            schedule = jsonObj['schedule']['name']
        except:
            schedule = None
        try:
            key_skills = [x['name'] for x in jsonObj['key_skills']]
        except:
            key_skills = [None]
        data.append([name, salary_from, salary_to, currency ,experience, schedule, schedule]+key_skills)



df = pandas.DataFrame(data, columns=header)
df.to_csv('C:/Users/user/Desktop/Auto_Parser/data1.csv', sep=';', encoding='utf8')
