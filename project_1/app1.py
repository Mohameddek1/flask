from flask import Flask, request, jsonify

app = Flask(__name__)


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


@app.route('/')
def index():
    return "Hello world"

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        if len(books_list) > 0:
            return jsonify(books_list)
        else:
            "Nothing Found", 404
    
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        new_id = books_list[-1]['id']+1
        
        new_obj = {
            'id': new_id,
            'author': new_author,
            'language': new_lang,
            'title': new_title
        }
        
        books_list.append(new_obj)
        return jsonify(books_list), 201
    
@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book), 200
        return jsonify({"error": "Book not found"}), 404
    
    if request.method == 'PUT':
        for book in books_list:
            if book['id'] == id:
                book['author'] = request.form['author']
                book['language'] = request.form['language']
                book['title'] = request.form['title']
                
                updated_obj = {
                    'id': id,
                    'author': book['author'],
                    'language': book['language'],
                    'title': book['title']
                }
                
                return jsonify(updated_obj)
    
    if request.method == 'DELETE':
        for index, book in enumerate(books_list):
            if book['id'] == id:
                books_list.pop(index)
                return jsonify(books_list)
                

if __name__ == '__main__':
    app.run(debug=True)