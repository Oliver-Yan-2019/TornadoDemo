from tornado.httpclient import HTTPClient


class SyncClient(HTTPClient):
    pass


if __name__ == '__main__':
    client = HTTPClient()
    response = client.fetch('https://www.baidu.com/')
    print(response.body.decode())
