from bson import ObjectId
from pymongo import AsyncMongoClient, MongoClient

client = MongoClient("localhost", 27017)
db = client['publishing_db']
publishers=db['publishers']
books = db['books']


publishers.insert_many([
  {
    "name": "Einaudi",
    "founded_year": 1933,
    "country": "Italia"
  },
  {
    "name": "Penguin Random House",
    "founded_year": 2013,
    "country": "USA"
  },
  {
    "name": "Mondadori",
    "founded_year": 1907,
    "country": "Italia"
  },
  {
    "name": "HarperCollins",
    "founded_year": 1989,
    "country": "USA"
  },
  {
    "name": "Feltrinelli",
    "founded_year": 1954,
    "country": "Italia"
  }
])

enaudi = publishers.find_one({"name": "Einaudi" })
Penguin_Random_House = publishers.find_one({"name": "Penguin Random House" })
Mondadori = publishers.find_one({"name": "Mondadori" })
HarperCollins = publishers.find_one({"name": "HarperCollins" })
Feltrinelli = publishers.find_one({"name": "Feltrinelli" })

book=[
  {
    "title": "Il barone rampante",
    "author": "Italo Calvino",
    "genre": "Romanzo",
    "year": 1957,
    "publisher_id": "OBJECT_ID_EINAUDI"
  },
  {
    "title": "Se una notte d'inverno un viaggiatore",
    "author": "Italo Calvino",
    "genre": "Romanzo",
    "year": 1979,
    "publisher_id": "OBJECT_ID_EINAUDI"
  },
  {
    "title": "Il nome della rosa",
    "author": "Umberto Eco",
    "genre": "Giallo",
    "year": 1980,
    "publisher_id": "OBJECT_ID_EINAUDI"
  },
  {
    "title": "Il codice da Vinci",
    "author": "Dan Brown",
    "genre": "Giallo",
    "year": 2003,
    "publisher_id": "OBJECT_ID_PENGUIN"
  },
  {
    "title": "Harry Potter e la pietra filosofale",
    "author": "J.K. Rowling",
    "genre": "Fantasy",
    "year": 1997,
    "publisher_id": "OBJECT_ID_PENGUIN"
  },
  {
    "title": "Il signore degli anelli",
    "author": "J.R.R. Tolkien",
    "genre": "Fantasy",
    "year": 1954,
    "publisher_id": "OBJECT_ID_PENGUIN"
  },
  {
    "title": "1984",
    "author": "George Orwell",
    "genre": "Romanzo",
    "year": 1949,
    "publisher_id": "OBJECT_ID_MONDADORI"
  },
  {
    "title": "Hunger Games",
    "author": "Suzanne Collins",
    "genre": "Fantasy",
    "year": 2008,
    "publisher_id": "OBJECT_ID_MONDADORI"
  },
  {
    "title": "La ragazza del treno",
    "author": "Paula Hawkins",
    "genre": "Giallo",
    "year": 2015,
    "publisher_id": "OBJECT_ID_MONDADORI"
  },
  {
    "title": "Harry Potter e il prigioniero di Azkaban",
    "author": "J.K. Rowling",
    "genre": "Fantasy",
    "year": 1999,
    "publisher_id": "OBJECT_ID_HARPERCOLLINS"
  },
  {
    "title": "Il piccolo principe",
    "author": "Antoine de Saint-Exupéry",
    "genre": "Romanzo",
    "year": 1943,
    "publisher_id": "OBJECT_ID_HARPERCOLLINS"
  },
  {
    "title": "Il vecchio e il mare",
    "author": "Ernest Hemingway",
    "genre": "Romanzo",
    "year": 1952,
    "publisher_id": "OBJECT_ID_HARPERCOLLINS"
  },
  {
    "title": "Sostiene Pereira",
    "author": "Antonio Tabucchi",
    "genre": "Romanzo",
    "year": 1994,
    "publisher_id": "OBJECT_ID_FELTRINELLI"
  },
  {
    "title": "La ragazza del treno",
    "author": "Paula Hawkins",
    "genre": "Giallo",
    "year": 2015,
    "publisher_id": "OBJECT_ID_FELTRINELLI"
  },
  {
    "title": "Cecità",
    "author": "José Saramago",
    "genre": "Romanzo",
    "year": 1995,
    "publisher_id": "OBJECT_ID_FELTRINELLI"
  }
]

for x in range(3):
    book[x]["publisher_id"]=enaudi["_id"]

for x in range(3,6):
    book[x]["publisher_id"]=Penguin_Random_House["_id"]

for x in range(6,9):
    book[x]["publisher_id"] = Mondadori["_id"]

for x in range(9,12):
    book[x]["publisher_id"] = HarperCollins["_id"]

for x in range(12,15):
    book[x]["publisher_id"] = Feltrinelli["_id"]


books.insert_many(book)