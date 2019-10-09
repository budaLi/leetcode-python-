import asyncio
import re
import aiohttp
import aiomysql
from pyquery import PyQuery
from lxml import etree
from queue import Queue

start_url = 'http://news.baidu.com/'
waitting_urs = Queue()
seen_uels = set()
stoppint = False
sem = asyncio.Semaphore(10)  # 现在并发为3个
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}


class async_text(object):
    async def fetch(self, url, session):
        async with sem:
            #     await asyncio.sleep(1)
            try:
                async with session.get(url, headers=headers, timeout=1) as resp:
                    # print('url status：{}'.format(resp.status))
                    # if resp.status in [200, 201]:
                    data = etree.HTML(await resp.read())
                    return data
            except Exception as e:
                print('错误为:{}  url:{}'.format(e, url))

    def extract_urls(self, html):
        try:
            for url in html.xpath('//a/@href'):
                if url and url.startswith("https") and url not in seen_uels:
                    waitting_urs.put(url)
        except:
            print("extract_url error")

    async def init_urls(self, url, session):
        html = await self.fetch(self, url, session)
        seen_uels.add(url)
        self.extract_urls(self, html)

    async def article_handler(self, url, session, pool):
        # 获取文章详情
        html = await self.fetch(self, url, session)
        seen_uels.add(url)
        # self.extract_urls(self, html)
        try:
            title = html.xpath('//div[@class=article-title]')[0].strip()
            print('title:{}'.format(title))
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    try:
                        # 插入
                        await cur.execute('insert into spider(title) values("{}")'.format(title))
                    except Exception as e:
                        print("insert error", e)
        except:
            pass

    async def consumer(self, pool):
        async with aiohttp.ClientSession() as session:
            while not stoppint:
                url = waitting_urs.get(timeout=3)
                if waitting_urs.qsize() < 10:
                    if url not in seen_uels:
                        asyncio.ensure_future(self.init_urls(self, url, session))
                print('start get url:{}'.format(url))
                if re.findall(r'baidu', url):
                    if url not in seen_uels:
                        asyncio.ensure_future(self.article_handler(self, url, session, pool))
                        await asyncio.sleep(0.1)

    @classmethod
    async def main(self, loop):
        pool = await aiomysql.create_pool(host='127.0.0.1', port=3306, user='root', password='root', db='aiospider',
                                          loop=loop,
                                          charset='utf8', autocommit=True)
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(self, start_url, session)
            seen_uels.add(start_url)
            self.extract_urls(self, html)

        asyncio.ensure_future(self.consumer(self, pool))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_text.main(loop))
    loop.run_forever()
