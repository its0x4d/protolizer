# Protolizer Documentation

## Introduction
Protolizer is a simple library to serialize and deserialize protobuf messages

## Installation

```bash
pip install protolizer
```

## Usage for serialization

```python
from protolizer import Serializer, fields

class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()

    class Meta:
        # Here we define our generated protobuf message name
        # our protobuf message is something like:
        # message Account {
        #     string username = 1;
        #     int32 balance = 2;
        # }
        schema = Account

# Define an account in JSON and Protobuf format
protobuf_data = Account(username='John', balance=100)
json_data = {'username': 'John', 'balance': 100}

# Serialize the data to Protobuf format
protobuf_serializer = AccountSerializer(protobuf_data)
print(protobuf_serializer.protobuf)

# Serialize the data to JSON format
json_serializer = AccountSerializer(json_data)
print(json_serializer.json)

# Deserialize the data from Protobuf format to JSON format
protobuf_deserializer = AccountSerializer(protobuf_serializer.protobuf)
print(protobuf_deserializer.data)

# Deserialize the data from JSON format to Protobuf format
json_deserializer = AccountSerializer(json_serializer.json)
print(json_deserializer.data)
```

## Contribute

```text
If you want to contribute to this project, please open an issue on GitHub.
```

## License

```text
This project is licensed under the MIT License.
```

## Author
This project is authored by [@uwsgi](https://instagram.com/uwsgi)


