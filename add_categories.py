from mysql.connector import connection
from io import open
import json

business_file = open('yelp_academic_dataset_business.json', 'r', encoding='utf8')
cnx = connection.MySQLConnection(user='root', password='', host='127.0.0.1', database='yelp')

json_line = None
finished_reading = False
numlines = 0
json_decoder = json.JSONDecoder()
insert_query = ("insert ignore into categories(`name`) values (%s);")

# Define set to hold categories
categories = set()

while not finished_reading:
    json_line = business_file.readline()
    numlines+=1
    if numlines%1000==0:
        print "%i rows added" % numlines
    if json_line == "":
        finished_reading = True
    else:
        try:
            decoded_obj = json_decoder.decode(json_line)
            for cat in decoded_obj['categories']:
                categories.add(cat)
        except Exception as e:
            str_err = str(e)
            print str_err


cursor = cnx.cursor()
for cat in categories:
    # Add to database
    cursor.execute(insert_query, (cat,) )
    cnx.commit()

cursor.close()
business_file.close()
cnx.close()


