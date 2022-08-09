import unittest

from protolizer import Serializer, fields, ValidationError
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()

    class Meta:
        schema = Account

    @staticmethod
    def validate_balance(value):
        if value < 0:
            raise ValidationError('Balance must be positive')
        return value * 100

    @staticmethod
    def validate_username(value):
        if len(value) < 3:
            raise ValidationError('Username must be at least 3 characters long')
        return value


class ValidationTestCase(unittest.TestCase):

    def test_validate_invalid_request(self):
        protobuf = Account(
            username='John Doe',
            balance=123
        )
        serializer = AccountSerializer(data=protobuf)
        self.assertIs(serializer.is_valid(), True)
        self.assertEqual(
            serializer.data, {
                'username': 'John Doe',
                'balance': 123 * 100
            }
        )

    def test_validate_invalid_request_negative_balance(self):
        protobuf = Account(
            username='Jo',
            balance=-123
        )
        serializer = AccountSerializer(data=protobuf)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(serializer.errors, {
            'balance': 'Balance must be positive',
            'username': 'Username must be at least 3 characters long'
        })


if __name__ == '__main__':
    unittest.main()
