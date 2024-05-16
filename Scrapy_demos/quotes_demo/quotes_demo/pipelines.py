# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import mysql.connector
from pymongo import MongoClient

## this class contains logic to save data in sqlite3 db
class QuotesDemoPipeline:

    def __init__(self) -> None:
        self.create_connection()    ### Create the connection with sqlite3db
        self.create_table()         ### Create a table withing sqlite3 database 


    def create_connection(self):
        self.connection = sqlite3.connect("myquotes.db")
        self.curr = self.connection.cursor()

    def create_table(self):
        self.curr.execute('''drop table if exists quotes_tb''')
        self.curr.execute('''create table quotes_tb(
             quote text,author text,tag text
             )''')

    def store_data(self,item):
        # Logic to add data inside table
        # self.curr.execute('''insert into quotes_tb values(item['quotes'][-1],item['author'][-1],' , '.join(item['tags']))''')
        self.curr.execute('''insert into quotes_tb values(?,?,?)''',(item['quotes'][-1],item['author'][-1],' , '.join(item['tags']))) 
        self.connection.commit()   

    def process_item(self, item, spider):
        # Logic to save data
        # print("Pipeline ----", item)
        self.store_data(item)
        return item
    
    def close_spider(self):
        self.curr.close()
        self.connection.close()


## this class contains logic to save data in mysql db
class StoreMySQL:

    def __init__(self):
        self.create_connection()
        self.create_table()
        

    def create_connection(self):
        self.connection = mysql.connector.connect(host='localhost',
                                                  user='root',
                                                  passwd='MySQL@12',
                                                  database='myquotes')
        self.curr = self.connection.cursor()

    def create_table(self):
        self.curr.execute('''drop table if exists quotes_tb''')
        self.curr.execute('''create table quotes_tb(
             quote text,author text,tag text
             )''')
        

    def store_data(self,item):
        # Logic to add data inside table
        # self.curr.execute('''insert into quotes_tb values(item['quotes'][-1],item['author'][-1],' , '.join(item['tags']))''')
        self.curr.execute('''insert into quotes_tb values(%s, %s, %s)''',(item['quotes'][-1],item['author'][-1],' , '.join(item['tags']))) 
        self.connection.commit()   

    def process_item(self, item, spider):
        # Logic to save data
        # print("Pipeline ----", item)
        self.store_data(item)
        return item
    
    # #cleanup by closing connections to database
    def close_spider(self):
        self.curr.close()
        self.connection.close()


class storeMongoDB:


    def __init__(self):
        # Create a connection
        client=MongoClient("mongodb://localhost:27017")

        # Connect to a database named myquotes
        self.db = client['myquotes']

        # Create a collection inside a database
        self.quotes_collection = self.db['quotes_tb']

    def process_item(self,item,spider):
        # adding the logic to store data in colleciton
        self.quotes_collection.insert_one(dict(item))
        return item 

    def close_spider(self, spider):
        self.db.client.close()
        
        




    
