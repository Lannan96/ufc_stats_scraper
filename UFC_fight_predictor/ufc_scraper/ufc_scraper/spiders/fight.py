import scrapy


class FightSpider(scrapy.Spider):
    name = "fight"
    allowed_domains = ["ufcstats.com"]
    start_urls = ["http://ufcstats.com/fight-details/ce99b089400a4ad3"]

    def parse(self, response):
        fight = ufc_fight_item()
        fight['fight_id'] = response.url.split('/')[-1]
        fight['fighter_a_id_FK'] = response.xpath('/html/body/section/div/div/div[1]/div[1]/div/h3/a/@href').extract_first().split('/')[-1]
        fight['fighter_b_id_FK'] = response.xpath('/html/body/section/div/div/div[1]/div[2]/div/h3/a/@href').extract_first().split('/')[-1]
        fight['event_id_FK'] = response.xpath('/html/body/section/div/h2/a/@href').extract_first().split('/')[-1]
        fight['weight_class'] = response.xpath('/html/body/section/div/div/div[2]/div[1]/i/text()').extract_first().strip()
        fight['method'] = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[1]/i[2]/text()').extract_first().strip()
        fight['round'] = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[2]/text()').extract()[1].strip()
        fight['time'] = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[3]/text()').extract()[1].strip()
        fight['time_format'] = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[4]/text()').extract()[1].strip()
        fight['referee'] = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[5]/span/text()').extract_first().strip()
        fight['judge1'] = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[2]/span/text()').extract()
        fight['judge2'] = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[3]/span/text()').extract()
        fight['judge3'] = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[4]/span/text()').extract()
        fight['judge_1_score'] = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[2]/text()').extract()[1].strip()
        fight['judge_2_score'] = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[3]/text()').extract()[1].strip()
        fight['judge_3_score'] =  response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[4]/text()').extract()[1].strip()
        fight['fighter_a_knockdowns_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[2]/p[1]/text()').extract_first().strip()
        fight['fighter_b_knockdowns_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[2]/p[2]/text()').extract_first().strip()
        fight['fighter_a_sig_strikes_landed_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[1]/text()').extract_first().strip().split()[0]
        fight['fighter_b_sig_strikes_landed_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[2]/text()').extract_first().strip().split()[0]
        fight['fighter_a_sig_strikes_attempted_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[1]/text()').extract_first().strip().split()[2]
        fight['fighter_b_sig_strikes_attempted_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[2]/text()').extract_first().strip().split()[2]
        fight['fighter_a_total_strikes_landed_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[1]/text()').extract_first().strip().split()[0]
        fight['fighter_b_total_strikes_landed_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[2]/text()').extract_first().strip().split()[0]
        fight['fighter_a_total_strikes_attempted_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[1]/text()').extract_first().strip().split()[2]
        fight['fighter_b_total_strikes_attempted_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[2]/text()').extract_first().strip().split()[2]
        fight['fighter_a_takedowns_total_landed'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[1]/text()').extract_first().strip().split()[0]
        fight['fighter_b_takedowns_total_landed'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[2]/text()').extract_first().strip().split()[0]
        fight['fighter_a_takedowns_attempted_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[1]/text()').extract_first().strip().split()[2]
        fight['fighter_b_takedowns_attempted_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[2]/text()').extract_first().strip().split()[2]
        fight['fighter_a_submissions_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[8]/p[1]/text()').extract_first().strip()
        fight['fighter_b_submissions_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[8]/p[2]/text()').extract_first().strip()
        fight['fighter_a_reversals_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[9]/p[1]/text()').extract_first().strip()
        fight['fighter_b_reversals_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[9]/p[2]/text()').extract_first().strip()
        fight['fighter_a_control_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[10]/p[1]/text()').extract_first().strip()
        fight['fighter_b_control_total'] = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[10]/p[2]/text()').extract_first().strip()
        fight['fighter_a_sig_head_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[4]/p[1]/text()').extract_first().strip().split()[0]
        fight['fighter_b_sig_head_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[4]/p[2]/text()').extract_first().strip().split()[0]
        fight['fighter_a_sig_head_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[4]/p[1]/text()').extract_first().strip().split()[2]
        fight['fighter_b_sig_head_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[4]/p[2]/text()').extract_first().strip().split()[2]
        fight['fighter_a_sig_body_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[5]/p[1]/text()').extract_first().strip().split()[0]
        fight['fighter_b_sig_body_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[5]/p[2]/text()').extract_first().strip().split()[0]
        fight['fighter_a_sig_body_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[5]/p[1]/text()').extract_first().strip().split()[2]
        fight['fighter_b_sig_body_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[5]/p[2]/text()').extract_first().strip().split()[2]
        fight['fighter_a_sig_leg_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[6]/p[1]/text()').extract_first().strip().split()[0]
        fight['fighter_b_sig_leg_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[6]/p[2]/text()').extract_first().strip().split()[0]
        fight['fighter_a_sig_leg_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[6]/p[1]/text()').extract_first().strip().split()[2]
        fight['fighter_b_sig_leg_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[6]/p[2]/text()').extract_first().strip().split()[2]
        fight['fighter_a_sig_distance_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[7]/p[1]/text()').extract_first().strip().split()[0]
        fight['fighter_b_sig_distance_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[7]/p[2]/text()').extract_first().strip().split()[0]
        fight['fighter_a_sig_distance_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[7]/p[1]/text()').extract_first().strip().split()[2]
        fight['fighter_b_sig_distance_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[7]/p[2]/text()').extract_first().strip().split()[2]
        fight['fighter_a_sig_clinch_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[8]/p[1]/text()').extract_first().strip().split()[0]
        fight['fighter_b_sig_clinch_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[8]/p[2]/text()').extract_first().strip().split()[0]
        fight['fighter_a_sig_clinch_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[8]/p[1]/text()').extract_first().strip().split()[2]
        fight['fighter_b_sig_clinch_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[8]/p[2]/text()').extract_first().strip().split()[2]
        fight['fighter_a_sig_ground_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[9]/p[1]/text()').extract_first().strip().split()[0]
        fight['fighter_b_sig_ground_landed_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[9]/p[2]/text()').extract_first().strip().split()[0]
        fight['fighter_a_sig_ground_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[9]/p[1]/text()').extract_first().strip().split()[2]
        fight['fighter_b_sig_ground_attempted_total'] = response.xpath('/html/body/section/div/div/table/tbody/tr/td[9]/p[2]/text()').extract_first().strip().split()[2]
        yield fight
        
        
    

# fight_id = response.url.split('/')[-1]
# fighter_a_id_FK = response.xpath('/html/body/section/div/div/div[1]/div[1]/div/h3/a/@href').extract_first().split('/')[-1]
# fighter_b_id_FK = response.xpath('/html/body/section/div/div/div[1]/div[2]/div/h3/a/@href').extract_first().split('/')[-1]
# event_id_FK = response.xpath('/html/body/section/div/h2/a/@href').extract_first().split('/')[-1]
# weight_class = response.xpath('/html/body/section/div/div/div[2]/div[1]/i/text()').extract_first().strip()
# method = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[1]/i[2]/text()').extract_first().strip()
# round = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[2]/text()').extract()[1].strip()
# time = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[3]/text()').extract()[1].strip()
# time_format = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[4]/text()').extract()[1].strip()
# referee = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[5]/span/text()').extract_first().strip()
# judge1 = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[2]/span/text()').extract()
# judge2 = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[3]/span/text()').extract()
# judge3 = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[4]/span/text()').extract()
# judge_1_score = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[2]/text()').extract()[1].strip()
# judge_2_score = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[3]/text()').extract()[1].strip()
# judge_3_score =  response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/i[4]/text()').extract()[1].strip()


# fighter_a_knockdowns_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[2]/p[1]/text()').extract_first().strip()
# fighter_b_knockdowns_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[2]/p[2]/text()').extract_first().strip()
# fighter_a_sig_strikes_landed_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[1]/text()').extract_first().strip().split()[0]
# fighter_b_sig_strikes_landed_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[2]/text()').extract_first().strip().split()[0]
# fighter_a_sig_strikes_attempted_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[1]/text()').extract_first().strip().split()[2]
# fighter_b_sig_strikes_attempted_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[2]/text()').extract_first().strip().split()[2]
# fighter_a_total_strikes_landed_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[1]/text()').extract_first().strip().split()[0]
# fighter_b_total_strikes_landed_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[2]/text()').extract_first().strip().split()[0]
# fighter_a_total_strikes_attempted_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[1]/text()').extract_first().strip().split()[2]
# fighter_b_total_strikes_attempted_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[2]/text()').extract_first().strip().split()[2]
# fighter_a_takedowns_total_landed = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[1]/text()').extract_first().strip().split()[0]
# fighter_b_takedowns_total_landed = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[2]/text()').extract_first().strip().split()[0]
# fighter_a_takedowns_attempted_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[1]/text()').extract_first().strip().split()[2]
# fighter_b_takedowns_attempted_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[2]/text()').extract_first().strip().split()[2]
# fighter_a_submissions_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[8]/p[1]/text()').extract_first().strip()
# fighter_b_submissions_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[8]/p[2]/text()').extract_first().strip()
# fighter_a_reversals_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[9]/p[1]/text()').extract_first().strip()
# fighter_b_reversals_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[9]/p[2]/text()').extract_first().strip()
# fighter_a_control_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[10]/p[1]/text()').extract_first().strip()
# fighter_b_control_total = response.xpath('/html/body/section/div/div/section[2]/table/tbody/tr/td[10]/p[2]/text()').extract_first().strip()

# fighter_a_knockdowns_rd_1
# fighter_b_knockdowns_rd_1
# fighter_a_sig_strikes_landed_rd_1
# fighter_b_sig_strikes_landed_rd_1
# fighter_a_sig_strikes_attempted_rd_1
# fighter_b_sig_strikes_attempted_rd_1
# fighter_a_total_strikes_landed_rd_1
# fighter_b_total_strikes_landed_rd_1
# fighter_a_takedowns_rd_1_landed
# fighter_b_takedowns_rd_1_landed
# fighter_a_takedowns_attempted_rd_1
# fighter_b_takedowns_attempted_rd_1
# fighter_a_submissions_rd_1
# fighter_b_submissions_rd_1
# fighter_a_reversals_rd_1
# fighter_b_reversals_rd_1
# fighter_a_control_rd_1
# fighter_b_control_rd_1

# fighter_a_knockdowns_rd_2
# fighter_b_knockdowns_rd_2
# fighter_a_sig_strikes_landed_rd_2
# fighter_b_sig_strikes_landed_rd_2
# fighter_a_sig_strikes_attempted_rd_2
# fighter_b_sig_strikes_attempted_rd_2
# fighter_a_total_strikes_landed_rd_2
# fighter_b_total_strikes_landed_rd_2
# fighter_a_takedowns_rd_2_landed
# fighter_b_takedowns_rd_2_landed
# fighter_a_takedowns_attempted_rd_2
# fighter_b_takedowns_attempted_rd_2
# fighter_a_submissions_rd_2
# fighter_b_submissions_rd_2
# fighter_a_reversals_rd_2
# fighter_b_reversals_rd_2
# fighter_a_control_rd_2
# fighter_b_control_rd_2

# fighter_a_knockdowns_rd_3
# fighter_b_knockdowns_rd_3
# fighter_a_sig_strikes_landed_rd_3
# fighter_b_sig_strikes_landed_rd_3
# fighter_a_sig_strikes_attempted_rd_3
# fighter_b_sig_strikes_attempted_rd_3
# fighter_a_total_strikes_landed_rd_3
# fighter_b_total_strikes_landed_rd_3
# fighter_a_takedowns_rd_3_landed
# fighter_b_takedowns_rd_3_landed
# fighter_a_takedowns_attempted_rd_3
# fighter_b_takedowns_attempted_rd_3
# fighter_a_submissions_rd_3
# fighter_b_submissions_rd_3
# fighter_a_reversals_rd_3
# fighter_b_reversals_rd_3
# fighter_a_control_rd_3
# fighter_b_control_rd_3

# fighter_a_knockdowns_rd_4
# fighter_b_knockdowns_rd_4
# fighter_a_sig_strikes_landed_rd_4
# fighter_b_sig_strikes_landed_rd_4
# fighter_a_sig_strikes_attempted_rd_4
# fighter_b_sig_strikes_attempted_rd_4
# fighter_a_total_strikes_landed_rd_4
# fighter_b_total_strikes_landed_rd_4
# fighter_a_takedowns_rd_4_landed
# fighter_b_takedowns_rd_4_landed
# fighter_a_takedowns_attempted_rd_4
# fighter_b_takedowns_attempted_rd_4
# fighter_a_submissions_rd_4
# fighter_b_submissions_rd_4
# fighter_a_reversals_rd_4
# fighter_b_reversals_rd_4
# fighter_a_control_rd_4
# fighter_b_control_rd_4

# fighter_a_knockdowns_rd_5
# fighter_b_knockdowns_rd_5
# fighter_a_sig_strikes_landed_rd_5
# fighter_b_sig_strikes_landed_rd_5
# fighter_a_sig_strikes_attempted_rd_5
# fighter_b_sig_strikes_attempted_rd_5
# fighter_a_total_strikes_landed_rd_5
# fighter_b_total_strikes_landed_rd_5
# fighter_a_takedowns_rd_5_landed
# fighter_b_takedowns_rd_5_landed
# fighter_a_takedowns_attempted_rd_5
# fighter_b_takedowns_attempted_rd_5
# fighter_a_submissions_rd_5
# fighter_b_submissions_rd_5
# fighter_a_reversals_rd_5
# fighter_b_reversals_rd_5
# fighter_a_control_rd_5
# fighter_b_control_rd_5

# fighter_a_sig_head_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[4]/p[1]/text()').extract_first().strip().split()[0]
# fighter_b_sig_head_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[4]/p[2]/text()').extract_first().strip().split()[0]
# fighter_a_sig_head_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[4]/p[1]/text()').extract_first().strip().split()[2]
# fighter_b_sig_head_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[4]/p[2]/text()').extract_first().strip().split()[2]
# fighter_a_sig_body_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[5]/p[1]/text()').extract_first().strip().split()[0]
# fighter_b_sig_body_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[5]/p[2]/text()').extract_first().strip().split()[0]
# fighter_a_sig_body_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[5]/p[1]/text()').extract_first().strip().split()[2]
# fighter_b_sig_body_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[5]/p[2]/text()').extract_first().strip().split()[2]
# fighter_a_sig_leg_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[6]/p[1]/text()').extract_first().strip().split()[0]
# fighter_b_sig_leg_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[6]/p[2]/text()').extract_first().strip().split()[0]
# fighter_a_sig_leg_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[6]/p[1]/text()').extract_first().strip().split()[2]
# fighter_b_sig_leg_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[6]/p[2]/text()').extract_first().strip().split()[2]
# fighter_a_sig_distance_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[7]/p[1]/text()').extract_first().strip().split()[0]
# fighter_b_sig_distance_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[7]/p[2]/text()').extract_first().strip().split()[0]
# fighter_a_sig_distance_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[7]/p[1]/text()').extract_first().strip().split()[2]
# fighter_b_sig_distance_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[7]/p[2]/text()').extract_first().strip().split()[2]
# fighter_a_sig_clinch_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[8]/p[1]/text()').extract_first().strip().split()[0]
# fighter_b_sig_clinch_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[8]/p[2]/text()').extract_first().strip().split()[0]
# fighter_a_sig_clinch_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[8]/p[1]/text()').extract_first().strip().split()[2]
# fighter_b_sig_clinch_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[8]/p[2]/text()').extract_first().strip().split()[2]
# fighter_a_sig_ground_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[9]/p[1]/text()').extract_first().strip().split()[0]
# fighter_b_sig_ground_landed_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[9]/p[2]/text()').extract_first().strip().split()[0]
# fighter_a_sig_ground_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[9]/p[1]/text()').extract_first().strip().split()[2]
# fighter_b_sig_ground_attempted_total = response.xpath('/html/body/section/div/div/table/tbody/tr/td[9]/p[2]/text()').extract_first().strip().split()[2]

# fighter_a_sig_head_landed_rd_1
# fighter_b_sig_head_landed_rd_1
# fighter_a_sig_head_attempted_rd_1
# fighter_b_sig_head_attempted_rd_1
# fighter_a_sig_body_landed_rd_1
# fighter_b_sig_body_landed_rd_1
# fighter_a_sig_body_attempted_rd_1
# fighter_b_sig_body_attempted_rd_1
# fighter_a_sig_leg_landed_rd_1
# fighter_b_sig_leg_landed_rd_1
# fighter_a_sig_leg_attempted_rd_1
# fighter_b_sig_leg_attempted_rd_1
# fighter_a_sig_distance_landed_rd_1
# fighter_b_sig_distance_landed_rd_1
# fighter_a_sig_distance_attempted_rd_1
# fighter_b_sig_distance_attempted_rd_1
# fighter_a_sig_clinch_landed_rd_1
# fighter_b_sig_clinch_landed_rd_1
# fighter_a_sig_clinch_attempted_rd_1
# fighter_b_sig_clinch_attempted_rd_1
# fighter_a_sig_ground_landed_rd_1
# fighter_b_sig_ground_landed_rd_1
# fighter_a_sig_ground_attempted_rd_1
# fighter_b_sig_ground_attempted_rd_1

# fighter_a_sig_head_landed_rd_2
# fighter_b_sig_head_landed_rd_2
# fighter_a_sig_head_attempted_rd_2
# fighter_b_sig_head_attempted_rd_2
# fighter_a_sig_body_landed_rd_2
# fighter_b_sig_body_landed_rd_2
# fighter_a_sig_body_attempted_rd_2
# fighter_b_sig_body_attempted_rd_2
# fighter_a_sig_leg_landed_rd_2
# fighter_b_sig_leg_landed_rd_2
# fighter_a_sig_leg_attempted_rd_2
# fighter_b_sig_leg_attempted_rd_2
# fighter_a_sig_distance_landed_rd_2
# fighter_b_sig_distance_landed_rd_2
# fighter_a_sig_distance_attempted_rd_2
# fighter_b_sig_distance_attempted_rd_2
# fighter_a_sig_clinch_landed_rd_2
# fighter_b_sig_clinch_landed_rd_2
# fighter_a_sig_clinch_attempted_rd_2
# fighter_b_sig_clinch_attempted_rd_2
# fighter_a_sig_ground_landed_rd_2
# fighter_b_sig_ground_landed_rd_2
# fighter_a_sig_ground_attempted_rd_2
# fighter_b_sig_ground_attempted_rd_2

# fighter_a_sig_head_landed_rd_3
# fighter_b_sig_head_landed_rd_3
# fighter_a_sig_head_attempted_rd_3
# fighter_b_sig_head_attempted_rd_3
# fighter_a_sig_body_landed_rd_3
# fighter_b_sig_body_landed_rd_3
# fighter_a_sig_body_attempted_rd_3
# fighter_b_sig_body_attempted_rd_3
# fighter_a_sig_leg_landed_rd_3
# fighter_b_sig_leg_landed_rd_3
# fighter_a_sig_leg_attempted_rd_3
# fighter_b_sig_leg_attempted_rd_3
# fighter_a_sig_distance_landed_rd_3
# fighter_b_sig_distance_landed_rd_3
# fighter_a_sig_distance_attempted_rd_3
# fighter_b_sig_distance_attempted_rd_3
# fighter_a_sig_clinch_landed_rd_3
# fighter_b_sig_clinch_landed_rd_3
# fighter_a_sig_clinch_attempted_rd_3
# fighter_b_sig_clinch_attempted_rd_3
# fighter_a_sig_ground_landed_rd_3
# fighter_b_sig_ground_landed_rd_3
# fighter_a_sig_ground_attempted_rd_3
# fighter_b_sig_ground_attempted_rd_3

# fighter_a_sig_head_landed_rd_4
# fighter_b_sig_head_landed_rd_4
# fighter_a_sig_head_attempted_rd_4
# fighter_b_sig_head_attempted_rd_4
# fighter_a_sig_body_landed_rd_4
# fighter_b_sig_body_landed_rd_4
# fighter_a_sig_body_attempted_rd_4
# fighter_b_sig_body_attempted_rd_4
# fighter_a_sig_leg_landed_rd_4
# fighter_b_sig_leg_landed_rd_4
# fighter_a_sig_leg_attempted_rd_4
# fighter_b_sig_leg_attempted_rd_4
# fighter_a_sig_distance_landed_rd_4
# fighter_b_sig_distance_landed_rd_4
# fighter_a_sig_distance_attempted_rd_4
# fighter_b_sig_distance_attempted_rd_4
# fighter_a_sig_clinch_landed_rd_4
# fighter_b_sig_clinch_landed_rd_4
# fighter_a_sig_clinch_attempted_rd_4
# fighter_b_sig_clinch_attempted_rd_4
# fighter_a_sig_ground_landed_rd_4
# fighter_b_sig_ground_landed_rd_4
# fighter_a_sig_ground_attempted_rd_4
# fighter_b_sig_ground_attempted_rd_4

# fighter_a_sig_head_landed_rd_5
# fighter_b_sig_head_landed_rd_5
# fighter_a_sig_head_attempted_rd_5
# fighter_b_sig_head_attempted_rd_5
# fighter_a_sig_body_landed_rd_5
# fighter_b_sig_body_landed_rd_5
# fighter_a_sig_body_attempted_rd_5
# fighter_b_sig_body_attempted_rd_5
# fighter_a_sig_leg_landed_rd_5
# fighter_b_sig_leg_landed_rd_5
# fighter_a_sig_leg_attempted_rd_5
# fighter_b_sig_leg_attempted_rd_5
# fighter_a_sig_distance_landed_rd_5
# fighter_b_sig_distance_landed_rd_5
# fighter_a_sig_distance_attempted_rd_5
# fighter_b_sig_distance_attempted_rd_5
# fighter_a_sig_clinch_landed_rd_5
# fighter_b_sig_clinch_landed_rd_5
# fighter_a_sig_clinch_attempted_rd_5
# fighter_b_sig_clinch_attempted_rd_5
# fighter_a_sig_ground_landed_rd_5
# fighter_b_sig_ground_landed_rd_5
# fighter_a_sig_ground_attempted_rd_5
# fighter_b_sig_ground_attempted_rd_5
