from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from .route_utilities import create_model, validate_model, get_models_with_filters
from ..db import db

# from app.models.book import books

bp = Blueprint("book_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)

# get all books
@bp.get("")
@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)

# get one book
@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    return book.to_dict()

# update one book
@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# delete one book
@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# def validate_model(cls, model_id):
#     try:
#         model_id = int(model_id)
#     except:
#         response = {"message": f"{cls.__name__} {model_id} invalid"}
#         abort(make_response(response , 400))

#     query = db.select(cls).where(cls.id == model_id)
#     model = db.session.scalar(query)
    
#     if not model:
#         response = {"message": f"{cls.__name__} {model_id} not found"}
#         abort(make_response(response, 404))
    
#     return model

# @books_bp.get("")
# def get_all_books():
#     books_response = []
#     for book in books:
#         books_response.append(
#             {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }
#         )
#     return books_response

# @books_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book(book_id)
#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description,
#     }


# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         response = {"message": f"book {book_id} invalid"}
#         abort(make_response(response, 400))

#     for book in books:
#         if book.id == book_id:
#             return book

#     response = {"message": f"book {book_id} not found"}
#     abort(make_response(response, 404))

