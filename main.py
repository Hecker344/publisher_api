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
        self.set_header("Content-Type", "application/json")
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


    async def post(self, id= None):
        self.set_header("Content-Type", "application/json")
        if id:
            self.write("metodo non accetato con id")
        else:
            data = tornado.escape.json_decode(self.request.body)
            ris = await publishers.insert_one(data)
            self.write(str(ris))

    async def delete(self, id= None):
        self.set_header("Content-Type", "application/json")
        if id:
            res= await publishers.delete_one({"_id": ObjectId(id)})
            self.write(res.deleted_count)
        else:
            self.write("é obbligatorio un id")


class BooksHandler(tornado.web.RequestHandler):
    async def get(self, id=None):
        self.set_header("Content-Type", "application/json")


        if id:
            all_books = books.find({"publisher_id": ObjectId(id)})
            list = []
            async for book in all_books:
                book["_id"] = str(book["_id"])
                book["publisher_id"]= str(book["publisher_id"])
                list.append(book)
            filtered_publisher = {"books": list}
            self.write(filtered_publisher)
        else:
            pass


    async def post(self):
        pass


def make_app():
    return tornado.web.Application([
        (r"/publishers", PublishersHandler),  # Per la lista di publisher
        (r"/publishers/([a-f0-9]{24})", PublishersHandler),  # Per il publisher con un ID esadecimale
        (r"/publishers/([a-f0-9]{24})/books", BooksHandler)
    ])

async def main(shutdown_event):
    app = make_app()
    app.listen(8888)
    print("Server attivo su http://localhost:8888/publishers")
    await shutdown_event.wait()
    print("Chiusura server...")


if __name__ == "__main__":
    shutdown_event = asyncio.Event()
    try:
        asyncio.run(main(shutdown_event))
    except KeyboardInterrupt:
        shutdown_event.set()