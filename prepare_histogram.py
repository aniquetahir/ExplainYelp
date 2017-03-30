import mysql.connector
from math import fabs
import matplotlib.pyplot as plt
# import numpy as np


cnx = mysql.connector.connect(user='root', password='root', database='yelp')
cursor = cnx.cursor()
# Top rated cities in AZ
avg_city_ratings_query = "select city, count(*) as rating from businesses where state='AZ' group by city;"

cursor.execute(avg_city_ratings_query)

ratings_data = []
for tuple in cursor:
    ratings_data.append(tuple)

cursor.close()
cnx.close()

#Plot data
tempe_data = filter(lambda x:x[0]=='Tempe', ratings_data)[0]
scottsdale_data = filter(lambda x:x[0]=='Scottsdale', ratings_data)[0]

ratings_data = ratings_data[:8]
ratings_data.append(tempe_data)
ratings_data.append(scottsdale_data)

data = map(lambda x:x[1], ratings_data)
labels = map(lambda x:x[0], ratings_data)
ax = plt.subplot()

width = 1
bins = map(lambda x:x*width, range(1,len(data)+1))

ax.bar(bins, data, width=0.5, label='Avg Rating')

ax.set_xticks(bins)
ax.set_xticklabels(labels, rotation=45, rotation_mode="anchor", ha="right")

ax.legend(loc='upper left')
plt.tight_layout()
plt.show()

#
# cnx = mysql.connector.connect(user='root', password='root', database='yelp')
# cursor = cnx.cursor()
#
#
#
# categories = set()
# category_data = {}
#
# query = ("select name,city,my_avg,num_bus from "
#             "( "
#             "	select categories.name,city, state, avg(stars) as my_avg, count(businesses.business_id) as num_bus "
#             "	from businesses  "
#             "		inner join business_category "
#             "			on business_category.business_id = businesses.business_id "
#             "		inner join categories "
#             "			on business_category.category_id = categories.id "
#             "	where state='AZ' and (city = 'Tempe' or city = 'Scottsdale') group by city,category_id order by categories.name "
#             ") tempe_scottsdale "
#             "where tempe_scottsdale.num_bus>20; ")
#
# cursor.execute(query)
#
# for (name, city, my_avg, num_bus) in cursor:
#     if name in categories:
#         category_data[name][city] = {
#             'avg': float(my_avg),
#             'num_bus': int(num_bus)
#         }
#
#     else:
#         categories.add(name)
#         category_data[name]={
#             city: {
#                 'avg': float(my_avg),
#                 'num_bus': int(num_bus)
#             }
#         }
#
#
#
# cursor.close()
# cnx.close()
#
# list_of_differences = []
# # Calculate difference in Scottsdale and Tempe
# for cat in categories:
#     if category_data[cat].has_key('Tempe') and category_data[cat].has_key('Scottsdale'):
#         difference = fabs(category_data[cat]['Tempe']['avg']
#                                                 - category_data[cat]['Scottsdale']['avg'])
#         category_data[cat]['difference'] = difference
#         list_of_differences.append((cat, difference))
#
# list_of_differences.sort(key=lambda x:x[1], reverse=False)
#
#
# # plot graph of the differences
# for cat, difference in list_of_differences:
#     print "%s, %s" % (cat, difference)
#
#
#
# #data
#
# # considered cats
# considered_cats = map(lambda x:x[0], list_of_differences)[0:10]
# considered_cats.append("Real Estate")
#
# data = map(lambda x: category_data[x]['Tempe']['avg'], considered_cats)
# data2 = map(lambda x: category_data[x]['Scottsdale']['avg'], considered_cats)
# names = considered_cats
#
# ax = plt.subplot(111)
# width=1.5
# bins = map(lambda x: width*x, range(1, len(data)+1))
# bins2 = map(lambda x: width*x+0.5, range(1, len(data)+1))
#
# ax.bar(bins, data, width=0.5, label='Tempe')
# ax.bar(bins2, data2, width=0.5, color='green', label='Scottsdale')
#
# ax.set_xticks(map(lambda x: width*x, range(1,len(data)+1)))
# ax.set_xticklabels(names,rotation=45, rotation_mode="anchor", ha="right")
#
# ax.legend(loc='upper right')
# plt.tight_layout()
# plt.show()


