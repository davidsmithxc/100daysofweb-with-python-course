import requests
import bs4
from colorama import Fore
import aiohttp
import asyncio

def get_html(episode_number: int) -> str:
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f'https://talkpython.fm/{episode_number}'
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.text

async def get_aio_html(episode_number: int) -> str:
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f'https://talkpython.fm/{episode_number}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.text()

def get_title(html: str, episode_number: int) -> str:
    print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "MISSING"

    return header.text.strip()

async def get_aio_title(html: str, episode_number: int) -> str:
    print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "MISSING"

    return await header.text.strip()

def main():
    ASYNC = True
    
    if ASYNC:
        loop = asyncio.get_event_loop()
        
        task1 = loop.create_task(get_aio_title_range())
        loop.run_until_complete(task1)
    else:
        get_title_range()
    print("Done.")

def get_title_range():
    # Please keep this range pretty small to not DDoS my site. ;)
    for n in range(150, 170):
        html = get_html(n)
        title = get_title(html, n)
        print(Fore.WHITE + f"Title found: {title}", flush=True)

async def get_aio_title_range():
    tasks = []
    for n in range(150, 170):
        tasks.append((n, asyncio.create_task(get_aio_html(n))))

    for n, t in tasks:
        html = await t
        title = get_title(html, n)
        print(Fore.WHITE + f"Title found: {title}", flush=True)


if __name__ == '__main__':
    main()
