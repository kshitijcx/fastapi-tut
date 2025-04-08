from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

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

class BookRequest(BaseModel):
    # id: Optional[int] = None
    #describe when id is not needed
    id: Optional[int] = Field(description="ID is not needed on create", default=None) 
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1,max_length=100)
    rating:int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "kshitij",
                "description": "A new description of a book",
                "rating": 5
            }
        }
    }

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