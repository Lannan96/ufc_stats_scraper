
import mysql.connector

'''
# write a function in the database object that either connects to the database or creates once if it doesn't exist

db = mysql.connector.connect(
    host='localhost',
    user='username',
    passwd='password',
    database='database_name'
)

mycursor = db.cursor()

#mycursor.execute('CREATE DATABASE ufc_database')

# create table

mycursor.execute(('CREATE TABLE Fighter (fighterID int PRIMARY KEY AUTO_INCREMENT)'))
mycursor.execute('DESCRIBE Fighter')
for x in mycursor:
    print(x)


# create fight table


# function to insert values into a table 
def insert_fighters(fighters_list):
    for fighter in fighters_list:
        mycursor.execute('INSERT INTO FIGHTER (name, age) VALUES (%s, %s)', (fighter[0], fighter[1]))



def retrieve_fighters():
    mycursor.execute('SELECT * FROM Fighter')

'''

