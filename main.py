
import tornado.web
import asyncio
from bson import ObjectId
from pymongo import AsyncMongoClient

client = AsyncMongoClient("localhost", 27017)
db = client['publishing_db']
publishers=db['publishers']
books= db['books']

class PublishersHandler(tornado.web.RequestHandler):
    async def get(self, id=None):
        name = self.get_query_argument("name", None)
        country=self.get_query_argument("country", None)


        if id:
            filtered_publisher = await publishers.find_one({"_id": ObjectId(id) })
            filtered_publisher["_id"]= str(filtered_publisher["_id"])
            self.write(filtered_publisher)
        else:
            if name and country:
                all_publishers= publishers.find({"$and": [{"name": name},{"country": country}]})
                list = []
                async for publisher in all_publishers:
                    publisher["_id"] = str(publisher["_id"])
                    list.append(publisher)
                filtered_publisher = {"publishers":list}
                self.write(filtered_publisher)
            elif name:
                all_publishers = publishers.find({"name": name})
                list = []
                async for publisher in all_publishers:
                    publisher["_id"] = str(publisher["_id"])
                    list.append(publisher)
                filtered_publisher = {"publishers":list}
                self.write(filtered_publisher)
            elif country:
                all_publishers = publishers.find({"country": country})
                list = []
                async for publisher in all_publishers:
                    publisher["_id"] = str(publisher["_id"])
                    list.append(publisher)
                filtered_publisher = {"publishers":list}
                self.write(filtered_publisher)
            else:
                all_publishers= publishers.find()
                list = []
                async for publisher in all_publishers:
                    publisher["_id"] = str(publisher["_id"])
                    list.append(publisher)
                filtered_publisher = {"publishers":list}
                self.write(filtered_publisher)


    def post(self):
        pass


def make_app():
    return tornado.web.Application([
        (r"/publishers", PublishersHandler),  # Per la lista di publisher
        (r"/publishers/([a-f0-9]{24})", PublishersHandler),  # Per il publisher con un ID esadecimale
    ])

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