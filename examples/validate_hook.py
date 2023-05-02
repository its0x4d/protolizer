from protolizer import Serializer, fields, ValidationError
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()

    class Meta:
        schema = Account

    @staticmethod
    def validate_balance(value):
        if value < 0:
            raise ValidationError('Balance must be positive')
        return value

    @staticmethod
    def validate_username(value):
        if len(value) < 3:
            raise ValidationError('Username must be at least 3 characters long')
        return value


json_data = [
    {
        'username': 'John Doe',
        'balance': 12345
    },
    {
        'username': 'Jo',
        'balance': -123
    }
]

# if `data` is not provided, `is_valid` will raise an exception
# The `many` argument is used to indicate that the data is a list of objects (or a protobuf repeated field)
serializer = AccountSerializer(data=json_data, many=True)
if serializer.is_valid():
    proto_data = serializer.protobuf
    print(proto_data.username)  # John Doe
    print(proto_data.balance)  # 12345
else:
    print(serializer.errors)
