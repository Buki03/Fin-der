import requests
import pprint
import pandas as pd
import sqlalchemy as db
from sqlalchemy.sql import text

# User credentials
user_fname = input("What is your first name?:" )
user_lname = input("What is your last name?:" )
user_email = input("What is your email?:" )

# Dictionary storing new users
users = {
    'first_name':['Mario', 'Melisa', 'Joaquin'], 
    'last_name':['Juarez', 'Jimenez', 'Muños'],
    'email':['mj@gmail.com', 'mjimenez@yahoo.com', 'joaq@outlook.com'],
    'city':['Orlando', 'Orlando', 'Miami'],
    'interest1':['Sports', 'Art', 'Travel'],
    'interest2':['Food', 'Enterntainment', 'Sports'],
    'interest3':['Art', 'Travel', 'Food']
}
users['first_name'].append(user_fname)
users['last_name'].append(user_lname)
users['email'].append(user_email)

# User interests
count = 1
dic_interests = {'1':'Sports', '2':'Food', '3':'Enterntainment', '4':'Art', '5':'Travel'}
while 1 <= count <= 3:
    user_interests = int(input('''
                        Which of these fit with your interests? (Choose only 3)
                        1)Sports  2)Food  3)Enterntainment  4)Art  5)Travel
                            ''')
                        )
    
    if (user_interests > 5) or (user_interests < 1):
        raise ValueError('Please choose only from given numbers')
    else:
        users[f'interest{count}'].append(dic_interests[f'{count}'])
        count += 1

# API KEY + requests
response = requests.get('https://api64.ipify.org?format=json')
ip_data = response.json()

# Extract the IP address from the response
ip_address = ip_data['ip']

api_key = 'at_yck1qHvVmQvHi5JvcCymzKh7EeQY7'
url = f'https://geo.ipify.org/api/v1?apiKey={api_key}&ipAddress={ip_address}'
response = requests.get(url)
geolocation_data = response.json()
print(ip_address)
# Extract the city from the geolocation data
city = geolocation_data.get('location', {}).get('city')

# Retriving user's location
#user_loc = response["data"]["location"]["city"]["name"]
# Storing locatioin in dictionary
users["city"].append(city)
print(city)

# Converting "users" dictionary to dataframe
users_df = pd.DataFrame.from_dict(users)
engine = db.create_engine('sqlite:///users_df.db')
users_df.to_sql('UserInfo', con=engine, if_exists='replace', index=False)

# Ordering table by city
with engine.connect() as connection:
    # # Querying for user index in table
    # curr_userid_querry = db.text("SELECT 'index' FROM UserInfo WHERE email = :umail;")
    # # curr_userid_vars = (user_fname, user_lname)
    # curr_userid = connection.execute(curr_userid_querry, {'umail': user_email}).fetchall()

    # Querying for users with same city
    same_city_querr = db.text("SELECT * FROM UserInfo ;")
    same_city = connection.execute(same_city_querr).fetchall()
    
    print(pd.DataFrame(same_city))