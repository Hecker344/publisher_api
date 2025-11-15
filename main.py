
import tornado.web
import asyncio

from bson import ObjectId
from pymongo import AsyncMongoClient

client = AsyncMongoClient("localhost", 27017)
db = client['publisher_db']
publishers=db['publishers']
books= db['books']

class Main(tornado.web.RequestHandler):
    async def get(self, id=None):
        name = self.get_query_argument("name", None)
        country=self.get_query_argument("country", None)


        if id:
            filtered_publisher = await publishers.find({"_id": id })
        else:
            if name and country:
                filtered_publisher= await publishers.find({"$and": [{"name": name},{"country": country}]})
            elif name:
                filtered_publisher = await publishers.find({"name": name})
            elif country:
                filtered_publisher = await publishers.find({"country": country})
            else:
                filtered_publisher= await publishers.find()


    def post(self):
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