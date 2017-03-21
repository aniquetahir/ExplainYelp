import mysql.connector
from math import fabs




cnx = mysql.connector.connect(user='root', password='', database='yelp')
cursor = cnx.cursor()

categories = set()
category_data = {}

query = ("select name,city,my_avg,num_bus from "
            "( "
            "	select categories.name,city, state, avg(stars) as my_avg, count(businesses.business_id) as num_bus "
            "	from businesses  "
            "		inner join business_category "
            "			on business_category.business_id = businesses.business_id "
            "		inner join categories "
            "			on business_category.category_id = categories.id "
            "	where state='AZ' and (city = 'Tempe' or city = 'Scottsdale') group by city,category_id order by categories.name "
            ") tempe_scottsdale "
            "where tempe_scottsdale.num_bus>20; ")

cursor.execute(query)

for (name, city, my_avg, num_bus) in cursor:
    if name in categories:
        category_data[name][city] = {
            'avg': float(my_avg),
            'num_bus': int(num_bus)
        }

    else:
        categories.add(name)
        category_data[name]={
            city: {
                'avg': float(my_avg),
                'num_bus': int(num_bus)
            }
        }



cursor.close()
cnx.close()

list_of_differences = []
# Calculate difference in Scottsdale and Tempe
for cat in categories:
    if category_data[cat].has_key('Tempe') and category_data[cat].has_key('Scottsdale'):
        difference = fabs(category_data[cat]['Tempe']['avg']
                                                - category_data[cat]['Scottsdale']['avg'])
        category_data[cat]['difference'] = difference
        list_of_differences.append((cat, difference))

list_of_differences.sort(key=lambda x:x[1], reverse=False)


# plot graph of the differences
for cat, difference in list_of_differences:
    print "%s, %s" % (cat, difference)

import matplotlib.pyplot as plt
import numpy as np

#data

# considered cats
considered_cats = map(lambda x:x[0], list_of_differences)[0:20]
considered_cats.append("Real Estate")
np.random.seed(42)

data = map(lambda x: category_data[x]['Tempe']['avg'], considered_cats)
data2 = map(lambda x: category_data[x]['Scottsdale']['avg'], considered_cats)
names = considered_cats

ax = plt.subplot(111)
width=1.5
bins = map(lambda x: width*x, range(1, len(data)+1))
bins2 = map(lambda x: width*x+0.5, range(1, len(data)+1))

ax.bar(bins, data, width=0.5, label='Tempe')
ax.bar(bins2, data2, width=0.5, color='green', label='Scottsdale')

ax.set_xticks(map(lambda x: width*x, range(1,len(data)+1)))
ax.set_xticklabels(names,rotation=90, rotation_mode="anchor", ha="right")

ax.legend(loc='upper right')

plt.show()


