import requests
import pprint
import pandas as pd
import sqlalchemy as db
from sqlalchemy.sql import text
import re
from api_key import api_key
from asciimages import title_im

q1 = input("Are you struggling to make friends? (yes/yes) ")
q2 = input("Are you sick of the friends you have? (yes/yes) ")
q3 = input("Do you want to meet new people? (yes/yes) ")
if q1 != 'yes' and q2 != 'yes' and q3 != 'yes':
    print("GOODBYE!!!!")
    sys.exit()

title_im()

print("")
print("")
input("Click any key to start: ")


print("")
print("")

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
        'Entertainment',
        'Sports',
        'Travel'],
    'interest3': [
        'Art',
        'Travel',
        'Food',
        'Food']}

# Initializing names
user_fname = input("What is your first name? ").lower().capitalize()
user_lname = input("What is your last name? ").lower().capitalize()

# Checking given names are appropriate


def name_check(namestr, colname, namevar):
    while True:
        regex = re.compile(r'[a-zA-Z]+')
        if namevar == "":
            print("Input your {namestr}!")
            continue
        elif re.fullmatch(regex, user_fname):
            users[f'{colname}'].append(user_fname)
            break
        else:
            print("Input valid {namestr}!")
            continue


name_check("first name", "first_name", user_fname)
name_check("last name", "last_name", user_lname)

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
    '3': 'Entertainment',
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
        users[f'interest{count}'].append(dic_interests[f'{user_interests}'])
        count += 1

# API KEY + requests
response = requests.get('https://api64.ipify.org?format=json')
ip_data = response.json()

# Extract the IP address from the response
ip_address = ip_data['ip']
api = api_key
url = f'https://geo.ipify.org/api/v1?apiKey={api}&ipAddress={ip_address}'
response = requests.get(url)
geolocation_data = response.json()

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
print("The city you are located in is: " + city + "!!!")

# Initializing database
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
        'interest3']).drop_duplicates(subset=['email'])

# Print the DataFrame
print("")
print("")
print("CONGRATS, you found your MATCH")
input("The following people are located near you! Click enter to see")
print("")
print(users_same_city_df)
