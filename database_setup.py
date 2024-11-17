# database_setup.py
import psycopg2

def create_connection(db_name, user, password, host, port):
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Successfully connected to the database")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def setup_database(connection):
    cursor = connection.cursor()

    # Створення таблиць
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Movies (
        movie_id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        genre VARCHAR(50),
        duration INTEGER,
        rating DECIMAL(3, 2)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cinemas (
        cinema_id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        ticket_price DECIMAL(5, 2),
        seat_count INTEGER,
        address VARCHAR(200),
        phone VARCHAR(15)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Showings (
        showing_id SERIAL PRIMARY KEY,
        movie_id INTEGER REFERENCES Movies(movie_id),
        cinema_id INTEGER REFERENCES Cinemas(cinema_id),
        start_date DATE,
        duration_days INTEGER
    );
    """)

    # Заповнення таблиць тестовими даними
    cursor.execute("""
    INSERT INTO Movies (title, genre, duration, rating) VALUES
    ('Romantic Love', 'Melodrama', 120, 7.5),
    ('Comedy Night', 'Comedy', 90, 8.3),
    ('Action Hero', 'Action', 140, 8.7),
    ('Drama Story', 'Melodrama', 110, 7.9),
    ('Funny Moments', 'Comedy', 100, 7.4),
    ('Action Legends', 'Action', 150, 8.9),
    ('Silent Tears', 'Melodrama', 105, 7.2),
    ('Laughter Therapy', 'Comedy', 95, 8.0),
    ('Heroic Journey', 'Action', 130, 8.5),
    ('Romantic Escape', 'Melodrama', 125, 7.3),
    ('Laugh Out Loud', 'Comedy', 105, 7.8);
    """)

    cursor.execute("""
    INSERT INTO Cinemas (name, ticket_price, seat_count, address, phone) VALUES
    ('Cinema City', 10.00, 200, '123 Cinema St', '555-1234'),
    ('Film Palace', 12.50, 250, '456 Movie Ave', '555-5678'),
    ('Galaxy Theaters', 15.00, 300, '789 Star Rd', '555-9876');
    """)

    cursor.execute("""
    INSERT INTO Showings (movie_id, cinema_id, start_date, duration_days) VALUES
    (1, 1, '2024-11-10', 7),
    (2, 2, '2024-11-11', 5),
    (3, 3, '2024-11-12', 10),
    (4, 1, '2024-11-13', 6),
    (5, 2, '2024-11-14', 8),
    (6, 3, '2024-11-15', 7),
    (7, 1, '2024-11-16', 5),
    (8, 2, '2024-11-17', 10),
    (9, 3, '2024-11-18', 9),
    (10, 1, '2024-11-19', 6),
    (11, 2, '2024-11-20', 7);
    """)

    # Збереження змін
    connection.commit()
    cursor.close()
    print("Database setup complete.")

# Використання
if __name__ == "__main__":
    connection = create_connection("postgres", "admin", "root", "127.0.0.1", "5432")
    if connection:
        setup_database(connection)
        connection.close()
