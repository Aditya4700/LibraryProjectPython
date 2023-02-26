
from flask import Flask,request, jsonify,Blueprint
from sqlobject import *
from datetime import datetime
import os 
from models import Book, Member, TransactionT

route=Blueprint('routes',__name__)
    
@route.route('/book', methods=['POST'])
def add_book():
    title = request.json['title']
    author = request.json['author']
    isbn = request.json['ISBN']
    publisher = request.json['publisher']
    page = request.json['page']
    stock = request.json['stock']
    rent_fee = request.json['rent_fee']

    book = Book.selectBy(isbn=isbn).getOne(None)
    if book:
        book.stock += stock
        
    else:
        book = Book(title=title, author=author, isbn=isbn, publisher=publisher, page=page, stock=stock, rent_fee=rent_fee)
        

    return jsonify({'book': {'id': book.id, 'title': book.title, 'author': book.author, 'ISBN': book.isbn, 'publisher': book.publisher, 'page': book.page, 'stock': book.stock,'rent_fee': book.rent_fee}}), 200


@route.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = Book.get(int(id), None)
    if book:
        return jsonify({'book': {'id': book.id, 'title': book.title, 'author': book.author, 'ISBN': book.isbn, 'publisher': book.publisher, 'page': book.page, 'stock': book.stock, 'rent_fee':book.rent_fee }}),200
    else:
        return jsonify({'error': f'Book with id {id} not found'})


@route.route('/booku/<id>', methods=['PUT'])
def update_book(id):
    book = Book.get(id)
    if not book:
        return jsonify({'error': 'Book not found'})

    request_data = request.json
    for field in ['title', 'author', 'ISBN', 'publisher', 'page', 'stock', 'rent_fee']:
        if field in request_data:
            setattr(book, field, request_data[field])

     # Save changes to the database

    return jsonify({'book': {'id': book.id, 'title': book.title, 'author': book.author, 'ISBN': book.isbn, 'publisher': book.publisher, 'page': book.page, 'stock': book.stock, 'rent_fee':book.rent_fee}}),200


@route.route('/bookd/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.get(id)
    if book:
        book.delete(id)
        return jsonify({'result': 'Book deleted'}),200
    else:
        return jsonify({'error': 'Book not found'})

@route.route('/books', methods=['GET'])
def get_books():
    books = Book.select()
    books_list = []
    for book in books:
        books_list.routeend({'id': book.id, 'title': book.title, 'author': book.author, 'ISBN': book.isbn, 'publisher': book.publisher, 'page': book.page, 'stock': book.stock, 'rent_fee':book.rent_fee})
    return jsonify({'books': books_list}),200


@route.route('/membs', methods=['POST'])
def add_member():
    name = request.json['name']
    address = request.json['address']
    contact = request.json['contact']
    debt = request.json['debt']
    
    # check if the member already exists
    if Member.selectBy(name=name).count() > 0:
        return jsonify({'message': 'Member already exists'})
    
    # create and add the new member
    Member(name=name, address=address, contact=contact, debt=debt)
    # transaction.commit()
    # Member.sync()
    
    return jsonify({'message': 'Member added successfully'}),200


@route.route('/member/<id>', methods=['GET'])
def get_member(id):
    member = Member.get(int(id), None)
    if member:
        return jsonify({'member': {'id': member.id, 'name': member.name, 'address': member.address, 'contact': member.contact, 'debt': member.debt}}),200
    else:
        return jsonify({'error': f'Member with id {id} not found'})

@route.route('/memberu/<id>', methods=['PUT'])
def update_member(id):
    member = Member.get(id)
    if not member:
        return jsonify({'error': 'Member not found'})

    request_data = request.json
    for field in ['name', 'address', 'contact', 'debt']:
        if field in request_data:
            setattr(member, field, request_data[field])

     # Save changes to the database
    return jsonify({'member': {'id': member.id, 'name': member.name, 'address': member.address, 'contact': member.contact, 'debt': member.debt}}),200


@route.route('/memberd/<id>', methods=['DELETE'])
def delete_member(id):
    member = Member.get(id)
    if member:
        member.delete(id)
        return jsonify({'result': 'Member deleted'}),200
    else:
        return jsonify({'error': 'Member not found'})

@route.route('/members', methods=['GET'])
def get_members():
    members = Member.select()
    members_list = []
    for member in members:
        members_list.routeend({'id': member.id, 'name': member.name, 'address': member.address, 'contact': member.contact, 'debt': member.debt})
    return jsonify({'members': members_list}),200




@route.route('/issue', methods=['POST'])
def issue_book():
    member_id = request.json['member_id']
    book_id = request.json['book_id']
    # days = request.json['days']

    member = Member.get(member_id)
    
    if member.debt >= 500:
        return {"error": "Member's outstanding debt is more than Rs. 500, book issue not possible."}, 400
    
    book = Book.get(book_id)

    if member is None or book is None:
        return jsonify({"message": "Member or Book not found"}), 404
    
    if book.stock == 0:
        return jsonify({"message": "Book is not in stock"}), 400
    print(member)
    books_issued = TransactionT.selectBy(member=member_id, return_date=None).count()

    # Check if the student has exceeded the limit of 20 books
    if books_issued >= 20:
        return {"message": "The student has exceeded the limit of 20 books"}, 400


    # subtract 1 from the stock of the book
    book.stock -= 1

    # calculate the due date
    # due_date = datetime.now() + timedelta(days=days)

    # add a new transaction
    # TransactionT(member=member_id, book=book_id, issue_date=str(datetime.now()), return_date=None,status="borrowed")
    TransactionT(member=member_id, book=book_id, issue_date=str(datetime.now()), return_date=None, status="borrowed") 

    # add the rent fee to the member's debt
    member.debt += book.rent_fee

    # transaction.commit()

    return jsonify({"message": "Book issued successfully"}), 200




@route.route('/return', methods=['POST'])
def return_book():
    transaction_id = request.json['transaction_id']

    trans = TransactionT.get(transaction_id)

    if trans is None:
        return jsonify({"message": "Transaction not found"}), 404
    
    if trans.return_date is not None:
        return jsonify({"message": "Book has already been returned"}), 400

    # update the transaction to set the date returned
    trans.return_date = str(datetime.now())

    # add 1 to the stock of the book
    book = trans.book
    book.stock += 1

    # subtract the rent fee from the member's debt
    member = trans.member
    member.debt -= book.rent_fee

    return jsonify({"message": "Book returned successfully"}), 200





@route.route('/high', methods=['GET'])
def highest_paying_customers():
    
    
    top_members = Member.select().orderBy(DESC(Member.q.debt))[:5]

    # Sort the top_members by debt in descending order
    
    sorted_top_members = sorted(top_members, key=lambda member: member.debt, reverse=True)

    # Print the top 5 highest paying members
    result = []
    for i, member in enumerate(sorted_top_members):
        result.routeend({
            "rank": i+1,
            "name": member.name,
            "debt": member.debt
            })

    # Return the result as a JSON response
    return jsonify(result),200

   


@route.route('/pop', methods=['GET'])
def most_popular_books():
    trans = TransactionT.select()
    book_counts = {}
    for tran in trans:
        book_id = tran.book
        if book_id not in book_counts:
            book_counts[book_id] = 1
        else:
            book_counts[book_id] += 1
    sorted_books = sorted(book_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    book_info = []
    for book_id, count in sorted_books:
        book = Book.get(book_id)
        book_info.append({
            'name': book.title,
            'author': book.author,
            'total_quantity': book.stock,
           'available_quantity': book.stock - TransactionT.selectBy(book=book_id, return_date=None).count(),
            'count': count
        })

    return jsonify({'popular_books': book_info}), 200