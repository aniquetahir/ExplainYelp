import mysql.connector
from math import fabs

cnx = mysql.connector.connect(user='root', password='root', database='yelp')
cursor = cnx.cursor()

categories = set()
category_data = {}

explanation_query = ("select name,city,my_avg,num_bus from "
                     "( "
                     "	select categories.name,city, state, avg(stars) as my_avg, count(businesses.business_id) as num_bus "
                     "	from businesses  "
                     "		inner join business_category "
                     "			on business_category.business_id = businesses.business_id "
                     "		inner join categories "
                     "			on business_category.category_id = categories.id "
                     "where state='AZ' and (city = 'Tempe' or city = 'Scottsdale') group by city,category_id order by "
                     "categories.name "
                     ") tempe_scottsdale "
                     "where tempe_scottsdale.num_bus>20; ")

data_query = ("	select categories.name category,city, state, stars, businesses.name businessname "
              "	from businesses  "
              "		inner join business_category "
              "			on business_category.business_id = businesses.business_id "
              "		inner join categories "
              "			on business_category.category_id = categories.id "
              "where state='AZ' and (city = 'Tempe' or city = 'Scottsdale') "
              )

cursor.execute(data_query)

for (name, city, my_avg, num_bus) in cursor:
    if name in categories:
        category_data[name][city] = {
            'avg': float(my_avg),
            'num_bus': int(num_bus)
        }

    else:
        categories.add(name)
        category_data[name] = {
            city: {
                'avg': float(my_avg),
                'num_bus': int(num_bus)
            }
        }

cursor.close()
cnx.close()
