from arango import ArangoClient
import os

# Set variables
password = os.environ.get('ARANGODB_PASSWORD')
url = os.environ.get('ARANGODB_URL')
print("1) Setting variables")
print("  ArangoDB Url: " + url)
print("  ArangoDB Password: " + password)

# Initialize the client for ArangoDB.
print("2) Initializing the ArangoDB client")
client = ArangoClient(hosts=url)

# Connect to "_system" database as root user.
print("3) Connecting to the '_system' database")
sys_db = client.db('_system', username='root', password=password)

# Create a new database named "test".
print("4) Creating the 'test-graph' database")
sys_db.create_database('test-graph',replication_factor=3)

# Connect to "test" database as root user.
print("5) Connect to 'test-graph' database as root user")
db = client.db('test-graph', username='root', password=password)

# Create a new graph named "school".
print("6) Create a new graph named 'school'")
graph = db.create_graph('school')

# Create vertex collections for the graph.
print("7) Create vertex collections for the graph (students,lectures)")
students = graph.create_vertex_collection('students')
lectures = graph.create_vertex_collection('lectures')

# Create an edge definition (relation) for the graph.
print("8) Create an edge definition (relation) for the graph")
register = graph.create_edge_definition(
    edge_collection='register',
    from_vertex_collections=['students'],
    to_vertex_collections=['lectures']
)

# Insert vertex documents into "students" (from) vertex collection.
print("9) Insert vertex documents into 'students' (from) vertex collection")
students.insert({'_key': '01', 'full_name': 'Anna Smith'})
students.insert({'_key': '02', 'full_name': 'Jake Clark'})
students.insert({'_key': '03', 'full_name': 'Lisa Jones'})

# Insert vertex documents into "lectures" (to) vertex collection.
print("10) Insert vertex documents into 'lectures' (to) vertex collection")
lectures.insert({'_key': 'MAT101', 'title': 'Calculus'})
lectures.insert({'_key': 'STA101', 'title': 'Statistics'})
lectures.insert({'_key': 'CSC101', 'title': 'Algorithms'})

# Insert edge documents into "register" edge collection.
print("11) Insert edge documents into 'register' edge collection")
register.insert({'_from': 'students/01', '_to': 'lectures/MAT101'})
register.insert({'_from': 'students/01', '_to': 'lectures/STA101'})
register.insert({'_from': 'students/01', '_to': 'lectures/CSC101'})
register.insert({'_from': 'students/02', '_to': 'lectures/MAT101'})
register.insert({'_from': 'students/02', '_to': 'lectures/STA101'})
register.insert({'_from': 'students/03', '_to': 'lectures/CSC101'})

# Traverse the graph in outbound direction, breadth-first.
print("12) Generating Graph")
result = graph.traverse(
    start_vertex='students/01',
    direction='outbound',
    strategy='breadthfirst'
)

# Print results
print("")
print("Graph Info:")
print(result)
print("")