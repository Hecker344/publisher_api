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
    async def get(self, id=None, id_book=None):
        self.set_header("Content-Type", "application/json")
        title = self.get_query_argument("title", None)
        author = self.get_query_argument("author", None)
        genre = self.get_query_argument("genre", None)
        if id_book and id:
            all_books = books.find({"$and": [{"_id": ObjectId(id_book)}, {"publisher_id": ObjectId(id)}]})
            list = []
            async for book in all_books:
                book["_id"] = str(book["_id"])
                book["publisher_id"] = str(book["publisher_id"])
                list.append(book)
            filtered_book = {"books": list}
            self.write(filtered_book)
        elif id:
                all_books = books.find({"publisher_id": ObjectId(id)})
                list = []
                async for book in all_books:
                    book["_id"] = str(book["_id"])
                    book["publisher_id"]= str(book["publisher_id"])
                    list.append(book)
                filtered_book = {"books": list}
                self.write(filtered_book)
                if title and author and genre:
                        all_books = books.find({"$and": [{"title": title}, {"author": author},{"genre":genre}]})
                        list = []
                        async for book in all_books:
                            book["_id"] = str(book["_id"])
                            list.append(book)
                        filtered_book = {"books": list}
                        self.write(filtered_book)
                elif title and author:
                    all_books = books.find({"$and": [{"title": title}, {"author": author}]})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
                elif title and genre:
                    all_books = books.find({"$and": [{"title": title}, {"genre": genre}]})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
                elif genre and author:
                    all_books = books.find({"$and": [{"author": author}, {"genre": genre}]})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
                elif title:
                    all_books = books.find({"title": title})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
                elif author:
                    all_books = books.find({"author": author})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
                elif genre:
                    all_books = books.find({"genre": genre})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
        else:
            self.write("id mancanti o errati")


    async def post(self):
        pass


def make_app():
    return tornado.web.Application([
        (r"/publishers", PublishersHandler),  # Per la lista di publisher
        (r"/publishers/([a-f0-9]{24})", PublishersHandler),  # Per il publisher con un ID esadecimale
        (r"/publishers/([a-f0-9]{24})/books", BooksHandler),
        (r"/publishers/([a-f0-9]{24})/books/([a-f0-9]{24})", BooksHandler)
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