# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from datetime import datetime


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
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS Fighter (fighter_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), height INT, weight INT, reach INT,stance VARCHAR(255), dob DATE, SLpM FLOAT, str_acc FLOAT, SApM FLOAT, str_def FLOAT, TD_avg FLOAT, TD_acc FLOAT, TD_def FLOAT, sub_avg FLOAT)')
    

    def process_item(self, item, spider):
        
        # Format data before inserting into the database
        formatted_item = self.format_data(item)
        
        # check if the fighter is already in the database
        self.cursor.execute('SELECT * FROM Fighter WHERE fighter_id = %s', (formatted_item['fighter_id'],))
        result = self.cursor.fetchone()
        if result:
            spider.logger.info(f'Fighter {formatted_item["name"]} already in the database')
        else:
        
            # insert values into the table  
            self.cursor.execute(
                'INSERT INTO FIGHTER (fighter_id, name, height, weight, reach, stance, dob, SLpM, str_acc, SApM, str_def, TD_avg, TD_acc, TD_def, sub_avg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                (item['fighter_id'],
                                 item['name'],
                                 item['height'], 
                                 item['weight'], 
                                 item['reach'],
                                 item['stance'],
                                 item['dob'],
                                 item['SLpM'],
                                 item['str_acc'],
                                 item['SApM'],
                                 item['str_def'],
                                 item['TD_avg'],
                                 item['TD_acc'],
                                 item['TD_def'],
                                 item['sub_avg']))
        
            # commit the transaction
            self.conn.commit()
        return item
    
    def format_data(self, item):
        format = "%b %d, %Y"
        # Format the data before inserting into the database
        item['fighter_id'] = item['fighter_id']
        item['name'] = item['name'].strip() if item['name'] and item['name'] != '--' else None
        item['height'] = int(item['height'].replace('\'', '').replace('"', '').split()[0]) * 12 + int(item['height'].replace('\'', '').replace('"', '').split()[1]) if item['height'] and item['height'] != '--' else None
        item['weight'] = int(item['weight'].replace(' lbs.', '')) if item['weight'] and item['weight'] != '--' else None
        item['reach'] = int(item['reach'].replace('"', '')) if item['reach'] and item['reach'] != '--' else None
        item['stance'] = item['stance'].strip() if item['stance'] and item['stance'] != '--' else None
        item['dob'] = datetime.strptime(item['dob'], format) if item['dob'] and item['dob'] != '--' else None
        item['SLpM'] = float(item['SLpM']) if item['SLpM'] and item['SLpM'] != '--' else None
        item['str_acc'] = float(item['str_acc'].replace('%', '')) if item['str_acc'] and item['str_acc'] != '--' else None
        item['SApM'] = float(item['SApM']) if item['SApM'] and item['SApM'] != '--' else None
        item['str_def'] = float(item['str_def'].replace('%', '')) if item['str_def'] and item['str_def'] != '--' else None
        item['TD_avg'] = float(item['TD_avg']) if item['TD_avg'] and item['TD_avg'] != '--' else None
        item['TD_acc'] = float(item['TD_acc'].replace('%', '')) if item['TD_acc'] and item['TD_acc'] != '--' else None
        item['TD_def'] = float(item['TD_def'].replace('%', '')) if item['TD_def'] and item['TD_def'] != '--' else None
        item['sub_avg'] = float(item['sub_avg']) if item['sub_avg'] and item['sub_avg'] != '--' else None
        return item

    
    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()
        
class ufc_fight_scraper_pipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='Ashtead96',
            database='ufc_database')
        
        # create a cursor object using the cursor() method
        self.cursor = self.conn.cursor()
        
        # create table if none exists
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS fight (fighter_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), height INT, weight INT, reach INT,stance VARCHAR(255), dob DATE, SLpM FLOAT, str_acc FLOAT, SApM FLOAT, str_def FLOAT, TD_avg FLOAT, TD_acc FLOAT, TD_def FLOAT, sub_avg FLOAT)')
    

    def process_item(self, item, spider):
        
        # Format data before inserting into the database
        formatted_item = self.format_data(item)
        
        # check if the fighter is already in the database
        self.cursor.execute('SELECT * FROM Fighter WHERE fighter_id = %s', (formatted_item['fighter_id'],))
        result = self.cursor.fetchone()
        if result:
            spider.logger.info(f'Fighter {formatted_item["name"]} already in the database')
        else:
        
            # insert values into the table  
            self.cursor.execute(
                'INSERT INTO FIGHTER (fighter_id, name, height, weight, reach, stance, dob, SLpM, str_acc, SApM, str_def, TD_avg, TD_acc, TD_def, sub_avg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                (item['fighter_id'],
                                 item['name'],
                                 item['height'], 
                                 item['weight'], 
                                 item['reach'],
                                 item['stance'],
                                 item['dob'],
                                 item['SLpM'],
                                 item['str_acc'],
                                 item['SApM'],
                                 item['str_def'],
                                 item['TD_avg'],
                                 item['TD_acc'],
                                 item['TD_def'],
                                 item['sub_avg']))
        
            # commit the transaction
            self.conn.commit()
        return item
    
    def format_data(self, item):
        format = "%b %d, %Y"
        # Format the data before inserting into the database
        item['fighter_id'] = item['fighter_id']
        item['name'] = item['name'].strip() if item['name'] and item['name'] != '--' else None
        item['height'] = int(item['height'].replace('\'', '').replace('"', '').split()[0]) * 12 + int(item['height'].replace('\'', '').replace('"', '').split()[1]) if item['height'] and item['height'] != '--' else None
        item['weight'] = int(item['weight'].replace(' lbs.', '')) if item['weight'] and item['weight'] != '--' else None
        item['reach'] = int(item['reach'].replace('"', '')) if item['reach'] and item['reach'] != '--' else None
        item['stance'] = item['stance'].strip() if item['stance'] and item['stance'] != '--' else None
        item['dob'] = datetime.strptime(item['dob'], format) if item['dob'] and item['dob'] != '--' else None
        item['SLpM'] = float(item['SLpM']) if item['SLpM'] and item['SLpM'] != '--' else None
        item['str_acc'] = float(item['str_acc'].replace('%', '')) if item['str_acc'] and item['str_acc'] != '--' else None
        item['SApM'] = float(item['SApM']) if item['SApM'] and item['SApM'] != '--' else None
        item['str_def'] = float(item['str_def'].replace('%', '')) if item['str_def'] and item['str_def'] != '--' else None
        item['TD_avg'] = float(item['TD_avg']) if item['TD_avg'] and item['TD_avg'] != '--' else None
        item['TD_acc'] = float(item['TD_acc'].replace('%', '')) if item['TD_acc'] and item['TD_acc'] != '--' else None
        item['TD_def'] = float(item['TD_def'].replace('%', '')) if item['TD_def'] and item['TD_def'] != '--' else None
        item['sub_avg'] = float(item['sub_avg']) if item['sub_avg'] and item['sub_avg'] != '--' else None
        return item

    
    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()
    
'''
fight_id = Field()
fighter_a_id_FK = Field()
fighter_b_id_FK = Field()
event_id_FK = Field()
weight_class = Field()
method = Field()
round = Field()
time = Field()
time_format = Field()
referee = Field()
judge1 = Field()
judge2 = Field()
judge3 = Field()
judge_1_score = Field()
judge_2_score = Field()
judge_3_score = Field()
fighter_a_knockdowns_total = Field()
fighter_b_knockdowns_total = Field()
fighter_a_sig_strikes_landed_total = Field()
fighter_b_sig_strikes_landed_total = Field()
fighter_a_sig_strikes_attempted_total = Field()
fighter_b_sig_strikes_attempted_total = Field()
fighter_a_total_strikes_landed_total = Field()
fighter_b_total_strikes_landed_total = Field()
fighter_a_total_strikes_attempted_total = Field()
fighter_b_total_strikes_attempted_total = Field()
fighter_a_takedowns_total_landed = Field()
fighter_b_takedowns_total_landed = Field()
fighter_a_takedowns_attempted_total = Field()
fighter_b_takedowns_attempted_total = Field()
fighter_a_submissions_total = Field()
fighter_b_submissions_total = Field()
fighter_a_reversals_total = Field()
fighter_b_reversals_total = Field()
fighter_a_control_total = Field()
fighter_b_control_total = Field()
fighter_a_sig_head_landed_total = Field()
fighter_b_sig_head_landed_total = Field()
fighter_a_sig_head_attempted_total = Field()
fighter_b_sig_head_attempted_total = Field()
fighter_a_sig_body_landed_total = Field()
fighter_b_sig_body_landed_total = Field()
fighter_a_sig_body_attempted_total = Field()
fighter_b_sig_body_attempted_total = Field()
fighter_a_sig_leg_landed_total = Field()
fighter_b_sig_leg_landed_total = Field()
fighter_a_sig_leg_attempted_total = Field()
fighter_b_sig_leg_attempted_total = Field()
fighter_a_sig_distance_landed_total = Field()
fighter_b_sig_distance_landed_total = Field()
fighter_a_sig_distance_attempted_total = Field()
fighter_b_sig_distance_attempted_total = Field()
fighter_a_sig_clinch_landed_total = Field()
fighter_b_sig_clinch_landed_total = Field()
fighter_a_sig_clinch_attempted_total = Field()
fighter_b_sig_clinch_attempted_total = Field()
fighter_a_sig_ground_landed_total = Field()
fighter_b_sig_ground_landed_total = Field()
fighter_a_sig_ground_attempted_total = Field()
fighter_b_sig_ground_attempted_total = Field()
'''