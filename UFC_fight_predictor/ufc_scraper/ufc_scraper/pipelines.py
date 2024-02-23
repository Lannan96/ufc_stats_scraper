# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from datetime import datetime


class ufc_fighter_scraper_pipeline:

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
            'CREATE TABLE IF NOT EXISTS fighter (fighter_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), height INT, weight INT, reach INT,stance VARCHAR(255), dob DATE, SLpM FLOAT, str_acc FLOAT, SApM FLOAT, str_def FLOAT, TD_avg FLOAT, TD_acc FLOAT, TD_def FLOAT, sub_avg FLOAT)')
    

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
                                (formatted_item['fighter_id'],
                                 formatted_item['name'],
                                 formatted_item['height'], 
                                 formatted_item['weight'], 
                                 formatted_item['reach'],
                                 formatted_item['stance'],
                                 formatted_item['dob'],
                                 formatted_item['SLpM'],
                                 formatted_item['str_acc'],
                                 formatted_item['SApM'],
                                 formatted_item['str_def'],
                                 formatted_item['TD_avg'],
                                 formatted_item['TD_acc'],
                                 formatted_item['TD_def'],
                                 formatted_item['sub_avg']))
        
            # commit the transaction
            self.conn.commit()
        return formatted_item
    
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
        self.cursor.execute('CREATE TABLE IF NOT EXISTS fight (fight_id VARCHAR(255) PRIMARY KEY, fighter_a_id_FK VARCHAR(255), FOREIGN KEY(fighter_a_id_FK) REFERENCES \
            fighter(fighter_id), fighter_b_id_FK VARCHAR(255), FOREIGN KEY(fighter_b_id_FK) REFERENCES fighter(fighter_id), \
            event_id_FK VARCHAR(255), FOREIGN KEY(event_id_FK) REFERENCES event(event_id), \
            winner VARCHAR(255), performance_bonus VARCHAR(255), weight_class VARCHAR(255), method VARCHAR(255), round INT, time VARCHAR(255), time_format VARCHAR(255), referee VARCHAR(255), judge1 VARCHAR(255), \
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
        result = self.cursor.fetchone()
        if result:
            spider.logger.info(f'Fight {formatted_item["fight_id"]} already in the database')
        else:
        
            # insert values into the table  
            self.cursor.execute(
                 'INSERT INTO fight (fight_id, fighter_a_id_FK, fighter_b_id_FK, event_id_FK, winner, performance_bonus, weight_class, method, round, time, time_format, referee, \
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
 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
         (formatted_item['fight_id'],formatted_item['fighter_a_id_FK'], formatted_item['fighter_b_id_FK'], formatted_item['event_id_FK'], formatted_item['winner'], formatted_item['performance_bonus'], formatted_item['weight_class'], formatted_item['method'], formatted_item['round'],
         formatted_item['time'], formatted_item['time_format'], formatted_item['referee'], formatted_item['judge1'], formatted_item['judge2'], formatted_item['judge3'], formatted_item['judge_1_score'], formatted_item['judge_2_score'],
         formatted_item['judge_3_score'], formatted_item['fighter_a_knockdowns_total'], formatted_item['fighter_b_knockdowns_total'], formatted_item['fighter_a_sig_strikes_landed_total'],
         formatted_item['fighter_b_sig_strikes_landed_total'], formatted_item['fighter_a_sig_strikes_attempted_total'], formatted_item['fighter_b_sig_strikes_attempted_total'],
         formatted_item['fighter_a_total_strikes_landed_total'], formatted_item['fighter_b_total_strikes_landed_total'], formatted_item['fighter_a_total_strikes_attempted_total'],
         formatted_item['fighter_b_total_strikes_attempted_total'], formatted_item['fighter_a_takedowns_total_landed'], formatted_item['fighter_b_takedowns_total_landed'],
         formatted_item['fighter_a_takedowns_attempted_total'], formatted_item['fighter_b_takedowns_attempted_total'], formatted_item['fighter_a_submissions_total'],
         formatted_item['fighter_b_submissions_total'], formatted_item['fighter_a_reversals_total'], formatted_item['fighter_b_reversals_total'], formatted_item['fighter_a_control_total'],
         formatted_item['fighter_b_control_total'], formatted_item['fighter_a_sig_head_landed_total'], formatted_item['fighter_b_sig_head_landed_total'], 
         formatted_item['fighter_a_sig_head_attempted_total'], formatted_item['fighter_b_sig_head_attempted_total'], formatted_item['fighter_a_sig_body_landed_total'], 
         formatted_item['fighter_b_sig_body_landed_total'], formatted_item['fighter_a_sig_body_attempted_total'], formatted_item['fighter_b_sig_body_attempted_total'], 
         formatted_item['fighter_a_sig_leg_landed_total'], formatted_item['fighter_b_sig_leg_landed_total'], formatted_item['fighter_a_sig_leg_attempted_total'], 
         formatted_item['fighter_b_sig_leg_attempted_total'], formatted_item['fighter_a_sig_distance_landed_total'], formatted_item['fighter_b_sig_distance_landed_total'],
         formatted_item['fighter_a_sig_distance_attempted_total'], formatted_item['fighter_b_sig_distance_attempted_total'], formatted_item['fighter_a_sig_clinch_landed_total'],
         formatted_item['fighter_b_sig_clinch_landed_total'], formatted_item['fighter_a_sig_clinch_attempted_total'], formatted_item['fighter_b_sig_clinch_attempted_total'], 
         formatted_item['fighter_a_sig_ground_landed_total'], formatted_item['fighter_b_sig_ground_landed_total'], formatted_item['fighter_a_sig_ground_attempted_total'], 
         formatted_item['fighter_b_sig_ground_attempted_total']))
        
            # commit the transaction
            self.conn.commit()
        return item
    
    def format_fight_data(self, item):
        # Format the data before inserting into the database
        item['fight_id'] = item['fight_id']
        item['fighter_a_id_FK'] = item['fighter_a_id_FK']
        item['fighter_b_id_FK'] = item['fighter_b_id_FK']
        item['event_id_FK'] = item['event_id_FK']
        item['winner'] = self.format_fight_winner(item['winner'])
        item['performance_bonus'] = self.format_fight_performance_bonus(item['performance_bonus'])
        item['weight_class'] = self.format_fight_weight_class(item['weight_class'])
        item['method'] = self.format_fight_method(item['method'])
        item['round'] = self.format_fight_round(item['round'])
        item['time'] = self.format_fight_time(item['time'])
        item['time_format'] = self.format_fight_time_format(item['time_format'])
        item['referee'] = self.format_fight_referee(item['referee'])
        item['judge1'] = self.format_fight_judge(item['judge1'])
        item['judge2'] = self.format_fight_judge(item['judge2'])
        item['judge3'] = self.format_fight_judge(item['judge3'])
        item['judge_1_score'] = self.format_fight_judge_score(item['judge_1_score'])
        item['judge_2_score'] = self.format_fight_judge_score(item['judge_2_score'])
        item['judge_3_score'] = self.format_fight_judge_score(item['judge_3_score'])
        item['fighter_a_knockdowns_total'] = self.format_fight_fighter_knockdowns_total(item['fighter_a_knockdowns_total'])
        item['fighter_b_knockdowns_total'] = self.format_fight_fighter_knockdowns_total(item['fighter_b_knockdowns_total'])
        item['fighter_a_sig_strikes_landed_total'] = self.format_fight_strikes_landed(item['fighter_a_sig_strikes_landed_total'])
        item['fighter_b_sig_strikes_landed_total'] = self.format_fight_strikes_landed(item['fighter_b_sig_strikes_landed_total'])
        item['fighter_a_sig_strikes_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_a_sig_strikes_attempted_total'])
        item['fighter_b_sig_strikes_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_b_sig_strikes_attempted_total'])
        item['fighter_a_total_strikes_landed_total'] = self.format_fight_strikes_landed(item['fighter_a_total_strikes_landed_total'])
        item['fighter_b_total_strikes_landed_total'] = self.format_fight_strikes_landed(item['fighter_b_total_strikes_landed_total'])
        item['fighter_a_total_strikes_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_a_total_strikes_attempted_total'])
        item['fighter_b_total_strikes_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_b_total_strikes_attempted_total'])
        item['fighter_a_takedowns_total_landed'] = self.format_fight_strikes_landed(item['fighter_a_takedowns_total_landed'])
        item['fighter_b_takedowns_total_landed'] = self.format_fight_strikes_landed(item['fighter_b_takedowns_total_landed'])
        item['fighter_a_takedowns_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_a_takedowns_attempted_total'])
        item['fighter_b_takedowns_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_b_takedowns_attempted_total'])
        item['fighter_a_submissions_total'] = self.format_fight_submission(item['fighter_a_submissions_total'])
        item['fighter_b_submissions_total'] = self.format_fight_submission(item['fighter_b_submissions_total'])
        item['fighter_a_reversals_total'] = self.format_fight_reversal(item['fighter_a_reversals_total'])
        item['fighter_b_reversals_total'] = self.format_fight_reversal(item['fighter_b_reversals_total'])
        item['fighter_a_control_total'] = self.format_fight_control(item['fighter_a_control_total'])
        item['fighter_b_control_total'] = self.format_fight_control(item['fighter_b_control_total'])
        item['fighter_a_sig_head_landed_total'] = self.format_fight_strikes_landed(item['fighter_a_sig_head_landed_total'])
        item['fighter_b_sig_head_landed_total'] = self.format_fight_strikes_landed(item['fighter_b_sig_head_landed_total'])
        item['fighter_a_sig_head_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_a_sig_head_attempted_total'])
        item['fighter_b_sig_head_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_b_sig_head_attempted_total'])
        item['fighter_a_sig_body_landed_total'] = self.format_fight_strikes_landed(item['fighter_a_sig_body_landed_total'])
        item['fighter_b_sig_body_landed_total'] = self.format_fight_strikes_landed(item['fighter_b_sig_body_landed_total'])
        item['fighter_a_sig_body_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_a_sig_body_attempted_total'])
        item['fighter_b_sig_body_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_b_sig_body_attempted_total'])
        item['fighter_a_sig_leg_landed_total'] = self.format_fight_strikes_landed(item['fighter_a_sig_leg_landed_total'])
        item['fighter_b_sig_leg_landed_total'] = self.format_fight_strikes_landed(item['fighter_b_sig_leg_landed_total'])
        item['fighter_a_sig_leg_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_a_sig_leg_attempted_total'])
        item['fighter_b_sig_leg_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_b_sig_leg_attempted_total'])
        item['fighter_a_sig_distance_landed_total'] = self.format_fight_strikes_landed(item['fighter_a_sig_distance_landed_total'])
        item['fighter_b_sig_distance_landed_total'] = self.format_fight_strikes_landed(item['fighter_b_sig_distance_landed_total'])
        item['fighter_a_sig_distance_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_a_sig_distance_attempted_total'])
        item['fighter_b_sig_distance_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_b_sig_distance_attempted_total'])
        item['fighter_a_sig_clinch_landed_total'] = self.format_fight_strikes_landed(item['fighter_a_sig_clinch_landed_total'])
        item['fighter_b_sig_clinch_landed_total'] = self.format_fight_strikes_landed(item['fighter_b_sig_clinch_landed_total'])
        item['fighter_a_sig_clinch_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_a_sig_clinch_attempted_total'])
        item['fighter_b_sig_clinch_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_b_sig_clinch_attempted_total'])
        item['fighter_a_sig_ground_landed_total'] = self.format_fight_strikes_landed(item['fighter_a_sig_ground_landed_total'])
        item['fighter_b_sig_ground_landed_total'] = self.format_fight_strikes_landed(item['fighter_b_sig_ground_landed_total'])
        item['fighter_a_sig_ground_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_a_sig_ground_attempted_total'])
        item['fighter_b_sig_ground_attempted_total'] = self.format_fight_strikes_attempted(item['fighter_b_sig_ground_attempted_total'])
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
    
    def format_fight_winner(self, value):
       if value != None:
           winner = value.strip()
           if winner == 'W':
               return 'Fighter A'
           elif winner == 'D':
               return 'Draw'
           elif winner == 'NC':
               return 'No Contest'
           else: return 'Fighter B'
       else: return None
            
    def format_fight_performance_bonus(self, value):
        
        if value != None:
            bonus_type = value[0].split('/')[-1]
            if bonus_type == 'fight.png':
                return 'Fight of the Night'
            elif bonus_type == 'ko.png':
                return 'Knockout of the Night'
            elif bonus_type == 'sub.png':
                return 'Submission of the Night'
            elif bonus_type == 'perf.png':
                return 'Performance of the Night'
            else: return None
        else:
            return None
    
    def format_fight_fighter_knockdowns_total(self, value):
        if value != None and value.strip() != '--':
            return int(value.strip())
        else: return None
        
    def format_fight_method(self, value):
        if value != None and value.strip() != '--':
            return value.strip()
        else: return None
    
    def format_fight_round(self, value):
        if value != None:
            return int(value[1].strip())
        else: return None
        
    def format_fight_time(self, value):
        if value != None:
            return value[1].strip()
        else: return None
        
    def format_fight_time_format(self, value):
        if value != None:
            return value[1].strip()
        else: return None
        
    def format_fight_referee(self, value):
        if value != None and value.strip() != '--':
            return value.strip()
        else: return None
    
    def format_fight_judge(self, value):
        if value != None and value.strip() != '--':
            return value.strip()
        else: return None
        
    def format_fight_judge_score(self, value):
        if value != None and value.strip() != '--':
            return value.strip()
        else: return None
        
    def format_fight_strikes_landed(self, value):
        if value != None and value.strip() != '--':
            return int(value.strip().split()[0])
        else: return None
        
    def format_fight_strikes_attempted(self, value):
        if value != None and value.strip() != '--':
            return int(value.strip().split()[2])
        else: return None
        
    def format_fight_submission(self, value):
        if value != None and value.strip() != '--':
            return int(value.strip())
        else: return None
    
    def format_fight_reversal(self, value):
        if value != None and value.strip() != '--':
            return int(value.strip())
        else: return None

    def format_fight_control(self, value):
        if value != None and value.strip() != '--':
            return value.strip()
        else: return None
        

    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()

class ufc_event_scraper_pipeline:

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
            'CREATE TABLE IF NOT EXISTS event (event_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), date DATE, location VARCHAR(255))')


    def process_item(self, item, spider):
        
        # Format data before inserting into the database
        formatted_item = self.format_event_data(item)
        
        # check if the fighter is already in the database
        self.cursor.execute('SELECT * FROM event WHERE event_id = %s', (formatted_item['event_id'],))
        result = self.cursor.fetchone()
        if result:
            spider.logger.info(f'Event {formatted_item["event_name"]} already in the database')
        else:
        
            # insert values into the table  
            self.cursor.execute(
                'INSERT INTO event (event_id, name, date, location) VALUES (%s, %s, %s, %s)',
                                (formatted_item['event_id'],
                                 formatted_item['event_name'],
                                 formatted_item['date'], 
                                 formatted_item['location']))
        
            # commit the transaction
            self.conn.commit()
        return item
    
    def format_event_data(self, item):
        format = "%B %d, %Y"
        # Format the data before inserting into the database
        item['event_id'] = item['event_id'][0].split('/')[-1] if item['event_id'] and item['event_id'][0] != '--' else None
        item['event_name'] = item['event_name'][0].strip() if item['event_name'] and item['event_name'][0] != '--' else None
        item['date'] = datetime.strptime(item['date'][0].strip(), format) if item['date'] and item['date'][0] != '--' else None
        item['location'] = item['location'][0].strip() if item['location'] and item['location'][0] != '--' else None
        return item

    
    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()
    