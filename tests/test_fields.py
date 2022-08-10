import unittest

from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import Account, FieldsMessage


class NestedFieldSerializer(Serializer):
    username = fields.CharField()
    balance = fields.IntField()

    class Meta:
        schema = Account


class TestFieldsSerializer(Serializer):
    int32_field = fields.IntField()
    float_field = fields.FloatField()
    # Python does not have an inbuilt double data type, but it has a float type that designates a floating-point number.
    double_field = fields.FloatField()
    bool_field = fields.BooleanField()
    string_field = fields.CharField()
    bytes_field = fields.CharField()
    nested_field = NestedFieldSerializer()
    repeated_nested_field = NestedFieldSerializer(many=True)

    class Meta:
        schema = FieldsMessage


class FieldsWithProtoTestCase(unittest.TestCase):

    def test_boolean_field(self):
        serializer = TestFieldsSerializer(
            FieldsMessage(
                bool_field=True
            )
        )
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.bool_field, True)

    def test_int_field(self):
        serializer = TestFieldsSerializer(
            FieldsMessage(
                int32_field=1
            )
        )
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.int32_field, 1)

    def test_float_field(self):
        serializer = TestFieldsSerializer(
            FieldsMessage(
                float_field=1.0
            )
        )
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.float_field, 1.0)

    def test_double_field(self):
        serializer = TestFieldsSerializer(
            FieldsMessage(
                double_field=1.0
            )
        )
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.double_field, 1.0)

    def test_string_field(self):
        serializer = TestFieldsSerializer(
            FieldsMessage(
                string_field='foo'
            )
        )
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.string_field, 'foo')

    def test_bytes_field(self):
        serializer = TestFieldsSerializer(
            FieldsMessage(
                bytes_field=b'foo'
            )
        )
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.bytes_field, b'foo')

    def test_nested_field(self):
        serializer = TestFieldsSerializer(
            FieldsMessage(
                nested_field=Account(
                    username='foo',
                    balance=1
                )
            )
        )
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.nested_field.username, 'foo')
        self.assertEqual(proto_data.nested_field.balance, 1)

    def test_repeated_nested_field(self):
        serializer = TestFieldsSerializer(
            FieldsMessage(
                repeated_nested_field=[
                    Account(
                        username='foo',
                        balance=1
                    ),
                    Account(
                        username='bar',
                        balance=2
                    )
                ]
            )
        )
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.repeated_nested_field[0].username, 'foo')
        self.assertEqual(proto_data.repeated_nested_field[0].balance, 1)
        self.assertEqual(proto_data.repeated_nested_field[1].username, 'bar')
        self.assertEqual(proto_data.repeated_nested_field[1].balance, 2)


class FieldsTestWithJsonTestCase(unittest.TestCase):

    def test_boolean_field(self):
        serializer = TestFieldsSerializer({
            'bool_field': True
        })
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.bool_field, True)

    def test_int_field(self):
        serializer = TestFieldsSerializer({
            'int32_field': 1
        })
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.int32_field, 1)

    def test_float_field(self):
        serializer = TestFieldsSerializer({
            'float_field': 1.0
        })
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.float_field, 1.0)

    def test_double_field(self):
        serializer = TestFieldsSerializer({
            'double_field': 1.0
        })
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.double_field, 1.0)

    def test_string_field(self):
        serializer = TestFieldsSerializer({
            'string_field': 'foo'
        })
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.string_field, 'foo')

    def test_bytes_field(self):
        serializer = TestFieldsSerializer({
            'bytes_field': b'foo'
        })
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.bytes_field, b'm\xfa(')

    def test_nested_field(self):
        serializer = TestFieldsSerializer({
            'nested_field': {
                'username': 'foo',
                'balance': 1
            }
        })
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.nested_field.username, 'foo')
        self.assertEqual(proto_data.nested_field.balance, 1)

    def test_repeated_nested_field(self):
        serializer = TestFieldsSerializer({
            'repeated_nested_field': [
                {
                    'username': 'foo',
                    'balance': 1
                },
                {
                    'username': 'bar',
                    'balance': 2
                }
            ]
        })
        proto_data = serializer.protobuf
        self.assertEqual(proto_data.repeated_nested_field[0].username, 'foo')
        self.assertEqual(proto_data.repeated_nested_field[0].balance, 1)
        self.assertEqual(proto_data.repeated_nested_field[1].username, 'bar')
        self.assertEqual(proto_data.repeated_nested_field[1].balance, 2)

    def test_repeated_nested_field_with_empty_list(self):
        serializer = TestFieldsSerializer({
            'repeated_nested_field': []
        })
        proto_data = serializer.protobuf
        self.assertEqual(len(proto_data.repeated_nested_field), 0)
