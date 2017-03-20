from mysql.connector import connection
from io import open
import json

business_file = open('yelp_academic_dataset_business.json', 'r', encoding='utf8')

cnx = connection.MySQLConnection(user='root', password='', host='127.0.0.1', database='yelp')

json_line = None
finished_reading = False
numlines = 0
json_decoder = json.JSONDecoder()
insert_query = ("insert into businesses(`business_id`, `name`, `neighborhood`, `address`, `city`, `state`, `postal code`, `coordinates`, `stars`, `review_count`, `is_open`, `type`) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, POINT(%s,%s), %s, %s, %s, %s) ")


cursor = cnx.cursor()
while not finished_reading:
    json_line = business_file.readline()
    numlines+=1
    if numlines<25395:
        continue
    if numlines%1000==0:
        print "%i rows added" % numlines
    if json_line == "":
        finished_reading = True
    else:
        try:
            decoded_obj = json_decoder.decode(json_line)
            # Add to database
            data_business = (decoded_obj['business_id'],
                                decoded_obj['name'],
                                decoded_obj['neighborhood'],
                                decoded_obj['address'],
                                decoded_obj['city'],
                                decoded_obj['state'],
                                decoded_obj['postal_code'],
                                decoded_obj['latitude'],
                                decoded_obj['longitude'],
                                decoded_obj['stars'],
                                decoded_obj['review_count'],
                                decoded_obj['is_open'],
                                decoded_obj['type'])
            cursor.execute(insert_query, data_business)
            cnx.commit()
        except Exception as e:
            str_err = str(e)
            print str_err

cursor.close()

business_file.close()
cnx.close()


