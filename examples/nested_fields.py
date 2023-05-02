from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account, AccountSettings


class AccountSettingsSerializer(Serializer):
    is_public = fields.BooleanField()


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()
    settings = AccountSettingsSerializer()

    class Meta:
        schema = Account


json_data = {
    'username': 'John Doe',
    'balance': 12345,
    'settings': {
        'is_public': False
    }
}

serializer = AccountSerializer(json_data)
proto_data = serializer.protobuf
print(proto_data.username)  # John Doe
print(proto_data.balance)  # 12345
print(proto_data.settings.is_public)  # True
