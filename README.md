# Protolizer Documentation

## Introduction
Protolizer is a simple library to serialize and deserialize protobuf messages (JSON/dict ↔ protobuf). It does **not** require gRPC—only the `protobuf` package.

## Installation

```bash
pip install protolizer
```

For running the project's tests and development tools:

```bash
pip install -e ".[dev]"
```

Or using requirements files:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

## Usage for serialization

```python
from protolizer import Serializer, fields

class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()

    class Meta:
        # schema must be your generated protobuf message class (e.g. from *_pb2 import Account)
        # Your .proto might look like:
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
print(json_serializer.data)

# Deserialize the data from Protobuf format to JSON format
protobuf_deserializer = AccountSerializer(protobuf_serializer.protobuf)
print(protobuf_deserializer.data)

# Deserialize the data from JSON format to Protobuf format
json_deserializer = AccountSerializer(json_serializer.data)
print(json_deserializer.protobuf)
```
If you want to see more examples, please check the [examples](examples) directory.

### Enum fields

```python
from myapp_pb2 import Account, Status

class AccountSerializer(Serializer):
    username = fields.CharField()
    status = fields.EnumField(Status)

    class Meta:
        schema = Account
```

### Partial updates

Pass `partial=True` to validate only the fields present in input (useful for PATCH-style updates):

```python
serializer = AccountSerializer(data={"balance": 200}, partial=True)
serializer.is_valid(raise_exception=True)
```

**Note:** `Meta.schema` must be the generated protobuf message class (from your `*_pb2` module). gRPC (`grpcio`) is only needed if you use gRPC services; for JSON ↔ protobuf conversion, the `protobuf` package alone is enough.

## Supported fields

- [X] CharField
- [X] BytesField
- [X] IntField
- [X] FloatField
- [X] BooleanField
- [X] DateTimeField
- [X] TimestampField
- [X] EnumField
- [X] DictField
- [X] ListField
- [X] CustomField (for custom responses)

Field options: `read_only`, `write_only`, `required`, `allow_null`.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## Security

See [SECURITY.md](SECURITY.md) to report vulnerabilities.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details



## Author
This project is authored by [@uwsgi](https://t.me/uwsgi) on Telegram.

