import requests
import pprint
import pandas as pd
import sqlalchemy as db

# User credentials
user_fname = input("What is your first name?:" )
user_lname = input("What is your last name?:" )
user_email = input("What is your email?:" )

# Dictionary storing new users
users = {
    'first_name':[], 
    'last_name':[],
    'email':[],
    'city':[],
    'interest1':[],
    'interest2':[],
    'interest3':[]
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
api = 'sDf70ANa1m7mGGYOBzj16IfL2suTebt4tv37UVYE'
in_ad = input() #input adress
ipaddress = in_ad.replace(':', '%3A')
url = 'https://api.ipbase.com/v2/info?apikey=' + api + '&ip=' + ipaddress
response = requests.get(url).json()


# Retriving user's location
user_loc = response["data"]["location"]["city"]["name"]
# Storing locatioin in dictionary
users['city'].append(user_loc)


# Converting "users" dictionary to dataframe
users_df = pd.DataFrame.from_dict(users)
engine = db.create_engine('sqlite:///users_df.db')
users_df.to_sql('UserInfo', con=engine, if_exists='replace', index=False)
with engine.connect() as connection:
   query_result = connection.execute(db.text("SELECT * FROM UserInfo;")).fetchall()
   print(pd.DataFrame(query_result))
