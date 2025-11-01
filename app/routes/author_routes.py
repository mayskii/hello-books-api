from flask import Blueprint, make_response, abort, request, Response
from app.models.author import Author
from app.models.book import Book
from .route_utilities import create_model, validate_model, get_models_with_filters
from ..db import db


bp = Blueprint("author_bp", __name__, url_prefix="/authors")


# Create author
@bp.post("")
def create_author():
    request_body = request.get_json()
    return create_model(Author, request_body)

# POST route for add book to author
@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)
    
    request_body = request.get_json()
    request_body["author_id"] = author.id
    return create_model(Book, request_body)

# get all authors
@bp.get("")
def get_all_authors():
    return get_models_with_filters(Author, request.args)

    # authors_response = []
    # for author in authors:
    # authors_response.append(author.to_dict())



# GETting All Books from an Author
@bp.get("/<author_id>/books")
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)

    response = [book.to_dict() for book in author.books]
    return response

# DELETE book from author
@bp.delete("/<author_id>/books/<book_id>")
def delete_book_from_author(author_id, book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# UPDATE book from author
@bp.put("/<author_id>/books/<book_id>")
def update_book_from_author(author_id, book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")
