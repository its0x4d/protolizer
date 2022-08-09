import unittest

from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()

    class Meta:
        schema = Account


class JsonToProtoTestCase(unittest.TestCase):

    def test_json_to_proto(self):
        json_data = {
            'username': 'John Doe',
            'balance': 12345
        }
        serializer = AccountSerializer(json_data)
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.username, 'John Doe')

    def test_json_to_proto_with_list(self):
        json_data = [
            {
                'username': 'John Doe',
                'balance': 12345
            },
            {
                'username': 'Jane Doe',
                'balance': 123456
            }

        ]
        serializer = AccountSerializer(json_data, many=True)
        proto_data = serializer.protobuf
        for c, i in enumerate(proto_data):
            self.assertEqual(i.username, json_data[c]['username'])

