from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account, AccountSettings


class AccountSettingsSerializer(Serializer):
    is_public = fields.BooleanField()

    def to_representation(self, instance):
        # You can access the context of the parent serializer
        # by using `self.context`. (If you pass `self` as context to nested serializers)
        is_public = self.context.get('is_public')
        return {
            'is_public': is_public,
            # This field Only supported in JSON output.
            # because it's not defined in the protobuf schema.
            # Uncomment the next line to see the error.
            # 'is_private': not is_public
            # if you want to see the output, you can only use `serializer.data` instead of `serializer.protobuf`
        }


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()
    # You can pass `self` as context to nested serializers
    # to access the context of the parent serializer.
    # Note.0: you can pass any data to the context. (not only `self`)
    # Note.1: you should pass data to the nested serializer as well.
    # Otherwise, the nested serializer will not be initialized.
    settings = AccountSettingsSerializer(context='self')

    class Meta:
        schema = Account


json_data = Account(
    username='John Doe',
    balance=12345,
    # This setting will be ignored because we pass `is_public=False` to the context.
    settings=AccountSettings(is_public=False)
)
serializer = AccountSerializer(json_data, context={'is_public': True})
proto_data = serializer.protobuf
print('------------------')
print('As Protobuf:')
print(proto_data)
print('------------------')
# You can access the data like a normal python object.
print(f"Username: {proto_data.username}")  # John Doe
print(f"Balance: {proto_data.balance}")  # 12345
print(f"Is Public: {proto_data.settings.is_public}")  # True

print('------------------')
print('As Json:')
print(serializer.data)
