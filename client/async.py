from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop


if __name__ == '__main__':
    async def fetch():
        client = AsyncHTTPClient()
        return await client.fetch('https://www.baidu.com/')

    io_loop = IOLoop()
    response = io_loop.run_sync(fetch)
    # 不返回结果
    # io_loop.spawn_callback(fetch)
    print(response.body.decode())
