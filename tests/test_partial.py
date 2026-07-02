import unittest

from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account


class AccountSerializer(Serializer):
    username = fields.CharField(required=True)
    balance = fields.IntField(required=True)

    class Meta:
        schema = Account


class PartialUpdateTestCase(unittest.TestCase):
    def test_partial_skips_missing_required_fields(self):
        serializer = AccountSerializer(data={"username": "John"}, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {"username": "John"})

    def test_partial_false_requires_all_fields(self):
        serializer = AccountSerializer(data={"username": "John"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("balance", serializer.errors)

    def test_partial_update_protobuf(self):
        serializer = AccountSerializer(data={"balance": 200}, partial=True)
        self.assertTrue(serializer.is_valid())
        proto = serializer.protobuf
        self.assertEqual(proto.balance, 200)
