# Problem Statement
The purpose of this project is to produce a model to predict winners of UFC fights. The comparison of this models performance will be judge against prediction I make myself based on my knowledge of the sport and later compared to the bookies favourite pick.

As we have access to a rich dataset there are numerous ways we can make prediction of the outcome of the fight. Listed below are the technique we will try and compare to each other.
    * Comparing fighters based career stats
    * Using career stats again, but calculating them so they are accurate to the time (I.E excluding fights that are in the future of the fight currently being predicted)
    * Predicting the stats of a fight and using these prediction to predict the winner

# Step 1) Data Exploration
The first step of any project is understanding our data, this is done by...
Whilst doing this I will keep two question in mind to help me later, these are, how will I clean this data and what features could I engineer.

First things first lets use information from the scraping to explain our database structure and the columns in the data.

## Database schema
Below we can see our database schema made up of three tables: 1) Fighter, 2) Fight, and 3) Event.
As we can see from the schema the 'fight' table links to 'fighter' and 'event' as all of our data follows the following format -> An event is made up of fights -> a fight contains two fighter.

![Database](ufc_database.png)

## Table information
Next we will outline what each of the columns in our tables represent and explain some technical definition to help understand our columns.

#### Fighter Table
The example data comes from the fighter found at the following URL - http://ufcstats.com/fighter-details/e1248941344b3288
<br>
<br>

| Column Name | Description | Format | Example |
| --- | --- | --- | --- |
| fighter_id | Primary key of the fighter formed from the last part of the URL. 'http://ufcstats.com/fighter-details/e1248941344b3288' the fighter_id would be 'e1248941344b3288' | varchar(255) PK | 'e1248941344b3288' |
| name | Name | varchar(255) | 'Alexander Volkanovski' |
| height | Height in Inches | int | '66' |
| weight | Weight in IBS | int | '145' |
| reach | Reach in Inches | int | '71' |
| stance | Stance | varchar(255) | 'Orthodox' |
| dob | DOB | date | '1988-09-29' |
| SLpM | Significant Strikes Landed per Minute | float | '6.19' |
| str_acc | Significant Striking Accuracy | float | '57' |
| SApM | Significant Strikes Absorbed per Minute | float | '3.42' |
| str_def | Significant Strike Defence (the % of opponents strikes that did not land) | float | '58' |
| TD_avg | Average Takedowns Landed per 15 minutes | float | '1.84' |
| TD_acc | Takedown Accuracy | float | '37' |
| TD_def | Takedown Defense (the % of opponents TD attempts that did not land) | float | '70' |
| sub_avg | Average Submissions Attempted per 15 minutes | float | '0.2' |



#### Fight Table
The example data comes from the fight found at the following URL - http://ufcstats.com/fight-details/bec3154a11df3299
<br>
<br>

| Column Name | Description | Format | Example |
| --- | --- | --- | --- |
| fight_id | Primary key of the fight formed from the last part of the URL. 'http://ufcstats.com/fight-details/bec3154a11df3299' the fight_id would be 'bec3154a11df3299'  | varchar(255) PK | 'bec3154a11df3299' |
| fighter_a_id_FK | Fighter_id for the red corner of the fight. Foreign Key from fighter table | varchar(255) FK | 'e1248941344b3288' |
| fighter_b_id_FK | Fighter_id for the blue corner of the fight. Foreign Key from fighter table | varchar(255) FK | '54f64b5e283b0ce7' |
| event_id_FK | Event_id Foreign Key from the event table | varchar(255) FK | 'dab0e6cb8c932162' |
| winner | Winner of the fighter | varchar(255) | 'Fighter B' |
| performance_bonus | If there was a performance bonus and what type | varchar(255) | NULL |
| weight_class | Weight class of the fight | varchar(255) | 'KO/TKO' |
| method | How the fight ended | varchar(255) | 'KO/TKO' |
| round | What round the fight ended | int | '2' |
| time | What time stamp the fight ended | varchar(255) | '3:32' |
| time_format | The format of the fight, how many rounds of X minutes | varchar(255) | '5 Rnd (5-5-5-5-5)' |
| referee | Referee | varchar(255) | 'Jason Herzog' |
| judge1 | Judge 1 - Is null if the fight didn't go to a decision | varchar(255) | NULL |
| judge2 | Judge 2 - Is null if the fight didn't go to a decision | varchar(255) | NULL |
| judge3 | Judge 3 - Is null if the fight didn't go to a decision | varchar(255) | NULL |
| judge_1_score | Judge 1 Score - Is null if the fight didn't go to a decision | varchar(255) | NULL |
| judge_2_score | Judge 2 Score - Is null if the fight didn't go to a decision | varchar(255) | NULL |
| judge_3_score | Judge 3 Score - Is null if the fight didn't go to a decision | varchar(255) | NULL |
| fighter_a_knockdowns_total | Number of times fighter knockdown their opponent with strikes | int | '0' |
| fighter_b_knockdowns_total | Number of times fighter knockdown their opponent with strikes | int | '1' |
| fighter_a_sig_strikes_landed_total | Number of significant strikes landed | int | '47' |
| fighter_b_sig_strikes_landed_total | Number of significant strikes landed | int | '35' |
| fighter_a_sig_strikes_attempted_total | Number of significant strikes attempted | int | '107' |
| fighter_b_sig_strikes_attempted_total | Number of significant strikes attempted | int | '77' |
| fighter_a_total_strikes_landed_total | Number of total strikes landed | int | '47' |
| fighter_b_total_strikes_landed_total | Number of total strikes landed | int | '36' |
| fighter_a_total_strikes_attempted_total | Number of total strikes attempted | int | '107' |
| fighter_b_total_strikes_attempted_total | Number of total strikes attempted | int | '78' |
| fighter_a_takedowns_total_landed | Number of successful takedowns | int | '0' |
| fighter_b_takedowns_total_landed | Number of successful takedowns | int | '0' |
| fighter_a_takedowns_attempted_total | Number of attempted takedowns | int | '0' |
| fighter_b_takedowns_attempted_total | Number of attempted takedowns | int | '0' |
| fighter_a_submissions_total | Number of submissions attempted | int | '0' |
| fighter_b_submissions_total | Number of submissions attempted | int | '0' |
| fighter_a_reversals_total | A reversal is scored when the bottom fighter actively moves to establish top position, without his opponent getting back to his feet in between. | int | '0' |
| fighter_b_reversals_total | A reversal is scored when the bottom fighter actively moves to establish top position, without his opponent getting back to his feet in between. | int | '0' |
| fighter_a_control_total | Amount of time fighter spends in a top position controlling their opponent | varchar(255) | '0:00' |
| fighter_b_control_total | Amount of time fighter spends in a top position controlling their opponent | varchar(255) | '0:03' |
| fighter_a_sig_head_landed_total | Significant strikes landed at the opponents head | int | '21' |
| fighter_b_sig_head_landed_total | Significant strikes landed at the opponents head | int | '17' |
| fighter_a_sig_head_attempted_total | Significant strikes attempted at the opponents head | int | '68' |
| fighter_b_sig_head_attempted_total | Significant strikes attempted at the opponents head | int | '53' |
| fighter_a_sig_body_landed_total | Significant strikes landed at the opponents body | int | '11' |
| fighter_b_sig_body_landed_total | Significant strikes landed at the opponents body | int | '12' |
| fighter_a_sig_body_attempted_total | Significant strikes attempted at the opponents body | int | '22' |
| fighter_b_sig_body_attempted_total | Significant strikes attempted at the opponents body | int | '16' |
| fighter_a_sig_leg_landed_total | Significant strikes landed at the opponents legs | int | '15' |
| fighter_b_sig_leg_landed_total | Significant strikes landed at the opponents legs | int | '6' |
| fighter_a_sig_leg_attempted_total | Significant strikes attempted at the opponents legs | int | '17' |
| fighter_b_sig_leg_attempted_total | Significant strikes attempted at the opponents legs | int | '8' |
| fighter_a_sig_distance_landed_total | Significant strike landed from distance | int | '44' |
| fighter_b_sig_distance_landed_total | Significant strike landed from distance | int | '28' |
| fighter_a_sig_distance_attempted_total | Significant strike attempted from distance | int | '102' |
| fighter_b_sig_distance_attempted_total | Significant strike attempted from distance | int | '70' |
| fighter_a_sig_clinch_landed_total | Significant strike landed from the clinch | int | '3' |
| fighter_b_sig_clinch_landed_total | Significant strike landed from the clinch | int | '4' |
| fighter_a_sig_clinch_attempted_total | Significant strike attempted from the clinch | int | '5' |
| fighter_b_sig_clinch_attempted_total | Significant strike attempted from the clinch | int | '4' |
| fighter_a_sig_ground_landed_total | Significant strike landed from the ground | int | '0' |
| fighter_b_sig_ground_landed_total | Significant strike landed from ground | int | '3' |
| fighter_a_sig_ground_attempted_total | Significant strike attempted from ground | int | '0' |
| fighter_b_sig_ground_attempted_total | Significant strike attempted from ground | int | '3' |




#### Event Table
The example data comes from the event found at the following URL - http://ufcstats.com/event-details/dab0e6cb8c932162
<br>
<br>

| Column Name | Description | Format | Example |
| --- | --- | --- | --- |
| event_id | Primary key of the event formed from the last part of the URL. 'http://ufcstats.com/event-details/dab0e6cb8c932162' the event_id would be 'dab0e6cb8c932162' | varchar(255) PK | 'dab0e6cb8c932162'|
| name | Event name | varchar(255) | 'UFC 298: Volkanovski vs. Topuria' |
| date | The date the event took place in the format of ... | date 'YYYY-MM-DD' | '2024-02-17' |
| location | Where the event took place. In the format of... | varchar(255) | 'Anaheim, California, USA' |


## Questions and comments
The weight we have is what the fighters fight at but not what we think they weigh when they fight, is there a way to find this information?
The weight class for fight isn't pulling through
Judge Score isn't pulling through
I don't scrape the fight end details if it doesn't go the distance
We don't scrape nicknames
Could expand this data explanation to include things like types of values in a column such as performance bonus.


```python
''' Now we have explained what data we have and what each column represents we now want to know what are 
the typical values, what is the distribution and perform some cleaning.

Part of this would be selecting only data that is useful, however, I am going to perform the data 
cleaning steps on all my data as I wrote the scrapers and may want to change how things are formatted in 
the database after working with them
'''
```


```python
#!pip install mysql-connector-python
#!pip uninstall mqsql-connector

```

    Requirement already satisfied: mysql-connector-python in c:\users\lanna\anaconda3\lib\site-packages (8.0.33)
    Requirement already satisfied: protobuf<=3.20.3,>=3.11.0 in c:\users\lanna\anaconda3\lib\site-packages (from mysql-connector-python) (3.19.6)
    

    WARNING: Ignoring invalid distribution -rotobuf (c:\users\lanna\anaconda3\lib\site-packages)
    WARNING: Ignoring invalid distribution -rotobuf (c:\users\lanna\anaconda3\lib\site-packages)
    WARNING: Ignoring invalid distribution -rotobuf (c:\users\lanna\anaconda3\lib\site-packages)
    WARNING: Ignoring invalid distribution -rotobuf (c:\users\lanna\anaconda3\lib\site-packages)
    WARNING: Ignoring invalid distribution -rotobuf (c:\users\lanna\anaconda3\lib\site-packages)
    WARNING: Ignoring invalid distribution -rotobuf (c:\users\lanna\anaconda3\lib\site-packages)
    

## Gather our data
Now that we understand our database structure and the data available to us we need to write a query to get the correct data from out database.


```python
# Import libaries
import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime 
from sklearn.preprocessing import LabelEncoder
```


```python
cnx = mysql.connector.connect(user='root', password='Ashtead96',
                              host='localhost',
                              database='ufc_database', auth_plugin='mysql_native_password')

```


```python
query = '''
SELECT 
    f.fight_id, 
    f.fighter_a_id_FK, 
    f.event_id_FK, 
    f.winner, 
    event.name,
    event.date,
    ftr_a.name AS fighter_a_name, 
    ftr_b.name AS fighter_b_name,
    ftr_a.height AS fighter_a_height, 
    ftr_b.height AS fighter_b_height,
    ftr_a.weight AS fighter_a_weight, 
    ftr_b.weight AS fighter_b_weight,
    ftr_a.reach AS fighter_a_reach, 
    ftr_b.reach AS fighter_b_reach,
    ftr_a.stance AS fighter_a_stance, 
    ftr_b.stance AS fighter_b_stance,
    ftr_a.dob AS fighter_a_dob, 
    ftr_b.dob AS fighter_b_dob,
    ftr_a.SLpM AS fighter_a_SLpM, 
    ftr_b.SLpM AS fighter_b_SLpM,
    ftr_a.str_acc AS fighter_a_str_acc, 
    ftr_b.str_acc AS fighter_b_str_acc,
    ftr_a.SApM AS fighter_a_SApM, 
    ftr_b.SApM AS fighter_b_SApM,
    ftr_a.str_def AS fighter_a_str_def, 
    ftr_b.str_def AS fighter_b_str_def,
    ftr_a.TD_avg AS fighter_a_TD_avg, 
    ftr_b.TD_avg AS fighter_b_TD_avg,
    ftr_a.TD_acc AS fighter_a_TD_acc, 
    ftr_b.TD_acc AS fighter_b_TD_acc,
    ftr_a.TD_def AS fighter_a_TD_def, 
    ftr_b.TD_def AS fighter_b_TD_def,
    ftr_a.sub_avg AS fighter_a_sub_avg, 
    ftr_b.sub_avg AS fighter_b_sub_avg
FROM 
    fight f
JOIN 
    fighter ftr_a ON f.fighter_a_id_FK = ftr_a.fighter_id
JOIN 
    fighter ftr_b ON f.fighter_b_id_FK = ftr_b.fighter_id
JOIN event ON f.event_id_FK = event.event_id;
'''

```


```python
cursor = cnx.cursor()
cursor.execute(query)
result = cursor.fetchall()
num_fields = len(cursor.description)
field_names = [i[0] for i in cursor.description]
cursor.close()
```




    True




```python
# First lets have a look at our data
pd.set_option('display.max_columns', None)
dataframe = pd.DataFrame(result, columns=field_names)
dataframe
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fight_id</th>
      <th>fighter_a_id_FK</th>
      <th>event_id_FK</th>
      <th>winner</th>
      <th>name</th>
      <th>date</th>
      <th>fighter_a_name</th>
      <th>fighter_b_name</th>
      <th>fighter_a_height</th>
      <th>fighter_b_height</th>
      <th>fighter_a_weight</th>
      <th>fighter_b_weight</th>
      <th>fighter_a_reach</th>
      <th>fighter_b_reach</th>
      <th>fighter_a_stance</th>
      <th>fighter_b_stance</th>
      <th>fighter_a_dob</th>
      <th>fighter_b_dob</th>
      <th>fighter_a_SLpM</th>
      <th>fighter_b_SLpM</th>
      <th>fighter_a_str_acc</th>
      <th>fighter_b_str_acc</th>
      <th>fighter_a_SApM</th>
      <th>fighter_b_SApM</th>
      <th>fighter_a_str_def</th>
      <th>fighter_b_str_def</th>
      <th>fighter_a_TD_avg</th>
      <th>fighter_b_TD_avg</th>
      <th>fighter_a_TD_acc</th>
      <th>fighter_b_TD_acc</th>
      <th>fighter_a_TD_def</th>
      <th>fighter_b_TD_def</th>
      <th>fighter_a_sub_avg</th>
      <th>fighter_b_sub_avg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0005e00b07cee542</td>
      <td>634e2fb70bde3fd5</td>
      <td>805ad1801eb26abb</td>
      <td>Fighter A</td>
      <td>UFC Fight Night: Holm vs. Aldana</td>
      <td>2020-10-03</td>
      <td>Holly Holm</td>
      <td>Irene Aldana</td>
      <td>68.0</td>
      <td>69.0</td>
      <td>135.0</td>
      <td>135.0</td>
      <td>69.0</td>
      <td>68.0</td>
      <td>Southpaw</td>
      <td>Orthodox</td>
      <td>1981-10-17</td>
      <td>1988-03-26</td>
      <td>3.21</td>
      <td>5.24</td>
      <td>40.0</td>
      <td>40.0</td>
      <td>2.79</td>
      <td>6.33</td>
      <td>56.0</td>
      <td>57.0</td>
      <td>0.90</td>
      <td>0.16</td>
      <td>30.0</td>
      <td>50.0</td>
      <td>78.0</td>
      <td>76.0</td>
      <td>0.1</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>000da3152b7b5ab1</td>
      <td>6da99156486ed6c2</td>
      <td>f70144caea5c4c80</td>
      <td>Fighter A</td>
      <td>UFC 61: Bitter Rivals</td>
      <td>2006-07-08</td>
      <td>Joshua Burkman</td>
      <td>Josh Neer</td>
      <td>70.0</td>
      <td>71.0</td>
      <td>170.0</td>
      <td>170.0</td>
      <td>72.0</td>
      <td>72.0</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1980-04-10</td>
      <td>1983-03-24</td>
      <td>2.69</td>
      <td>3.29</td>
      <td>43.0</td>
      <td>46.0</td>
      <td>3.13</td>
      <td>3.63</td>
      <td>51.0</td>
      <td>58.0</td>
      <td>2.53</td>
      <td>1.09</td>
      <td>36.0</td>
      <td>34.0</td>
      <td>72.0</td>
      <td>46.0</td>
      <td>0.3</td>
      <td>1.3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>001441f70c293931</td>
      <td>7826923b47f8d72a</td>
      <td>1d00756835ca67c9</td>
      <td>Fighter A</td>
      <td>UFC Fight Night: Volkov vs. Aspinall</td>
      <td>2022-03-19</td>
      <td>Paddy Pimblett</td>
      <td>Kazula Vargas</td>
      <td>70.0</td>
      <td>68.0</td>
      <td>155.0</td>
      <td>155.0</td>
      <td>73.0</td>
      <td>71.0</td>
      <td>Orthodox</td>
      <td>Southpaw</td>
      <td>1995-01-03</td>
      <td>1985-08-15</td>
      <td>5.13</td>
      <td>3.65</td>
      <td>52.0</td>
      <td>53.0</td>
      <td>3.70</td>
      <td>1.77</td>
      <td>41.0</td>
      <td>57.0</td>
      <td>0.98</td>
      <td>0.40</td>
      <td>25.0</td>
      <td>25.0</td>
      <td>56.0</td>
      <td>30.0</td>
      <td>1.6</td>
      <td>0.4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0019ec81fd706ade</td>
      <td>85073dbd1be65ed9</td>
      <td>3ae10ac4df3df05c</td>
      <td>No Contest</td>
      <td>UFC Fight Night: Reyes vs. Weidman</td>
      <td>2019-10-18</td>
      <td>Greg Hardy</td>
      <td>Ben Sosoli</td>
      <td>77.0</td>
      <td>72.0</td>
      <td>265.0</td>
      <td>265.0</td>
      <td>80.0</td>
      <td>72.0</td>
      <td>Orthodox</td>
      <td>Southpaw</td>
      <td>1988-07-28</td>
      <td>1989-12-10</td>
      <td>4.79</td>
      <td>2.31</td>
      <td>50.0</td>
      <td>31.0</td>
      <td>3.31</td>
      <td>4.30</td>
      <td>55.0</td>
      <td>47.0</td>
      <td>0.20</td>
      <td>0.00</td>
      <td>33.0</td>
      <td>0.0</td>
      <td>64.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0027e179b743c86c</td>
      <td>91ea901c458e95dd</td>
      <td>f54200f1dfb9b5d4</td>
      <td>Fighter A</td>
      <td>UFC 185: Pettis vs Dos Anjos</td>
      <td>2015-03-14</td>
      <td>Jared Rosholt</td>
      <td>Josh Copeland</td>
      <td>74.0</td>
      <td>73.0</td>
      <td>265.0</td>
      <td>265.0</td>
      <td>75.0</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1986-08-04</td>
      <td>1982-10-20</td>
      <td>2.08</td>
      <td>1.03</td>
      <td>46.0</td>
      <td>31.0</td>
      <td>1.52</td>
      <td>3.01</td>
      <td>59.0</td>
      <td>55.0</td>
      <td>1.83</td>
      <td>0.00</td>
      <td>41.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>57.0</td>
      <td>0.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>7514</th>
      <td>ffe4379d6bd1e82b</td>
      <td>2a542ee8a8b83559</td>
      <td>0cf935519d439ba6</td>
      <td>Fighter A</td>
      <td>UFC 39: The Warriors Return</td>
      <td>2002-09-27</td>
      <td>Tim Sylvia</td>
      <td>Wesley Correira</td>
      <td>80.0</td>
      <td>75.0</td>
      <td>265.0</td>
      <td>260.0</td>
      <td>80.0</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1976-03-05</td>
      <td>1978-11-11</td>
      <td>4.23</td>
      <td>2.60</td>
      <td>41.0</td>
      <td>36.0</td>
      <td>2.61</td>
      <td>8.80</td>
      <td>61.0</td>
      <td>40.0</td>
      <td>0.11</td>
      <td>0.00</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>75.0</td>
      <td>90.0</td>
      <td>0.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7515</th>
      <td>ffe629a5232a878b</td>
      <td>08ae5cd9aef7ddd3</td>
      <td>108afe61a26bcbf4</td>
      <td>Fighter A</td>
      <td>UFC 43: Meltdown</td>
      <td>2003-06-06</td>
      <td>Kimo Leopoldo</td>
      <td>David Abbott</td>
      <td>75.0</td>
      <td>72.0</td>
      <td>235.0</td>
      <td>265.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Switch</td>
      <td>1968-01-05</td>
      <td>None</td>
      <td>0.76</td>
      <td>1.35</td>
      <td>83.0</td>
      <td>30.0</td>
      <td>2.12</td>
      <td>3.55</td>
      <td>30.0</td>
      <td>38.0</td>
      <td>4.55</td>
      <td>1.07</td>
      <td>100.0</td>
      <td>33.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>2.3</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7516</th>
      <td>ffea776913451b6d</td>
      <td>22a92d7f62195791</td>
      <td>ad4e9055bf8cd04d</td>
      <td>Fighter A</td>
      <td>UFC 184: Rousey vs Zingano</td>
      <td>2015-02-28</td>
      <td>Tony Ferguson</td>
      <td>Gleison Tibau</td>
      <td>71.0</td>
      <td>70.0</td>
      <td>155.0</td>
      <td>155.0</td>
      <td>76.0</td>
      <td>71.0</td>
      <td>Orthodox</td>
      <td>Southpaw</td>
      <td>1984-02-12</td>
      <td>1983-10-07</td>
      <td>4.94</td>
      <td>1.95</td>
      <td>45.0</td>
      <td>31.0</td>
      <td>4.41</td>
      <td>2.51</td>
      <td>55.0</td>
      <td>63.0</td>
      <td>0.39</td>
      <td>4.08</td>
      <td>35.0</td>
      <td>53.0</td>
      <td>67.0</td>
      <td>92.0</td>
      <td>0.9</td>
      <td>0.8</td>
    </tr>
    <tr>
      <th>7517</th>
      <td>fffa21388cdd78b7</td>
      <td>c80095f6092271a7</td>
      <td>eae4aec1a5a8ff01</td>
      <td>Fighter A</td>
      <td>UFC 166: Velasquez vs Dos Santos 3</td>
      <td>2013-10-19</td>
      <td>Tim Boetsch</td>
      <td>CB Dollaway</td>
      <td>72.0</td>
      <td>74.0</td>
      <td>185.0</td>
      <td>185.0</td>
      <td>74.0</td>
      <td>76.0</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1981-01-28</td>
      <td>1983-08-10</td>
      <td>2.93</td>
      <td>2.65</td>
      <td>50.0</td>
      <td>47.0</td>
      <td>2.90</td>
      <td>2.58</td>
      <td>57.0</td>
      <td>54.0</td>
      <td>1.45</td>
      <td>3.55</td>
      <td>34.0</td>
      <td>54.0</td>
      <td>59.0</td>
      <td>62.0</td>
      <td>0.8</td>
      <td>1.2</td>
    </tr>
    <tr>
      <th>7518</th>
      <td>fffdc57255274be1</td>
      <td>2f5cbecbbe18bac4</td>
      <td>5717efc6f271cd52</td>
      <td>Fighter B</td>
      <td>UFC 283: Teixeira vs. Hill</td>
      <td>2023-01-21</td>
      <td>Shamil Abdurakhimov</td>
      <td>Jailton Almeida</td>
      <td>75.0</td>
      <td>75.0</td>
      <td>235.0</td>
      <td>205.0</td>
      <td>76.0</td>
      <td>79.0</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1981-09-02</td>
      <td>1991-06-26</td>
      <td>2.41</td>
      <td>2.78</td>
      <td>44.0</td>
      <td>64.0</td>
      <td>3.02</td>
      <td>0.52</td>
      <td>55.0</td>
      <td>43.0</td>
      <td>1.01</td>
      <td>5.14</td>
      <td>23.0</td>
      <td>55.0</td>
      <td>45.0</td>
      <td>75.0</td>
      <td>0.1</td>
      <td>2.4</td>
    </tr>
  </tbody>
</table>
<p>7519 rows × 34 columns</p>
</div>




```python
# Lets look at some basic information about our data
dataframe.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 7519 entries, 0 to 7518
    Data columns (total 34 columns):
     #   Column             Non-Null Count  Dtype  
    ---  ------             --------------  -----  
     0   fight_id           7519 non-null   object 
     1   fighter_a_id_FK    7519 non-null   object 
     2   event_id_FK        7519 non-null   object 
     3   winner             7519 non-null   object 
     4   name               7519 non-null   object 
     5   date               7519 non-null   object 
     6   fighter_a_name     7519 non-null   object 
     7   fighter_b_name     7519 non-null   object 
     8   fighter_a_height   7514 non-null   float64
     9   fighter_b_height   7497 non-null   float64
     10  fighter_a_weight   7516 non-null   float64
     11  fighter_b_weight   7500 non-null   float64
     12  fighter_a_reach    7098 non-null   float64
     13  fighter_b_reach    6615 non-null   float64
     14  fighter_a_stance   7493 non-null   object 
     15  fighter_b_stance   7448 non-null   object 
     16  fighter_a_dob      7442 non-null   object 
     17  fighter_b_dob      7327 non-null   object 
     18  fighter_a_SLpM     7519 non-null   float64
     19  fighter_b_SLpM     7519 non-null   float64
     20  fighter_a_str_acc  7519 non-null   float64
     21  fighter_b_str_acc  7519 non-null   float64
     22  fighter_a_SApM     7519 non-null   float64
     23  fighter_b_SApM     7519 non-null   float64
     24  fighter_a_str_def  7519 non-null   float64
     25  fighter_b_str_def  7519 non-null   float64
     26  fighter_a_TD_avg   7519 non-null   float64
     27  fighter_b_TD_avg   7519 non-null   float64
     28  fighter_a_TD_acc   7519 non-null   float64
     29  fighter_b_TD_acc   7519 non-null   float64
     30  fighter_a_TD_def   7519 non-null   float64
     31  fighter_b_TD_def   7519 non-null   float64
     32  fighter_a_sub_avg  7519 non-null   float64
     33  fighter_b_sub_avg  7519 non-null   float64
    dtypes: float64(22), object(12)
    memory usage: 2.0+ MB
    


```python
# Lets describe our dataset - We are trying to understand which of our columns are categorical and 
# which are continous as this will change how we deal with them in later steps
empty_values = dataframe.isna().sum()
empty_values = empty_values[empty_values > 0]
empty_values
```




    fighter_a_height      5
    fighter_b_height     22
    fighter_a_weight      3
    fighter_b_weight     19
    fighter_a_reach     421
    fighter_b_reach     904
    fighter_a_stance     26
    fighter_b_stance     71
    fighter_a_dob        77
    fighter_b_dob       192
    dtype: int64



When we look at the missing values we can see some values are missing much more than other. As a general rule we don't want to lose information if we can help it particularly if we think it will be useful for our model.

The missing values in this dataset I would suspect is caused by a combination of two things:

1. Earlier fights in the UFC don't have as strong stats records
2. Fighters that had a shorter career (usually due to them being released by the UFC) often don't have full stats, this is particularly common when the fight is also an earlier fight.

Let's investigate!!




```python
# Investigating the missing 904 values from 'fighter_b_reach'
#dataframe[dataframe['fighter_b_reach'].isna()]
missing_value_data = dataframe[dataframe.isna().any(axis=1)]
missing_value_data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fight_id</th>
      <th>fighter_a_id_FK</th>
      <th>event_id_FK</th>
      <th>winner</th>
      <th>name</th>
      <th>date</th>
      <th>fighter_a_name</th>
      <th>fighter_b_name</th>
      <th>fighter_a_height</th>
      <th>fighter_b_height</th>
      <th>fighter_a_weight</th>
      <th>fighter_b_weight</th>
      <th>fighter_a_reach</th>
      <th>fighter_b_reach</th>
      <th>fighter_a_stance</th>
      <th>fighter_b_stance</th>
      <th>fighter_a_dob</th>
      <th>fighter_b_dob</th>
      <th>fighter_a_SLpM</th>
      <th>fighter_b_SLpM</th>
      <th>fighter_a_str_acc</th>
      <th>fighter_b_str_acc</th>
      <th>fighter_a_SApM</th>
      <th>fighter_b_SApM</th>
      <th>fighter_a_str_def</th>
      <th>fighter_b_str_def</th>
      <th>fighter_a_TD_avg</th>
      <th>fighter_b_TD_avg</th>
      <th>fighter_a_TD_acc</th>
      <th>fighter_b_TD_acc</th>
      <th>fighter_a_TD_def</th>
      <th>fighter_b_TD_def</th>
      <th>fighter_a_sub_avg</th>
      <th>fighter_b_sub_avg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>0027e179b743c86c</td>
      <td>91ea901c458e95dd</td>
      <td>f54200f1dfb9b5d4</td>
      <td>Fighter A</td>
      <td>UFC 185: Pettis vs Dos Anjos</td>
      <td>2015-03-14</td>
      <td>Jared Rosholt</td>
      <td>Josh Copeland</td>
      <td>74.0</td>
      <td>73.0</td>
      <td>265.0</td>
      <td>265.0</td>
      <td>75.0</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1986-08-04</td>
      <td>1982-10-20</td>
      <td>2.08</td>
      <td>1.03</td>
      <td>46.0</td>
      <td>31.0</td>
      <td>1.52</td>
      <td>3.01</td>
      <td>59.0</td>
      <td>55.0</td>
      <td>1.83</td>
      <td>0.00</td>
      <td>41.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>57.0</td>
      <td>0.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>0072df705378477c</td>
      <td>9b68bf67c5695185</td>
      <td>2f3f12002564bb55</td>
      <td>Fighter B</td>
      <td>UFC 117: Silva vs Sonnen</td>
      <td>2010-08-07</td>
      <td>Todd Brown</td>
      <td>Tim Boetsch</td>
      <td>71.0</td>
      <td>72.0</td>
      <td>205.0</td>
      <td>185.0</td>
      <td>NaN</td>
      <td>74.0</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1976-12-13</td>
      <td>1981-01-28</td>
      <td>2.15</td>
      <td>2.93</td>
      <td>45.0</td>
      <td>50.0</td>
      <td>3.85</td>
      <td>2.90</td>
      <td>48.0</td>
      <td>57.0</td>
      <td>0.00</td>
      <td>1.45</td>
      <td>0.0</td>
      <td>34.0</td>
      <td>50.0</td>
      <td>59.0</td>
      <td>0.0</td>
      <td>0.8</td>
    </tr>
    <tr>
      <th>22</th>
      <td>00731068c3195f7f</td>
      <td>22aa91e402d0fe1f</td>
      <td>505934897b8b4824</td>
      <td>Fighter A</td>
      <td>UFC on FX: Maynard vs Guida</td>
      <td>2012-06-22</td>
      <td>Ramsey Nijem</td>
      <td>CJ Keith</td>
      <td>71.0</td>
      <td>72.0</td>
      <td>155.0</td>
      <td>155.0</td>
      <td>75.0</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1988-04-01</td>
      <td>1986-08-09</td>
      <td>3.05</td>
      <td>0.86</td>
      <td>44.0</td>
      <td>50.0</td>
      <td>1.62</td>
      <td>1.82</td>
      <td>62.0</td>
      <td>50.0</td>
      <td>5.32</td>
      <td>0.00</td>
      <td>62.0</td>
      <td>0.0</td>
      <td>55.0</td>
      <td>62.0</td>
      <td>1.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>00835554f95fa911</td>
      <td>429e7d3725852ce9</td>
      <td>a6a9ab5a824e8f66</td>
      <td>Fighter A</td>
      <td>UFC 2: No Way Out</td>
      <td>1994-03-11</td>
      <td>Royce Gracie</td>
      <td>Patrick Smith</td>
      <td>73.0</td>
      <td>74.0</td>
      <td>175.0</td>
      <td>225.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Southpaw</td>
      <td>Orthodox</td>
      <td>1966-12-12</td>
      <td>1963-08-28</td>
      <td>0.88</td>
      <td>0.00</td>
      <td>41.0</td>
      <td>0.0</td>
      <td>1.13</td>
      <td>0.00</td>
      <td>37.0</td>
      <td>0.0</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>0.0</td>
      <td>0.8</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>008d0158831dcbd4</td>
      <td>1fcfc3709fe58151</td>
      <td>194fc025f9355db6</td>
      <td>Fighter A</td>
      <td>UFC Fight Night: Jedrzejczyk vs Penne</td>
      <td>2015-06-20</td>
      <td>Peter Sobotta</td>
      <td>Steve Kennedy</td>
      <td>72.0</td>
      <td>71.0</td>
      <td>170.0</td>
      <td>170.0</td>
      <td>75.0</td>
      <td>NaN</td>
      <td>Southpaw</td>
      <td>Orthodox</td>
      <td>1987-01-11</td>
      <td>1983-03-07</td>
      <td>2.14</td>
      <td>2.28</td>
      <td>40.0</td>
      <td>35.0</td>
      <td>2.90</td>
      <td>5.52</td>
      <td>58.0</td>
      <td>45.0</td>
      <td>1.53</td>
      <td>2.51</td>
      <td>32.0</td>
      <td>33.0</td>
      <td>77.0</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>7486</th>
      <td>fea1931b041cc5ff</td>
      <td>6aa1cbc1466e9a0b</td>
      <td>271fe91f4ba9d2c5</td>
      <td>Fighter A</td>
      <td>UFC 55: Fury</td>
      <td>2005-10-07</td>
      <td>Marcio Cruz</td>
      <td>Keigo Kunihara</td>
      <td>76.0</td>
      <td>72.0</td>
      <td>232.0</td>
      <td>235.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1978-04-24</td>
      <td>None</td>
      <td>2.92</td>
      <td>0.17</td>
      <td>46.0</td>
      <td>10.0</td>
      <td>1.51</td>
      <td>1.99</td>
      <td>68.0</td>
      <td>57.0</td>
      <td>0.53</td>
      <td>4.97</td>
      <td>7.0</td>
      <td>40.0</td>
      <td>37.0</td>
      <td>100.0</td>
      <td>1.6</td>
      <td>2.5</td>
    </tr>
    <tr>
      <th>7495</th>
      <td>fee1d48d7bc17e56</td>
      <td>a8e6a69796280f17</td>
      <td>577ec7e108b94be3</td>
      <td>Fighter A</td>
      <td>Ortiz vs Shamrock 3: The Final Chapter</td>
      <td>2006-10-10</td>
      <td>Nate Marquardt</td>
      <td>Crafton Wallace</td>
      <td>72.0</td>
      <td>72.0</td>
      <td>185.0</td>
      <td>185.0</td>
      <td>74.0</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1979-04-20</td>
      <td>1975-11-10</td>
      <td>2.71</td>
      <td>1.55</td>
      <td>49.0</td>
      <td>44.0</td>
      <td>2.32</td>
      <td>2.36</td>
      <td>55.0</td>
      <td>47.0</td>
      <td>1.87</td>
      <td>0.00</td>
      <td>51.0</td>
      <td>0.0</td>
      <td>70.0</td>
      <td>42.0</td>
      <td>0.8</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7509</th>
      <td>ff8802aae3b81c3f</td>
      <td>75e5fec9f72910ef</td>
      <td>304fcd812f12c589</td>
      <td>Fighter A</td>
      <td>UFC Fight Night: Stout vs Fisher</td>
      <td>2007-06-12</td>
      <td>Gleison Tibau</td>
      <td>Jeff Cox</td>
      <td>70.0</td>
      <td>70.0</td>
      <td>155.0</td>
      <td>155.0</td>
      <td>71.0</td>
      <td>NaN</td>
      <td>Southpaw</td>
      <td>Orthodox</td>
      <td>1983-10-07</td>
      <td>1968-08-02</td>
      <td>1.95</td>
      <td>0.56</td>
      <td>31.0</td>
      <td>25.0</td>
      <td>2.51</td>
      <td>1.69</td>
      <td>63.0</td>
      <td>33.0</td>
      <td>4.08</td>
      <td>4.23</td>
      <td>53.0</td>
      <td>50.0</td>
      <td>92.0</td>
      <td>80.0</td>
      <td>0.8</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7514</th>
      <td>ffe4379d6bd1e82b</td>
      <td>2a542ee8a8b83559</td>
      <td>0cf935519d439ba6</td>
      <td>Fighter A</td>
      <td>UFC 39: The Warriors Return</td>
      <td>2002-09-27</td>
      <td>Tim Sylvia</td>
      <td>Wesley Correira</td>
      <td>80.0</td>
      <td>75.0</td>
      <td>265.0</td>
      <td>260.0</td>
      <td>80.0</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1976-03-05</td>
      <td>1978-11-11</td>
      <td>4.23</td>
      <td>2.60</td>
      <td>41.0</td>
      <td>36.0</td>
      <td>2.61</td>
      <td>8.80</td>
      <td>61.0</td>
      <td>40.0</td>
      <td>0.11</td>
      <td>0.00</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>75.0</td>
      <td>90.0</td>
      <td>0.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7515</th>
      <td>ffe629a5232a878b</td>
      <td>08ae5cd9aef7ddd3</td>
      <td>108afe61a26bcbf4</td>
      <td>Fighter A</td>
      <td>UFC 43: Meltdown</td>
      <td>2003-06-06</td>
      <td>Kimo Leopoldo</td>
      <td>David Abbott</td>
      <td>75.0</td>
      <td>72.0</td>
      <td>235.0</td>
      <td>265.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Switch</td>
      <td>1968-01-05</td>
      <td>None</td>
      <td>0.76</td>
      <td>1.35</td>
      <td>83.0</td>
      <td>30.0</td>
      <td>2.12</td>
      <td>3.55</td>
      <td>30.0</td>
      <td>38.0</td>
      <td>4.55</td>
      <td>1.07</td>
      <td>100.0</td>
      <td>33.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>2.3</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>1068 rows × 34 columns</p>
</div>




```python
# Lets have a look how many missing values are from earlier UFC events - We will make a visual of this
# so it is easier to see!

# first convert the column to a datetime so we can filter
missing_value_data['date'] = pd.to_datetime(missing_value_data['date'], format='%Y-%m-%d')

# next lets declare a year list so we can see what percentage at each year is missing
years = list(range(2000, 2021))
missing_values = [len(missing_value_data[missing_value_data['date'] < str(year)+'-01-01']) 
                  for year in years]

# calculate the percentages so we can label out boxes
total_missing_values = len(missing_value_data['date'])
percentages = [(count / total_missing_values) * 100 for count in missing_values]

# create the bar chart
plt.figure(figsize=(10, 6))
ax = sns.barplot(years, missing_values, color='turquoise')
plt.xlabel('Year')
plt.ylabel('Count of Missing Values')
plt.title('Count of Missing Values Before Each Year')
plt.xticks(rotation=45)

# Add percentage labels
for i, p in enumerate(ax.patches):
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2.,
            height + 0.1,
            f'{percentages[i]:.2f}%',
            ha='center', va='bottom', rotation=90)

plt.tight_layout()

# show the plot
plt.show()
```

    C:\Users\lanna\Anaconda3\lib\site-packages\ipykernel_launcher.py:5: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      """
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variables as keyword args: x, y. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    


    
![png](output_14_1.png)
    


Looking at the the chart above we can see that 77.43% of missing values occur before 2014 as we suspected. We could drop these values but we would lose roughly 700 rows which is about 10% of our data! I don't want to lose that much information so I will impute these missing values.

Before we impute values we need to do two things:
1. Check that our data is in the correct format
2. Understand the distribution of our data

These are important steps as how we impute missing values will depend on what sort of data we have and what distribution that data falls under. For example, if we have continuous data we can impute the mean or median but for categorical we might want to use the mode. For the distribution, if our distribution is normal we can use the mean, but if the distribution is skewed this will artificially increase or decrease the mean as it is sensitive to outliers, in this situation the median value may be more appropriate.


```python
# Lets check our data types are correct
dataframe.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 7519 entries, 0 to 7518
    Data columns (total 34 columns):
     #   Column             Non-Null Count  Dtype  
    ---  ------             --------------  -----  
     0   fight_id           7519 non-null   object 
     1   fighter_a_id_FK    7519 non-null   object 
     2   event_id_FK        7519 non-null   object 
     3   winner             7519 non-null   object 
     4   name               7519 non-null   object 
     5   date               7519 non-null   object 
     6   fighter_a_name     7519 non-null   object 
     7   fighter_b_name     7519 non-null   object 
     8   fighter_a_height   7514 non-null   float64
     9   fighter_b_height   7497 non-null   float64
     10  fighter_a_weight   7516 non-null   float64
     11  fighter_b_weight   7500 non-null   float64
     12  fighter_a_reach    7098 non-null   float64
     13  fighter_b_reach    6615 non-null   float64
     14  fighter_a_stance   7493 non-null   object 
     15  fighter_b_stance   7448 non-null   object 
     16  fighter_a_dob      7442 non-null   object 
     17  fighter_b_dob      7327 non-null   object 
     18  fighter_a_SLpM     7519 non-null   float64
     19  fighter_b_SLpM     7519 non-null   float64
     20  fighter_a_str_acc  7519 non-null   float64
     21  fighter_b_str_acc  7519 non-null   float64
     22  fighter_a_SApM     7519 non-null   float64
     23  fighter_b_SApM     7519 non-null   float64
     24  fighter_a_str_def  7519 non-null   float64
     25  fighter_b_str_def  7519 non-null   float64
     26  fighter_a_TD_avg   7519 non-null   float64
     27  fighter_b_TD_avg   7519 non-null   float64
     28  fighter_a_TD_acc   7519 non-null   float64
     29  fighter_b_TD_acc   7519 non-null   float64
     30  fighter_a_TD_def   7519 non-null   float64
     31  fighter_b_TD_def   7519 non-null   float64
     32  fighter_a_sub_avg  7519 non-null   float64
     33  fighter_b_sub_avg  7519 non-null   float64
    dtypes: float64(22), object(12)
    memory usage: 2.0+ MB
    

We can see from the above most of our data is in the format of float64, which is what we expect given what the columns represent. We have some object values though which normally represent text values. Looking at our table information we can work out some of these columns are categorical variables stored as text such as stance and winner. To deal with this we should encode these categorical variable as numeric values so we can work with them easily. 

In addition, some of the other values aren't required such as names...

Finally, the DOB column requires some feature engineering to convert it into age. We will note this down to complete in the feature engineering section later!


```python
# First we are going to encode the stance columns

# Let check the values to make sure we don't have any weird values we weren't expecting
print(dataframe['fighter_a_stance'].value_counts())
print(dataframe['fighter_b_stance'].value_counts())
```

    Orthodox       5623
    Southpaw       1506
    Switch          347
    Open Stance      15
    Sideways          2
    Name: fighter_a_stance, dtype: int64
    Orthodox       5588
    Southpaw       1446
    Switch          401
    Open Stance       9
    Sideways          4
    Name: fighter_b_stance, dtype: int64
    


```python
# So we have some values I wasn't expecting in 'Open Stance' & 'Sideways' lets have a look at these values
# before we decide what to do with them
dataframe.loc[dataframe['fighter_a_stance'] == 'Open Stance']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fight_id</th>
      <th>fighter_a_id_FK</th>
      <th>event_id_FK</th>
      <th>winner</th>
      <th>name</th>
      <th>date</th>
      <th>fighter_a_name</th>
      <th>fighter_b_name</th>
      <th>fighter_a_height</th>
      <th>fighter_b_height</th>
      <th>fighter_a_weight</th>
      <th>fighter_b_weight</th>
      <th>fighter_a_reach</th>
      <th>fighter_b_reach</th>
      <th>fighter_a_stance</th>
      <th>fighter_b_stance</th>
      <th>fighter_a_dob</th>
      <th>fighter_b_dob</th>
      <th>fighter_a_SLpM</th>
      <th>fighter_b_SLpM</th>
      <th>fighter_a_str_acc</th>
      <th>fighter_b_str_acc</th>
      <th>fighter_a_SApM</th>
      <th>fighter_b_SApM</th>
      <th>fighter_a_str_def</th>
      <th>fighter_b_str_def</th>
      <th>fighter_a_TD_avg</th>
      <th>fighter_b_TD_avg</th>
      <th>fighter_a_TD_acc</th>
      <th>fighter_b_TD_acc</th>
      <th>fighter_a_TD_def</th>
      <th>fighter_b_TD_def</th>
      <th>fighter_a_sub_avg</th>
      <th>fighter_b_sub_avg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>456</th>
      <td>0ea087a71863184d</td>
      <td>59583ff832fe9d68</td>
      <td>49efbdc6c9f650c4</td>
      <td>Fighter A</td>
      <td>UFC 110: Nogueira vs Velasquez</td>
      <td>2010-02-20</td>
      <td>Krzysztof Soszynski</td>
      <td>Stephan Bonnar</td>
      <td>73.0</td>
      <td>76.0</td>
      <td>205.0</td>
      <td>205.0</td>
      <td>77.0</td>
      <td>79.0</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1977-08-02</td>
      <td>1977-04-04</td>
      <td>3.37</td>
      <td>2.76</td>
      <td>39.0</td>
      <td>38.0</td>
      <td>3.13</td>
      <td>3.01</td>
      <td>58.0</td>
      <td>52.0</td>
      <td>0.52</td>
      <td>1.32</td>
      <td>25.0</td>
      <td>40.0</td>
      <td>71.0</td>
      <td>60.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>967</th>
      <td>1f64e532f942ef57</td>
      <td>59583ff832fe9d68</td>
      <td>1652f3213655b935</td>
      <td>Fighter A</td>
      <td>UFC 97: Redemption</td>
      <td>2009-04-18</td>
      <td>Krzysztof Soszynski</td>
      <td>Brian Stann</td>
      <td>73.0</td>
      <td>73.0</td>
      <td>205.0</td>
      <td>205.0</td>
      <td>77.0</td>
      <td>74.0</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1977-08-02</td>
      <td>1980-09-24</td>
      <td>3.37</td>
      <td>3.28</td>
      <td>39.0</td>
      <td>42.0</td>
      <td>3.13</td>
      <td>2.65</td>
      <td>58.0</td>
      <td>59.0</td>
      <td>0.52</td>
      <td>0.12</td>
      <td>25.0</td>
      <td>12.0</td>
      <td>71.0</td>
      <td>60.0</td>
      <td>1.0</td>
      <td>0.3</td>
    </tr>
    <tr>
      <th>2466</th>
      <td>516868e246064e2b</td>
      <td>52cae54377b433b7</td>
      <td>3ed134d85dfbd7b4</td>
      <td>Fighter B</td>
      <td>UFC Fight Night: Florian vs Gomi</td>
      <td>2010-03-31</td>
      <td>Nate Quarry</td>
      <td>Jorge Rivera</td>
      <td>72.0</td>
      <td>73.0</td>
      <td>185.0</td>
      <td>185.0</td>
      <td>72.0</td>
      <td>73.0</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1972-03-18</td>
      <td>1972-02-28</td>
      <td>4.96</td>
      <td>3.16</td>
      <td>44.0</td>
      <td>48.0</td>
      <td>2.80</td>
      <td>2.64</td>
      <td>66.0</td>
      <td>54.0</td>
      <td>0.25</td>
      <td>0.84</td>
      <td>33.0</td>
      <td>50.0</td>
      <td>60.0</td>
      <td>63.0</td>
      <td>0.0</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>2530</th>
      <td>536c26ef4da9ace7</td>
      <td>59583ff832fe9d68</td>
      <td>140745cbbcb023ac</td>
      <td>Fighter B</td>
      <td>UFC 116: Lesnar vs Carwin</td>
      <td>2010-07-03</td>
      <td>Krzysztof Soszynski</td>
      <td>Stephan Bonnar</td>
      <td>73.0</td>
      <td>76.0</td>
      <td>205.0</td>
      <td>205.0</td>
      <td>77.0</td>
      <td>79.0</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1977-08-02</td>
      <td>1977-04-04</td>
      <td>3.37</td>
      <td>2.76</td>
      <td>39.0</td>
      <td>38.0</td>
      <td>3.13</td>
      <td>3.01</td>
      <td>58.0</td>
      <td>52.0</td>
      <td>0.52</td>
      <td>1.32</td>
      <td>25.0</td>
      <td>40.0</td>
      <td>71.0</td>
      <td>60.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2861</th>
      <td>5e3f46e6f46d5a90</td>
      <td>59583ff832fe9d68</td>
      <td>0ff11cc094e887bc</td>
      <td>Fighter A</td>
      <td>UFC 122: Marquardt vs Okami</td>
      <td>2010-11-13</td>
      <td>Krzysztof Soszynski</td>
      <td>Goran Reljic</td>
      <td>73.0</td>
      <td>75.0</td>
      <td>205.0</td>
      <td>205.0</td>
      <td>77.0</td>
      <td>81.0</td>
      <td>Open Stance</td>
      <td>Southpaw</td>
      <td>1977-08-02</td>
      <td>1984-03-20</td>
      <td>3.37</td>
      <td>1.69</td>
      <td>39.0</td>
      <td>37.0</td>
      <td>3.13</td>
      <td>2.69</td>
      <td>58.0</td>
      <td>59.0</td>
      <td>0.52</td>
      <td>1.69</td>
      <td>25.0</td>
      <td>50.0</td>
      <td>71.0</td>
      <td>33.0</td>
      <td>1.0</td>
      <td>1.1</td>
    </tr>
    <tr>
      <th>3617</th>
      <td>793432d042384a02</td>
      <td>52cae54377b433b7</td>
      <td>1652f3213655b935</td>
      <td>Fighter A</td>
      <td>UFC 97: Redemption</td>
      <td>2009-04-18</td>
      <td>Nate Quarry</td>
      <td>Jason MacDonald</td>
      <td>72.0</td>
      <td>75.0</td>
      <td>185.0</td>
      <td>185.0</td>
      <td>72.0</td>
      <td>80.0</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1972-03-18</td>
      <td>1975-06-03</td>
      <td>4.96</td>
      <td>1.55</td>
      <td>44.0</td>
      <td>52.0</td>
      <td>2.80</td>
      <td>2.70</td>
      <td>66.0</td>
      <td>46.0</td>
      <td>0.25</td>
      <td>1.43</td>
      <td>33.0</td>
      <td>16.0</td>
      <td>60.0</td>
      <td>35.0</td>
      <td>0.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>5321</th>
      <td>b46679306287ea79</td>
      <td>52cae54377b433b7</td>
      <td>f341f9551ba744e2</td>
      <td>Fighter A</td>
      <td>UFC Fight Night: Thomas vs Florian</td>
      <td>2007-09-19</td>
      <td>Nate Quarry</td>
      <td>Pete Sell</td>
      <td>72.0</td>
      <td>71.0</td>
      <td>185.0</td>
      <td>170.0</td>
      <td>72.0</td>
      <td>75.0</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1972-03-18</td>
      <td>1982-08-05</td>
      <td>4.96</td>
      <td>2.60</td>
      <td>44.0</td>
      <td>42.0</td>
      <td>2.80</td>
      <td>3.65</td>
      <td>66.0</td>
      <td>51.0</td>
      <td>0.25</td>
      <td>0.91</td>
      <td>33.0</td>
      <td>21.0</td>
      <td>60.0</td>
      <td>47.0</td>
      <td>0.0</td>
      <td>0.9</td>
    </tr>
    <tr>
      <th>5362</th>
      <td>b589aba75770bc6b</td>
      <td>52cae54377b433b7</td>
      <td>a8ea84cbe1655f0a</td>
      <td>Fighter A</td>
      <td>UFC Fight Night: Diaz vs Guillard</td>
      <td>2009-09-16</td>
      <td>Nate Quarry</td>
      <td>Tim Credeur</td>
      <td>72.0</td>
      <td>75.0</td>
      <td>185.0</td>
      <td>185.0</td>
      <td>72.0</td>
      <td>75.0</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1972-03-18</td>
      <td>1977-07-09</td>
      <td>4.96</td>
      <td>3.59</td>
      <td>44.0</td>
      <td>30.0</td>
      <td>2.80</td>
      <td>3.13</td>
      <td>66.0</td>
      <td>57.0</td>
      <td>0.25</td>
      <td>0.41</td>
      <td>33.0</td>
      <td>100.0</td>
      <td>60.0</td>
      <td>50.0</td>
      <td>0.0</td>
      <td>3.3</td>
    </tr>
    <tr>
      <th>5388</th>
      <td>b675c94f20551631</td>
      <td>52cae54377b433b7</td>
      <td>ad047e3073a775f3</td>
      <td>Fighter A</td>
      <td>UFC 83: Serra vs St-Pierre 2</td>
      <td>2008-04-19</td>
      <td>Nate Quarry</td>
      <td>Kalib Starnes</td>
      <td>72.0</td>
      <td>75.0</td>
      <td>185.0</td>
      <td>185.0</td>
      <td>72.0</td>
      <td>74.0</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1972-03-18</td>
      <td>1975-01-06</td>
      <td>4.96</td>
      <td>2.71</td>
      <td>44.0</td>
      <td>48.0</td>
      <td>2.80</td>
      <td>4.43</td>
      <td>66.0</td>
      <td>53.0</td>
      <td>0.25</td>
      <td>1.46</td>
      <td>33.0</td>
      <td>33.0</td>
      <td>60.0</td>
      <td>25.0</td>
      <td>0.0</td>
      <td>0.6</td>
    </tr>
    <tr>
      <th>5633</th>
      <td>bf1525f9761a116e</td>
      <td>52cae54377b433b7</td>
      <td>3f24c96753dbd9f9</td>
      <td>Fighter A</td>
      <td>UFC Fight Night 1</td>
      <td>2005-08-06</td>
      <td>Nate Quarry</td>
      <td>Pete Sell</td>
      <td>72.0</td>
      <td>71.0</td>
      <td>185.0</td>
      <td>170.0</td>
      <td>72.0</td>
      <td>75.0</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1972-03-18</td>
      <td>1982-08-05</td>
      <td>4.96</td>
      <td>2.60</td>
      <td>44.0</td>
      <td>42.0</td>
      <td>2.80</td>
      <td>3.65</td>
      <td>66.0</td>
      <td>51.0</td>
      <td>0.25</td>
      <td>0.91</td>
      <td>33.0</td>
      <td>21.0</td>
      <td>60.0</td>
      <td>47.0</td>
      <td>0.0</td>
      <td>0.9</td>
    </tr>
    <tr>
      <th>5981</th>
      <td>ca3230227ee700b7</td>
      <td>52cae54377b433b7</td>
      <td>d3711d3784b76255</td>
      <td>Fighter A</td>
      <td>UFC 53: Heavy Hitters</td>
      <td>2005-06-04</td>
      <td>Nate Quarry</td>
      <td>Shonie Carter</td>
      <td>72.0</td>
      <td>70.0</td>
      <td>185.0</td>
      <td>170.0</td>
      <td>72.0</td>
      <td>NaN</td>
      <td>Open Stance</td>
      <td>Southpaw</td>
      <td>1972-03-18</td>
      <td>1972-05-03</td>
      <td>4.96</td>
      <td>1.62</td>
      <td>44.0</td>
      <td>36.0</td>
      <td>2.80</td>
      <td>2.32</td>
      <td>66.0</td>
      <td>47.0</td>
      <td>0.25</td>
      <td>0.75</td>
      <td>33.0</td>
      <td>66.0</td>
      <td>60.0</td>
      <td>75.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>6493</th>
      <td>dd400f38c483f629</td>
      <td>59583ff832fe9d68</td>
      <td>c4b6099f0d25f75e</td>
      <td>Fighter A</td>
      <td>UFC 98: Evans vs Machida</td>
      <td>2009-05-23</td>
      <td>Krzysztof Soszynski</td>
      <td>Andre Gusmao</td>
      <td>73.0</td>
      <td>72.0</td>
      <td>205.0</td>
      <td>205.0</td>
      <td>77.0</td>
      <td>NaN</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1977-08-02</td>
      <td>1977-05-19</td>
      <td>3.37</td>
      <td>2.79</td>
      <td>39.0</td>
      <td>43.0</td>
      <td>3.13</td>
      <td>3.28</td>
      <td>58.0</td>
      <td>60.0</td>
      <td>0.52</td>
      <td>0.00</td>
      <td>25.0</td>
      <td>0.0</td>
      <td>71.0</td>
      <td>60.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>6577</th>
      <td>e03ec6b24fca2386</td>
      <td>59583ff832fe9d68</td>
      <td>6d7886b094b471ac</td>
      <td>Fighter B</td>
      <td>UFC 140: Jones vs Machida</td>
      <td>2011-12-10</td>
      <td>Krzysztof Soszynski</td>
      <td>Igor Pokrajac</td>
      <td>73.0</td>
      <td>72.0</td>
      <td>205.0</td>
      <td>205.0</td>
      <td>77.0</td>
      <td>74.0</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1977-08-02</td>
      <td>1979-01-02</td>
      <td>3.37</td>
      <td>2.25</td>
      <td>39.0</td>
      <td>45.0</td>
      <td>3.13</td>
      <td>4.26</td>
      <td>58.0</td>
      <td>40.0</td>
      <td>0.52</td>
      <td>0.87</td>
      <td>25.0</td>
      <td>29.0</td>
      <td>71.0</td>
      <td>51.0</td>
      <td>1.0</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>7001</th>
      <td>edeba52fc9b2855f</td>
      <td>59583ff832fe9d68</td>
      <td>ea398c802d9998ee</td>
      <td>Fighter A</td>
      <td>The Ultimate Fighter: Team Nogueira vs. Team M...</td>
      <td>2008-12-13</td>
      <td>Krzysztof Soszynski</td>
      <td>Shane Primm</td>
      <td>73.0</td>
      <td>75.0</td>
      <td>205.0</td>
      <td>205.0</td>
      <td>77.0</td>
      <td>NaN</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1977-08-02</td>
      <td>1984-07-30</td>
      <td>3.37</td>
      <td>0.83</td>
      <td>39.0</td>
      <td>26.0</td>
      <td>3.13</td>
      <td>2.25</td>
      <td>58.0</td>
      <td>62.0</td>
      <td>0.52</td>
      <td>1.78</td>
      <td>25.0</td>
      <td>20.0</td>
      <td>71.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7181</th>
      <td>f434775e97920d95</td>
      <td>52cae54377b433b7</td>
      <td>fbbde91f7bc2d3c5</td>
      <td>Fighter A</td>
      <td>The Ultimate Fighter: Team Couture vs. Team Li...</td>
      <td>2005-04-09</td>
      <td>Nate Quarry</td>
      <td>Lodune Sincaid</td>
      <td>72.0</td>
      <td>69.0</td>
      <td>185.0</td>
      <td>185.0</td>
      <td>72.0</td>
      <td>NaN</td>
      <td>Open Stance</td>
      <td>Orthodox</td>
      <td>1972-03-18</td>
      <td>1973-05-07</td>
      <td>4.96</td>
      <td>2.72</td>
      <td>44.0</td>
      <td>42.0</td>
      <td>2.80</td>
      <td>6.17</td>
      <td>66.0</td>
      <td>57.0</td>
      <td>0.25</td>
      <td>0.00</td>
      <td>33.0</td>
      <td>0.0</td>
      <td>60.0</td>
      <td>75.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Now we have encoded the stance let encode the the winner column
# first lets have a look at the values
dataframe['winner'].value_counts()
```




    Fighter A     4842
    Fighter B     2535
    No Contest      84
    Draw            58
    Name: winner, dtype: int64



When looking at the target variable (the one we are trying to predict) we have discovered a few interesting things that we need to deal with. ...that our target variable, the winner column, is unbalanced!
This can be a big deal in machine learning. Let look at why! 

In our dataset the split on the target variable  is roughly 64% fighter a and 33% fighter b (with the remaining no contests and draws). If I train a model with this split the model might overfit to the overrepresented class, in this case fighter a.

This is particularly an issue because our model would show an accuracy around 64%, but the model will be incredibly fragile. Meaning that our model performance could suffer greatly in production! 

The most common way to deal with an unbalanced dataset is to resample our data. Resampling can be split into two main types:
1. Undersampling - 
2. Oversampling - 

Alternatively, we could create synthetic data using tools like SMOTE. However, in this case I will use oversampling of the minority class to solve the imbalance. We will deal with this problem later when we do our feature engineering but for now we will encode the winner column into numerical values to make it easier to work with when we train our model.

meaning the split in the classes are not equal. Because of some background knowledge of the UFC I know that the 'Red corner' fighter or Fighter_a in our data is the higher ranked fighter that it is common for them to win, so this could be an important feature to use, however, I want to base my model of the stats of a fighter and not use the corner as a feature. To do this I need to split the data so there is a 50/50 split between fighter A winning and fighter B. Luckily this is easy enough with our data set


```python
# Create encoder object
encoder = LabelEncoder()

# Fit and transform the 'winner' column
encoder.fit(dataframe['winner'])
dataframe['winner'] = encoder.transform(dataframe['winner'])

# check the values in the column
dataframe
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fight_id</th>
      <th>fighter_a_id_FK</th>
      <th>event_id_FK</th>
      <th>winner</th>
      <th>name</th>
      <th>date</th>
      <th>fighter_a_name</th>
      <th>fighter_b_name</th>
      <th>fighter_a_height</th>
      <th>fighter_b_height</th>
      <th>fighter_a_weight</th>
      <th>fighter_b_weight</th>
      <th>fighter_a_reach</th>
      <th>fighter_b_reach</th>
      <th>fighter_a_stance</th>
      <th>fighter_b_stance</th>
      <th>fighter_a_dob</th>
      <th>fighter_b_dob</th>
      <th>fighter_a_SLpM</th>
      <th>fighter_b_SLpM</th>
      <th>fighter_a_str_acc</th>
      <th>fighter_b_str_acc</th>
      <th>fighter_a_SApM</th>
      <th>fighter_b_SApM</th>
      <th>fighter_a_str_def</th>
      <th>fighter_b_str_def</th>
      <th>fighter_a_TD_avg</th>
      <th>fighter_b_TD_avg</th>
      <th>fighter_a_TD_acc</th>
      <th>fighter_b_TD_acc</th>
      <th>fighter_a_TD_def</th>
      <th>fighter_b_TD_def</th>
      <th>fighter_a_sub_avg</th>
      <th>fighter_b_sub_avg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0005e00b07cee542</td>
      <td>634e2fb70bde3fd5</td>
      <td>805ad1801eb26abb</td>
      <td>1</td>
      <td>UFC Fight Night: Holm vs. Aldana</td>
      <td>2020-10-03</td>
      <td>Holly Holm</td>
      <td>Irene Aldana</td>
      <td>68.0</td>
      <td>69.0</td>
      <td>135.0</td>
      <td>135.0</td>
      <td>69.0</td>
      <td>68.0</td>
      <td>Southpaw</td>
      <td>Orthodox</td>
      <td>1981-10-17</td>
      <td>1988-03-26</td>
      <td>3.21</td>
      <td>5.24</td>
      <td>40.0</td>
      <td>40.0</td>
      <td>2.79</td>
      <td>6.33</td>
      <td>56.0</td>
      <td>57.0</td>
      <td>0.90</td>
      <td>0.16</td>
      <td>30.0</td>
      <td>50.0</td>
      <td>78.0</td>
      <td>76.0</td>
      <td>0.1</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>000da3152b7b5ab1</td>
      <td>6da99156486ed6c2</td>
      <td>f70144caea5c4c80</td>
      <td>1</td>
      <td>UFC 61: Bitter Rivals</td>
      <td>2006-07-08</td>
      <td>Joshua Burkman</td>
      <td>Josh Neer</td>
      <td>70.0</td>
      <td>71.0</td>
      <td>170.0</td>
      <td>170.0</td>
      <td>72.0</td>
      <td>72.0</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1980-04-10</td>
      <td>1983-03-24</td>
      <td>2.69</td>
      <td>3.29</td>
      <td>43.0</td>
      <td>46.0</td>
      <td>3.13</td>
      <td>3.63</td>
      <td>51.0</td>
      <td>58.0</td>
      <td>2.53</td>
      <td>1.09</td>
      <td>36.0</td>
      <td>34.0</td>
      <td>72.0</td>
      <td>46.0</td>
      <td>0.3</td>
      <td>1.3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>001441f70c293931</td>
      <td>7826923b47f8d72a</td>
      <td>1d00756835ca67c9</td>
      <td>1</td>
      <td>UFC Fight Night: Volkov vs. Aspinall</td>
      <td>2022-03-19</td>
      <td>Paddy Pimblett</td>
      <td>Kazula Vargas</td>
      <td>70.0</td>
      <td>68.0</td>
      <td>155.0</td>
      <td>155.0</td>
      <td>73.0</td>
      <td>71.0</td>
      <td>Orthodox</td>
      <td>Southpaw</td>
      <td>1995-01-03</td>
      <td>1985-08-15</td>
      <td>5.13</td>
      <td>3.65</td>
      <td>52.0</td>
      <td>53.0</td>
      <td>3.70</td>
      <td>1.77</td>
      <td>41.0</td>
      <td>57.0</td>
      <td>0.98</td>
      <td>0.40</td>
      <td>25.0</td>
      <td>25.0</td>
      <td>56.0</td>
      <td>30.0</td>
      <td>1.6</td>
      <td>0.4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0019ec81fd706ade</td>
      <td>85073dbd1be65ed9</td>
      <td>3ae10ac4df3df05c</td>
      <td>3</td>
      <td>UFC Fight Night: Reyes vs. Weidman</td>
      <td>2019-10-18</td>
      <td>Greg Hardy</td>
      <td>Ben Sosoli</td>
      <td>77.0</td>
      <td>72.0</td>
      <td>265.0</td>
      <td>265.0</td>
      <td>80.0</td>
      <td>72.0</td>
      <td>Orthodox</td>
      <td>Southpaw</td>
      <td>1988-07-28</td>
      <td>1989-12-10</td>
      <td>4.79</td>
      <td>2.31</td>
      <td>50.0</td>
      <td>31.0</td>
      <td>3.31</td>
      <td>4.30</td>
      <td>55.0</td>
      <td>47.0</td>
      <td>0.20</td>
      <td>0.00</td>
      <td>33.0</td>
      <td>0.0</td>
      <td>64.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0027e179b743c86c</td>
      <td>91ea901c458e95dd</td>
      <td>f54200f1dfb9b5d4</td>
      <td>1</td>
      <td>UFC 185: Pettis vs Dos Anjos</td>
      <td>2015-03-14</td>
      <td>Jared Rosholt</td>
      <td>Josh Copeland</td>
      <td>74.0</td>
      <td>73.0</td>
      <td>265.0</td>
      <td>265.0</td>
      <td>75.0</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1986-08-04</td>
      <td>1982-10-20</td>
      <td>2.08</td>
      <td>1.03</td>
      <td>46.0</td>
      <td>31.0</td>
      <td>1.52</td>
      <td>3.01</td>
      <td>59.0</td>
      <td>55.0</td>
      <td>1.83</td>
      <td>0.00</td>
      <td>41.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>57.0</td>
      <td>0.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>7514</th>
      <td>ffe4379d6bd1e82b</td>
      <td>2a542ee8a8b83559</td>
      <td>0cf935519d439ba6</td>
      <td>1</td>
      <td>UFC 39: The Warriors Return</td>
      <td>2002-09-27</td>
      <td>Tim Sylvia</td>
      <td>Wesley Correira</td>
      <td>80.0</td>
      <td>75.0</td>
      <td>265.0</td>
      <td>260.0</td>
      <td>80.0</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1976-03-05</td>
      <td>1978-11-11</td>
      <td>4.23</td>
      <td>2.60</td>
      <td>41.0</td>
      <td>36.0</td>
      <td>2.61</td>
      <td>8.80</td>
      <td>61.0</td>
      <td>40.0</td>
      <td>0.11</td>
      <td>0.00</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>75.0</td>
      <td>90.0</td>
      <td>0.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7515</th>
      <td>ffe629a5232a878b</td>
      <td>08ae5cd9aef7ddd3</td>
      <td>108afe61a26bcbf4</td>
      <td>1</td>
      <td>UFC 43: Meltdown</td>
      <td>2003-06-06</td>
      <td>Kimo Leopoldo</td>
      <td>David Abbott</td>
      <td>75.0</td>
      <td>72.0</td>
      <td>235.0</td>
      <td>265.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Switch</td>
      <td>1968-01-05</td>
      <td>None</td>
      <td>0.76</td>
      <td>1.35</td>
      <td>83.0</td>
      <td>30.0</td>
      <td>2.12</td>
      <td>3.55</td>
      <td>30.0</td>
      <td>38.0</td>
      <td>4.55</td>
      <td>1.07</td>
      <td>100.0</td>
      <td>33.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>2.3</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7516</th>
      <td>ffea776913451b6d</td>
      <td>22a92d7f62195791</td>
      <td>ad4e9055bf8cd04d</td>
      <td>1</td>
      <td>UFC 184: Rousey vs Zingano</td>
      <td>2015-02-28</td>
      <td>Tony Ferguson</td>
      <td>Gleison Tibau</td>
      <td>71.0</td>
      <td>70.0</td>
      <td>155.0</td>
      <td>155.0</td>
      <td>76.0</td>
      <td>71.0</td>
      <td>Orthodox</td>
      <td>Southpaw</td>
      <td>1984-02-12</td>
      <td>1983-10-07</td>
      <td>4.94</td>
      <td>1.95</td>
      <td>45.0</td>
      <td>31.0</td>
      <td>4.41</td>
      <td>2.51</td>
      <td>55.0</td>
      <td>63.0</td>
      <td>0.39</td>
      <td>4.08</td>
      <td>35.0</td>
      <td>53.0</td>
      <td>67.0</td>
      <td>92.0</td>
      <td>0.9</td>
      <td>0.8</td>
    </tr>
    <tr>
      <th>7517</th>
      <td>fffa21388cdd78b7</td>
      <td>c80095f6092271a7</td>
      <td>eae4aec1a5a8ff01</td>
      <td>1</td>
      <td>UFC 166: Velasquez vs Dos Santos 3</td>
      <td>2013-10-19</td>
      <td>Tim Boetsch</td>
      <td>CB Dollaway</td>
      <td>72.0</td>
      <td>74.0</td>
      <td>185.0</td>
      <td>185.0</td>
      <td>74.0</td>
      <td>76.0</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1981-01-28</td>
      <td>1983-08-10</td>
      <td>2.93</td>
      <td>2.65</td>
      <td>50.0</td>
      <td>47.0</td>
      <td>2.90</td>
      <td>2.58</td>
      <td>57.0</td>
      <td>54.0</td>
      <td>1.45</td>
      <td>3.55</td>
      <td>34.0</td>
      <td>54.0</td>
      <td>59.0</td>
      <td>62.0</td>
      <td>0.8</td>
      <td>1.2</td>
    </tr>
    <tr>
      <th>7518</th>
      <td>fffdc57255274be1</td>
      <td>2f5cbecbbe18bac4</td>
      <td>5717efc6f271cd52</td>
      <td>2</td>
      <td>UFC 283: Teixeira vs. Hill</td>
      <td>2023-01-21</td>
      <td>Shamil Abdurakhimov</td>
      <td>Jailton Almeida</td>
      <td>75.0</td>
      <td>75.0</td>
      <td>235.0</td>
      <td>205.0</td>
      <td>76.0</td>
      <td>79.0</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1981-09-02</td>
      <td>1991-06-26</td>
      <td>2.41</td>
      <td>2.78</td>
      <td>44.0</td>
      <td>64.0</td>
      <td>3.02</td>
      <td>0.52</td>
      <td>55.0</td>
      <td>43.0</td>
      <td>1.01</td>
      <td>5.14</td>
      <td>23.0</td>
      <td>55.0</td>
      <td>45.0</td>
      <td>75.0</td>
      <td>0.1</td>
      <td>2.4</td>
    </tr>
  </tbody>
</table>
<p>7519 rows × 34 columns</p>
</div>




```python
# Next lets drop the columns that we don't need 
columns_to_remove = ['fight_id', 'fighter_a_id_FK', 'event_id_FK', 'name', 'date', 'fighter_a_name', 
                    'fighter_b_name']

dataframe.drop(columns=columns_to_remove, axis=1, inplace=True)
dataframe
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>winner</th>
      <th>fighter_a_height</th>
      <th>fighter_b_height</th>
      <th>fighter_a_weight</th>
      <th>fighter_b_weight</th>
      <th>fighter_a_reach</th>
      <th>fighter_b_reach</th>
      <th>fighter_a_stance</th>
      <th>fighter_b_stance</th>
      <th>fighter_a_dob</th>
      <th>fighter_b_dob</th>
      <th>fighter_a_SLpM</th>
      <th>fighter_b_SLpM</th>
      <th>fighter_a_str_acc</th>
      <th>fighter_b_str_acc</th>
      <th>fighter_a_SApM</th>
      <th>fighter_b_SApM</th>
      <th>fighter_a_str_def</th>
      <th>fighter_b_str_def</th>
      <th>fighter_a_TD_avg</th>
      <th>fighter_b_TD_avg</th>
      <th>fighter_a_TD_acc</th>
      <th>fighter_b_TD_acc</th>
      <th>fighter_a_TD_def</th>
      <th>fighter_b_TD_def</th>
      <th>fighter_a_sub_avg</th>
      <th>fighter_b_sub_avg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>68.0</td>
      <td>69.0</td>
      <td>135.0</td>
      <td>135.0</td>
      <td>69.0</td>
      <td>68.0</td>
      <td>Southpaw</td>
      <td>Orthodox</td>
      <td>1981-10-17</td>
      <td>1988-03-26</td>
      <td>3.21</td>
      <td>5.24</td>
      <td>40.0</td>
      <td>40.0</td>
      <td>2.79</td>
      <td>6.33</td>
      <td>56.0</td>
      <td>57.0</td>
      <td>0.90</td>
      <td>0.16</td>
      <td>30.0</td>
      <td>50.0</td>
      <td>78.0</td>
      <td>76.0</td>
      <td>0.1</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>70.0</td>
      <td>71.0</td>
      <td>170.0</td>
      <td>170.0</td>
      <td>72.0</td>
      <td>72.0</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1980-04-10</td>
      <td>1983-03-24</td>
      <td>2.69</td>
      <td>3.29</td>
      <td>43.0</td>
      <td>46.0</td>
      <td>3.13</td>
      <td>3.63</td>
      <td>51.0</td>
      <td>58.0</td>
      <td>2.53</td>
      <td>1.09</td>
      <td>36.0</td>
      <td>34.0</td>
      <td>72.0</td>
      <td>46.0</td>
      <td>0.3</td>
      <td>1.3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>70.0</td>
      <td>68.0</td>
      <td>155.0</td>
      <td>155.0</td>
      <td>73.0</td>
      <td>71.0</td>
      <td>Orthodox</td>
      <td>Southpaw</td>
      <td>1995-01-03</td>
      <td>1985-08-15</td>
      <td>5.13</td>
      <td>3.65</td>
      <td>52.0</td>
      <td>53.0</td>
      <td>3.70</td>
      <td>1.77</td>
      <td>41.0</td>
      <td>57.0</td>
      <td>0.98</td>
      <td>0.40</td>
      <td>25.0</td>
      <td>25.0</td>
      <td>56.0</td>
      <td>30.0</td>
      <td>1.6</td>
      <td>0.4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>77.0</td>
      <td>72.0</td>
      <td>265.0</td>
      <td>265.0</td>
      <td>80.0</td>
      <td>72.0</td>
      <td>Orthodox</td>
      <td>Southpaw</td>
      <td>1988-07-28</td>
      <td>1989-12-10</td>
      <td>4.79</td>
      <td>2.31</td>
      <td>50.0</td>
      <td>31.0</td>
      <td>3.31</td>
      <td>4.30</td>
      <td>55.0</td>
      <td>47.0</td>
      <td>0.20</td>
      <td>0.00</td>
      <td>33.0</td>
      <td>0.0</td>
      <td>64.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>74.0</td>
      <td>73.0</td>
      <td>265.0</td>
      <td>265.0</td>
      <td>75.0</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1986-08-04</td>
      <td>1982-10-20</td>
      <td>2.08</td>
      <td>1.03</td>
      <td>46.0</td>
      <td>31.0</td>
      <td>1.52</td>
      <td>3.01</td>
      <td>59.0</td>
      <td>55.0</td>
      <td>1.83</td>
      <td>0.00</td>
      <td>41.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>57.0</td>
      <td>0.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>7514</th>
      <td>1</td>
      <td>80.0</td>
      <td>75.0</td>
      <td>265.0</td>
      <td>260.0</td>
      <td>80.0</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1976-03-05</td>
      <td>1978-11-11</td>
      <td>4.23</td>
      <td>2.60</td>
      <td>41.0</td>
      <td>36.0</td>
      <td>2.61</td>
      <td>8.80</td>
      <td>61.0</td>
      <td>40.0</td>
      <td>0.11</td>
      <td>0.00</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>75.0</td>
      <td>90.0</td>
      <td>0.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7515</th>
      <td>1</td>
      <td>75.0</td>
      <td>72.0</td>
      <td>235.0</td>
      <td>265.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Orthodox</td>
      <td>Switch</td>
      <td>1968-01-05</td>
      <td>None</td>
      <td>0.76</td>
      <td>1.35</td>
      <td>83.0</td>
      <td>30.0</td>
      <td>2.12</td>
      <td>3.55</td>
      <td>30.0</td>
      <td>38.0</td>
      <td>4.55</td>
      <td>1.07</td>
      <td>100.0</td>
      <td>33.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>2.3</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7516</th>
      <td>1</td>
      <td>71.0</td>
      <td>70.0</td>
      <td>155.0</td>
      <td>155.0</td>
      <td>76.0</td>
      <td>71.0</td>
      <td>Orthodox</td>
      <td>Southpaw</td>
      <td>1984-02-12</td>
      <td>1983-10-07</td>
      <td>4.94</td>
      <td>1.95</td>
      <td>45.0</td>
      <td>31.0</td>
      <td>4.41</td>
      <td>2.51</td>
      <td>55.0</td>
      <td>63.0</td>
      <td>0.39</td>
      <td>4.08</td>
      <td>35.0</td>
      <td>53.0</td>
      <td>67.0</td>
      <td>92.0</td>
      <td>0.9</td>
      <td>0.8</td>
    </tr>
    <tr>
      <th>7517</th>
      <td>1</td>
      <td>72.0</td>
      <td>74.0</td>
      <td>185.0</td>
      <td>185.0</td>
      <td>74.0</td>
      <td>76.0</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1981-01-28</td>
      <td>1983-08-10</td>
      <td>2.93</td>
      <td>2.65</td>
      <td>50.0</td>
      <td>47.0</td>
      <td>2.90</td>
      <td>2.58</td>
      <td>57.0</td>
      <td>54.0</td>
      <td>1.45</td>
      <td>3.55</td>
      <td>34.0</td>
      <td>54.0</td>
      <td>59.0</td>
      <td>62.0</td>
      <td>0.8</td>
      <td>1.2</td>
    </tr>
    <tr>
      <th>7518</th>
      <td>2</td>
      <td>75.0</td>
      <td>75.0</td>
      <td>235.0</td>
      <td>205.0</td>
      <td>76.0</td>
      <td>79.0</td>
      <td>Orthodox</td>
      <td>Orthodox</td>
      <td>1981-09-02</td>
      <td>1991-06-26</td>
      <td>2.41</td>
      <td>2.78</td>
      <td>44.0</td>
      <td>64.0</td>
      <td>3.02</td>
      <td>0.52</td>
      <td>55.0</td>
      <td>43.0</td>
      <td>1.01</td>
      <td>5.14</td>
      <td>23.0</td>
      <td>55.0</td>
      <td>45.0</td>
      <td>75.0</td>
      <td>0.1</td>
      <td>2.4</td>
    </tr>
  </tbody>
</table>
<p>7519 rows × 27 columns</p>
</div>




```python
# Next lets encode with the stance of the fighters
stances = pd.concat([dataframe['fighter_a_stance'], dataframe['fighter_b_stance']]).unique()
stances = np.delete(stances, np.where(stances == None))
values = list(range(5))
replacement_dict = { k:v for (k,v) in zip(stances, values)} 

dataframe['fighter_a_stance'] = dataframe['fighter_a_stance'].replace(replacement_dict)
dataframe['fighter_b_stance'] = dataframe['fighter_b_stance'].replace(replacement_dict)
dataframe
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>winner</th>
      <th>fighter_a_height</th>
      <th>fighter_b_height</th>
      <th>fighter_a_weight</th>
      <th>fighter_b_weight</th>
      <th>fighter_a_reach</th>
      <th>fighter_b_reach</th>
      <th>fighter_a_stance</th>
      <th>fighter_b_stance</th>
      <th>fighter_a_dob</th>
      <th>fighter_b_dob</th>
      <th>fighter_a_SLpM</th>
      <th>fighter_b_SLpM</th>
      <th>fighter_a_str_acc</th>
      <th>fighter_b_str_acc</th>
      <th>fighter_a_SApM</th>
      <th>fighter_b_SApM</th>
      <th>fighter_a_str_def</th>
      <th>fighter_b_str_def</th>
      <th>fighter_a_TD_avg</th>
      <th>fighter_b_TD_avg</th>
      <th>fighter_a_TD_acc</th>
      <th>fighter_b_TD_acc</th>
      <th>fighter_a_TD_def</th>
      <th>fighter_b_TD_def</th>
      <th>fighter_a_sub_avg</th>
      <th>fighter_b_sub_avg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>68.0</td>
      <td>69.0</td>
      <td>135.0</td>
      <td>135.0</td>
      <td>69.0</td>
      <td>68.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>1981-10-17</td>
      <td>1988-03-26</td>
      <td>3.21</td>
      <td>5.24</td>
      <td>40.0</td>
      <td>40.0</td>
      <td>2.79</td>
      <td>6.33</td>
      <td>56.0</td>
      <td>57.0</td>
      <td>0.90</td>
      <td>0.16</td>
      <td>30.0</td>
      <td>50.0</td>
      <td>78.0</td>
      <td>76.0</td>
      <td>0.1</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>70.0</td>
      <td>71.0</td>
      <td>170.0</td>
      <td>170.0</td>
      <td>72.0</td>
      <td>72.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1980-04-10</td>
      <td>1983-03-24</td>
      <td>2.69</td>
      <td>3.29</td>
      <td>43.0</td>
      <td>46.0</td>
      <td>3.13</td>
      <td>3.63</td>
      <td>51.0</td>
      <td>58.0</td>
      <td>2.53</td>
      <td>1.09</td>
      <td>36.0</td>
      <td>34.0</td>
      <td>72.0</td>
      <td>46.0</td>
      <td>0.3</td>
      <td>1.3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>70.0</td>
      <td>68.0</td>
      <td>155.0</td>
      <td>155.0</td>
      <td>73.0</td>
      <td>71.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1995-01-03</td>
      <td>1985-08-15</td>
      <td>5.13</td>
      <td>3.65</td>
      <td>52.0</td>
      <td>53.0</td>
      <td>3.70</td>
      <td>1.77</td>
      <td>41.0</td>
      <td>57.0</td>
      <td>0.98</td>
      <td>0.40</td>
      <td>25.0</td>
      <td>25.0</td>
      <td>56.0</td>
      <td>30.0</td>
      <td>1.6</td>
      <td>0.4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>77.0</td>
      <td>72.0</td>
      <td>265.0</td>
      <td>265.0</td>
      <td>80.0</td>
      <td>72.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1988-07-28</td>
      <td>1989-12-10</td>
      <td>4.79</td>
      <td>2.31</td>
      <td>50.0</td>
      <td>31.0</td>
      <td>3.31</td>
      <td>4.30</td>
      <td>55.0</td>
      <td>47.0</td>
      <td>0.20</td>
      <td>0.00</td>
      <td>33.0</td>
      <td>0.0</td>
      <td>64.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>74.0</td>
      <td>73.0</td>
      <td>265.0</td>
      <td>265.0</td>
      <td>75.0</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1986-08-04</td>
      <td>1982-10-20</td>
      <td>2.08</td>
      <td>1.03</td>
      <td>46.0</td>
      <td>31.0</td>
      <td>1.52</td>
      <td>3.01</td>
      <td>59.0</td>
      <td>55.0</td>
      <td>1.83</td>
      <td>0.00</td>
      <td>41.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>57.0</td>
      <td>0.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>7514</th>
      <td>1</td>
      <td>80.0</td>
      <td>75.0</td>
      <td>265.0</td>
      <td>260.0</td>
      <td>80.0</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1976-03-05</td>
      <td>1978-11-11</td>
      <td>4.23</td>
      <td>2.60</td>
      <td>41.0</td>
      <td>36.0</td>
      <td>2.61</td>
      <td>8.80</td>
      <td>61.0</td>
      <td>40.0</td>
      <td>0.11</td>
      <td>0.00</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>75.0</td>
      <td>90.0</td>
      <td>0.1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7515</th>
      <td>1</td>
      <td>75.0</td>
      <td>72.0</td>
      <td>235.0</td>
      <td>265.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>1968-01-05</td>
      <td>None</td>
      <td>0.76</td>
      <td>1.35</td>
      <td>83.0</td>
      <td>30.0</td>
      <td>2.12</td>
      <td>3.55</td>
      <td>30.0</td>
      <td>38.0</td>
      <td>4.55</td>
      <td>1.07</td>
      <td>100.0</td>
      <td>33.0</td>
      <td>0.0</td>
      <td>66.0</td>
      <td>2.3</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7516</th>
      <td>1</td>
      <td>71.0</td>
      <td>70.0</td>
      <td>155.0</td>
      <td>155.0</td>
      <td>76.0</td>
      <td>71.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1984-02-12</td>
      <td>1983-10-07</td>
      <td>4.94</td>
      <td>1.95</td>
      <td>45.0</td>
      <td>31.0</td>
      <td>4.41</td>
      <td>2.51</td>
      <td>55.0</td>
      <td>63.0</td>
      <td>0.39</td>
      <td>4.08</td>
      <td>35.0</td>
      <td>53.0</td>
      <td>67.0</td>
      <td>92.0</td>
      <td>0.9</td>
      <td>0.8</td>
    </tr>
    <tr>
      <th>7517</th>
      <td>1</td>
      <td>72.0</td>
      <td>74.0</td>
      <td>185.0</td>
      <td>185.0</td>
      <td>74.0</td>
      <td>76.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1981-01-28</td>
      <td>1983-08-10</td>
      <td>2.93</td>
      <td>2.65</td>
      <td>50.0</td>
      <td>47.0</td>
      <td>2.90</td>
      <td>2.58</td>
      <td>57.0</td>
      <td>54.0</td>
      <td>1.45</td>
      <td>3.55</td>
      <td>34.0</td>
      <td>54.0</td>
      <td>59.0</td>
      <td>62.0</td>
      <td>0.8</td>
      <td>1.2</td>
    </tr>
    <tr>
      <th>7518</th>
      <td>2</td>
      <td>75.0</td>
      <td>75.0</td>
      <td>235.0</td>
      <td>205.0</td>
      <td>76.0</td>
      <td>79.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1981-09-02</td>
      <td>1991-06-26</td>
      <td>2.41</td>
      <td>2.78</td>
      <td>44.0</td>
      <td>64.0</td>
      <td>3.02</td>
      <td>0.52</td>
      <td>55.0</td>
      <td>43.0</td>
      <td>1.01</td>
      <td>5.14</td>
      <td>23.0</td>
      <td>55.0</td>
      <td>45.0</td>
      <td>75.0</td>
      <td>0.1</td>
      <td>2.4</td>
    </tr>
  </tbody>
</table>
<p>7519 rows × 27 columns</p>
</div>




```python
plt.rcParams['figure.max_open_warning'] = 50
numerical_columns = list(dataframe.describe().columns)

# create a loop to make a boxplot and histogram for each point
for i in numerical_columns:
    plt.figure()
    plt.tight_layout()
    sns.set(rc={'figure.figsize':(8,5)})
    
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=False)
    plt.gca().set(xlabel = i, ylabel = 'Frequency')
    sns.boxplot(data=dataframe, x=dataframe[i], ax=ax_box, linewidth=1.0)
    sns.histplot(data=dataframe, x=dataframe[i], ax=ax_hist, bins=10, kde=True)
```


    <Figure size 800x500 with 0 Axes>



    
![png](output_25_1.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_3.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_5.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_7.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_9.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_11.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_13.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_15.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_17.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_19.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_21.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_23.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_25.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_27.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_29.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_31.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_33.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_35.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_37.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_39.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_41.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_43.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_45.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_47.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_25_49.png)
    


Looking at the graphs above it seems that the data isn't overly skewed so using the mean to impute values seems like a good idea

With the exception of the weight column, some domain knowledge tells us it is a much better idea to impute the weight as the same as the opponent in the other column as fights occur at agreed upon weights (outside the heavyweight division) 


```python
# Next lets impute the missing values

# Now we have sorted the value types (excluding)

dataframe.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>winner</th>
      <th>fighter_a_height</th>
      <th>fighter_b_height</th>
      <th>fighter_a_weight</th>
      <th>fighter_b_weight</th>
      <th>fighter_a_reach</th>
      <th>fighter_b_reach</th>
      <th>fighter_a_stance</th>
      <th>fighter_b_stance</th>
      <th>fighter_a_SLpM</th>
      <th>fighter_b_SLpM</th>
      <th>fighter_a_str_acc</th>
      <th>fighter_b_str_acc</th>
      <th>fighter_a_SApM</th>
      <th>fighter_b_SApM</th>
      <th>fighter_a_str_def</th>
      <th>fighter_b_str_def</th>
      <th>fighter_a_TD_avg</th>
      <th>fighter_b_TD_avg</th>
      <th>fighter_a_TD_acc</th>
      <th>fighter_b_TD_acc</th>
      <th>fighter_a_TD_def</th>
      <th>fighter_b_TD_def</th>
      <th>fighter_a_sub_avg</th>
      <th>fighter_b_sub_avg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>7519.000000</td>
      <td>7514.000000</td>
      <td>7497.000000</td>
      <td>7516.000000</td>
      <td>7500.000000</td>
      <td>7098.000000</td>
      <td>6615.000000</td>
      <td>7493.000000</td>
      <td>7448.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
      <td>7519.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>1.351776</td>
      <td>70.329518</td>
      <td>70.303988</td>
      <td>168.695317</td>
      <td>168.277867</td>
      <td>72.136940</td>
      <td>71.982162</td>
      <td>0.850127</td>
      <td>0.863722</td>
      <td>3.403030</td>
      <td>3.268089</td>
      <td>44.128475</td>
      <td>42.902248</td>
      <td>3.278053</td>
      <td>3.450549</td>
      <td>54.284080</td>
      <td>52.224764</td>
      <td>1.593326</td>
      <td>1.457615</td>
      <td>38.825509</td>
      <td>35.941748</td>
      <td>60.346323</td>
      <td>56.587844</td>
      <td>0.647626</td>
      <td>0.599668</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.515593</td>
      <td>3.527235</td>
      <td>3.497144</td>
      <td>36.198808</td>
      <td>36.796266</td>
      <td>4.262536</td>
      <td>4.186640</td>
      <td>0.485053</td>
      <td>0.488992</td>
      <td>1.312669</td>
      <td>1.457575</td>
      <td>9.254967</td>
      <td>11.055371</td>
      <td>1.220889</td>
      <td>1.551828</td>
      <td>9.825433</td>
      <td>11.683590</td>
      <td>1.265590</td>
      <td>1.302384</td>
      <td>18.653186</td>
      <td>21.348346</td>
      <td>20.544122</td>
      <td>23.970968</td>
      <td>0.792348</td>
      <td>0.807511</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
      <td>60.000000</td>
      <td>60.000000</td>
      <td>115.000000</td>
      <td>115.000000</td>
      <td>58.000000</td>
      <td>58.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>1.000000</td>
      <td>68.000000</td>
      <td>68.000000</td>
      <td>145.000000</td>
      <td>145.000000</td>
      <td>70.000000</td>
      <td>69.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>2.570000</td>
      <td>2.340000</td>
      <td>40.000000</td>
      <td>39.000000</td>
      <td>2.510000</td>
      <td>2.600000</td>
      <td>51.000000</td>
      <td>49.000000</td>
      <td>0.625000</td>
      <td>0.490000</td>
      <td>29.000000</td>
      <td>25.000000</td>
      <td>50.000000</td>
      <td>45.000000</td>
      <td>0.100000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>1.000000</td>
      <td>70.000000</td>
      <td>70.000000</td>
      <td>170.000000</td>
      <td>155.000000</td>
      <td>72.000000</td>
      <td>72.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>3.320000</td>
      <td>3.250000</td>
      <td>45.000000</td>
      <td>44.000000</td>
      <td>3.170000</td>
      <td>3.270000</td>
      <td>56.000000</td>
      <td>54.000000</td>
      <td>1.330000</td>
      <td>1.160000</td>
      <td>39.000000</td>
      <td>36.000000</td>
      <td>63.000000</td>
      <td>61.000000</td>
      <td>0.500000</td>
      <td>0.400000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>2.000000</td>
      <td>73.000000</td>
      <td>73.000000</td>
      <td>185.000000</td>
      <td>185.000000</td>
      <td>75.000000</td>
      <td>75.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>4.190000</td>
      <td>4.110000</td>
      <td>50.000000</td>
      <td>49.000000</td>
      <td>3.930000</td>
      <td>4.170000</td>
      <td>60.000000</td>
      <td>59.000000</td>
      <td>2.290000</td>
      <td>2.110000</td>
      <td>50.000000</td>
      <td>48.000000</td>
      <td>74.000000</td>
      <td>72.000000</td>
      <td>0.900000</td>
      <td>0.800000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>3.000000</td>
      <td>83.000000</td>
      <td>83.000000</td>
      <td>345.000000</td>
      <td>770.000000</td>
      <td>84.000000</td>
      <td>84.000000</td>
      <td>4.000000</td>
      <td>4.000000</td>
      <td>10.220000</td>
      <td>12.150000</td>
      <td>83.000000</td>
      <td>100.000000</td>
      <td>15.480000</td>
      <td>42.000000</td>
      <td>84.000000</td>
      <td>100.000000</td>
      <td>11.110000</td>
      <td>13.950000</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>21.900000</td>
      <td>16.400000</td>
    </tr>
  </tbody>
</table>
</div>



## Feature Engineering

Some of the features we think we can engineer from our data preprocessing steps include the following:
  1. Age from the DOB column
  2. Clustering to determine fighter styles
  3. Balance our target variable


```python
# Lets look at how important each column is to the winner column

# Select the column to compare with
target_column = 'target_column'

# Calculate the correlation of all columns with the target column
correlation_with_target = df.corrwith(df[target_column])

# Plot the correlation
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_with_target.to_frame(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title(f'Correlation with {target_column}')
plt.show()

```


    
![png](output_29_0.png)
    



```python
# Investigating the missing 21 values from 'fighter_a_knockdowns_total'
dataframe[dataframe['fighter_a_knockdowns_total'].isna()]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fight_id</th>
      <th>fighter_a_id_FK</th>
      <th>fighter_b_id_FK</th>
      <th>event_id_FK</th>
      <th>winner</th>
      <th>performance_bonus</th>
      <th>weight_class</th>
      <th>method</th>
      <th>round</th>
      <th>time</th>
      <th>time_format</th>
      <th>referee</th>
      <th>judge1</th>
      <th>judge2</th>
      <th>judge3</th>
      <th>judge_1_score</th>
      <th>judge_2_score</th>
      <th>judge_3_score</th>
      <th>fighter_a_knockdowns_total</th>
      <th>fighter_b_knockdowns_total</th>
      <th>fighter_a_sig_strikes_landed_total</th>
      <th>fighter_b_sig_strikes_landed_total</th>
      <th>fighter_a_sig_strikes_attempted_total</th>
      <th>fighter_b_sig_strikes_attempted_total</th>
      <th>fighter_a_total_strikes_landed_total</th>
      <th>fighter_b_total_strikes_landed_total</th>
      <th>fighter_a_total_strikes_attempted_total</th>
      <th>fighter_b_total_strikes_attempted_total</th>
      <th>fighter_a_takedowns_total_landed</th>
      <th>fighter_b_takedowns_total_landed</th>
      <th>fighter_a_takedowns_attempted_total</th>
      <th>fighter_b_takedowns_attempted_total</th>
      <th>fighter_a_submissions_total</th>
      <th>fighter_b_submissions_total</th>
      <th>fighter_a_reversals_total</th>
      <th>fighter_b_reversals_total</th>
      <th>fighter_a_control_total</th>
      <th>fighter_b_control_total</th>
      <th>fighter_a_sig_head_landed_total</th>
      <th>fighter_b_sig_head_landed_total</th>
      <th>fighter_a_sig_head_attempted_total</th>
      <th>fighter_b_sig_head_attempted_total</th>
      <th>fighter_a_sig_body_landed_total</th>
      <th>fighter_b_sig_body_landed_total</th>
      <th>fighter_a_sig_body_attempted_total</th>
      <th>fighter_b_sig_body_attempted_total</th>
      <th>fighter_a_sig_leg_landed_total</th>
      <th>fighter_b_sig_leg_landed_total</th>
      <th>fighter_a_sig_leg_attempted_total</th>
      <th>fighter_b_sig_leg_attempted_total</th>
      <th>fighter_a_sig_distance_landed_total</th>
      <th>fighter_b_sig_distance_landed_total</th>
      <th>fighter_a_sig_distance_attempted_total</th>
      <th>fighter_b_sig_distance_attempted_total</th>
      <th>fighter_a_sig_clinch_landed_total</th>
      <th>fighter_b_sig_clinch_landed_total</th>
      <th>fighter_a_sig_clinch_attempted_total</th>
      <th>fighter_b_sig_clinch_attempted_total</th>
      <th>fighter_a_sig_ground_landed_total</th>
      <th>fighter_b_sig_ground_landed_total</th>
      <th>fighter_a_sig_ground_attempted_total</th>
      <th>fighter_b_sig_ground_attempted_total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1438</th>
      <td>2f449bd58b3d9a99</td>
      <td>2efbc83a6b9b7f86</td>
      <td>53e533db1b8e9712</td>
      <td>9b5b5a75523728f3</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>4:46</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1812</th>
      <td>3badedeb2c5533f4</td>
      <td>20ec0061400178ca</td>
      <td>b3bbe88fecd6a0d2</td>
      <td>6ceff86fae4f6b3b</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>1:33</td>
      <td>1 Rnd (15)</td>
      <td>Joe Hamilton</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2284</th>
      <td>4b334c9727eee450</td>
      <td>a6a9ab5a824e8f66</td>
      <td>304fcd812f12c589</td>
      <td>5af480a3b2e1726b</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>TKO - Doctor's Stoppage</td>
      <td>1</td>
      <td>0:48</td>
      <td>1 Rnd (20)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2300</th>
      <td>4bce0ce561a65288</td>
      <td>b19fc66613dc75b9</td>
      <td>56f4b81ec4db61af</td>
      <td>749685d24e2cac50</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>1:20</td>
      <td>1 Rnd (12)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2617</th>
      <td>565ecefd8a37ad7e</td>
      <td>1d147d4163a6989b</td>
      <td>4985113c0928aa62</td>
      <td>96eff1a628adcc7f</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>0:48</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2634</th>
      <td>5701dbbbfa4f8313</td>
      <td>0e9869d712e81f8f</td>
      <td>f62850b3c7480db9</td>
      <td>b63e800c18e011b5</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>0:50</td>
      <td>1 Rnd (10)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3004</th>
      <td>635fbf57001897c7</td>
      <td>e8efeb9cf33b1941</td>
      <td>7ca4c3f8aa8bacae</td>
      <td>32a3025d5db456ae</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>10:27</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3029</th>
      <td>6449a1a9a69a830c</td>
      <td>19ffeb5e3fffd6d5</td>
      <td>3f24c96753dbd9f9</td>
      <td>31bbd46d57dfbcb7</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>4:38</td>
      <td>1 Rnd (15)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3575</th>
      <td>77bf1e37929b0d59</td>
      <td>3da19339ee7051d5</td>
      <td>abbc4fc02e0d84b3</td>
      <td>96eff1a628adcc7f</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>0:14</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3802</th>
      <td>7ffcc3a72e082ace</td>
      <td>18524b46c570730b</td>
      <td>02fc8f50f56eb307</td>
      <td>31bbd46d57dfbcb7</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>5:29</td>
      <td>1 Rnd (15)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4149</th>
      <td>8b258bbb37f74a66</td>
      <td>a54a35a670d8e852</td>
      <td>4dc496aa0cfc0d95</td>
      <td>4a01dc8376736ef5</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Decision - Unanimous</td>
      <td>2</td>
      <td>3:00</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4240</th>
      <td>8e03db41687d9132</td>
      <td>dedc3bb440d09554</td>
      <td>3e03cec9767d37e6</td>
      <td>1c3f5e85b59ec710</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>3:06</td>
      <td>1 Rnd (20)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4811</th>
      <td>a1db4c917777aa79</td>
      <td>19ffeb5e3fffd6d5</td>
      <td>598a58db87b890ee</td>
      <td>b60391da771deefe</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>0:14</td>
      <td>No Time Limit</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4927</th>
      <td>a5c90086fb65f58e</td>
      <td>18524b46c570730b</td>
      <td>6cbb7661c3258617</td>
      <td>9b5b5a75523728f3</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>1:45</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5260</th>
      <td>b297c3e938e1005e</td>
      <td>a6a9ab5a824e8f66</td>
      <td>237187ed9f419285</td>
      <td>1c3f5e85b59ec710</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>2:01</td>
      <td>1 Rnd (20)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5428</th>
      <td>b80872821bc4f6ba</td>
      <td>1c2f2571b18791b6</td>
      <td>601cf40c09090853</td>
      <td>749685d24e2cac50</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>1:15</td>
      <td>1 Rnd (12)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5429</th>
      <td>b80e6a799c95d499</td>
      <td>e8fb8e53bc2e29d6</td>
      <td>ee5df903f80c6816</td>
      <td>b60391da771deefe</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>4:55</td>
      <td>No Time Limit</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5782</th>
      <td>c413b0abc04358c3</td>
      <td>977081bc01197656</td>
      <td>1f5f75658551f2d3</td>
      <td>6ceff86fae4f6b3b</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>1:45</td>
      <td>1 Rnd (15)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6375</th>
      <td>d93c8c77e1091a16</td>
      <td>13e62d766b709aa6</td>
      <td>e8fb8e53bc2e29d6</td>
      <td>9b5b5a75523728f3</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>1:37</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6720</th>
      <td>e4fe950846b51bdf</td>
      <td>96d173b7f92aa520</td>
      <td>d3b5ad3b15a64a18</td>
      <td>5af480a3b2e1726b</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>5:26</td>
      <td>1 Rnd (20)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7222</th>
      <td>f59b1215176636f6</td>
      <td>0e9869d712e81f8f</td>
      <td>6cbb7661c3258617</td>
      <td>aee8eecfc4bfb1e7</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Decision - Unanimous</td>
      <td>2</td>
      <td>3:00</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



So when we investigate these rows I can see that the values missing from the column 'fighter_a_knockdowns_total' are the same 21 values missing from the other columns, when we investigate by looking up the event on the UFC stats website we can see that we were correct these are indeed earlier fights that did not record these stats. As there is no way of finding these values, we could impute them with average values but given there are only 21 rows out of over 7000, we can drop these rows without worry about too much data loss.

![Missing Stats](ufc_fight_missing_stats.png)


```python
# Next lets investigate control time
dataframe[dataframe['fighter_a_control_total'].isna()]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fight_id</th>
      <th>fighter_a_id_FK</th>
      <th>fighter_b_id_FK</th>
      <th>event_id_FK</th>
      <th>winner</th>
      <th>performance_bonus</th>
      <th>weight_class</th>
      <th>method</th>
      <th>round</th>
      <th>time</th>
      <th>time_format</th>
      <th>referee</th>
      <th>judge1</th>
      <th>judge2</th>
      <th>judge3</th>
      <th>judge_1_score</th>
      <th>judge_2_score</th>
      <th>judge_3_score</th>
      <th>fighter_a_knockdowns_total</th>
      <th>fighter_b_knockdowns_total</th>
      <th>fighter_a_sig_strikes_landed_total</th>
      <th>fighter_b_sig_strikes_landed_total</th>
      <th>fighter_a_sig_strikes_attempted_total</th>
      <th>fighter_b_sig_strikes_attempted_total</th>
      <th>fighter_a_total_strikes_landed_total</th>
      <th>fighter_b_total_strikes_landed_total</th>
      <th>fighter_a_total_strikes_attempted_total</th>
      <th>fighter_b_total_strikes_attempted_total</th>
      <th>fighter_a_takedowns_total_landed</th>
      <th>fighter_b_takedowns_total_landed</th>
      <th>fighter_a_takedowns_attempted_total</th>
      <th>fighter_b_takedowns_attempted_total</th>
      <th>fighter_a_submissions_total</th>
      <th>fighter_b_submissions_total</th>
      <th>fighter_a_reversals_total</th>
      <th>fighter_b_reversals_total</th>
      <th>fighter_a_control_total</th>
      <th>fighter_b_control_total</th>
      <th>fighter_a_sig_head_landed_total</th>
      <th>fighter_b_sig_head_landed_total</th>
      <th>fighter_a_sig_head_attempted_total</th>
      <th>fighter_b_sig_head_attempted_total</th>
      <th>fighter_a_sig_body_landed_total</th>
      <th>fighter_b_sig_body_landed_total</th>
      <th>fighter_a_sig_body_attempted_total</th>
      <th>fighter_b_sig_body_attempted_total</th>
      <th>fighter_a_sig_leg_landed_total</th>
      <th>fighter_b_sig_leg_landed_total</th>
      <th>fighter_a_sig_leg_attempted_total</th>
      <th>fighter_b_sig_leg_attempted_total</th>
      <th>fighter_a_sig_distance_landed_total</th>
      <th>fighter_b_sig_distance_landed_total</th>
      <th>fighter_a_sig_distance_attempted_total</th>
      <th>fighter_b_sig_distance_attempted_total</th>
      <th>fighter_a_sig_clinch_landed_total</th>
      <th>fighter_b_sig_clinch_landed_total</th>
      <th>fighter_a_sig_clinch_attempted_total</th>
      <th>fighter_b_sig_clinch_attempted_total</th>
      <th>fighter_a_sig_ground_landed_total</th>
      <th>fighter_b_sig_ground_landed_total</th>
      <th>fighter_a_sig_ground_attempted_total</th>
      <th>fighter_b_sig_ground_attempted_total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>24</th>
      <td>00835554f95fa911</td>
      <td>429e7d3725852ce9</td>
      <td>46c8ec317aff28ac</td>
      <td>a6a9ab5a824e8f66</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>1:17</td>
      <td>No Time Limit</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>4.0</td>
      <td>2.0</td>
      <td>11.0</td>
      <td>2.0</td>
      <td>11.0</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>None</td>
      <td>None</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>130</th>
      <td>03afd7b6a217aaac</td>
      <td>5898357a45a73674</td>
      <td>c058823a2595ab09</td>
      <td>a220be6d41d6f97d</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>TKO - Doctor's Stoppage</td>
      <td>1</td>
      <td>10:01</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>Tony Mullinax</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>9.0</td>
      <td>17.0</td>
      <td>19.0</td>
      <td>42.0</td>
      <td>14.0</td>
      <td>33.0</td>
      <td>26.0</td>
      <td>60.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>None</td>
      <td>None</td>
      <td>6.0</td>
      <td>14.0</td>
      <td>15.0</td>
      <td>38.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>3.0</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>6.0</td>
      <td>8.0</td>
      <td>4.0</td>
      <td>2.0</td>
      <td>10.0</td>
      <td>4.0</td>
      <td>2.0</td>
      <td>15.0</td>
      <td>3.0</td>
      <td>30.0</td>
    </tr>
    <tr>
      <th>142</th>
      <td>040ecf01338dff9e</td>
      <td>c670aa48827d6be6</td>
      <td>dedc3bb440d09554</td>
      <td>b60391da771deefe</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>1:45</td>
      <td>No Time Limit</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>8.0</td>
      <td>0.0</td>
      <td>9.0</td>
      <td>0.0</td>
      <td>12.0</td>
      <td>0.0</td>
      <td>14.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>157</th>
      <td>0473ef44197be419</td>
      <td>53e533db1b8e9712</td>
      <td>21f2974fd08085e3</td>
      <td>5bd533d50c8e7b8a</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>1:23</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>Joe Hamilton</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>11.0</td>
      <td>1.0</td>
      <td>13.0</td>
      <td>5.0</td>
      <td>13.0</td>
      <td>1.0</td>
      <td>15.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>None</td>
      <td>None</td>
      <td>11.0</td>
      <td>0.0</td>
      <td>13.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>11.0</td>
      <td>0.0</td>
      <td>11.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>247</th>
      <td>07423d10cc23bfeb</td>
      <td>cedfdf8d423d500c</td>
      <td>4c805f5f58a75df0</td>
      <td>32a3025d5db456ae</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Decision - Split</td>
      <td>3</td>
      <td>3:00</td>
      <td>1 Rnd + 2OT (15-3-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>19.0</td>
      <td>24.0</td>
      <td>34.0</td>
      <td>43.0</td>
      <td>95.0</td>
      <td>145.0</td>
      <td>111.0</td>
      <td>173.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>9.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>None</td>
      <td>None</td>
      <td>2.0</td>
      <td>2.0</td>
      <td>12.0</td>
      <td>20.0</td>
      <td>12.0</td>
      <td>20.0</td>
      <td>14.0</td>
      <td>21.0</td>
      <td>5.0</td>
      <td>2.0</td>
      <td>8.0</td>
      <td>2.0</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>14.0</td>
      <td>12.0</td>
      <td>15.0</td>
      <td>23.0</td>
      <td>20.0</td>
      <td>29.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>7354</th>
      <td>fa3b940bd48da7e2</td>
      <td>32a3025d5db456ae</td>
      <td>9199e0735b83dd32</td>
      <td>dedc3bb440d09554</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>1:23</td>
      <td>1 Rnd (20)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>17.0</td>
      <td>2.0</td>
      <td>28.0</td>
      <td>2.0</td>
      <td>30.0</td>
      <td>6.0</td>
      <td>41.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>None</td>
      <td>None</td>
      <td>7.0</td>
      <td>2.0</td>
      <td>17.0</td>
      <td>2.0</td>
      <td>10.0</td>
      <td>0.0</td>
      <td>11.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>14.0</td>
      <td>0.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>9.0</td>
      <td>0.0</td>
      <td>5.0</td>
      <td>2.0</td>
      <td>5.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>7356</th>
      <td>fa48320affd3b2b4</td>
      <td>63b65af1c5cb02cb</td>
      <td>1c3f5e85b59ec710</td>
      <td>9b5b5a75523728f3</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>5:48</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>22.0</td>
      <td>1.0</td>
      <td>39.0</td>
      <td>3.0</td>
      <td>70.0</td>
      <td>12.0</td>
      <td>91.0</td>
      <td>15.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>None</td>
      <td>None</td>
      <td>21.0</td>
      <td>0.0</td>
      <td>38.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>22.0</td>
      <td>0.0</td>
      <td>38.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7391</th>
      <td>fb8e8d1a734b6fe8</td>
      <td>8f2d9ee27f206f1f</td>
      <td>a24e080000fa7a35</td>
      <td>c9bbf1a0285a8076</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>7:57</td>
      <td>1 Rnd + OT (12-3)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>24.0</td>
      <td>4.0</td>
      <td>37.0</td>
      <td>26.0</td>
      <td>25.0</td>
      <td>30.0</td>
      <td>39.0</td>
      <td>59.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>None</td>
      <td>None</td>
      <td>10.0</td>
      <td>3.0</td>
      <td>20.0</td>
      <td>25.0</td>
      <td>5.0</td>
      <td>1.0</td>
      <td>6.0</td>
      <td>1.0</td>
      <td>9.0</td>
      <td>0.0</td>
      <td>11.0</td>
      <td>0.0</td>
      <td>10.0</td>
      <td>0.0</td>
      <td>16.0</td>
      <td>14.0</td>
      <td>14.0</td>
      <td>0.0</td>
      <td>21.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>12.0</td>
    </tr>
    <tr>
      <th>7426</th>
      <td>fcd8e8ec45eb6b9f</td>
      <td>429e7d3725852ce9</td>
      <td>4565d435005319c0</td>
      <td>a6a9ab5a824e8f66</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>Submission</td>
      <td>1</td>
      <td>5:08</td>
      <td>No Time Limit</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>4.0</td>
      <td>7.0</td>
      <td>110.0</td>
      <td>12.0</td>
      <td>114.0</td>
      <td>16.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>7432</th>
      <td>fcf632627ce40195</td>
      <td>18524b46c570730b</td>
      <td>a2b06ca02bca14c0</td>
      <td>5af480a3b2e1726b</td>
      <td>Fighter A</td>
      <td>None</td>
      <td></td>
      <td>KO/TKO</td>
      <td>1</td>
      <td>1:41</td>
      <td>1 Rnd (20)</td>
      <td>John McCarthy</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>4.0</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>13.0</td>
      <td>5.0</td>
      <td>23.0</td>
      <td>8.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>None</td>
      <td>None</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>202 rows × 62 columns</p>
</div>




```python
# Looking at the time format I suspect these are also old fights, Lets have a look at the values modern 
# fights are fought over 3 5 minute rounds or 5 5 minute rounds for main events (This is some 
# knowledge I have from being a fan of the sport. Domain knowledge is always helpful!)
dataframe[dataframe['fighter_a_control_total'].isna()]['time_format'].value_counts()
```




    1 Rnd + OT (12-3)       88
    No Time Limit           31
    1 Rnd (20)              25
    1 Rnd + 2OT (15-3-3)    20
    1 Rnd (15)              12
    1 Rnd (10)               7
    1 Rnd (12)               6
    1 Rnd + OT (30-5)        3
    1 Rnd (18)               2
    1 Rnd + OT (15-3)        2
    1 Rnd + OT (30-3)        1
    1 Rnd + OT (27-3)        1
    1 Rnd + 2OT (24-3-3)     1
    1 Rnd (30)               1
    3 Rnd (5-5-5)            1
    1 Rnd + OT (31-5)        1
    Name: time_format, dtype: int64



After investigating our missing values we now know that old events were causing some missing values, given the number of these events and how the sport have evolved since then (Domain knowledge again!) I suggest we have a cut off date for the events which will remove these missing values. (A little investigation is needed to decide a date)

In addition the columns for judges scores and performance bonus have too many missing values to provide useful and are not pivotal to our end goal so I would suggest dropping these columns.

Now we have removed missing values it is time to look at the distribution of our data, we are interested in removing outliers that may affect the performance of our model and look for other interesting features of our data, always keeping in mind potential for feature engineering. (It is also important to note that what we do in these earlier steps with data cleaning and feature engineering will have the biggest impact on our model performance out of anything we could potentially do so these are vital steps! See 'The Unreasonable Effectiveness of Data' and remember Garbage in, Garbage out!)


```python
# Lets look at how our data is split up between continous and categorical
# As a general rule the float values will be continous (but remember to check for pesky categorical variables
#that are maskerading as floats and integers) and the object variables are categorical
dataframe.dtypes.value_counts()
```




    float64    42
    object     19
    int64       1
    dtype: int64




```python
# Let look closer at our columns
dataframe.dtypes
```




    fight_id                                 object
    fighter_a_id_FK                          object
    fighter_b_id_FK                          object
    event_id_FK                              object
    winner                                   object
                                             ...   
    fighter_b_sig_clinch_attempted_total    float64
    fighter_a_sig_ground_landed_total       float64
    fighter_b_sig_ground_landed_total       float64
    fighter_a_sig_ground_attempted_total    float64
    fighter_b_sig_ground_attempted_total    float64
    Length: 62, dtype: object




```python
# Lets look at our numerical values - we are 'sense' checking the value that they seem right and checking
# if these values are categorical or continious
dataframe.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>round</th>
      <th>fighter_a_knockdowns_total</th>
      <th>fighter_b_knockdowns_total</th>
      <th>fighter_a_sig_strikes_landed_total</th>
      <th>fighter_b_sig_strikes_landed_total</th>
      <th>fighter_a_sig_strikes_attempted_total</th>
      <th>fighter_b_sig_strikes_attempted_total</th>
      <th>fighter_a_total_strikes_landed_total</th>
      <th>fighter_b_total_strikes_landed_total</th>
      <th>fighter_a_total_strikes_attempted_total</th>
      <th>fighter_b_total_strikes_attempted_total</th>
      <th>fighter_a_takedowns_total_landed</th>
      <th>fighter_b_takedowns_total_landed</th>
      <th>fighter_a_takedowns_attempted_total</th>
      <th>fighter_b_takedowns_attempted_total</th>
      <th>fighter_a_submissions_total</th>
      <th>fighter_b_submissions_total</th>
      <th>fighter_a_reversals_total</th>
      <th>fighter_b_reversals_total</th>
      <th>fighter_a_sig_head_landed_total</th>
      <th>fighter_b_sig_head_landed_total</th>
      <th>fighter_a_sig_head_attempted_total</th>
      <th>fighter_b_sig_head_attempted_total</th>
      <th>fighter_a_sig_body_landed_total</th>
      <th>fighter_b_sig_body_landed_total</th>
      <th>fighter_a_sig_body_attempted_total</th>
      <th>fighter_b_sig_body_attempted_total</th>
      <th>fighter_a_sig_leg_landed_total</th>
      <th>fighter_b_sig_leg_landed_total</th>
      <th>fighter_a_sig_leg_attempted_total</th>
      <th>fighter_b_sig_leg_attempted_total</th>
      <th>fighter_a_sig_distance_landed_total</th>
      <th>fighter_b_sig_distance_landed_total</th>
      <th>fighter_a_sig_distance_attempted_total</th>
      <th>fighter_b_sig_distance_attempted_total</th>
      <th>fighter_a_sig_clinch_landed_total</th>
      <th>fighter_b_sig_clinch_landed_total</th>
      <th>fighter_a_sig_clinch_attempted_total</th>
      <th>fighter_b_sig_clinch_attempted_total</th>
      <th>fighter_a_sig_ground_landed_total</th>
      <th>fighter_b_sig_ground_landed_total</th>
      <th>fighter_a_sig_ground_attempted_total</th>
      <th>fighter_b_sig_ground_attempted_total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>7519.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
      <td>7498.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>2.337013</td>
      <td>0.248066</td>
      <td>0.182715</td>
      <td>38.361696</td>
      <td>33.578821</td>
      <td>83.788744</td>
      <td>78.362630</td>
      <td>58.259002</td>
      <td>49.700053</td>
      <td>106.424780</td>
      <td>96.728861</td>
      <td>1.220459</td>
      <td>0.894505</td>
      <td>2.943852</td>
      <td>2.657909</td>
      <td>0.453988</td>
      <td>0.326620</td>
      <td>0.136036</td>
      <td>0.133502</td>
      <td>24.393572</td>
      <td>20.942251</td>
      <td>65.060283</td>
      <td>61.040277</td>
      <td>7.869298</td>
      <td>6.954121</td>
      <td>11.206455</td>
      <td>10.200453</td>
      <td>6.098826</td>
      <td>5.682449</td>
      <td>7.522006</td>
      <td>7.121899</td>
      <td>26.897039</td>
      <td>25.000000</td>
      <td>67.307949</td>
      <td>65.790077</td>
      <td>5.310349</td>
      <td>4.795545</td>
      <td>7.558282</td>
      <td>7.002401</td>
      <td>6.154308</td>
      <td>3.783276</td>
      <td>8.922513</td>
      <td>5.570152</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.015575</td>
      <td>0.522739</td>
      <td>0.459030</td>
      <td>32.692857</td>
      <td>30.722946</td>
      <td>71.082010</td>
      <td>68.534223</td>
      <td>45.979618</td>
      <td>41.637469</td>
      <td>79.610327</td>
      <td>76.074174</td>
      <td>1.808955</td>
      <td>1.519582</td>
      <td>3.707804</td>
      <td>3.700101</td>
      <td>0.894802</td>
      <td>0.765843</td>
      <td>0.428298</td>
      <td>0.415031</td>
      <td>22.773937</td>
      <td>21.387068</td>
      <td>57.791174</td>
      <td>56.107637</td>
      <td>8.867918</td>
      <td>8.077144</td>
      <td>12.159781</td>
      <td>11.181823</td>
      <td>8.075621</td>
      <td>7.583556</td>
      <td>9.896388</td>
      <td>9.318820</td>
      <td>29.463747</td>
      <td>27.230514</td>
      <td>68.494964</td>
      <td>65.075124</td>
      <td>7.813834</td>
      <td>6.864527</td>
      <td>10.605134</td>
      <td>9.389515</td>
      <td>9.897989</td>
      <td>7.718130</td>
      <td>14.403955</td>
      <td>11.003423</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>14.000000</td>
      <td>10.000000</td>
      <td>29.000000</td>
      <td>24.000000</td>
      <td>22.000000</td>
      <td>16.000000</td>
      <td>40.000000</td>
      <td>33.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>8.000000</td>
      <td>5.000000</td>
      <td>22.000000</td>
      <td>17.000000</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>5.000000</td>
      <td>5.000000</td>
      <td>15.000000</td>
      <td>15.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>3.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>31.000000</td>
      <td>25.000000</td>
      <td>66.000000</td>
      <td>61.000000</td>
      <td>50.000000</td>
      <td>41.000000</td>
      <td>95.000000</td>
      <td>83.500000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>18.000000</td>
      <td>15.000000</td>
      <td>51.000000</td>
      <td>46.000000</td>
      <td>5.000000</td>
      <td>4.000000</td>
      <td>7.000000</td>
      <td>7.000000</td>
      <td>3.000000</td>
      <td>3.000000</td>
      <td>4.000000</td>
      <td>4.000000</td>
      <td>17.000000</td>
      <td>16.000000</td>
      <td>45.000000</td>
      <td>45.000000</td>
      <td>2.000000</td>
      <td>2.000000</td>
      <td>4.000000</td>
      <td>4.000000</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>3.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>54.000000</td>
      <td>49.000000</td>
      <td>120.000000</td>
      <td>115.000000</td>
      <td>83.000000</td>
      <td>73.000000</td>
      <td>155.000000</td>
      <td>144.000000</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>4.000000</td>
      <td>4.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>34.000000</td>
      <td>30.000000</td>
      <td>92.000000</td>
      <td>89.000000</td>
      <td>11.000000</td>
      <td>10.000000</td>
      <td>16.000000</td>
      <td>15.000000</td>
      <td>8.000000</td>
      <td>8.000000</td>
      <td>10.000000</td>
      <td>10.000000</td>
      <td>39.000000</td>
      <td>36.000000</td>
      <td>99.000000</td>
      <td>98.000000</td>
      <td>7.000000</td>
      <td>7.000000</td>
      <td>10.000000</td>
      <td>10.000000</td>
      <td>8.000000</td>
      <td>4.000000</td>
      <td>12.000000</td>
      <td>6.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>5.000000</td>
      <td>5.000000</td>
      <td>4.000000</td>
      <td>445.000000</td>
      <td>241.000000</td>
      <td>744.000000</td>
      <td>495.000000</td>
      <td>447.000000</td>
      <td>355.000000</td>
      <td>746.000000</td>
      <td>497.000000</td>
      <td>21.000000</td>
      <td>12.000000</td>
      <td>27.000000</td>
      <td>49.000000</td>
      <td>10.000000</td>
      <td>7.000000</td>
      <td>6.000000</td>
      <td>4.000000</td>
      <td>274.000000</td>
      <td>187.000000</td>
      <td>553.000000</td>
      <td>414.000000</td>
      <td>117.000000</td>
      <td>92.000000</td>
      <td>133.000000</td>
      <td>112.000000</td>
      <td>78.000000</td>
      <td>95.000000</td>
      <td>101.000000</td>
      <td>102.000000</td>
      <td>439.000000</td>
      <td>225.000000</td>
      <td>737.000000</td>
      <td>447.000000</td>
      <td>95.000000</td>
      <td>78.000000</td>
      <td>115.000000</td>
      <td>89.000000</td>
      <td>96.000000</td>
      <td>100.000000</td>
      <td>141.000000</td>
      <td>130.000000</td>
    </tr>
  </tbody>
</table>
</div>



Looking at the above we have some questions to investigate:

1) Round is a categorical value - A way to tell is that we don't measure the round it is round 1 or it is round 2 not round 2.5

2) fighter_a_sig_strikes_landed has a max value of 445 strikes this seems high, lets have a look

3) fighter_a_sig_strikes_attempted has a max value of 744 strikes this seems high, lets have a look

4) fighter_a_takedowns_total_landed has a max value of 21 strikes this seems high, lets have a look
4) fighter_b_takedowns_total_landed has a max value of 49 strikes this seems high, lets have a look


```python
# create a list of the column names belonging to numerical columns
numerical_columns = list(dataframe.describe().columns)

# create a loop to make a boxplot and histogram for each point
for i in numerical_columns:
    plt.figure()
    plt.tight_layout()
    sns.set(rc={'figure.figsize':(8,5)})
    
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=False)
    plt.gca().set(xlabel = i, ylabel = 'Frequency')
    sns.boxplot(dataframe[i], ax=ax_box, linewidth=1.0)
    sns.histplot(dataframe[i], ax=ax_hist, bins=10, kde=True)
```

    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\ipykernel_launcher.py:6: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    C:\Users\lanna\Anaconda3\lib\site-packages\seaborn\_decorators.py:43: FutureWarning: Pass the following variable as a keyword arg: x. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      FutureWarning
    


    <Figure size 800x500 with 0 Axes>



    
![png](output_39_2.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_4.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_6.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_8.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_10.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_12.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_14.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_16.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_18.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_20.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_22.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_24.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_26.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_28.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_30.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_32.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_34.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_36.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_38.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_40.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_42.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_44.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_46.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_48.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_50.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_52.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_54.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_56.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_58.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_60.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_62.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_64.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_66.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_68.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_70.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_72.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_74.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_76.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_78.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_80.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_82.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_84.png)
    



    <Figure size 800x500 with 0 Axes>



    
![png](output_39_86.png)
    


# Later sections - don't delete just yet!


```python
'''
When we look at the missing values some make sense for example judges & judges score only have a 
value if the fight ends by decision, this often doesn't happen leading to lots of empty values.

Secondly, performance bonus has a lot of empty values because that column is blank unless a fight
wins the additional performance bonus. - It would be an interesting question to what % of fights 
gets a performance bonus and of these fights how they usually end and if they can be predicted.

Next, it seems control time is missing quite a few values, I can't see a good reason for this so we will 
have to invesigate this. My assumption is maybe these are earlier fights in the UFC and these stats
weren't recorded yet

Finally, we have 21 missing values in a lot of the striking columns, again we will have to investigate
but my assumption is that again these are earlier fights in the UFC and these stats
weren't recorded yet.

Let's investigate!!

'''
```




    "\nWhen we look at the missing values some make sense for example judges & judges score only have a \nvalue if the fight ends by decision, this often doesn't happen leading to lots of empty values.\n\nSecondly, performance bonus has a lot of empty values because that column is blank unless a fight\nwins the additional performance bonus. - It would be an interesting question to what % of fights \ngets a performance bonus and of these fights how they usually end and if they can be predicted.\n\nNext, it seems control time is missing quite a few values, I can't see a good reason for this so we will \nhave to invesigate this. My assumption is maybe these are earlier fights in the UFC and these stats\nweren't recorded yet\n\nFinally, we have 21 missing values in a lot of the striking columns, again we will have to investigate\nbut my assumption is that again these are earlier fights in the UFC and these stats\nweren't recorded yet.\n\nLet's investigate!!\n\n"




```python
# check for missing values - No mising values
dataframe['method'].value_counts()
```




    Decision - Unanimous       2642
    KO/TKO                     2390
    Submission                 1486
    Decision - Split            713
    Decision - Majority          92
    TKO - Doctor's Stoppage      89
    Overturned                   57
    Could Not Continue           27
    DQ                           21
    Other                         2
    Name: method, dtype: int64




```python
# does a split and majority decision differ & what is the split between KO and tko?
```


```python
# Lets split the method into main method and sub method
```


```python



# find the all the values in the method column
#keys = dataframe['method'].unique()
#data = dataframe['method'].value_counts()
# create a visual for the way fights are won
#palette_color = sns.color_palette('bright') 
  
# plotting data on chart 
#plt.pie(data, colors=palette_color, autopct='%.0f%%') 
  
# displaying chart 
#plt.show() 

```

## Exploring our dataset
To start out project we need to first understand our data. This will follow the format of first understanding what each data point shows us, looking at the distribution of our data and looking for patterns that we might want to explore. It will also involve curating a list of question we might want to investigate that may help us with prediction later.

 This problem will be split into two predictive steps, first will use regression to estimate the number of strikes between two fighters. The second will be the classifier of who would win the fight based on the stats we have estimated.
