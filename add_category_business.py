from mysql.connector import connection
from io import open
import json

business_file = open('yelp_academic_dataset_business.json', 'r', encoding='utf8')
cnx = connection.MySQLConnection(user='root', password='', host='127.0.0.1', database='yelp')

json_line = None
finished_reading = False
numlines = 0
json_decoder = json.JSONDecoder()
insert_query = ("insert into business_category(`business_id`, `category_id`) "
	                "select %s, id from categories "
	                "where categories.name = %s; ")


cursor = cnx.cursor()
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
            business_id = decoded_obj['business_id']
            for cat in decoded_obj['categories']:
                cursor.execute(insert_query, (business_id, cat,))
                cnx.commit()
        except Exception as e:
            str_err = str(e)
            print str_err


cursor.close()
business_file.close()
cnx.close()


