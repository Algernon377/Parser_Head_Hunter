# Auto_Parser
Создан из любопытства и для практики. Ну и конечно же чтобы посмотреть какие ключевые навыки на head hanter чаще всего встречаються. 

Предыстория: к концу 2022 года начал изучать Python и выучив синтаксиз и изучая ООП встал вопрос что же дальше учить. И решил посмотреть какие ключевые навыки встречаютсья чаще всего чтобы понять что учить в первую очередь. Для этого и был создан этот парсер. Сразу скажу что я не доволен его реализацией но делался он больше для себя поэтому в нем минимум чистки кода и оптимизации. Сейчас бы я наверно сделал его по другому. Но свою функцию он выполняет. А именно выводит в консоль количество встречающихся ключевых навыков и создает файл со следующими столбцами:

name - наименование вакансии
salary_from - зарплата ОТ 
salary_to - зарплата ДО
currency - валюта (была мысль все ЗП сразу приводить к одной валюте, но не стал реализовывать)
experience - опыт работы
schedule - формат работы (удаленка, полный день и т.д)

Все что нужно находиться внизу:

page = 20                          # сколько страниц запрашиваем

text = 'Python'                    # текст поиска как в поиске hh

derectory = './dict_hh'            # Дерриктория куда будут сохраняться страницы с карточками
derectory_vacancy = './vacancy_hh' # дерриктория куда будут сохраняться карточки

Если надо поработать уже со скаченными карточками то просто закоментите эти строчки:

Sbor_str(page, text, derectory) #собирает список страниц на котором представленна урезанная карточка по профессии
Zapros_kartochek(derectory, derectory_vacancy)    # Выполняет функцию по сбору самих карточек и сохраняет их в отдельные файлы

При правильнйо работе есть строки прогресса по скачиванию страниц и скчиванию карточек (выводит в консоль) 
При повторном использовании зачистите деректории от старых карточек в ручную чтобы не создавались помехи - в виде старых карточек. 
