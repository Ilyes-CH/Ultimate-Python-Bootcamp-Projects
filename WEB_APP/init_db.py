import sqlite3

conn = sqlite3.connect("blog.db")
c = conn.cursor()

# users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
          username TEXT PRIMARY KEY,
          password TEXT NOT NULL
          )
''')

# Posts table
c.execute('''
CREATE TABLE IF NOT EXISTS posts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          author TEXT NOT NULL,
          content TEXT NOT NULL
          )
''')

conn.commit()
conn.close()