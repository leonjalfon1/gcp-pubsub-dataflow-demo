# Python driver for ArangoDB Demo (python-arango)

## Prerequisites

- Create a virtual environment
```
virtualenv arango
```
```
source arango/bin/activate
```

- Install the arangodb driver
```
pip install python-arango
```

- Set the ArangoDB Url environment variable:
```
export ARANGODB_URL="your-url:port"
```

- Set the ArangoDB Password environment variable:
```
export ARANGODB_PASSWORD="your-password"
```

## Writing and Reading Documents

- To see a full example run (a database called 'test-document' will be created):

```
python documents.py
```

## Writing and Reading Graphs

- To see a full example run (a database called 'test-graph' will be created):

```
python graphs.py
```