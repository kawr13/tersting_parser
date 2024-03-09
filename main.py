import requests
import json
import lxml
from lxml import html
from my_multi import task, set_max_threads
import asyncio
import httpx
from icecream import ic

set_max_threads(4)

LST_AUTHORS = []


async def request_url(session, url: str) -> list:
    """
    Асинхронный запрос к URL и возврат ответа в виде текста.

    :param session: Сессия HTTPX для выполнения запроса.
    :param url: URL для запроса.
    :return: Ответ сервера в виде текста.
    """
    headers = {
        # Определение заголовков запроса
    }
    
    response = await session.get(url, headers=headers)
    response_text = response.text
    return response_text


async def author_(data: str) -> list:
    """
    Асинхронное извлечение авторов из HTML-данных и добавление их в глобальный список LST_AUTHORS.

    :param data: HTML-данные для парсинга.
    :return: None
    """
    tree = html.fromstring(data)
    authors = tree.xpath('/html/body/div[1]/w56sks5e/w56snpi/fs25oa55ul/yjuxqtv1yz2/yjuxqtv1yz2[1]/fs25oa55ul/div/div[1]/div[2]/div[2]/span[1]/a')
    LST_AUTHORS.append('new author')
    for author in authors:
        LST_AUTHORS.append(author.text_content())


async def all_url(session, data: str) -> list:
    """
    Асинхронное извлечение всех URL из HTML-данных и создание задач для извлечения авторов.

    :param session: Сессия HTTPX для выполнения запросов.
    :param data: HTML-данные для парсинга.
    :return: None
    """
    tree = html.fromstring(data)
    urls = tree.xpath('/html/body/div[1]/w56sks5e/w56snpi/utah4xrpfw/yjuxqtv1yz2[3]/yjuxqtv1yz2/fs25oa55ul/article/div[1]/a')
    task = [author_(await request_url(session, data.get('href'))) for data in urls]
    await asyncio.gather(*task)


async def main():
    """
    Главная асинхронная функция, которая запускает процесс сбора авторов.

    :return: None
    """
    pages = int(input('Введите количество страниц: '))
    async with httpx.AsyncClient() as session:
        session.proxyes = {'http': 'http://178.218.44.79:3128', 'https': 'https://178.218.44.79:3128'}
        for page in range(1, pages + 1):
            url = 'https://4pda.to/page/{pag}'
            url = url.format(pag=page)
            data = await request_url(session, url)
            await all_url(session, data)
            await asyncio.sleep(2)
    ic(LST_AUTHORS)
    

if __name__ == '__main__':
    asyncio.run(main())
