
import requests
import json

def test_add_book():
    url = 'http://127.0.0.1:5000/book'
    data = {"title": "Testing Book", "author": "Test Author", "ISBN": "7890", "publisher": "Test Publisher", "page": 100, "stock": 5, "rent_fee": 100}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json()['book']['title'] == "Testing Book"

def test_get_book():
    url = 'http://127.0.0.1:5000/book/2'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['book']['id'] == 2

def test_update_book():
    url = 'http://127.0.0.1:5000/booku/7'
    data = {"title": "Updated Test Book"}
    response = requests.put(url, json=data)
    assert response.status_code == 200
    assert response.json()['book']['title'] == "Updated Test Book"

def test_delete_book():
    url = 'http://127.0.0.1:5000/bookd/7'
    response = requests.delete(url)
    assert response.status_code == 200
    assert response.json()['result'] == "Book deleted"

def test_get_books():
    url = 'http://127.0.0.1:5000/books'
    response = requests.get(url)
    assert response.status_code == 200
   


def test_add_member():
    url = 'http://127.0.0.1:5000/membs'
    data = {"name": "Test Member", "address": "Test Address", "contact": "9898988879", "debt": 0}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json()['message'] == "Member added successfully"

def test_get_member():
    url = 'http://127.0.0.1:5000/member/8'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['member']['id'] == 1

def test_update_member():
    url = 'http://127.0.0.1:5000/memberu/8'
    data = {"name": "Updated Test Member"}
    response = requests.put(url, json=data)
    assert response.status_code == 200
    assert response.json()['member']['name'] == "Updated Test Member"

def test_delete_member():
    url = 'http://127.0.0.1:5000/memberd/8'
    response = requests.delete(url)
    assert response.status_code == 200
    assert response.json()['result'] == "Member deleted"

def test_get_members():
    url = 'http://127.0.0.1:5000/members'
    response = requests.get(url)
    assert response.status_code == 200


base_url = "http://127.0.0.1:5000"


def test_issue_book():
    member_id = 5
    book_id = 5
    data = {"member_id": member_id, "book_id": book_id}
    response = requests.post(f"{base_url}/issue", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Book issued successfully"


def test_issue_book_invalid_member_or_book():
    member_id = 100
    book_id = 100
    data = {"member_id": member_id, "book_id": book_id}
    response = requests.post(f"{base_url}/issue", json=data)
    assert response.status_code == 404
    assert response.json()["message"] == "Member or Book not found"


def test_issue_book_outstanding_debt():
    member_id = 12
    book_id = 4
    data = {"member_id": member_id, "book_id": book_id}
    response = requests.post(f"{base_url}/issue", json=data)
    assert response.status_code == 400
    assert response.json()["error"] == "Member's outstanding debt is more than Rs. 500, book issue not possible."


def test_issue_book_exceeded_limit():
    member_id = 3
    book_id = 4
    data = {"member_id": member_id, "book_id": book_id}
    response = requests.post(f"{base_url}/issue", json=data)
    assert response.status_code == 400
    assert response.json()["message"] == "The student has exceeded the limit of 20 books"


def test_issue_book_not_in_stock():
    member_id = 7
    book_id = 12
    data = {"member_id": member_id, "book_id": book_id}
    response = requests.post(f"{base_url}/issue", json=data)
    assert response.status_code == 400
    assert response.json()["message"] == "Book is not in stock"


def test_return_book():
    transaction_id = 2
    data = {"transaction_id": transaction_id}
    response = requests.post(f"{base_url}/return", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Book returned successfully"


def test_return_book_not_found():
    transaction_id = 100
    data = {"transaction_id": transaction_id}
    response = requests.post(f"{base_url}/return", json=data)
    assert response.status_code == 404
    assert response.json()["message"] == "Transaction not found"


def test_return_book_already_returned():
    transaction_id = 1
    data = {"transaction_id": transaction_id}
    response = requests.post(f"{base_url}/return", json=data)
    assert response.status_code == 400
    assert response.json()["message"] == "Book has already been returned"


def test_highest_paying_customers():
    response = requests.get(f"{base_url}/high")
    assert response.status_code == 200
    # assert len(response.json()) == 5


def test_most_popular_books():
    response = requests.get(f"{base_url}/pop")
    assert response.status_code == 200
    # assert len(response.json()["popular_books"]) == 5
