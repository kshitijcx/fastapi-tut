from fastapi import FastAPI

app = FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int

    def __init__(self,id,title,author,description,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating

BOOKS = [
    Book(1,'Computer Science Pro', 'kshitij', 'nice book', 5),
    Book(2,'FastAPI', 'kshitij', 'great book', 5),
    Book(3,'Master Endpoints', 'kshitij', 'awesome book', 5),
    Book(4,'HP1', 'author 1', 'description', 2),
    Book(5,'HP2', 'author 2', 'description', 3),
    Book(6,'HP3', 'author 3', 'description', 1),
]

@app.get("/books")
async def read_all_books():
    return BOOKS

#pydantics library used for data modeling, data parsing, efficient error handling
#pydantics mainly used for data validation of incoming data
