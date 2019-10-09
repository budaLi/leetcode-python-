# @Time    : 2019/9/30 9:46
# @Author  : Libuda
# @FileName: aiohttp_spider.py
# @Software: PyCharm
import aiohttp
import asyncio
import aiomysql
from queue import Queue
from pyquery import PyQuery
import re


class Spider:
    def __init__(self):
        self.start_url = 'https://yq.aliyun.com/articles/'
        self.headers = {
            ':authority': 'yq.aliyun.com',
            ':method': 'GET',
            ':path': '/articles/',
            ':scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'aliyun_choice=CN;cna=xKTJFVuFeQACASRuT8KdmnAJ; UM_distinctid=16c506ce97e6e8-047ff319f8ea46-c343162-e1000-16c506ce97face; _ga=GA1.2.611970734.1564717411; login_aliyunid_pk=1957967501020753; CLOSE_HELP_GUIDE_V2=true; login_aliyunid_pks="BG+pVUHS4CbevK4HkfYcGFSHbukebNukp/XY0GrwOaXC/g="; aliyun_country=CN; aliyun_site=CN; console_base_assets_version=2.4.0; channel=dKsTees6Al%2BETn5saZWBVIiMkEEWwVjf2lZVKjq6%2FMY%3D; yunqi_abtest=60; _gid=GA1.2.1375707368.1570527799; isToDeveloperShow=show; nonce_csrf=7YRILGCBNR; yunqi_csrf=BG4LV2B34U; CNZZDATA1256835944=1931888980-1564716700-https%253A%252F%252Fgithub.com%252F%7C1570585375; CNZZDATA1256757167=2046087809-1564715225-https%253A%252F%252Fgithub.com%252F%7C1570583072; _gat=1; l=cBPdyZg7qYelLNwzBOCwourza77OSIRAguPzaNbMi_5CzsL_3oQOk99h1Up6VjWdti8B4tm2-g29-etkmUiZt1uvgbwC.; isg=BCQknefUJQr41VGYX1d3KS8G9SIWvUgn5FAA_z5FsO-y6cSzZs0Yt1pLqQHUMYB_',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        self.pool = ""
        self.stop = False
        self.waitting_url = Queue()
        self.seen_urls = set()

    def extract_urls(self, html):
        """
        从html中解析url  因为此处是占用cpu而不是占用io  所以在这里不需要使用async
        :return:
        """
        urls = []
        pq = PyQuery(html)
        for link in pq.items("a"):
            url = link.attr("href")
            pattern = re.compile('.*?[0-9]$')
            if url and url.startswith("/articles/") and re.match(pattern, url) and url not in self.seen_urls:
                urls.append("https://yq.aliyun.com" + url)
                self.waitting_url.put("https://yq.aliyun.com" + url)
                # return urls

    async def article_handler(self, url, session, pool):
        """
        获取文章详情并解析入库
        :param url:
        :param session:
        :return:
        """
        html = await self.fetch(url, session)
        self.seen_urls.add(url)
        self.extract_urls(html)
        pq = PyQuery(html)
        title = pq("#blog-title").text()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                insert_sql = "insert into spider(title) values('{}')".format(title)
                await cur.execute(insert_sql)

    async def consumer(self, pool, session):
        while not self.stop:
            url = self.waitting_url.get()
            if re.match("https://yq.aliyun.com/articles/\d*", url):
                if url not in self.seen_urls:
                    asyncio.ensure_future(self.article_handler(url, session, pool))
                    await asyncio.sleep(30)
                    # else:
                    #     if url not in self.seen_urls:
                    #         asyncio.ensure_future(self.init_urls(url, session))

    async def init_urls(self, url, session):
        html = await self.fetch(url, session)
        self.seen_urls.add(url)
        self.extract_urls(html)

    async def fetch(self, url, session):
        try:
            async with session.get(url) as response:
                # await print(response.text)
                if response.status in [200, 201]:
                    data = await response.text()
                    return data
        except Exception as e:
            print("访问 {} 异常".format(e))
            return None

    async def main(self, loop):
        self.pool = await aiomysql.create_pool(host="127.0.0.1", port=3306, user='root', password='root',
                                               db='aiospider',
                                               loop=loop, charset='utf8', autocommit=True)
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(self.start_url, session)
            self.seen_urls.add(self.start_url)
            if html:
                self.extract_urls(html)

        asyncio.ensure_future(self.consumer(self.pool, session))

if __name__ == "__main__":
    spider = Spider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.main(loop))
    loop.run_forever()
