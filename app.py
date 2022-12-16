
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy import update
import requests
import json

from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    stockQty = db.Column(db.Integer, nullable=False, default=0)
    timesIssued = db.Column(db.Integer, nullable=False, default=0)
    
    def __repr__(self):
        return 'Book'+str(self.book_id)

        
class Customer(db.Model):
    __tablename__ = 'customer'
    cust_id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String(255), nullable=False)
    debt = db.Column(db.Integer, nullable=False, default=0)
    total_trans = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return 'Customer '+str(self.cust_id)


transactions = db.Table('transactions',
    db.Column('trans_id', db.Integer, primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('customer.cust_id')),
    db.Column('cust_id', db.Integer, db.ForeignKey('books.book_id')),
    db.Column('cost', db.Integer, nullable=False, default=0),
    db.Column('status', db.String(25), nullable=False, default="live"),
    db.Column('issue_date', db.DateTime, default=datetime.now())
)

@app.before_first_request
def create_tables():
    db.create_all()
    # new_book =Books(title="Life of Teenager",authors="Grejo Joby",stockQty=10,timesIssued=0)
    # db.session.add(new_book)
    # db.session.commit()
    # new_customer =Customer(name="Hayden Cordeiro")
    # db.session.add(new_customer)
    # db.session.commit()


@app.route('/')
def index():
    
    most_popular=Books.query.order_by(Books.timesIssued.desc()).limit(5).all()
    least_stock=Books.query.order_by(Books.stockQty).limit(5).all()
    highest_paying=Customer.query.order_by(Customer.total_trans.desc()).limit(5).all()
    highest_debt=Customer.query.order_by(Customer.debt.desc()).limit(5).all()
    sum = Books.query.with_entities(func.sum(Books.stockQty).label('total')).first().total
    total_debt = Customer.query.with_entities(func.sum(Customer.debt).label('total')).first().total
    customer_count=Customer.query.count()
    total_titles=Books.query.count()
    total_issues=db.session.query(transactions).count()
    total_amount = db.session.query(transactions).with_entities(func.sum(transactions.c.cost).label('total')).first().total

    return render_template('index.html',most_popular=most_popular,highest_paying=highest_paying,
                                        total_books=sum,total_customer=customer_count,
                                        total_issues=total_issues,highest_debt=highest_debt,
                                        least_stock=least_stock,total_amount=total_amount,
                                        total_titles=total_titles,total_debt=total_debt)


@app.route('/books')
def books():
    all_books=Books.query.all()
    return render_template('books.html', all_books=all_books)

@app.route('/add_books', methods=['GET', 'POST'])
def add_books():
    if request.method=='POST':
        book_id=int(request.form['book_id'])
        book_title=request.form['title']
        book_author=request.form['author']
        book_stockQty=request.form['stockQty']
        new_book =Books(title=book_title,authors=book_author,stockQty=book_stockQty,timesIssued=0)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/books')

    else:
        return render_template('add_books.html')

@app.route('/books/edit/<int:id>', methods=['GET', 'POST'])
def update_book(id):
    book = Books.query.filter_by(book_id=id).first()
    if request.method=='POST':
        title=request.form['title']
        authors=request.form['authors']
        stockQty=request.form['stockQty']
        book.title = title
        book.authors = authors
        book.stockQty = stockQty
        db.session.commit()
        return redirect('/books')
    else:
        return render_template('edit_book.html',book=book)
    
@app.route('/books/delete/<int:id>')
def delete_book(id):
    book=Books.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/books')

@app.route('/issue_book', methods=['GET', 'POST'])
@app.route('/issue_book/<int:id>', methods=['GET','POST'])
def issue_book(id=1):
    if request.method=='POST':
        book_id=int(request.form['book_id'])
        cust_id=int(request.form['cust_id'])
        book = Books.query.filter_by(book_id=book_id).first()
        book.timesIssued += 1
        book.stockQty -= 1
        t = transactions.insert().values(book_id=book_id,cust_id=cust_id)
        db.engine.execute(t)
        db.session.commit()
        return redirect('/return_issue')
    elif request.method=='GET':
        return render_template('issue_book.html',id=id)
    else:
        return render_template('issue_book.html')

@app.route('/return_issue', methods=['GET', 'POST'])
def return_issue():
    issued_books=db.session.query(transactions).all()
    books_issued=[]
    for book in issued_books:
        bi = []
        bi.append(book.trans_id)
        bi.append(book.book_id)
        book_title = Books.query.filter_by(book_id=book[1]).one()
        bi.append(book_title.title)
        bi.append(book.cust_id)
        cust_details = Customer.query.filter_by(cust_id=book[2]).one()
        bi.append(cust_details.name)
        bi.append(book.cost)
        date = book.issue_date.date()
        bi.append(date)
        bi.append(book.status)
        print(bi)
        books_issued.append(bi)
    return render_template('return_issue.html',issued_books=books_issued)

@app.route('/books/return/<int:id>', methods=['GET', 'POST'])
def return_book(id):
    if request.method=='POST':
        costForm=int(request.form['cost'])
        cust_id = int(request.form['cust_id'])

        stmt1 = ( update(transactions).where(transactions.c.trans_id == id).values(cost = costForm))
        stmt2 = ( update(transactions).where(transactions.c.trans_id == id).values(status = "closed"))
        db.engine.execute(stmt1)
        db.engine.execute(stmt2)
        cust = Customer.query.filter_by(cust_id=cust_id).first()
        cust.total_trans += costForm
        cust.debt += costForm

        db.session.commit()
    return redirect('/return_issue')


@app.route('/customers')
def customers():
    all_customers=Customer.query.all()
    return render_template('customers.html', all_customers=all_customers)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method=='POST':
        cust_id=int(request.form['cust_id'])
        name=request.form['name']
        new_customer =Customer(name=name)
        db.session.add(new_customer)
        db.session.commit()
        return redirect('/customers')

    else:
        return render_template('add_customer.html')
    
@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def update_customer(id):
    cust = Customer.query.filter_by(cust_id=id).first()
    if request.method=='POST':
        name=request.form['name']
        cust.name = name
        db.session.commit()
        return redirect('/customers')
    else:
        return render_template('edit_customer.html',cust=cust)
    
@app.route('/customers/delete/<int:id>')
def delete_customers(id):
    customer=Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect('/customers')

@app.route('/customers/pay/<int:id>', methods=['GET', 'POST'])
def pay_dues(id):
    cust = Customer.query.filter_by(cust_id=id).first()
    if request.method=='POST':
        due=int(request.form['due'])
        cust.debt -= due
        db.session.commit()
        return redirect('/customers')
    else:
        return render_template('pay_dues.html',cust=cust)

@app.route('/books_store/<int:id>/<search>', methods=['GET', 'POST'])
@app.route('/books_store/<int:id>', methods=['GET', 'POST'])
@app.route('/books_store', methods=['GET', 'POST'])
def books_store(id=1,search=''):
    if request.method=='POST' or search != "":
        try:
            search=request.form['search_box']
        except:
            pass
        if not search=="":
            r = requests.get('https://frappe.io/api/method/frappe-library?title='+search+'&page='+str(id))
        # result = request.get_json("https://frappe.io/api/method/frappe-library?title="+search)
            print(r)
            return render_template('books_store.html',books=json.loads(r.text)['message'],search=search,page_no=id+1)
        else:
            return render_template('books_store.html')    

    else:
        return render_template('books_store.html')

@app.route('/books/import/<int:id>', methods=['GET', 'POST'])
def import_book(id):
    r = requests.get('https://frappe.io/api/method/frappe-library?isbn='+str(id))
    book_details = json.loads(r.text)['message'][0]
    book_title=book_details["title"]
    book_author=book_details["authors"]
    book_stockQty=request.form['qty']
    new_book =Books(title=book_title,authors=book_author,stockQty=book_stockQty,timesIssued=0)
    db.session.add(new_book)
    db.session.commit()
    return redirect('/books')


if __name__ == '__main__':
    # try:
    #     new_book =Books(book_id=1,title="book_title",authors="book_author",stockQty=0,timesIssued=0)
    #     db.session.add(new_book)
    #     db.session.commit()
    #     new_customer =Customer(cust_id=1,name="name")
    #     db.session.add(new_customer)
    #     db.session.commit()
    # except:
    #     pass
    
    app.run(host='0.0.0.0',port=7070,debug=True)
    
