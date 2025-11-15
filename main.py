
import tornado.web
import asyncio
from pymongo import AsyncMongoClient

client = AsyncMongoClient("localhost", 27017)
db = client['publisher_db']
publishers=db['publishers']
books= db['books']

class Main(tornado.web.RequestHandler):
    def post(self):
        pass

    def get(self):
        pass

def make_app():
       return tornado.web.Application([])

async def main(shutdown_event):
    app = make_app()
    app.listen(8888)
    print("Server attivo su http://localhost:8888/main")
    await shutdown_event.wait()
    print("Chiusura server...")


if __name__ == "__main__":
    shutdown_event = asyncio.Event()
    try:
        asyncio.run(main(shutdown_event))
    except KeyboardInterrupt:
        shutdown_event.set()