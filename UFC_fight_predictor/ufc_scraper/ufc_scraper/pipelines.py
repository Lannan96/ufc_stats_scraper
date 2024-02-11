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
        formatted_item = self.format_fighter_data(item)
        
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
    
    def format_fighter_data(self, item):
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
        self.cursor.execute('CREATE TABLE IF NOT EXISTS fight (fight_id VARCHAR(255) PRIMARY KEY, fighter_a_id_FK VARCHAR(255), fighter_b_id_FK VARCHAR(255), event_id_FK VARCHAR(255), \
            weight_class VARCHAR(255), method VARCHAR(255), round INT, time VARCHAR(255), time_format VARCHAR(255), referee VARCHAR(255), judge1 VARCHAR(255), \
            judge2 VARCHAR(255), judge3 VARCHAR(255), judge_1_score VARCHAR(255), judge_2_score VARCHAR(255), judge_3_score VARCHAR(255), fighter_a_knockdowns_total INT, \
          fighter_b_knockdowns_total INT, fighter_a_sig_strikes_landed_total INT, fighter_b_sig_strikes_landed_total INT, fighter_a_sig_strikes_attempted_total INT, \
         fighter_b_sig_strikes_attempted_total INT, fighter_a_total_strikes_landed_total INT, fighter_b_total_strikes_landed_total INT, \
         fighter_a_total_strikes_attempted_total INT, fighter_b_total_strikes_attempted_total INT, fighter_a_takedowns_total_landed INT, fighter_b_takedowns_total_landed INT, \
        fighter_a_takedowns_attempted_total INT, fighter_b_takedowns_attempted_total INT, fighter_a_submissions_total INT, fighter_b_submissions_total INT, \
        fighter_a_reversals_total INT, fighter_b_reversals_total INT, fighter_a_control_total VARCHAR(255), fighter_b_control_total VARCHAR(255), fighter_a_sig_head_landed_total INT, \
        fighter_b_sig_head_landed_total INT, fighter_a_sig_head_attempted_total INT, fighter_b_sig_head_attempted_total INT, fighter_a_sig_body_landed_total INT, \
        fighter_b_sig_body_landed_total INT, fighter_a_sig_body_attempted_total INT, fighter_b_sig_body_attempted_total INT, fighter_a_sig_leg_landed_total INT, \
        fighter_b_sig_leg_landed_total INT, fighter_a_sig_leg_attempted_total INT, fighter_b_sig_leg_attempted_total INT, fighter_a_sig_distance_landed_total INT, \
        fighter_b_sig_distance_landed_total INT, fighter_a_sig_distance_attempted_total INT, fighter_b_sig_distance_attempted_total INT, \
        fighter_a_sig_clinch_landed_total INT, fighter_b_sig_clinch_landed_total INT, fighter_a_sig_clinch_attempted_total INT, fighter_b_sig_clinch_attempted_total INT,\
       fighter_a_sig_ground_landed_total INT, fighter_b_sig_ground_landed_total INT, fighter_a_sig_ground_attempted_total INT, fighter_b_sig_ground_attempted_total INT)')
    

    def process_item(self, item, spider):
        
        # Format data before inserting into the database
        formatted_item = self.format_fight_data(item)
        
        # check if the fighter is already in the database
        self.cursor.execute('SELECT * FROM fight WHERE fight_id = %s', (formatted_item['fight_id'],))
        #self.cursor.execute('SELECT * FROM fight WHERE fight_id = %s', (item['fight_id'],))
        result = self.cursor.fetchone()
        if result:
            spider.logger.info(f'Fighter {formatted_item["fight_id"]} already in the database')
            #spider.logger.info(f'Fight {item["fight_id"]} already in the database')
        else:
        
            # insert values into the table  
            self.cursor.execute(
                'INSERT INTO fight (fight_id, fighter_a_id_FK, fighter_b_id_FK, event_id_FK, weight_class, method, round, time, time_format, referee, \
                judge1, judge2, judge3, judge_1_score, judge_2_score, judge_3_score, fighter_a_knockdowns_total, fighter_b_knockdowns_total, \
                fighter_a_sig_strikes_landed_total, fighter_b_sig_strikes_landed_total, fighter_a_sig_strikes_attempted_total, fighter_b_sig_strikes_attempted_total, \
                fighter_a_total_strikes_landed_total, fighter_b_total_strikes_landed_total, fighter_a_total_strikes_attempted_total, fighter_b_total_strikes_attempted_total, \
                fighter_a_takedowns_total_landed, fighter_b_takedowns_total_landed, fighter_a_takedowns_attempted_total, fighter_b_takedowns_attempted_total, \
                fighter_a_submissions_total, fighter_b_submissions_total, fighter_a_reversals_total, fighter_b_reversals_total, fighter_a_control_total, fighter_b_control_total, \
                fighter_a_sig_head_landed_total, fighter_b_sig_head_landed_total, fighter_a_sig_head_attempted_total, fighter_b_sig_head_attempted_total, \
                fighter_a_sig_body_landed_total, fighter_b_sig_body_landed_total, fighter_a_sig_body_attempted_total, fighter_b_sig_body_attempted_total, \
                fighter_a_sig_leg_landed_total, fighter_b_sig_leg_landed_total, fighter_a_sig_leg_attempted_total, fighter_b_sig_leg_attempted_total, \
                fighter_a_sig_distance_landed_total, fighter_b_sig_distance_landed_total, fighter_a_sig_distance_attempted_total, fighter_b_sig_distance_attempted_total, \
                fighter_a_sig_clinch_landed_total, fighter_b_sig_clinch_landed_total, fighter_a_sig_clinch_attempted_total, fighter_b_sig_clinch_attempted_total, \
                fighter_a_sig_ground_landed_total, fighter_b_sig_ground_landed_total, fighter_a_sig_ground_attempted_total, fighter_b_sig_ground_attempted_total) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
               %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (item['fight_id'],item['fighter_a_id_FK'], item['fighter_b_id_FK'], item['event_id_FK'], item['weight_class'], item['method'], item['round'],
                        item['time'], item['time_format'], item['referee'], item['judge1'], item['judge2'], item['judge3'], item['judge_1_score'], item['judge_2_score'],
                        item['judge_3_score'], item['fighter_a_knockdowns_total'], item['fighter_b_knockdowns_total'], item['fighter_a_sig_strikes_landed_total'],
                        item['fighter_b_sig_strikes_landed_total'], item['fighter_a_sig_strikes_attempted_total'], item['fighter_b_sig_strikes_attempted_total'],
                        item['fighter_a_total_strikes_landed_total'], item['fighter_b_total_strikes_landed_total'], item['fighter_a_total_strikes_attempted_total'],
                        item['fighter_b_total_strikes_attempted_total'], item['fighter_a_takedowns_total_landed'], item['fighter_b_takedowns_total_landed'],
                        item['fighter_a_takedowns_attempted_total'], item['fighter_b_takedowns_attempted_total'], item['fighter_a_submissions_total'],
                        item['fighter_b_submissions_total'], item['fighter_a_reversals_total'], item['fighter_b_reversals_total'], item['fighter_a_control_total'],
                        item['fighter_b_control_total'], item['fighter_a_sig_head_landed_total'], item['fighter_b_sig_head_landed_total'], 
                        item['fighter_a_sig_head_attempted_total'], item['fighter_b_sig_head_attempted_total'], item['fighter_a_sig_body_landed_total'], 
                        item['fighter_b_sig_body_landed_total'], item['fighter_a_sig_body_attempted_total'], item['fighter_b_sig_body_attempted_total'], 
                        item['fighter_a_sig_leg_landed_total'], item['fighter_b_sig_leg_landed_total'], item['fighter_a_sig_leg_attempted_total'], 
                        item['fighter_b_sig_leg_attempted_total'], item['fighter_a_sig_distance_landed_total'], item['fighter_b_sig_distance_landed_total'],
                        item['fighter_a_sig_distance_attempted_total'], item['fighter_b_sig_distance_attempted_total'], item['fighter_a_sig_clinch_landed_total'],
                        item['fighter_b_sig_clinch_landed_total'], item['fighter_a_sig_clinch_attempted_total'], item['fighter_b_sig_clinch_attempted_total'], 
                        item['fighter_a_sig_ground_landed_total'], item['fighter_b_sig_ground_landed_total'], item['fighter_a_sig_ground_attempted_total'], 
                        item['fighter_b_sig_ground_attempted_total']))
        
            # commit the transaction
            self.conn.commit()
        return item
    
    def format_fight_data(self, item):
        # Format the data before inserting into the database
        item['fight_id'] = item['fight_id']
        item['fighter_a_id_FK'] = item['fighter_a_id_FK']
        item['fighter_b_id_FK'] = item['fighter_b_id_FK']
        item['event_id_FK'] = item['event_id_FK']
        item['weight_class'] = self.format_fight_weight_class(item['weight_class'])
        item['method'] = item['method']
        item['round'] = item['round']
        item['time'] = item['time']
        item['time_format'] = item['time_format']
        item['referee'] = item['referee']
        item['judge1'] = item['judge1'].strip() if item['judge1'] and item['judge1'] != '--' else None
        item['judge2'] = item['judge2'].strip() if item['judge2'] and item['judge2'] != '--' else None
        item['judge3'] = item['judge3'].strip() if item['judge3'] and item['judge3'] != '--' else None
        item['judge_1_score'] = item['judge_1_score'][1] if item['judge_1_score'] and item['judge_1_score'] != '--' else None
        item['judge_2_score'] = item['judge_2_score'][1] if item['judge_2_score'] and item['judge_2_score'] != '--' else None
        item['judge_3_score'] = item['judge_3_score'][1] if item['judge_3_score'] and item['judge_3_score'] != '--' else None
        item['fighter_a_knockdowns_total'] = int(item['fighter_a_knockdowns_total'])
        item['fighter_b_knockdowns_total'] = int(item['fighter_b_knockdowns_total'])
        item['fighter_a_sig_strikes_landed_total'] = int(item['fighter_a_sig_strikes_landed_total'])
        item['fighter_b_sig_strikes_landed_total'] = int(item['fighter_b_sig_strikes_landed_total'])
        item['fighter_a_sig_strikes_attempted_total'] = int(item['fighter_a_sig_strikes_attempted_total'])
        item['fighter_b_sig_strikes_attempted_total'] = int(item['fighter_b_sig_strikes_attempted_total'])
        item['fighter_a_total_strikes_landed_total'] = int(item['fighter_a_total_strikes_landed_total'])
        item['fighter_b_total_strikes_landed_total'] = int(item['fighter_b_total_strikes_landed_total'])
        item['fighter_a_total_strikes_attempted_total'] = int(item['fighter_a_total_strikes_attempted_total'])
        item['fighter_b_total_strikes_attempted_total'] = int(item['fighter_b_total_strikes_attempted_total'])
        item['fighter_a_takedowns_total_landed'] = int(item['fighter_a_takedowns_total_landed'])
        item['fighter_b_takedowns_total_landed'] = int(item['fighter_b_takedowns_total_landed'])
        item['fighter_a_takedowns_attempted_total'] = int(item['fighter_a_takedowns_attempted_total'])
        item['fighter_b_takedowns_attempted_total'] = int(item['fighter_b_takedowns_attempted_total'])
        item['fighter_a_submissions_total'] = int(item['fighter_a_submissions_total'])
        item['fighter_b_submissions_total'] = int(item['fighter_b_submissions_total'])
        item['fighter_a_reversals_total'] = int(item['fighter_a_reversals_total'])
        item['fighter_b_reversals_total'] = int(item['fighter_b_reversals_total'])
        item['fighter_a_control_total'] = item['fighter_a_control_total']
        item['fighter_b_control_total'] = item['fighter_b_control_total']
        item['fighter_a_sig_head_landed_total'] = int(item['fighter_a_sig_head_landed_total'])
        item['fighter_b_sig_head_landed_total'] = int(item['fighter_b_sig_head_landed_total'])
        item['fighter_a_sig_head_attempted_total'] = int(item['fighter_a_sig_head_attempted_total'])
        item['fighter_b_sig_head_attempted_total'] = int(item['fighter_b_sig_head_attempted_total'])
        item['fighter_a_sig_body_landed_total'] = int(item['fighter_a_sig_body_landed_total'])
        item['fighter_b_sig_body_landed_total'] = item['fighter_b_sig_body_landed_total']
        item['fighter_a_sig_body_attempted_total'] = item['fighter_a_sig_body_attempted_total']
        item['fighter_b_sig_body_attempted_total'] = item['fighter_b_sig_body_attempted_total']
        item['fighter_a_sig_leg_landed_total'] = item['fighter_a_sig_leg_landed_total']
        item['fighter_b_sig_leg_landed_total'] = item['fighter_b_sig_leg_landed_total']
        item['fighter_a_sig_leg_attempted_total'] = item['fighter_a_sig_leg_attempted_total']
        item['fighter_b_sig_leg_attempted_total'] = item['fighter_b_sig_leg_attempted_total']
        item['fighter_a_sig_distance_landed_total'] = item['fighter_a_sig_distance_landed_total']
        item['fighter_b_sig_distance_landed_total'] = item['fighter_b_sig_distance_landed_total']
        item['fighter_a_sig_distance_attempted_total'] = item['fighter_a_sig_distance_attempted_total']
        item['fighter_b_sig_distance_attempted_total'] = item['fighter_b_sig_distance_attempted_total']
        item['fighter_a_sig_clinch_landed_total'] = item['fighter_a_sig_clinch_landed_total']
        item['fighter_b_sig_clinch_landed_total'] = item['fighter_b_sig_clinch_landed_total']
        item['fighter_a_sig_clinch_attempted_total'] = item['fighter_a_sig_clinch_attempted_total']
        item['fighter_b_sig_clinch_attempted_total'] = item['fighter_b_sig_clinch_attempted_total']
        item['fighter_a_sig_ground_landed_total'] = item['fighter_a_sig_ground_landed_total']
        item['fighter_b_sig_ground_landed_total'] = item['fighter_b_sig_ground_landed_total']
        item['fighter_a_sig_ground_attempted_total'] = item['fighter_a_sig_ground_attempted_total']
        item['fighter_b_sig_ground_attempted_total'] = item['fighter_b_sig_ground_attempted_total']
        return item
    
    def format_fight_weight_class(self, value):
        if len(value) == 1:
            value = value[0].strip() 
        else: 
            value = value[1].strip()
        
        if value[:3] == 'UFC':
            return value[4:]
        else:
            return value

    
    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()
    