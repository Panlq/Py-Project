"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17validate/validate.proto\x12\x08validate\x1a google/protobuf/descriptor.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xc8\x08\n\nFieldRules\x120\n\x07message\x18\x11 \x01(\x0b2\x16.validate.MessageRulesR\x07message\x12,\n\x05float\x18\x01 \x01(\x0b2\x14.validate.FloatRulesH\x00R\x05float\x12/\n\x06double\x18\x02 \x01(\x0b2\x15.validate.DoubleRulesH\x00R\x06double\x12,\n\x05int32\x18\x03 \x01(\x0b2\x14.validate.Int32RulesH\x00R\x05int32\x12,\n\x05int64\x18\x04 \x01(\x0b2\x14.validate.Int64RulesH\x00R\x05int64\x12/\n\x06uint32\x18\x05 \x01(\x0b2\x15.validate.UInt32RulesH\x00R\x06uint32\x12/\n\x06uint64\x18\x06 \x01(\x0b2\x15.validate.UInt64RulesH\x00R\x06uint64\x12/\n\x06sint32\x18\x07 \x01(\x0b2\x15.validate.SInt32RulesH\x00R\x06sint32\x12/\n\x06sint64\x18\x08 \x01(\x0b2\x15.validate.SInt64RulesH\x00R\x06sint64\x122\n\x07fixed32\x18\t \x01(\x0b2\x16.validate.Fixed32RulesH\x00R\x07fixed32\x122\n\x07fixed64\x18\n \x01(\x0b2\x16.validate.Fixed64RulesH\x00R\x07fixed64\x125\n\x08sfixed32\x18\x0b \x01(\x0b2\x17.validate.SFixed32RulesH\x00R\x08sfixed32\x125\n\x08sfixed64\x18\x0c \x01(\x0b2\x17.validate.SFixed64RulesH\x00R\x08sfixed64\x12)\n\x04bool\x18\r \x01(\x0b2\x13.validate.BoolRulesH\x00R\x04bool\x12/\n\x06string\x18\x0e \x01(\x0b2\x15.validate.StringRulesH\x00R\x06string\x12,\n\x05bytes\x18\x0f \x01(\x0b2\x14.validate.BytesRulesH\x00R\x05bytes\x12)\n\x04enum\x18\x10 \x01(\x0b2\x13.validate.EnumRulesH\x00R\x04enum\x125\n\x08repeated\x18\x12 \x01(\x0b2\x17.validate.RepeatedRulesH\x00R\x08repeated\x12&\n\x03map\x18\x13 \x01(\x0b2\x12.validate.MapRulesH\x00R\x03map\x12&\n\x03any\x18\x14 \x01(\x0b2\x12.validate.AnyRulesH\x00R\x03any\x125\n\x08duration\x18\x15 \x01(\x0b2\x17.validate.DurationRulesH\x00R\x08duration\x128\n\ttimestamp\x18\x16 \x01(\x0b2\x18.validate.TimestampRulesH\x00R\ttimestampB\x06\n\x04type"\xb0\x01\n\nFloatRules\x12\x14\n\x05const\x18\x01 \x01(\x02R\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x02R\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x02R\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x02R\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x02R\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x02R\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x02R\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb1\x01\n\x0bDoubleRules\x12\x14\n\x05const\x18\x01 \x01(\x01R\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x01R\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x01R\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x01R\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x01R\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x01R\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x01R\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb0\x01\n\nInt32Rules\x12\x14\n\x05const\x18\x01 \x01(\x05R\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x05R\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x05R\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x05R\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x05R\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x05R\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x05R\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb0\x01\n\nInt64Rules\x12\x14\n\x05const\x18\x01 \x01(\x03R\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x03R\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x03R\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x03R\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x03R\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x03R\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x03R\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb1\x01\n\x0bUInt32Rules\x12\x14\n\x05const\x18\x01 \x01(\rR\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\rR\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\rR\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\rR\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\rR\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\rR\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\rR\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb1\x01\n\x0bUInt64Rules\x12\x14\n\x05const\x18\x01 \x01(\x04R\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x04R\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x04R\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x04R\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x04R\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x04R\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x04R\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb1\x01\n\x0bSInt32Rules\x12\x14\n\x05const\x18\x01 \x01(\x11R\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x11R\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x11R\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x11R\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x11R\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x11R\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x11R\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb1\x01\n\x0bSInt64Rules\x12\x14\n\x05const\x18\x01 \x01(\x12R\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x12R\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x12R\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x12R\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x12R\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x12R\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x12R\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb2\x01\n\x0cFixed32Rules\x12\x14\n\x05const\x18\x01 \x01(\x07R\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x07R\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x07R\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x07R\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x07R\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x07R\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x07R\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb2\x01\n\x0cFixed64Rules\x12\x14\n\x05const\x18\x01 \x01(\x06R\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x06R\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x06R\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x06R\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x06R\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x06R\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x06R\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb3\x01\n\rSFixed32Rules\x12\x14\n\x05const\x18\x01 \x01(\x0fR\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x0fR\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x0fR\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x0fR\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x0fR\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x0fR\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x0fR\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"\xb3\x01\n\rSFixed64Rules\x12\x14\n\x05const\x18\x01 \x01(\x10R\x05const\x12\x0e\n\x02lt\x18\x02 \x01(\x10R\x02lt\x12\x10\n\x03lte\x18\x03 \x01(\x10R\x03lte\x12\x0e\n\x02gt\x18\x04 \x01(\x10R\x02gt\x12\x10\n\x03gte\x18\x05 \x01(\x10R\x03gte\x12\x0e\n\x02in\x18\x06 \x03(\x10R\x02in\x12\x15\n\x06not_in\x18\x07 \x03(\x10R\x05notIn\x12!\n\x0cignore_empty\x18\x08 \x01(\x08R\x0bignoreEmpty"!\n\tBoolRules\x12\x14\n\x05const\x18\x01 \x01(\x08R\x05const"\xd4\x05\n\x0bStringRules\x12\x14\n\x05const\x18\x01 \x01(\tR\x05const\x12\x10\n\x03len\x18\x13 \x01(\x04R\x03len\x12\x17\n\x07min_len\x18\x02 \x01(\x04R\x06minLen\x12\x17\n\x07max_len\x18\x03 \x01(\x04R\x06maxLen\x12\x1b\n\tlen_bytes\x18\x14 \x01(\x04R\x08lenBytes\x12\x1b\n\tmin_bytes\x18\x04 \x01(\x04R\x08minBytes\x12\x1b\n\tmax_bytes\x18\x05 \x01(\x04R\x08maxBytes\x12\x18\n\x07pattern\x18\x06 \x01(\tR\x07pattern\x12\x16\n\x06prefix\x18\x07 \x01(\tR\x06prefix\x12\x16\n\x06suffix\x18\x08 \x01(\tR\x06suffix\x12\x1a\n\x08contains\x18\t \x01(\tR\x08contains\x12!\n\x0cnot_contains\x18\x17 \x01(\tR\x0bnotContains\x12\x0e\n\x02in\x18\n \x03(\tR\x02in\x12\x15\n\x06not_in\x18\x0b \x03(\tR\x05notIn\x12\x16\n\x05email\x18\x0c \x01(\x08H\x00R\x05email\x12\x1c\n\x08hostname\x18\r \x01(\x08H\x00R\x08hostname\x12\x10\n\x02ip\x18\x0e \x01(\x08H\x00R\x02ip\x12\x14\n\x04ipv4\x18\x0f \x01(\x08H\x00R\x04ipv4\x12\x14\n\x04ipv6\x18\x10 \x01(\x08H\x00R\x04ipv6\x12\x12\n\x03uri\x18\x11 \x01(\x08H\x00R\x03uri\x12\x19\n\x07uri_ref\x18\x12 \x01(\x08H\x00R\x06uriRef\x12\x1a\n\x07address\x18\x15 \x01(\x08H\x00R\x07address\x12\x14\n\x04uuid\x18\x16 \x01(\x08H\x00R\x04uuid\x12@\n\x10well_known_regex\x18\x18 \x01(\x0e2\x14.validate.KnownRegexH\x00R\x0ewellKnownRegex\x12\x1c\n\x06strict\x18\x19 \x01(\x08:\x04trueR\x06strict\x12!\n\x0cignore_empty\x18\x1a \x01(\x08R\x0bignoreEmptyB\x0c\n\nwell_known"\xe2\x02\n\nBytesRules\x12\x14\n\x05const\x18\x01 \x01(\x0cR\x05const\x12\x10\n\x03len\x18\r \x01(\x04R\x03len\x12\x17\n\x07min_len\x18\x02 \x01(\x04R\x06minLen\x12\x17\n\x07max_len\x18\x03 \x01(\x04R\x06maxLen\x12\x18\n\x07pattern\x18\x04 \x01(\tR\x07pattern\x12\x16\n\x06prefix\x18\x05 \x01(\x0cR\x06prefix\x12\x16\n\x06suffix\x18\x06 \x01(\x0cR\x06suffix\x12\x1a\n\x08contains\x18\x07 \x01(\x0cR\x08contains\x12\x0e\n\x02in\x18\x08 \x03(\x0cR\x02in\x12\x15\n\x06not_in\x18\t \x03(\x0cR\x05notIn\x12\x10\n\x02ip\x18\n \x01(\x08H\x00R\x02ip\x12\x14\n\x04ipv4\x18\x0b \x01(\x08H\x00R\x04ipv4\x12\x14\n\x04ipv6\x18\x0c \x01(\x08H\x00R\x04ipv6\x12!\n\x0cignore_empty\x18\x0e \x01(\x08R\x0bignoreEmptyB\x0c\n\nwell_known"k\n\tEnumRules\x12\x14\n\x05const\x18\x01 \x01(\x05R\x05const\x12!\n\x0cdefined_only\x18\x02 \x01(\x08R\x0bdefinedOnly\x12\x0e\n\x02in\x18\x03 \x03(\x05R\x02in\x12\x15\n\x06not_in\x18\x04 \x03(\x05R\x05notIn">\n\x0cMessageRules\x12\x12\n\x04skip\x18\x01 \x01(\x08R\x04skip\x12\x1a\n\x08required\x18\x02 \x01(\x08R\x08required"\xb0\x01\n\rRepeatedRules\x12\x1b\n\tmin_items\x18\x01 \x01(\x04R\x08minItems\x12\x1b\n\tmax_items\x18\x02 \x01(\x04R\x08maxItems\x12\x16\n\x06unique\x18\x03 \x01(\x08R\x06unique\x12*\n\x05items\x18\x04 \x01(\x0b2\x14.validate.FieldRulesR\x05items\x12!\n\x0cignore_empty\x18\x05 \x01(\x08R\x0bignoreEmpty"\xdc\x01\n\x08MapRules\x12\x1b\n\tmin_pairs\x18\x01 \x01(\x04R\x08minPairs\x12\x1b\n\tmax_pairs\x18\x02 \x01(\x04R\x08maxPairs\x12\x1b\n\tno_sparse\x18\x03 \x01(\x08R\x08noSparse\x12(\n\x04keys\x18\x04 \x01(\x0b2\x14.validate.FieldRulesR\x04keys\x12,\n\x06values\x18\x05 \x01(\x0b2\x14.validate.FieldRulesR\x06values\x12!\n\x0cignore_empty\x18\x06 \x01(\x08R\x0bignoreEmpty"M\n\x08AnyRules\x12\x1a\n\x08required\x18\x01 \x01(\x08R\x08required\x12\x0e\n\x02in\x18\x02 \x03(\tR\x02in\x12\x15\n\x06not_in\x18\x03 \x03(\tR\x05notIn"\xe9\x02\n\rDurationRules\x12\x1a\n\x08required\x18\x01 \x01(\x08R\x08required\x12/\n\x05const\x18\x02 \x01(\x0b2\x19.google.protobuf.DurationR\x05const\x12)\n\x02lt\x18\x03 \x01(\x0b2\x19.google.protobuf.DurationR\x02lt\x12+\n\x03lte\x18\x04 \x01(\x0b2\x19.google.protobuf.DurationR\x03lte\x12)\n\x02gt\x18\x05 \x01(\x0b2\x19.google.protobuf.DurationR\x02gt\x12+\n\x03gte\x18\x06 \x01(\x0b2\x19.google.protobuf.DurationR\x03gte\x12)\n\x02in\x18\x07 \x03(\x0b2\x19.google.protobuf.DurationR\x02in\x120\n\x06not_in\x18\x08 \x03(\x0b2\x19.google.protobuf.DurationR\x05notIn"\xf3\x02\n\x0eTimestampRules\x12\x1a\n\x08required\x18\x01 \x01(\x08R\x08required\x120\n\x05const\x18\x02 \x01(\x0b2\x1a.google.protobuf.TimestampR\x05const\x12*\n\x02lt\x18\x03 \x01(\x0b2\x1a.google.protobuf.TimestampR\x02lt\x12,\n\x03lte\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampR\x03lte\x12*\n\x02gt\x18\x05 \x01(\x0b2\x1a.google.protobuf.TimestampR\x02gt\x12,\n\x03gte\x18\x06 \x01(\x0b2\x1a.google.protobuf.TimestampR\x03gte\x12\x15\n\x06lt_now\x18\x07 \x01(\x08R\x05ltNow\x12\x15\n\x06gt_now\x18\x08 \x01(\x08R\x05gtNow\x121\n\x06within\x18\t \x01(\x0b2\x19.google.protobuf.DurationR\x06within*F\n\nKnownRegex\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x14\n\x10HTTP_HEADER_NAME\x10\x01\x12\x15\n\x11HTTP_HEADER_VALUE\x10\x02:<\n\x08disabled\x12\x1f.google.protobuf.MessageOptions\x18\xaf\x08 \x01(\x08R\x08disabled::\n\x07ignored\x12\x1f.google.protobuf.MessageOptions\x18\xb0\x08 \x01(\x08R\x07ignored::\n\x08required\x12\x1d.google.protobuf.OneofOptions\x18\xaf\x08 \x01(\x08R\x08required:J\n\x05rules\x12\x1d.google.protobuf.FieldOptions\x18\xaf\x08 \x01(\x0b2\x14.validate.FieldRulesR\x05rulesBP\n\x1aio.envoyproxy.pgv.validateZ2github.com/envoyproxy/protoc-gen-validate/validate')
_KNOWNREGEX = DESCRIPTOR.enum_types_by_name['KnownRegex']
KnownRegex = enum_type_wrapper.EnumTypeWrapper(_KNOWNREGEX)
UNKNOWN = 0
HTTP_HEADER_NAME = 1
HTTP_HEADER_VALUE = 2
DISABLED_FIELD_NUMBER = 1071
disabled = DESCRIPTOR.extensions_by_name['disabled']
IGNORED_FIELD_NUMBER = 1072
ignored = DESCRIPTOR.extensions_by_name['ignored']
REQUIRED_FIELD_NUMBER = 1071
required = DESCRIPTOR.extensions_by_name['required']
RULES_FIELD_NUMBER = 1071
rules = DESCRIPTOR.extensions_by_name['rules']
_FIELDRULES = DESCRIPTOR.message_types_by_name['FieldRules']
_FLOATRULES = DESCRIPTOR.message_types_by_name['FloatRules']
_DOUBLERULES = DESCRIPTOR.message_types_by_name['DoubleRules']
_INT32RULES = DESCRIPTOR.message_types_by_name['Int32Rules']
_INT64RULES = DESCRIPTOR.message_types_by_name['Int64Rules']
_UINT32RULES = DESCRIPTOR.message_types_by_name['UInt32Rules']
_UINT64RULES = DESCRIPTOR.message_types_by_name['UInt64Rules']
_SINT32RULES = DESCRIPTOR.message_types_by_name['SInt32Rules']
_SINT64RULES = DESCRIPTOR.message_types_by_name['SInt64Rules']
_FIXED32RULES = DESCRIPTOR.message_types_by_name['Fixed32Rules']
_FIXED64RULES = DESCRIPTOR.message_types_by_name['Fixed64Rules']
_SFIXED32RULES = DESCRIPTOR.message_types_by_name['SFixed32Rules']
_SFIXED64RULES = DESCRIPTOR.message_types_by_name['SFixed64Rules']
_BOOLRULES = DESCRIPTOR.message_types_by_name['BoolRules']
_STRINGRULES = DESCRIPTOR.message_types_by_name['StringRules']
_BYTESRULES = DESCRIPTOR.message_types_by_name['BytesRules']
_ENUMRULES = DESCRIPTOR.message_types_by_name['EnumRules']
_MESSAGERULES = DESCRIPTOR.message_types_by_name['MessageRules']
_REPEATEDRULES = DESCRIPTOR.message_types_by_name['RepeatedRules']
_MAPRULES = DESCRIPTOR.message_types_by_name['MapRules']
_ANYRULES = DESCRIPTOR.message_types_by_name['AnyRules']
_DURATIONRULES = DESCRIPTOR.message_types_by_name['DurationRules']
_TIMESTAMPRULES = DESCRIPTOR.message_types_by_name['TimestampRules']
FieldRules = _reflection.GeneratedProtocolMessageType('FieldRules', (_message.Message,), {'DESCRIPTOR': _FIELDRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(FieldRules)
FloatRules = _reflection.GeneratedProtocolMessageType('FloatRules', (_message.Message,), {'DESCRIPTOR': _FLOATRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(FloatRules)
DoubleRules = _reflection.GeneratedProtocolMessageType('DoubleRules', (_message.Message,), {'DESCRIPTOR': _DOUBLERULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(DoubleRules)
Int32Rules = _reflection.GeneratedProtocolMessageType('Int32Rules', (_message.Message,), {'DESCRIPTOR': _INT32RULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(Int32Rules)
Int64Rules = _reflection.GeneratedProtocolMessageType('Int64Rules', (_message.Message,), {'DESCRIPTOR': _INT64RULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(Int64Rules)
UInt32Rules = _reflection.GeneratedProtocolMessageType('UInt32Rules', (_message.Message,), {'DESCRIPTOR': _UINT32RULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(UInt32Rules)
UInt64Rules = _reflection.GeneratedProtocolMessageType('UInt64Rules', (_message.Message,), {'DESCRIPTOR': _UINT64RULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(UInt64Rules)
SInt32Rules = _reflection.GeneratedProtocolMessageType('SInt32Rules', (_message.Message,), {'DESCRIPTOR': _SINT32RULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(SInt32Rules)
SInt64Rules = _reflection.GeneratedProtocolMessageType('SInt64Rules', (_message.Message,), {'DESCRIPTOR': _SINT64RULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(SInt64Rules)
Fixed32Rules = _reflection.GeneratedProtocolMessageType('Fixed32Rules', (_message.Message,), {'DESCRIPTOR': _FIXED32RULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(Fixed32Rules)
Fixed64Rules = _reflection.GeneratedProtocolMessageType('Fixed64Rules', (_message.Message,), {'DESCRIPTOR': _FIXED64RULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(Fixed64Rules)
SFixed32Rules = _reflection.GeneratedProtocolMessageType('SFixed32Rules', (_message.Message,), {'DESCRIPTOR': _SFIXED32RULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(SFixed32Rules)
SFixed64Rules = _reflection.GeneratedProtocolMessageType('SFixed64Rules', (_message.Message,), {'DESCRIPTOR': _SFIXED64RULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(SFixed64Rules)
BoolRules = _reflection.GeneratedProtocolMessageType('BoolRules', (_message.Message,), {'DESCRIPTOR': _BOOLRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(BoolRules)
StringRules = _reflection.GeneratedProtocolMessageType('StringRules', (_message.Message,), {'DESCRIPTOR': _STRINGRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(StringRules)
BytesRules = _reflection.GeneratedProtocolMessageType('BytesRules', (_message.Message,), {'DESCRIPTOR': _BYTESRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(BytesRules)
EnumRules = _reflection.GeneratedProtocolMessageType('EnumRules', (_message.Message,), {'DESCRIPTOR': _ENUMRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(EnumRules)
MessageRules = _reflection.GeneratedProtocolMessageType('MessageRules', (_message.Message,), {'DESCRIPTOR': _MESSAGERULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(MessageRules)
RepeatedRules = _reflection.GeneratedProtocolMessageType('RepeatedRules', (_message.Message,), {'DESCRIPTOR': _REPEATEDRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(RepeatedRules)
MapRules = _reflection.GeneratedProtocolMessageType('MapRules', (_message.Message,), {'DESCRIPTOR': _MAPRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(MapRules)
AnyRules = _reflection.GeneratedProtocolMessageType('AnyRules', (_message.Message,), {'DESCRIPTOR': _ANYRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(AnyRules)
DurationRules = _reflection.GeneratedProtocolMessageType('DurationRules', (_message.Message,), {'DESCRIPTOR': _DURATIONRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(DurationRules)
TimestampRules = _reflection.GeneratedProtocolMessageType('TimestampRules', (_message.Message,), {'DESCRIPTOR': _TIMESTAMPRULES, '__module__': 'validate.validate_pb2'})
_sym_db.RegisterMessage(TimestampRules)
if _descriptor._USE_C_DESCRIPTORS == False:
    google_dot_protobuf_dot_descriptor__pb2.MessageOptions.RegisterExtension(disabled)
    google_dot_protobuf_dot_descriptor__pb2.MessageOptions.RegisterExtension(ignored)
    google_dot_protobuf_dot_descriptor__pb2.OneofOptions.RegisterExtension(required)
    google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(rules)
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x1aio.envoyproxy.pgv.validateZ2github.com/envoyproxy/protoc-gen-validate/validate'
    _KNOWNREGEX._serialized_start = 5909
    _KNOWNREGEX._serialized_end = 5979
    _FIELDRULES._serialized_start = 137
    _FIELDRULES._serialized_end = 1233
    _FLOATRULES._serialized_start = 1236
    _FLOATRULES._serialized_end = 1412
    _DOUBLERULES._serialized_start = 1415
    _DOUBLERULES._serialized_end = 1592
    _INT32RULES._serialized_start = 1595
    _INT32RULES._serialized_end = 1771
    _INT64RULES._serialized_start = 1774
    _INT64RULES._serialized_end = 1950
    _UINT32RULES._serialized_start = 1953
    _UINT32RULES._serialized_end = 2130
    _UINT64RULES._serialized_start = 2133
    _UINT64RULES._serialized_end = 2310
    _SINT32RULES._serialized_start = 2313
    _SINT32RULES._serialized_end = 2490
    _SINT64RULES._serialized_start = 2493
    _SINT64RULES._serialized_end = 2670
    _FIXED32RULES._serialized_start = 2673
    _FIXED32RULES._serialized_end = 2851
    _FIXED64RULES._serialized_start = 2854
    _FIXED64RULES._serialized_end = 3032
    _SFIXED32RULES._serialized_start = 3035
    _SFIXED32RULES._serialized_end = 3214
    _SFIXED64RULES._serialized_start = 3217
    _SFIXED64RULES._serialized_end = 3396
    _BOOLRULES._serialized_start = 3398
    _BOOLRULES._serialized_end = 3431
    _STRINGRULES._serialized_start = 3434
    _STRINGRULES._serialized_end = 4158
    _BYTESRULES._serialized_start = 4161
    _BYTESRULES._serialized_end = 4515
    _ENUMRULES._serialized_start = 4517
    _ENUMRULES._serialized_end = 4624
    _MESSAGERULES._serialized_start = 4626
    _MESSAGERULES._serialized_end = 4688
    _REPEATEDRULES._serialized_start = 4691
    _REPEATEDRULES._serialized_end = 4867
    _MAPRULES._serialized_start = 4870
    _MAPRULES._serialized_end = 5090
    _ANYRULES._serialized_start = 5092
    _ANYRULES._serialized_end = 5169
    _DURATIONRULES._serialized_start = 5172
    _DURATIONRULES._serialized_end = 5533
    _TIMESTAMPRULES._serialized_start = 5536
    _TIMESTAMPRULES._serialized_end = 5907