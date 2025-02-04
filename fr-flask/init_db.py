import os
import psycopg2
import json

#Environment Variables
# Database connection parameters should be in environment variables or a config file
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

conn = psycopg2.connect(
        host='localhost',
        database='filmrec',
        user='adminfr',
        password='Server123!')

# Open a cursor to perform database operations
cur = conn.cursor()

# Drop all tables if exist
cur.execute('DROP TABLE IF EXISTS preferences;')
cur.execute('DROP TABLE IF EXISTS watched_movies;')
cur.execute('DROP TABLE IF EXISTS do_not_recommend')
cur.execute('DROP TABLE IF EXISTS user_data;')
cur.execute('DROP TABLE IF EXISTS time_period')

# Creation of the time period table
cur.execute('''CREATE TABLE time_period (
                    time_period_id INTEGER PRIMARY KEY,
                    time_period VARCHAR(255) NOT NULL
            );''')

# Creation for the user_data table (passwords will be added later)
cur.execute('''CREATE TABLE user_data (
                    username VARCHAR(255) PRIMARY KEY NOT NULL,
                    password bytea NOT NULL
            );''')

# Creation for the preferences table (ADD TIME PERIOD, FOREIGN)
cur.execute("""
            CREATE TABLE preferences (
                username VARCHAR(255) PRIMARY KEY REFERENCES user_data(username),
                action BOOLEAN NOT NULL,
                adventure BOOLEAN NOT NULL,
                animation BOOLEAN NOT NULL,
                biography BOOLEAN NOT NULL,
                comedy BOOLEAN NOT NULL,
                crime BOOLEAN NOT NULL,
                documentary BOOLEAN NOT NULL,
                drama BOOLEAN NOT NULL,
                fantasy BOOLEAN NOT NULL,
                film_noir BOOLEAN NOT NULL,
                history BOOLEAN NOT NULL,
                horror BOOLEAN NOT NULL,
                music BOOLEAN NOT NULL,
                musical BOOLEAN NOT NULL,
                mystery BOOLEAN NOT NULL,
                romance BOOLEAN NOT NULL,
                sci_fi BOOLEAN NOT NULL,
                sport BOOLEAN NOT NULL,
                thriller BOOLEAN NOT NULL,
                war BOOLEAN NOT NULL,
                western BOOLEAN NOT NULL,
                ok_with_foreign BOOLEAN NOT NULL
            );
""")

# Creation of the watched_movies table
cur.execute('''
            CREATE TABLE watched_movies (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) REFERENCES user_data(username),
                movie_id VARCHAR(255) NOT NULL,
                movie_title VARCHAR(255) NOT NULL,
                favorite BOOLEAN NOT NULL,
                UNIQUE(username, movie_id)
            );
            ''')
#Creation of the do not recommend table
cur.execute('''
            CREATE TABLE do_not_recommend (
                username VARCHAR(255) NOT NULL,
                original_title VARCHAR(255) NOT NULL,
                CONSTRAINT fk_username FOREIGN KEY (username) REFERENCES user_data(username),
                CONSTRAINT pk_do_not_recommend PRIMARY KEY (username, original_title)
            );
''')
# cur.execute('''
#             CREATE TABLE tmdb (
#             adult BOOLEAN NOT NULL,
#             id INTEGER PRIMARY KEY NOT NULL,
#             original_title VARCHAR(255) NOT NULL,
#             popularity DECIMAL NOT NULL,
#             video BOOLEAN NOT NULL
#             );    
#             ''')

# # Read JSON data
# with open('fr-flask\movies.json', 'r', encoding='utf-8') as file:
#     for line in file:
#         # Parse each line (which is a JSON object) into a Python dictionary
#         movie = json.loads(line)

#         # Construct the INSERT query. Modify table_name and column names as per your database schema.
#         insert_query = "INSERT INTO tmdb (adult, id, original_title, popularity, video) VALUES (%s, %s, %s, %s, %s)"
        
#         # Execute the query with data from the JSON object
#         cur.execute(insert_query, (movie['adult'], movie['id'], movie['original_title'], movie['popularity'], movie['video']))
# # Insert test data into the user_data table
# cur.execute('''INSERT INTO user_data(user_id, username, password)
#                     VALUES 
#                         (1, 'jake', 'testpass'),
#                         (2, 'jake2', 'testpass1'),
#                         (3, 'jake3', 'testpass3');
#             ''')

# # Insert test data into the watched_movies table
# cur.execute('''INSERT INTO watched_movies (user_id, movie_id, movie_title) VALUES 
#                 (1, 'tt0111161', 'The Shawshank Redemption'), 
#                 (1, 'tt0068646', 'The Godfather'), 
#                 (1, 'tt0071562', 'The Godfather: Part II'), 
#                 (1, 'tt0468569', 'The Dark Knight'), 
#                 (1, 'tt0050083', '12 Angry Men'), 
#                 (1, 'tt0108052', 'Schindler''s List'), 
#                 (1, 'tt0167260', 'The Lord of the Rings: The Return of the King'), 
#                 (1, 'tt0110912', 'Pulp Fiction'), 
#                 (1, 'tt0060196', 'The Good, the Bad and the Ugly'), 
#                 (1, 'tt0137523', 'Fight Club'), 
#                 (1, 'tt0120737', 'The Lord of the Rings: The Fellowship of the Ring'), 
#                 (1, 'tt0109830', 'Forrest Gump'), 
#                 (1, 'tt1375666', 'Inception'), 
#                 (1, 'tt0080684', 'Star Wars: Episode V - The Empire Strikes Back'), 
#                 (1, 'tt0167261', 'The Lord of the Rings: The Two Towers'), 
#                 (1, 'tt0133093', 'The Matrix'), 
#                 (1, 'tt0073486', 'One Flew Over the Cuckoo''s Nest'), 
#                 (1, 'tt0099685', 'Goodfellas'), 
#                 (1, 'tt0047478', 'Seven Samurai'), 
#                 (1, 'tt0114369', 'Se7en'), 
#                 (1, 'tt0317248', 'City of God'), 
#                 (1, 'tt0118799', 'Life Is Beautiful'), 
#                 (1, 'tt0038650', 'It''s a Wonderful Life'), 
#                 (1, 'tt0076759', 'Star Wars'), 
#                 (1, 'tt0245429', 'Spirited Away');
#             ''')

# # Insert test data into the watched_movies table
# cur.execute('''INSERT INTO watched_movies (user_id, movie_id, movie_title) VALUES 
#                 (3, 'tt0111161', 'The Spongebob Movie'), 
#                 (3, 'tt0068646', 'How To Train Your Dragon'), 
#                 (3, 'tt0071562', 'The Dark Knight'), 
#                 (3, 'tt0468569', 'Boogie Nights'), 
#                 (3, 'tt0050083', 'Trainspotting'),
#                 (3, 'tt0050083', 'Red Rocket'), 
#                 (3, 'tt0050083', 'The Fifth Element');
#             ''')

# # Insert test data into preferences
# cur.execute('''
#     INSERT INTO preferences (
#         user_id, action, adventure, animation, biography, comedy, crime, documentary, drama,
#         fantasy, film_noir, history, horror, music, musical, mystery, romance, sci_fi, sport,
#         thriller, war, western, ok_with_foreign, time_period_id
#     ) VALUES
#     (1, true, false, true, false, true, false, true, false, true, false, false, true, false, false, true, false, true, false, true, false, false, true, 10),
#     (2, false, true, false, true, false, true, false, true, false, true, true, false, true, false, false, true, false, true, false, true, true, false, 8),
#     (3, true, true, true, false, true, false, false, false, true, false, false, false, true, false, true, false, true, true, false, false, false, false, 8);
# ''')

cur.execute('SELECT * FROM preferences')

rows = cur.fetchall()

for row in rows:
    print(row)

cur.execute('SELECT * FROM user_data')

rows = cur.fetchall()

for row in rows:
    print(row)

#Committing any changes and closing connections
conn.commit()
cur.close()
conn.close()
