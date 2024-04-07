import sqlite3

# Класс для управления базой данных книг
class BookLibrary:
    def __init__(self, db_name: str):
        # Устанавливаем соединение с базой данных и создаем курсор
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Создаем таблицу книг, если она еще не существует
        self.create_table()

    # Метод для создания таблицы books
    def create_table(self):
        """Метод для создания таблицы books"""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books
        (id INTEGER PRIMARY KEY, title TEXT, author TEXT, description TEXT, genre TEXT)''')
        self.conn.commit()

    # Метод для добавления новой книги в базу данных
    def add_book(self, title: str, author: str, description: str, genre: str):
        """Метод для добавления новой книги в базу данных
        :params title: Заголовок (название) книги
        :params author: Автори книги
        :params description: Описание книги
        :params genre: Жанр (название) книги"""
    
        self.cursor.execute("INSERT INTO books (title, author, description, genre) VALUES (?, ?, ?, ?)",
        (title, author, description, genre))
        self.conn.commit()

    # Метод для получения списка всех книг из базы данных
    def get_all_books(self):
        """Метод для получения списка всех книг из базы данных"""
        self.cursor.execute("SELECT id, title, author FROM books")
        return self.cursor.fetchall()

    # Метод для получения списка книг определенного жанра из базы данных
    def get_books_by_genre(self, genre: str):
        """Метод для получения списка книг определенного жанра из базы данных"""
        self.cursor.execute("SELECT id, title, author FROM books WHERE genre=?", (genre,))
        return self.cursor.fetchall()

    # Метод для поиска книги по названию или автору в базе данных
    def search_books(self, keyword: str):
        """Метод для поиска книги по названию или автору в базе данных"""
        self.cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%'+keyword+'%', '%'+keyword+'%'))
        return self.cursor.fetchall()

    # Метод для удаления книги из базы данных по идентификатору
    def delete_book(self, book_id: int):
        """Метод для удаления книги из базы данных по идентификатору"""
        self.cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.conn.commit()
