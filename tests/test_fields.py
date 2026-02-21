import unittest
from datetime import datetime

from protolizer import Serializer, fields
from protolizer.exceptions import InvalidDataError
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
    repeated_string_field = fields.ListField(fields.CharField())
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

    def test_repeated_string_field(self):
        serializer = TestFieldsSerializer({
            'repeated_string_field': ['a', 'b', 'c']
        })
        proto_data = serializer.protobuf
        self.assertEqual(list(proto_data.repeated_string_field), ['a', 'b', 'c'])
        serializer2 = TestFieldsSerializer(proto_data)
        self.assertEqual(serializer2.data['repeated_string_field'], ['a', 'b', 'c'])


class FieldEdgeCasesTestCase(unittest.TestCase):
    """Tests for DateTimeField, TimestampField, InvalidDataError, and field defaults."""

    def test_datetime_field_roundtrip(self):
        field = fields.DateTimeField(fmt='%Y-%m-%dT%H:%M:%S')
        field.bind('created', None)
        s = '2024-01-15T12:00:00'
        internal = field.to_internal_value(s)
        self.assertIsInstance(internal, datetime)
        self.assertEqual(internal.year, 2024)
        self.assertEqual(internal.month, 1)
        self.assertEqual(internal.day, 15)
        rep = field.to_representation(internal)
        self.assertEqual(rep, s)

    def test_timestamp_field_roundtrip(self):
        field = fields.TimestampField()
        field.bind('ts', None)
        internal = field.to_internal_value(1705312800)  # 2024-01-15 12:00:00 UTC approx
        self.assertIsInstance(internal, (int, float))
        rep = field.to_representation(internal)
        self.assertIsInstance(rep, (int, float))

    def test_int_field_invalid_raises_invalid_data_error(self):
        field = fields.IntField()
        field.bind('balance', None)
        with self.assertRaises(InvalidDataError) as ctx:
            field.run_validation('not a number')
        self.assertEqual(ctx.exception.field, 'balance')
        self.assertIn('integer', str(ctx.exception.expected_type))

    def test_float_field_invalid_raises_invalid_data_error(self):
        field = fields.FloatField()
        field.bind('score', None)
        with self.assertRaises(InvalidDataError) as ctx:
            field.run_validation('not a float')
        self.assertEqual(ctx.exception.field, 'score')

    def test_boolean_field_invalid_raises_invalid_data_error(self):
        field = fields.BooleanField()
        field.bind('flag', None)
        with self.assertRaises(InvalidDataError) as ctx:
            field.run_validation('invalid_bool')
        self.assertEqual(ctx.exception.field, 'flag')

    def test_char_field_trim_whitespace(self):
        field = fields.CharField(trim_whitespace=True)
        field.bind('name', None)
        self.assertEqual(field.to_internal_value('  hello  '), 'hello')
