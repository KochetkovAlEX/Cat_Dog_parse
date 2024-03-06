import aiohttp, json, os, typing
import asyncio, requests, aiofiles
from bs4 import BeautifulSoup


async def main(path: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(path) as response:
            print("Status:", response.status)
            html = await response.text()
            # print(html)
            return html


async def save_dog_pic(page: json, count: int, path: str):
    if not os.path.exists(path):
        os.mkdir(path)
    file = json.loads(page)
    print(file['url'])
    link = file['url'].rfind('.')
    # response = requests.get(file['url'])
    async with aiohttp.ClientSession() as session:
        async with session.get(file['url']) as response:
            async with aiofiles.open(f'{path}\\dog{count}{file["""url"""][link:]}', 'wb') as file:
                async for data, _ in response.content.iter_chunks():
                    await file.write(data)


async def save_cat_pic(page: str, count: int, path: str):
    file = json.loads(page)
    # print(page)
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


async def do_task_main(path: str, quantity: int):
    tasks = []
    for i in range(quantity):
        task = asyncio.create_task(main(path))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    print(res, type(res))
    return res


async def do_tasks_save_dog(res: list):
    tasks = []
    for i in range(len(res)):
        task = asyncio.create_task(save_dog_pic(page=res[i], count=i + 1, path=path))
        tasks.append(task)
        # print(i)
    await asyncio.gather(*tasks)


async def do_tasks_save_cat(res: list):
    tasks = []
    for i in range(len(res)):
        task = asyncio.create_task(save_cat_pic(page=res[i], count=i + 1, path=path))
        tasks.append(task)
    # print(i)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    cat = "https://api.thecatapi.com/v1/images/search"
    dog = "https://random.dog/woof.json"
    user = input('cat / dog / all? \n')
    quantity = int(input("quantity: "))
    path = input("path: ")
    if user.lower() == 'dog':
        res = asyncio.run(do_task_main(dog, quantity))
        # print(res)
        asyncio.run(do_tasks_save_dog(res))
    elif user.lower() == 'cat':
        res = asyncio.run(do_task_main(cat, quantity))
        # print(res)
        asyncio.run(do_tasks_save_cat(res))
    elif user.lower() == 'all':
        res_dog = asyncio.run(do_task_main(path=dog, quantity=quantity // 2))
        res_cat = asyncio.run(do_task_main(path=cat, quantity=quantity // 2))
        asyncio.run(do_tasks_save_dog(res_dog))
        asyncio.run(do_tasks_save_cat(res_cat))
    print("Done")
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
