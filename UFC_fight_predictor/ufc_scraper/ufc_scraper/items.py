# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class ufc_fighter_scraper_item(scrapy.Item):
    # define the fields for your item here like:
    fighter_id = Field()
    name = Field()
    height = Field()
    weight = Field()
    reach = Field()
    stance = Field()
    dob = Field()
    SLpM = Field()
    str_acc = Field()
    SApM = Field()
    str_def = Field()
    TD_avg = Field()
    TD_acc = Field()
    TD_def = Field()
    sub_avg = Field()

class ufc_fight_item(scrapy.Item):
    # define the fields for your item here like:
    fight_id = Field()
    fighter_a_id_FK = Field()
    fighter_b_id_FK = Field()
    event_id_FK = Field()
    winner = Field()
    performance_bonus = Field()
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
    
class ufc_event_item(scrapy.Item):
        event_id = Field()
        event_name = Field()
        date = Field()
        location = Field()
    




