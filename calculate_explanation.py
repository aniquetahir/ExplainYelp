import mysql.connector
from math import fabs

cnx = mysql.connector.connect(user='root', password='root', database='yelp')


# TODO Explanation Query
# explanation_query = ("select name,city,my_avg,num_bus from "
#                      "( "
#                      "	select categories.name,city, state, avg(stars) as my_avg, count(businesses.business_id) as num_bus "
#                      "	from businesses  "
#                      "		inner join business_category "
#                      "			on business_category.business_id = businesses.business_id "
#                      "		inner join categories "
#                      "			on business_category.category_id = categories.id "
#                      "where state='AZ' and (city = 'Tempe' or city = 'Scottsdale') group by city,category_id order by "
#                      "categories.name "
#                      ") tempe_scottsdale "
#                      "where tempe_scottsdale.num_bus>20; ")

data_query_q1 = (
    "select categories.name category, postal_code, stars, businesses.name, businesses.business_id "
    "from businesses   "
    "	inner join business_category  "
    "		on business_category.business_id = businesses.business_id  "
    "	inner join categories  "
    "		on business_category.category_id = categories.id  "
    "where state='AZ' and (city = 'Scottsdale'); "
)

data_query_q2 = (
    "select categories.name category, postal_code, stars, businesses.name, businesses.business_id "
    "from businesses   "
    "	inner join business_category  "
    "		on business_category.business_id = businesses.business_id  "
    "	inner join categories  "
    "		on business_category.category_id = categories.id  "
    "where state='AZ' and (city = 'Tempe'); "
)

q1 = (

)

cursor = cnx.cursor()
cursor.execute(data_query_q1)
q1_category_bids = {}
q1_pcode_bids = {}
q1_b_name_bids = {}

categories = set()
p_codes = set()
b_names = set()
for (cat, p_code, stars, b_name, b_id) in cursor:
    categories.add(cat)
    if not cat in q1_category_bids:
        q1_category_bids[cat] = set()
    q1_category_bids[cat].append(b_id)

    p_codes.add(p_code)
    if not p_code in q1_pcode_bids:
        q1_pcode_bids[p_code] = set()
    q1_pcode_bids[p_code].append(b_id)

    b_names.add(b_name)
    if not b_name in q1_b_name_bids:
        q1_b_name_bids[b_name] = set()
    q1_b_name_bids[b_name].append(b_id)


cursor.close()

cursor = cnx.cursor()
cursor.execute(data_query_q1)
q2_category_bids = {}
q2_pcode_bids = {}
q2_b_name_bids = {}

categories = set()
p_codes = set()
b_names = set()
for (cat, p_code, stars, b_name, b_id) in cursor:
    categories.add(cat)
    if not cat in q2_category_bids:
        q2_category_bids[cat] = set()
    q2_category_bids[cat].add(b_id)

    p_codes.add(p_code)
    if not p_code in q2_pcode_bids:
        q2_pcode_bids[p_code] = set()
    q2_pcode_bids[p_code].add(b_id)

    b_names.add(b_name)
    if not b_name in q2_b_name_bids:
        q2_b_name_bids[b_name] = set()
    q2_b_name_bids[b_name].add(b_id)


cursor.close()

# Find explanation over permutation of categories
cats = set()
for cat in q1_category_bids:
    cats.add(cat)
for cat in q2_category_bids:
    cats.add(cat)

for cat in cats:

# Find explanation over permutation of postal_codes
# Find explanation over permutation of b_names
# Find explanation over permutation of b_ids


cnx.close()
