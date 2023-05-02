from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()
    bio = fields.CharField()

    class Meta:
        schema = Account

    def pre_serialize(self, data):
        # Here you can modify the data before it is serialized.
        # For example, you can remove a field that is not present in the protobuf schema.
        # In this case, we remove the balance field.
        # Note N.01: This method is called before the data is validated.
        # Note N.02: The data is a python dictionary. and it will only be passed to `data` if it's defined in the
        #            serializer.
        del data['bio']
        return data


json_data = {
    'username': 'John Doe',
    'balance': 12345,
    'bio': 'I am a person.'
}
serializer = AccountSerializer(json_data)
proto_data = serializer.protobuf
print('------------------')
print('As Protobuf:')
print(proto_data)
print('------------------')
# You can access the data like a normal python object.
print(f"Username: {proto_data.username}")  # John Doe
print(f"Balance: {proto_data.balance}")  # 12345

print('------------------')
print('As Json:')
print(serializer.data)
