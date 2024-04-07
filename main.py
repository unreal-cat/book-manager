from quart import Quart, request, jsonify, send_file
from tools.base import BookLibrary 

app = Quart(__name__)  

# BookLibrary передаем название файла БАЗЫ ДАННЫХ
library = BookLibrary('tools/books.db')

# Маршрут для обработки запроса на главную страницу
@app.route('/')
async def get_index():
    # Отправляем файл index.html в качестве ответа
    return await send_file('templates/index.html')  

# Маршрут для добавления новой книги
@app.route('/books', methods=['POST'])
async def add_book():
    """Маршрут для добавления новой книги"""

    data = await request.json  # Получаем данные из запроса в формате JSON
    title = data.get('title')  # Извлекаем название книги из данных запроса
    author = data.get('author')  # Извлекаем автора книги из данных запроса
    description = data.get('description')  # Извлекаем описание книги из данных запроса
    genre = data.get('genre')  # Извлекаем жанр книги из данных запроса

    # Проверяем, все ли обязательные поля заполнены
    if not all([title, author, genre]):
        
        # Возвращаем ошибку 400, если не все поля заполнены
        return jsonify({"error": "Не все обязательные поля заполнены"}), 400  

    library.add_book(title, author, description, genre)  # Добавляем книгу в библиотеку
    return jsonify({"message": "Книга успешно добавлена"}), 201  # Возвращаем сообщение об успешном добавлении книги

# Маршрут для получения списка всех книг
@app.route('/books', methods=['GET'])
async def get_books():
    # Возвращаем список всех книг в формате JSON
    return jsonify(library.get_all_books())

# Маршрут для получения списка книг по заданному жанру
@app.route('/books/genre/<string:genre>', methods=['GET'])
async def get_books_by_genre(genre):
    # Возвращаем список книг по заданному жанру в формате JSON
    return jsonify(library.get_books_by_genre(genre))  

# Маршрут для поиска книги по ключевому слову
@app.route('/books/search', methods=['GET'])
async def search_book():
    # Получаем ключевое слово для поиска из параметров запроса
    keyword = request.args.get('keyword') 
    if not keyword:
        # Возвращаем ошибку 400, если ключевое слово не указано
        return jsonify({"error": "Необходимо указать ключевое слово для поиска"}), 400  

    result = library.search_books(keyword)  # Ищем книги по ключевому слову
    return jsonify(result)  # Возвращаем результаты поиска в формате JSON

# Маршрут для удаления книги по её идентификатору
@app.route('/books/<int:book_id>', methods=['DELETE'])
async def delete_book(book_id):
    library.delete_book(book_id)  # Удаляем книгу из библиотеки по её идентификатору
    return jsonify({"message": "Книга успешно удалена"})  # Возвращаем сообщение об успешном удалении книги

# Запускаем приложение в режиме отладки, если файл является точкой входа
if __name__ == '__main__':
    app.run(debug=True)  
