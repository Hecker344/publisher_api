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
            try:
                new_publisher={  "name": data["name"],
                            "founded_year": data["founded_year"],
                            "country": data["country"]
                                 }
                ris = await publishers.insert_one(new_publisher)
                self.write(str(ris))
            except:
                self.write("body della post non valido")


    async def delete(self, id= None):
        self.set_header("Content-Type", "application/json")
        if id:
            res= await publishers.delete_one({"_id": ObjectId(id)})
            self.write(str(res.deleted_count))
        else:
            self.write("é obbligatorio un id")

    async def put(self, id= None):
        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        k=0
        if id:
            filtered_publisher = await publishers.find_one({"_id": ObjectId(id)})
            if filtered_publisher:
                if data["name"]:
                    await publishers.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": {"name": data["name"]}}
                    )
                    k=k+1
                    self.write("Name modificato")
                if data["founded_year"]:
                    await publishers.update_one(
                        {"_id": ObjectId(id)},
                        {"$set": {"founded_year": data["founded_year"]}}
                    )
                    k=k+1
                    self.write("founded_year modificato")
                if data["country"]:
                    await publishers.update_one(
                        {"_id": ObjectId(id)},
                        {"$set": {"country": data["country"]}}
                    )
                    k=k+1
                    self.write("country modificato")
                if k==0:
                    self.write("Argomenti della post non validi")
            else:
                self.write("id errato")
        else:
            self.write("id mancante")



class BooksHandler(tornado.web.RequestHandler):
    async def get(self, id=None, id_book=None):
        self.set_header("Content-Type", "application/json")
        title = self.get_query_argument("title", None)
        author = self.get_query_argument("author", None)
        genre = self.get_query_argument("genre", None)
        if id_book and id:
            filtered_book = await books.find_one({"$and": [{"_id": ObjectId(id_book)}, {"publisher_id": ObjectId(id)}]})
            filtered_book["_id"] = str(filtered_book["_id"])
            filtered_book["publisher_id"] = str(filtered_book["publisher_id"])
            self.write(filtered_book)
        elif id:
                if title and author and genre:
                        all_books = books.find({"$and": [{"title": title}, {"author": author},{"genre":genre},{"publisher_id": ObjectId(id)}]})
                        list = []
                        async for book in all_books:
                            book["_id"] = str(book["_id"])
                            book["publisher_id"] = str(book["publisher_id"])
                            list.append(book)
                        filtered_book = {"books": list}
                        self.write(filtered_book)
                elif title and author:
                    all_books = books.find({"$and": [{"title": title}, {"author": author},{"publisher_id": ObjectId(id)}]})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        book["publisher_id"] = str(book["publisher_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
                elif title and genre:
                    all_books = books.find({"$and": [{"title": title}, {"genre": genre},{"publisher_id": ObjectId(id)}]})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        book["publisher_id"] = str(book["publisher_id"])
                        list.append(book)
                    filtered_book = {"books": list}

                    self.write(filtered_book)
                elif genre and author:
                    all_books = books.find({"$and": [{"author": author}, {"genre": genre},{"publisher_id": ObjectId(id)}]})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        book["publisher_id"] = str(book["publisher_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
                elif title:
                    all_books = books.find({"$and": [{"title": title},{"publisher_id": ObjectId(id)}]})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        book["publisher_id"] = str(book["publisher_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
                elif author:
                    all_books = books.find({"$and": [{"author": author},{"publisher_id": ObjectId(id)}]})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        book["publisher_id"] = str(book["publisher_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
                elif genre:
                    all_books = books.find({"$and": [{"genre": genre},{"publisher_id": ObjectId(id)}]})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        book["publisher_id"] = str(book["publisher_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
                else:
                    all_books = books.find({"publisher_id": ObjectId(id)})
                    list = []
                    async for book in all_books:
                        book["_id"] = str(book["_id"])
                        book["publisher_id"] = str(book["publisher_id"])
                        list.append(book)
                    filtered_book = {"books": list}
                    self.write(filtered_book)
        else:
            self.write("id mancanti o errati")


    async def post(self):
        self.set_header("Content-Type", "application/json")
        if id:
            self.write("metodo non accetato con id")
        else:
            data = tornado.escape.json_decode(self.request.body)
            try:
                new_book = {"title": data["title"],
                            "author": data["author"],
                            "genre": data["genre"],
                            "year": data["year"],
                            "publisher_id": ObjectId(data["publisher_id"])}
                ris = await books.insert_one(new_book)
                self.write(str(ris))
            except:
                self.write("body della post non valido")


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