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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers'
    }
    
    response = await session.get(url, headers=headers)
    response_text = response.text
    return response_text



async def author_(data: str) -> list:
    tree = html.fromstring(data)
    authors = tree.xpath('/html/body/div[1]/w56sks5e/w56snpi/fs25oa55ul/yjuxqtv1yz2/yjuxqtv1yz2[1]/fs25oa55ul/div/div[1]/div[2]/div[2]/span[1]/a')
    LST_AUTHORS.append('new author')
    for author in authors:
        LST_AUTHORS.append(author.text_content())


async def all_url(session, data: str) -> list:
    tree = html.fromstring(data)
    urls = tree.xpath('/html/body/div[1]/w56sks5e/w56snpi/utah4xrpfw/yjuxqtv1yz2[3]/yjuxqtv1yz2/fs25oa55ul/article/div[1]/a')
    task = [author_(await request_url(session, data.get('href'))) for data in urls]
    await asyncio.gather(*task)


async def main():
    
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