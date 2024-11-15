from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.Error as e:
        print(e)
    
    return conn

"""
books_list = [
    {"id": 1, "author": "George Orwell", "language": "English", "title": "1984"},
    {"id": 2, "author": "Haruki Murakami", "language": "Japanese", "title": "Kafka on the Shore"},
    {"id": 3, "author": "Gabriel García Márquez", "language": "Spanish", "title": "One Hundred Years of Solitude"},
    {"id": 4, "author": "Chinua Achebe", "language": "English", "title": "Things Fall Apart"},
    {"id": 5, "author": "Fyodor Dostoevsky", "language": "Russian", "title": "Crime and Punishment"},
    {"id": 6, "author": "Jane Austen", "language": "English", "title": "Pride and Prejudice"},
    {"id": 7, "author": "J.K. Rowling", "language": "English", "title": "Harry Potter and the Sorcerer's Stone"},
    {"id": 8, "author": "J.R.R. Tolkien", "language": "English", "title": "The Hobbit"},
    {"id": 9, "author": "Isabel Allende", "language": "Spanish", "title": "The House of the Spirits"},
    {"id": 10, "author": "Albert Camus", "language": "French", "title": "The Stranger"}
]
"""

@app.route('/')
def index():
    return "Hello world"

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM book")
        books = [
            {"id": row[0], "author": row[1], "language": row[2], "title": row[3]}
            for row in cursor.fetchall()
        ]
        conn.close()

        if books is not None:
            return jsonify(books), 200
    
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO book (author, language, title)
                 VALUES (?, ?, ?)"""
        
        cursor = cursor.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created successful", 201

       
    
@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book where id=?", (id,))
        rows = cursor.fetchone()
        # rows = cursor.fetchall
        
        # for r in rows:
        #     book = r
        
        # if book is not None:
        #     return jsonify(book), 200
        # else:
        #     return jsonify({"error": "Book not found"}), 404


        if rows:
            book =  {"id": rows[0], "author": rows[1], "language": rows[2], "title": rows[3]}
            return jsonify(book), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    
    if request.method == 'PUT':
        sql = """UPDATE book
                SET author=?,
                    language=?,
                    title=?
                WHERE id=?"""
        
        updated_author = request.form['author']
        updated_language = request.form['language']
        updated_title = request.form['title']
        
        updated_obj = {
            'id': id,
            'author': updated_author,
            'language': updated_language,
            'title': updated_title
        }
                
        conn.execute(sql, (updated_author, updated_language, updated_title, id))
        conn.commit()
        return jsonify(updated_obj)
    
    if request.method == 'DELETE':
        sql = """DELETE from book where id=?"""
        conn.execute(sql, (id,))
        conn.commit()
        return "The book with id: {} has been deleted".format(id), 200
                

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')