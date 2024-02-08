# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class UfcScraperPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='Ashtead96',
            database='ufc_database')
        
        # create a cursor object using the cursor() method
        self.cursor = self.conn.cursor()
        
        # create table if none exists
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Fighter (fighterID int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), age INT)')
    

    def process_item(self, item, spider):
        
        # insert values into the table  
        self.cursor.execute('INSERT INTO FIGHTER (name, age) VALUES (%s, %s)',
                            (item['name'],
                             item['age']))
        
        # commit the transaction
        self.conn.commit()
    
    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()
    

