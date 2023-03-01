from api_endpoint import base_url
import requests
import json
import pytest


@pytest.fixture
def issue_book_data():
    member_id = 7
    book_id = 12
    data = {"member_id": member_id, "book_id": book_id}
    return data

@pytest.fixture
def return_book_data():
    transaction_id=20
    data = {"transaction_id": transaction_id}
    return data
    
def test_add_book():
    url = f"{base_url}/book"
    data = {"title": "Testing Book", "author": "Test Author", "ISBN": "7890", "publisher": "Test Publisher", "page": 100, "stock": 5, "rent_fee": 100}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json()['book']['title'] == "Testing Book"

def test_get_book():
    url = f"{base_url}/book/2"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['book']['id'] == 2

def test_update_book():
    url = f"{base_url}/booku/7"
    data = {"title": "Updated Test Book"}
    response = requests.put(url, json=data)
    assert response.status_code == 200
    assert response.json()['book']['title'] == "Updated Test Book"

def test_delete_book():
    url = f"{base_url}/bookd/7"
    response = requests.delete(url)
    assert response.status_code == 200
    assert response.json()['result'] == "Book deleted"

def test_get_books():
    url = f"{base_url}/books"
    response = requests.get(url)
    assert response.status_code == 200

def test_add_member():
    url = f"{base_url}/membs"
    data = {"name": "Test Member", "address": "Test Address", "contact": "9898988879", "debt": 0}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json()['message'] == "Member added successfully"

def test_get_member():
    url = f"{base_url}/member/8"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['member']['id'] == 1

def test_update_member():
    url = f"{base_url}/memberu/8"
    data = {"name": "Updated Test Member"}
    response = requests.put(url, json=data)
    assert response.status_code == 200
    assert response.json()['member']['name'] == "Updated Test Member"

def test_delete_member():
    url = f"{base_url}/memberd/8"
    response = requests.delete(url)
    assert response.status_code == 200
    assert response.json()['result'] == "Member deleted"

def test_get_members():
    url = f"{base_url}/members"
    response = requests.get(url)
    assert response.status_code == 200

def test_issue_book(issue_book_data):
    response = requests.post(f"{base_url}/issue", json=issue_book_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Book issued successfully"


def test_issue_book_invalid_member_or_book(issue_book_data):
    response = requests.post(f"{base_url}/issue", json=issue_book_data)
    assert response.status_code == 404
    assert response.json()["message"] == "Member or Book not found"


def test_issue_book_outstanding_debt(issue_book_data):
    response = requests.post(f"{base_url}/issue", json=issue_book_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Member's outstanding debt is more than Rs. 500, book issue not possible."


def test_issue_book_exceeded_limit(issue_book_data):
    response = requests.post(f"{base_url}/issue", json=issue_book_data)
    assert response.status_code == 400
    assert response.json()["message"] == "The student has exceeded the limit of 20 books"


def test_issue_book_not_in_stock(issue_book_data):
    response = requests.post(f"{base_url}/issue", json=issue_book_data)
    assert response.status_code == 400
    assert response.json()["message"] == "Book is not in stock"


def test_return_book(return_book_data):
    response = requests.post(f"{base_url}/return", json=return_book_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Book returned successfully"


def test_return_book_not_found(return_book_data):
    response = requests.post(f"{base_url}/return", json=return_book_data)
    assert response.status_code == 404
    assert response.json()["message"] == "Transaction not found"


def test_return_book_already_returned(return_book_data):
    response = requests.post(f"{base_url}/return", json=return_book_data)
    assert response.status_code == 400
    assert response.json()["message"] == "Book has already been returned"


def test_highest_paying_customers():
    response = requests.get(f"{base_url}/high")
    assert response.status_code == 200
    


def test_most_popular_books():
    response = requests.get(f"{base_url}/pop")
    assert response.status_code == 200
    
