import unittest

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
        return 597 * 2


class CustomResponseTestCase(unittest.TestCase):

    def test_custom_response(self):
        json_data = {
            'username': 'John Doe'
        }
        serializer = AccountSerializer(json_data)
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.username, 'John Doe')
        self.assertEqual(proto_data.balance, 1194)

    def test_custom_field_to_representation_with_list(self):
        """CustomField with child must return a list when value is a list (not pass list to child)."""
        field = fields.CustomField(child=fields.CharField())
        field.bind('tags', None)
        result = field.to_representation(['a', 'b', 'c'])
        self.assertEqual(result, ['a', 'b', 'c'])


if __name__ == '__main__':
    unittest.main()
