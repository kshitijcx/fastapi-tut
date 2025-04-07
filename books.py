from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title":"Title One", "author":"Author One", "category":"science"},
    {"title":"Title Two", "author":"Author Two", "category":"science"},
    {"title":"Title Three", "author":"Author Three", "category":"history"},
    {"title":"Title Four", "author":"Author Four", "category":"math"},
    {"title":"Title Five", "author":"Author Five", "category":"math"},
    {"title":"Title Six", "author":"Author Two", "category":"math"}
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}") #path params
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/") #query param /books/?category=science
async def read_category_by_query(category:str):
    booksToReturn = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            booksToReturn.append(book)
    return booksToReturn

@app.get('/books/{book_author}/') #path and query params together
async def read_author_category_by_query(book_author:str, category:str):
    booksToReturn = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            booksToReturn.append(book)
    return booksToReturn

@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put('/books/update_book')
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
    
@app.delete('/books/{book_title}')
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

@app.get('/books/byauthor/{author}')
async def read_books_by_author_path(author:str):
    booksToReturn = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            booksToReturn.append(book)
    
    return booksToReturn

#uvicorn books:app --reload
#async is optional for fastAPI
#other ways to run
#fastapi run books.py
#fastapi dev books.py
#%20 -> space in url

#order matters with dynamic and non dynamic params