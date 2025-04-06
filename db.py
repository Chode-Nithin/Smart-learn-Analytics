import mysql.connector
import json

# Sample dictionary
my_dict = {'id': 1, 'name': 'John Doe', 'age': 30}

# Serialize the dictionary to JSON format
serialized_dict = json.dumps(my_dict)

# Connect to MySQL database
db_password = "Tejas@root29"
db_name = "server"
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_password,
    database=db_name
)
# Create a cursor object to execute SQL queries
cursor = conn.cursor()
main_id = 1
sub_id = 1
score = 2.3
val_counts = [1, 2, 34]
history_id = 1
# Define your SQL query to insert the serialized dictionary into the table
sql = "update history set main_id = "+str(main_id)+",sub_id = "+str(sub_id)+",score="+str(score)+",val_counts='" + \
    str(val_counts)+"',v2top=(%s),v3top=(%s),v4dates=(%s),v4scores=(%s) where id ="+str(history_id)

# Execute the SQL query with the serialized dictionary as a parameter
cursor.execute(sql, (serialized_dict, serialized_dict,
               serialized_dict, serialized_dict,))

# Commit the transaction
conn.commit()

sql = "select * from history;"
cursor.execute(sql)
k = cursor.fetchall()
print(k)
for i in k[0]:
    print(i, type(i))

print(k[0][7])
s = k[0][7]
s = json.loads(s)
print(s, type(s))
print(k[0][6])
s = k[0][6]
s = json.loads(s)
print(s, type(s))

# Close the cursor and connection
cursor.close()
conn.close()
