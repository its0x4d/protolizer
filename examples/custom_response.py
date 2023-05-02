import random

from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField(custom=True)

    class Meta:
        schema = Account

    @staticmethod
    def get_custom_balance(obj):
        # The obj is all the data passed to the serializer, so you can play with the data as you like...
        return random.randint(1000, 2000)


json_data = {
    'username': 'John Doe'
    # We don't need to pass the `balance`, because it's a custom field
}
serializer = AccountSerializer(json_data)
proto_data = serializer.protobuf
print(proto_data.username)  # John Doe
print(proto_data.balance)  # This will be a random number between 1000 and 2000
