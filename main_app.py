#importing Flask for using it as a Framework
from flask import Flask , request
#importing our DataBase
from flask_sqlalchemy import SQLAlchemy
app = Flask (__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.app_context().push()



#making a class for our database structure
class Books_data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(80), unique = True, nullable = False)
    author = db.Column(db.String(150))
    publisher = db.Column(db.String(200))

    def __repr__(self):
        return f"{self.id} - {self.author} - {self.book_name} - {self.publisher}"

#creating the first route or the first webpage when we launch our app
@app.route('/')
def index():
    return 'Hello World'

#creating the second page on the app to display the added data 
@app.route('/Books')
def get_books():
    books = Books_data.query.all()
    output = []
    for book in books:
        book_data = {'id' : book.id, 'author' : book.author,
                     'book_name': book.book_name, 'publisher': book.publisher
                     }
        output.append(book_data)
    return {'Books' : output}

#creating the third web page when we want to display our data by putting only the id and will display the data 
@app.route('/Books/<id>')
def get_id(id):
    book = Books_data.query.get(id)
    return {'id' : book.id, 'author' : book.author,'book_name': book.book_name, 'publisher': book.publisher}



#creating the a function based adding data to add data by using Pastman and using the 'POST' method
@app.route('/Books', methods= ['POST'])
def add_books():
    book = Books_data (book_name = request.json['book_name'], author = request.json['author'], publisher = request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id' : book.id, 'author' : book.author,'book_name': book.book_name, 'publisher': book.publisher}


#creating the a function based deleting data to delete data by using Pastman and using the 'DELETE' method

@app.route('/Books/<id>', methods = ['DELETE'])
def delete_book(id):
    book = Books_data.query.get(id)

    if book is None:
        return {'message': ' There is no record...'}
    
    db.session.delete(book)
    db.session.commit()

    return {'message':'Record Deleted!'}





#some database code for using it in you python terminal 
#the app will run by "flask --app main_app  run"
#db.create_all() will create a table
#db.session.add(class_name("attributes")) will add data into the table 
#db.session.commit() is a must to commit the changes into the database
#class_name will display the data











if __name__ == "__main__":
    app.run()