import unittest

from google.protobuf.json_format import MessageToDict

from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()

    class Meta:
        schema = Account

    def pre_serialize(self, data):
        del data['balance']
        return data


class PerSerializeTestCase(unittest.TestCase):

    def test_with_json_input(self):
        json_data = {
            'username': 'John Doe',
            'balance': 12345
        }
        serializer = AccountSerializer(json_data)
        proto_data = serializer.protobuf
        self.assertNotIn('balance', MessageToDict(proto_data))

    def test_with_protobuf_input(self):
        pass


if __name__ == '__main__':
    unittest.main()
