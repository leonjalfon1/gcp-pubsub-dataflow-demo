from arango import ArangoClient
import os

# Set variables
password = os.environ.get('ARANGODB_PASSWORD')
url = os.environ.get('ARANGODB_URL')
print("1) Setting variables")
print("ArangoDB Url: " + url)
print("ArangoDB Password: " + password)

# Initialize the client for ArangoDB.
print("2) Initializing the ArangoDB client")
client = ArangoClient(hosts=url)

# Connect to "_system" database as root user.
print("3) Connecting to the '_system' database")
sys_db = client.db('_system', username='root', password=password)

# Create a new database named "test".
print("4) Creating the 'test-document' database")
sys_db.create_database('test-document')

# Connect to "test" database as root user.
print("5) Connecting to the 'test-document' database")
db = client.db('test-document', username='root', password=password)

# Create a new collection named "students".
print("6) Creating a new callection 'students'")
students = db.create_collection('students')

# Add a hash index to the collection.
print("7) Adding a Hash index to the collection 'name'")
students.add_hash_index(fields=['name'], unique=True)

# Insert new documents into the collection.
print("8) Inserting data into the collection")
print("{'name': 'jane', 'age': 39}")
print("{'name': 'josh', 'age': 18}")
print("{'name': 'judy', 'age': 21}")
students.insert({'name': 'jane', 'age': 39})
students.insert({'name': 'josh', 'age': 18})
students.insert({'name': 'judy', 'age': 21})

# Execute an AQL query and iterate through the result cursor.
print("9) Retriving names from the collection")
cursor = db.aql.execute('FOR doc IN students RETURN doc')
student_names = [document['name'] for document in cursor]

# Print results
print("")
print("Data:")
print(student_names)
print("")
