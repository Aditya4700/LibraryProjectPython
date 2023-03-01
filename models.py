from sqlobject import *
from datetime import datetime
import os 


db_filename= os.path.abspath("lib.sqlite")
conn = 'sqlite:' + db_filename
connection = connectionForURI(conn)
sqlhub.processConnection = connection




class Book(SQLObject):
    title = StringCol(length=100, notNone=True)
    author = StringCol(length=100, notNone=True)
    isbn = StringCol(length=13, notNone=True)
    publisher = StringCol(length=100, notNone=True)
    page = IntCol(notNone=True)
    stock = IntCol(notNone=True)
    rent_fee = IntCol(notNone=True)
    
Book.createTable(ifNotExists=True)    

   
  
class Member(SQLObject):
    name = StringCol(length=100, notNone=True)
    address = StringCol(length=100, notNone=True)
    contact = StringCol(length=100, notNone=True)
    debt = IntCol(notNone=True)
    paid_money= IntCol(default=0, notNone=True)
Member.createTable(ifNotExists=True)
    
class TransactionT(SQLObject):
    member=IntCol(notNone=True)
    book=IntCol(notNone=True)
    issue_date=StringCol(length=100)
    return_date=StringCol(length=100)
    status=StringCol(length=100)
TransactionT.createTable(ifNotExists=True)    
    
        
