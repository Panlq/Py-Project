
'Generated protocol buffer code.'
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ...validate import validate_pb2 as validate_dot_validate__pb2
from google.type import datetime_pb2 as google_dot_type_dot_datetime__pb2
from ...payment.v1alpha1 import payment_pb2 as payment_dot_v1alpha1_dot_payment__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10pet/v1/pet.proto\x12\x06pet.v1\x1a\x17validate/validate.proto\x1a\x1agoogle/type/datetime.proto\x1a\x1epayment/v1alpha1/payment.proto"Z\n\x12PurchasePetRequest\x12\x15\n\x06pet_id\x18\x01 \x01(\tR\x05petId\x12-\n\x05order\x18\x02 \x01(\x0b2\x17.payment.v1alpha1.OrderR\x05order"\x15\n\x13PurchasePetResponse"\x9c\x01\n\x03Pet\x12*\n\x08pet_type\x18\x01 \x01(\x0e2\x0f.pet.v1.PetTypeR\x07petType\x12\x1f\n\x06pet_id\x18\x02 \x01(\tB\x08\xfaB\x05r\x03\x98\x01$R\x05petId\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x124\n\ncreated_at\x18\x04 \x01(\x0b2\x15.google.type.DateTimeR\tcreatedAt"&\n\rGetPetRequest\x12\x15\n\x06pet_id\x18\x01 \x01(\tR\x05petId"/\n\x0eGetPetResponse\x12\x1d\n\x03pet\x18\x01 \x01(\x0b2\x0b.pet.v1.PetR\x03pet"O\n\rPutPetRequest\x12*\n\x08pet_type\x18\x01 \x01(\x0e2\x0f.pet.v1.PetTypeR\x07petType\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name"/\n\x0ePutPetResponse\x12\x1d\n\x03pet\x18\x01 \x01(\x0b2\x0b.pet.v1.PetR\x03pet")\n\x10DeletePetRequest\x12\x15\n\x06pet_id\x18\x01 \x01(\tR\x05petId"\x13\n\x11DeletePetResponse*q\n\x07PetType\x12\x18\n\x14PET_TYPE_UNSPECIFIED\x10\x00\x12\x10\n\x0cPET_TYPE_CAT\x10\x01\x12\x10\n\x0cPET_TYPE_DOG\x10\x02\x12\x12\n\x0ePET_TYPE_SNAKE\x10\x03\x12\x14\n\x10PET_TYPE_HAMSTER\x10\x042\x95\x02\n\x0fPetStoreService\x129\n\x06GetPet\x12\x15.pet.v1.GetPetRequest\x1a\x16.pet.v1.GetPetResponse"\x00\x129\n\x06PutPet\x12\x15.pet.v1.PutPetRequest\x1a\x16.pet.v1.PutPetResponse"\x00\x12B\n\tDeletePet\x12\x18.pet.v1.DeletePetRequest\x1a\x19.pet.v1.DeletePetResponse"\x00\x12H\n\x0bPurchasePet\x12\x1a.pet.v1.PurchasePetRequest\x1a\x1b.pet.v1.PurchasePetResponse"\x00B\x07Z\x05./genb\x06proto3')
_PETTYPE = DESCRIPTOR.enum_types_by_name['PetType']
PetType = enum_type_wrapper.EnumTypeWrapper(_PETTYPE)
PET_TYPE_UNSPECIFIED = 0
PET_TYPE_CAT = 1
PET_TYPE_DOG = 2
PET_TYPE_SNAKE = 3
PET_TYPE_HAMSTER = 4
_PURCHASEPETREQUEST = DESCRIPTOR.message_types_by_name['PurchasePetRequest']
_PURCHASEPETRESPONSE = DESCRIPTOR.message_types_by_name['PurchasePetResponse']
_PET = DESCRIPTOR.message_types_by_name['Pet']
_GETPETREQUEST = DESCRIPTOR.message_types_by_name['GetPetRequest']
_GETPETRESPONSE = DESCRIPTOR.message_types_by_name['GetPetResponse']
_PUTPETREQUEST = DESCRIPTOR.message_types_by_name['PutPetRequest']
_PUTPETRESPONSE = DESCRIPTOR.message_types_by_name['PutPetResponse']
_DELETEPETREQUEST = DESCRIPTOR.message_types_by_name['DeletePetRequest']
_DELETEPETRESPONSE = DESCRIPTOR.message_types_by_name['DeletePetResponse']
PurchasePetRequest = _reflection.GeneratedProtocolMessageType('PurchasePetRequest', (_message.Message,), {'DESCRIPTOR': _PURCHASEPETREQUEST, '__module__': 'pet.v1.pet_pb2'})
_sym_db.RegisterMessage(PurchasePetRequest)
PurchasePetResponse = _reflection.GeneratedProtocolMessageType('PurchasePetResponse', (_message.Message,), {'DESCRIPTOR': _PURCHASEPETRESPONSE, '__module__': 'pet.v1.pet_pb2'})
_sym_db.RegisterMessage(PurchasePetResponse)
Pet = _reflection.GeneratedProtocolMessageType('Pet', (_message.Message,), {'DESCRIPTOR': _PET, '__module__': 'pet.v1.pet_pb2'})
_sym_db.RegisterMessage(Pet)
GetPetRequest = _reflection.GeneratedProtocolMessageType('GetPetRequest', (_message.Message,), {'DESCRIPTOR': _GETPETREQUEST, '__module__': 'pet.v1.pet_pb2'})
_sym_db.RegisterMessage(GetPetRequest)
GetPetResponse = _reflection.GeneratedProtocolMessageType('GetPetResponse', (_message.Message,), {'DESCRIPTOR': _GETPETRESPONSE, '__module__': 'pet.v1.pet_pb2'})
_sym_db.RegisterMessage(GetPetResponse)
PutPetRequest = _reflection.GeneratedProtocolMessageType('PutPetRequest', (_message.Message,), {'DESCRIPTOR': _PUTPETREQUEST, '__module__': 'pet.v1.pet_pb2'})
_sym_db.RegisterMessage(PutPetRequest)
PutPetResponse = _reflection.GeneratedProtocolMessageType('PutPetResponse', (_message.Message,), {'DESCRIPTOR': _PUTPETRESPONSE, '__module__': 'pet.v1.pet_pb2'})
_sym_db.RegisterMessage(PutPetResponse)
DeletePetRequest = _reflection.GeneratedProtocolMessageType('DeletePetRequest', (_message.Message,), {'DESCRIPTOR': _DELETEPETREQUEST, '__module__': 'pet.v1.pet_pb2'})
_sym_db.RegisterMessage(DeletePetRequest)
DeletePetResponse = _reflection.GeneratedProtocolMessageType('DeletePetResponse', (_message.Message,), {'DESCRIPTOR': _DELETEPETRESPONSE, '__module__': 'pet.v1.pet_pb2'})
_sym_db.RegisterMessage(DeletePetResponse)
_PETSTORESERVICE = DESCRIPTOR.services_by_name['PetStoreService']
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z\x05./gen'
    _PET.fields_by_name['pet_id']._options = None
    _PET.fields_by_name['pet_id']._serialized_options = b'\xfaB\x05r\x03\x98\x01$'
    _PETTYPE._serialized_start = 670
    _PETTYPE._serialized_end = 783
    _PURCHASEPETREQUEST._serialized_start = 113
    _PURCHASEPETREQUEST._serialized_end = 203
    _PURCHASEPETRESPONSE._serialized_start = 205
    _PURCHASEPETRESPONSE._serialized_end = 226
    _PET._serialized_start = 229
    _PET._serialized_end = 385
    _GETPETREQUEST._serialized_start = 387
    _GETPETREQUEST._serialized_end = 425
    _GETPETRESPONSE._serialized_start = 427
    _GETPETRESPONSE._serialized_end = 474
    _PUTPETREQUEST._serialized_start = 476
    _PUTPETREQUEST._serialized_end = 555
    _PUTPETRESPONSE._serialized_start = 557
    _PUTPETRESPONSE._serialized_end = 604
    _DELETEPETREQUEST._serialized_start = 606
    _DELETEPETREQUEST._serialized_end = 647
    _DELETEPETRESPONSE._serialized_start = 649
    _DELETEPETRESPONSE._serialized_end = 668
    _PETSTORESERVICE._serialized_start = 786
    _PETSTORESERVICE._serialized_end = 1063
