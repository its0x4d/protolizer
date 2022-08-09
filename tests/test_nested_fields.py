import unittest

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


class NestedFieldTestCase(unittest.TestCase):

    def test_nested_fields(self):
        json_data = {
            'username': 'John Doe',
            'balance': 12345,
            'settings': {
                'is_public': True
            }
        }
        serializer = AccountSerializer(json_data)
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.username, 'John Doe')
        self.assertEqual(proto_data.balance, 12345)
        self.assertTrue(proto_data.settings.is_public)

    def test_nested_fields_from_proto(self):
        protobuf = Account(
            username='John Doe',
            balance=12345,
            settings=AccountSettings(is_public=True)
        )
        serializer = AccountSerializer(protobuf)
        json_data = serializer.data
        self.assertEqual(json_data['username'], 'John Doe')
        self.assertEqual(json_data['balance'], 12345)
        self.assertTrue(json_data['settings']['is_public'])


if __name__ == '__main__':
    unittest.main()
