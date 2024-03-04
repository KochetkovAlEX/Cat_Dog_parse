import aiohttp, json, os
import asyncio, requests, aiofiles
from bs4 import BeautifulSoup


async def main(path):
    async with aiohttp.ClientSession() as session:
        async with session.get(path) as response:
            print("Status:", response.status)
            html = await response.text()
            # print(html)
            return html


"""
https://api.thecatapi.com/v1/images/search - cat
https://random.dog/woof.json - dog
"""


async def save_dog_pic(page: json, count: int, path: str):
    file = json.loads(page)
    print(file['url'])
    link = file['url'].rfind('.')
    # response = requests.get(file['url'])
    if not os.path.exists(path):
        os.mkdir(path)
    async with aiohttp.ClientSession() as session:
        async with session.get(file['url']) as response:
            async with aiofiles.open(f'{path}\\dog{count}{file["""url"""][link:]}', 'wb') as file:
                async for data, _ in response.content.iter_chunks():
                    await file.write(data)
    print("Done")


async def save_cat_pic(page: str, count: int, path: str):
    file = json.loads(page)
    print(file[0]['url'])
    link = file[0]['url'].rfind('.')
    # response = requests.get(file['url'])
    if not os.path.exists(path):
        os.mkdir(path)
    async with aiohttp.ClientSession() as session:
        async with session.get(file[0]['url']) as response:
            async with aiofiles.open(f'{path}\\cat{count}{file[0]["""url"""][link:]}', 'wb') as file:
                async for data, _ in response.content.iter_chunks():
                    await file.write(data)

    print("Done")


if __name__ == '__main__':
    user = input('cat / dog / all? \n')
    quantity = int(input("quantity: "))
    path = input("path: ")
    if user.lower() == 'dog':
        count = 1
        for i in range(quantity):
            page = asyncio.run(main("https://random.dog/woof.json"))
            asyncio.run(save_dog_pic(page=page, count=count, path=path))
            count += 1
    elif user.lower() == 'cat':
        count = 1
        for i in range(quantity):
            page = asyncio.run(main("https://api.thecatapi.com/v1/images/search"))
            asyncio.run(save_cat_pic(page=page, count=count, path=path))
            count += 1
    elif user.lower() == 'all':
        count = 1
        for i in range(quantity // 2):
            cats = asyncio.run(main("https://api.thecatapi.com/v1/images/search"))
            dogs = asyncio.run(main("https://random.dog/woof.json"))
            asyncio.run(save_cat_pic(page=cats, count=count, path=path))
            asyncio.run(save_dog_pic(page=dogs, count=count, path=path))
            count += 1

""" 
print(page)
soup = BeautifulSoup(page, 'html.parser')
for i in range(3):
    page = asyncio.run(main())
    # print(page)
    soup = BeautifulSoup(page, 'html.parser')
    all_dog = soup.findAll(('source', 'img'))
    data = "https://random.dog/" + all_dog[0].get('src')
    link = data.rfind('.')
    print(data, type(data))
    response = requests.get(data)
    with open(f'new_dir\\img{i}{data[link:]}', 'wb') as f:
        f.write(response.content)
        print(i)
"""
