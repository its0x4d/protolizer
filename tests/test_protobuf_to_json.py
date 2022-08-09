import unittest

from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()

    class Meta:
        schema = Account


class ProtobufToJsonTestCase(unittest.TestCase):

    def test_single_dict_to_json(self):
        protobuf = Account(
            username='John Doe',
            balance=123
        )
        serializer = AccountSerializer(protobuf)
        json_data = serializer.data
        self.assertEqual(json_data['username'], 'John Doe')

    def test_list_of_dict_to_json(self):
        protobuf = [
            Account(
                username='John Doe',
                balance=123
            ),
            Account(
                username='Jane Doe',
                balance=1234
            )
        ]
        serializer = AccountSerializer(protobuf, many=True)
        json_data = serializer.data
        for c, i in enumerate(json_data):
            self.assertEqual(i['username'], protobuf[c].username)


if __name__ == '__main__':
    unittest.main()
