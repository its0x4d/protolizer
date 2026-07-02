import unittest

from protolizer import Serializer, fields
from tests.config.generated_proto.protobuf_pb2 import FieldsMessage, Status


class FieldsSerializer(Serializer):
    status_field = fields.EnumField(Status)

    class Meta:
        schema = FieldsMessage


class EnumFieldTestCase(unittest.TestCase):
    def test_enum_from_protobuf(self):
        serializer = FieldsSerializer(FieldsMessage(status_field=Status.ACTIVE))
        self.assertEqual(serializer.data["status_field"], Status.ACTIVE)
        self.assertEqual(serializer.protobuf.status_field, Status.ACTIVE)

    def test_enum_from_int_json(self):
        serializer = FieldsSerializer({"status_field": Status.INACTIVE})
        self.assertEqual(serializer.protobuf.status_field, Status.INACTIVE)

    def test_enum_from_name_json(self):
        serializer = FieldsSerializer({"status_field": "ACTIVE"})
        self.assertEqual(serializer.protobuf.status_field, Status.ACTIVE)

    def test_enum_by_name_representation(self):
        class NamedEnumSerializer(Serializer):
            status_field = fields.EnumField(Status, by_name=True)

            class Meta:
                schema = FieldsMessage

        serializer = NamedEnumSerializer(FieldsMessage(status_field=Status.ACTIVE))
        self.assertEqual(serializer.data["status_field"], "ACTIVE")

    def test_enum_invalid_value_raises_on_validation(self):
        serializer = FieldsSerializer(data={"status_field": "NOT_A_STATUS"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("status_field", serializer.errors)
