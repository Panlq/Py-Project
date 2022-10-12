
'Generated protocol buffer code.'
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.type import money_pb2 as google_dot_type_dot_money__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1epayment/v1alpha1/payment.proto\x12\x10payment.v1alpha1\x1a\x17google/type/money.proto"\xbf\x01\n\x05Order\x12\x19\n\x08order_id\x18\x01 \x01(\tR\x07orderId\x12!\n\x0crecipient_id\x18\x02 \x01(\tR\x0brecipientId\x12*\n\x06amount\x18\x03 \x01(\x0b2\x12.google.type.MoneyR\x06amount\x12L\n\x10payment_provider\x18\x04 \x01(\x0e2!.payment.v1alpha1.PaymentProviderR\x0fpaymentProvider*\x89\x01\n\x0fPaymentProvider\x12 \n\x1cPAYMENT_PROVIDER_UNSPECIFIED\x10\x00\x12\x1b\n\x17PAYMENT_PROVIDER_STRIPE\x10\x01\x12\x1b\n\x17PAYMENT_PROVIDER_PAYPAL\x10\x02\x12\x1a\n\x16PAYMENT_PROVIDER_APPLE\x10\x03B\x07Z\x05./genb\x06proto3')
_PAYMENTPROVIDER = DESCRIPTOR.enum_types_by_name['PaymentProvider']
PaymentProvider = enum_type_wrapper.EnumTypeWrapper(_PAYMENTPROVIDER)
PAYMENT_PROVIDER_UNSPECIFIED = 0
PAYMENT_PROVIDER_STRIPE = 1
PAYMENT_PROVIDER_PAYPAL = 2
PAYMENT_PROVIDER_APPLE = 3
_ORDER = DESCRIPTOR.message_types_by_name['Order']
Order = _reflection.GeneratedProtocolMessageType('Order', (_message.Message,), {'DESCRIPTOR': _ORDER, '__module__': 'payment.v1alpha1.payment_pb2'})
_sym_db.RegisterMessage(Order)
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z\x05./gen'
    _PAYMENTPROVIDER._serialized_start = 272
    _PAYMENTPROVIDER._serialized_end = 409
    _ORDER._serialized_start = 78
    _ORDER._serialized_end = 269
