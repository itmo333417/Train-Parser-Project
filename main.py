import requests
from bs4 import BeautifulSoup
import lxml
import json

# ссылка на поезда из Питера в Рязань
#пример- https://www.tutu.ru/poezda/rasp_d.php?nnst1=2004000&nnst2=2000080
from_SPb_url = input('Введите ссылку на маршрут в нужный город:')
if from_SPb_url == "":
    from_SPb_url = "https://www.tutu.ru/poezda/rasp_d.php?nnst1=2004000&nnst2=2000080"
# ссылка на поезда из Рязани в Питер

#пример- https://www.tutu.ru/poezda/rasp_d.php?nnst1=2000080&nnst2=2004000
to_SPb_url = input('Введите ссылку на маршрут в обратном направлении:')
if to_SPb_url == "":
    to_SPb_url = "https://www.tutu.ru/poezda/rasp_d.php?nnst1=2000080&nnst2=2004000"

# словарь заголовков; отправляются вместе с запросом, чтобы браузер не заподозрил нас в парсинге.
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.102 Safari/537.36 OPR/84.0.4316.30 '
}


# функция получает html сайта
def get_html(url):
    html = requests.get(url, headers=HEADERS)  # отправляем гет запрос к сайту, чтобы получить его html.
    return html


# функция составляет словарь с нужными данными
def get_content(src):
    soup = BeautifulSoup(src, 'lxml')  # объект класса BeautifulSoup, который поможет нам в парсинге html сайта
    items = soup.find_all('div', class_='_1Ez_M27zDb5G85SbU1gHPy')  # находим класс, который есть в каждой карточке поезда
    cards = []
    number_variant = 0
    for item in items:

        number_variant += 1
        cards.append(
            {
                'Вариант №': number_variant,
                'Номер поезда': item.find('span', class_='_1GQoCHBzQjl0_POH1xrg6_ _2gLSi9calKNbRt31r6JIRG o33517 o33510')
                                .get_text(),

                'Цена на купе': item.find('div', {'data-ti': 'tariffContent-1'})
                                .find('span').get_text().replace('\xa0', ' '),

                'Цена на плацкарт': item.find('div', {'data-ti': 'tariffContent-0'})
                                    .find('span').get_text().replace('\xa0', ' '),

                'Время отправления': item.find('div', {'data-ti': 'card-departure'})
                                     .find('span', class_='o33555').get_text(),

                'Время прибытия': item.find('div', {'data-ti': 'card-arrival'})
                                  .find('span', class_='o33555').get_text(),

                'Время в пути': item.find('span', class_='o33678 o33517 o33507 o33512')
                                .get_text().replace('\u202f', '').replace('\xa0', ' '),

                'Даты поездок': item.find('a', class_='o33489 o33490 _1rng-lUS9NiNi-JrVT_sOL _1I5jcX7PnBcYfFkLaOzgjV o33517 o33508 o33513')
                                .get('href'),
            }
        )

    return cards


# основная функция; создает 2 файла с конечными данными в формате json
def parser():
    from_SPb_html = get_html(from_SPb_url)
    to_SPb_html = get_html(to_SPb_url)
    # проверка статуса подключения к серверу
    if from_SPb_html.status_code == 200 and to_SPb_html.status_code == 200:
        from_SPb_result = get_content(from_SPb_html.text)

        with open('Питер-Рязань.json', 'w', encoding='utf-8') as file:
            json.dump(from_SPb_result, file, indent=2, ensure_ascii=False)
        file.close()

        to_SPb_result = get_content(to_SPb_html.text)
        with open('Рязань-Питер.json', 'w', encoding='utf-8') as file:
            json.dump(to_SPb_result, file, indent=2, ensure_ascii=False)
        file.close()

    else:
        print("Error: web-site is not available now.")


# запуск программы; (опциональная в данной программе) проверка на точку входа
if __name__ == '__main__':
    parser()
    print('Работа выполнена. Проверьте файлы с маршрутами.')

