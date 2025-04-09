from fastapi import FastAPI, Path   
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    id:int 
    title:str
    author:str
    description:str
    rating:int
    published_date:int

    def __init__(self,id,title,author,description,rating,published_date):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.published_date=published_date  

class BookRequest(BaseModel):
    # id: Optional[int] = None
    #describe when id is not needed
    id: Optional[int] = Field(description="ID is not needed on create", default=None) 
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1,max_length=100)
    rating:int = Field(gt=0, lt=6)
    publised_data:int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "kshitij",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2029
            }
        }
    }

BOOKS = [
    Book(1,'Computer Science Pro', 'kshitij', 'nice book', 5, 2030),
    Book(2,'FastAPI', 'kshitij', 'great book', 5, 2030),
    Book(3,'Master Endpoints', 'kshitij', 'awesome book', 5, 2029),
    Book(4,'HP1', 'author 1', 'description', 2, 2028),
    Book(5,'HP2', 'author 2', 'description', 3, 2027),
    Book(6,'HP3', 'author 3', 'description', 1, 2026),
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

@app.get("/books/")
async def read_book_by_rating(book_rating:int):
    booksToReturn = []
    for book in BOOKS:
        if book.rating == book_rating:
            booksToReturn.append(book)
    return booksToReturn

#pydantics library used for data modeling, data parsing, efficient error handling
#pydantics mainly used for data validation of incoming data

@app.get('/books/publish/')
async def read_books_by_publish_date(published_date:int):
    booksToReturn = []
    for book in BOOKS:
        if book.published_date == published_date:
            booksToReturn.append(book)
    return booksToReturn

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_id(new_book))

# The three biggest are:
# 1. .dict() function is now renamed to .model_dump()
# 2. schema_extra function within a Config class is now renamed to json_schema_extra
# 3. Optional variables need a =None example: id: Optional[int] = None

def find_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1;
    return book

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i]=book

@app.delete('/books/{book_id}')
async def delete_book(book_id:int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break