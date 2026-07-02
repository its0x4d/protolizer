import unittest

from protolizer import Serializer, ValidationError, fields
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()

    class Meta:
        schema = Account

    @staticmethod
    def validate_balance(value):
        if value < 0:
            raise ValidationError("Balance must be positive")
        return value * 100

    @staticmethod
    def validate_username(value):
        if len(value) < 3:
            raise ValidationError("Username must be at least 3 characters long")
        return value


class ValidationRegressionTestCase(unittest.TestCase):
    def test_read_path_skips_validate_hooks(self):
        protobuf = Account(username="John Doe", balance=123)
        serializer = AccountSerializer(protobuf)
        self.assertEqual(
            serializer.data,
            {
                "username": "John Doe",
                "balance": 123,
            },
        )

    def test_invalid_data_error_surfaces_in_is_valid(self):
        serializer = AccountSerializer(data={"username": "John", "balance": "not-a-number"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("balance", serializer.errors)

    def test_validate_hook_receives_validated_value(self):
        class TrimSerializer(Serializer):
            username = fields.CharField(trim_whitespace=True)

            class Meta:
                schema = Account

            @staticmethod
            def validate_username(value):
                assert value == "John"
                return value

        serializer = TrimSerializer(data={"username": "  John  ", "balance": 1})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["username"], "John")
