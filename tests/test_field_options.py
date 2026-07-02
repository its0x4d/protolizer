import unittest

from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()
    secret_token = fields.CharField(write_only=True)
    computed_label = fields.CharField(read_only=True, custom=True)

    class Meta:
        schema = Account

    @staticmethod
    def get_custom_computed_label(obj):
        return f"user:{obj.get('username', '')}"


class FieldOptionsTestCase(unittest.TestCase):
    def test_write_only_field_excluded_from_output(self):
        serializer = AccountSerializer(
            {
                "username": "John",
                "balance": 10,
                "secret_token": "abc123",
            }
        )
        self.assertEqual(serializer.data["username"], "John")
        self.assertNotIn("secret_token", serializer.data)

    def test_read_only_field_excluded_from_input_validation(self):
        serializer = AccountSerializer(
            data={
                "username": "John",
                "balance": 10,
                "computed_label": "ignored",
            }
        )
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("computed_label", serializer.validated_data)

    def test_read_only_field_included_in_output(self):
        serializer = AccountSerializer({"username": "Jane", "balance": 5})
        self.assertEqual(serializer.data["computed_label"], "user:Jane")

    def test_required_field_missing(self):
        class RequiredSerializer(Serializer):
            username = fields.CharField(required=True)
            balance = fields.IntField()

            class Meta:
                schema = Account

        serializer = RequiredSerializer(data={"balance": 1})
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_allow_null_false_rejects_none(self):
        class StrictSerializer(Serializer):
            username = fields.CharField(allow_null=False)
            balance = fields.IntField()

            class Meta:
                schema = Account

        serializer = StrictSerializer(data={"username": None, "balance": 1})
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
