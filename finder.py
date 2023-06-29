import requests
import pprint
import pandas as pd
import sqlalchemy as db
from sqlalchemy.sql import text
import re

# Dictionary storing new users
users = {
    'first_name': [
        'Mario',
        'Melisa',
        'Joaquin',
        'Henry'],
    'last_name': [
        'Juarez',
        'Jimenez',
        'Muños',
        'James'],
    'email': [
        'mj@gmail.com',
        'mjimenez@yahoo.com',
        'joaq@outlook.com',
        'henryj@hotmail.com'],
    'city': [
        'Orlando',
        'Orlando',
        'Miami',
        'Ashburn'],
    'interest1': [
        'Sports',
        'Art',
        'Travel',
        'Sports'],
    'interest2': [
        'Food',
        'Enterntainment',
        'Sports',
        'Travel'],
    'interest3': [
        'Art',
        'Travel',
        'Food',
        'Food']}
while True:
    user_fname = input("What is your first name? ").lower().capitalize()
    if user_fname == "":
        print("Input your name!")
        continue
    else:
        users['first_name'].append(user_fname)
        break

while True:
    user_lname = input("What is your last name? ").lower().capitalize()
    if user_lname == "":
        print("Input your last name!")
        continue
    else:
        users['last_name'].append(user_lname)
        break

# Promping for valid Email Address
while True:
    user_email = input("What is your email? ")
    regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, user_email):
        users['email'].append(user_email)
        break
    else:
        print("Invalid email")
        continue

# User interests
count = 1
dic_interests = {
    '1': 'Sports',
    '2': 'Food',
    '3': 'Enterntainment',
    '4': 'Art',
    '5': 'Travel'}
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
new_user = {
    'first_name': user_fname,
    'last_name': user_lname,
    'email': user_email,
    'city': city,
    'interest1': users['interest1'][-1],
    'interest2': users['interest2'][-1],
    'interest3': users['interest3'][-1]
}
# users["city"].append(city)
# Retriving user's location
# user_loc = response["data"]["location"]["city"]["name"]
# Storing locatioin in dictionary
#
print(city)

database_file = 'users_df.db'


# Create a database engine
engine = db.create_engine(f'sqlite:///{database_file}')

# Convert the new user dictionary to a DataFrame
new_user_df = pd.DataFrame(new_user, index=[0])

# Connect to the database and add the new user to the UserInfo table
with engine.connect() as connection:
    new_user_df.to_sql(
        'UserInfo',
        con=connection,
        if_exists='append',
        index=False)
    query = db.text(
        "SELECT * FROM UserInfo WHERE city = :city AND email != :email;")
    result = connection.execute(
        query, {'city': city, 'email': user_email}).fetchall()

# Convert the query result to a pandas DataFrame
users_same_city_df = pd.DataFrame(
    result,
    columns=[
        'first_name',
        'last_name',
        'email',
        'city',
        'interest1',
        'interest2',
        'interest3'])

# Print the DataFrame
print(users_same_city_df)
