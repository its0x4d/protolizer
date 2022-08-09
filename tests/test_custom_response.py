import unittest

from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField(custom=True)

    class Meta:
        schema = Account

    @staticmethod
    def get_custom_balance(obj, value):
        return value * 2


class CustomResponseTestCase(unittest.TestCase):

    def test_custom_response(self):
        json_data = {
            'username': 'John Doe',
            'balance': 597
        }
        serializer = AccountSerializer(json_data)
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.username, 'John Doe')
        self.assertEqual(proto_data.balance, 1194)


if __name__ == '__main__':
    unittest.main()
