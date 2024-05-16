import sqlite3

connection = sqlite3.connect("myquotes.db")

curr = connection.cursor()

# Create Table

# curr.execute('''create table quotes_tb(
#              quote text,author text,tag text
#              )''')

## Add data in table quotes_tb

curr.execute('''insert into quotes_tb values('Scrapy is awesome', 'Zyte', 'Web Scrapping')''')

connection.commit()
connection.close()