import requests

def getPage(page, area):
    params = {
        'text': 'Python',  # текст запроса
        'area': area,         # Поиск в зоне
        'page': page,         # Номер страницы
        'per_page': 100,     # Кол-во вакансий на 1 странице

    }
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    return data

a = getPage(1,1)
b = getPage(1,2)
print(a)
ыаыва
# def request():
#     url = 'https://api.hh.ru/?text=Python'
#     data = requests.get(url).json()
#     return data
# resultat = request()
# print(resultat)



