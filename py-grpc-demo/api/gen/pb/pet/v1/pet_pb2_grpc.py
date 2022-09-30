"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from ...pet.v1 import pet_pb2 as pet_dot_v1_dot_pet__pb2

class PetStoreServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetPet = channel.unary_unary('/pet.v1.PetStoreService/GetPet', request_serializer=pet_dot_v1_dot_pet__pb2.GetPetRequest.SerializeToString, response_deserializer=pet_dot_v1_dot_pet__pb2.GetPetResponse.FromString)
        self.PutPet = channel.unary_unary('/pet.v1.PetStoreService/PutPet', request_serializer=pet_dot_v1_dot_pet__pb2.PutPetRequest.SerializeToString, response_deserializer=pet_dot_v1_dot_pet__pb2.PutPetResponse.FromString)
        self.DeletePet = channel.unary_unary('/pet.v1.PetStoreService/DeletePet', request_serializer=pet_dot_v1_dot_pet__pb2.DeletePetRequest.SerializeToString, response_deserializer=pet_dot_v1_dot_pet__pb2.DeletePetResponse.FromString)
        self.PurchasePet = channel.unary_unary('/pet.v1.PetStoreService/PurchasePet', request_serializer=pet_dot_v1_dot_pet__pb2.PurchasePetRequest.SerializeToString, response_deserializer=pet_dot_v1_dot_pet__pb2.PurchasePetResponse.FromString)

class PetStoreServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetPet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PutPet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeletePet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PurchasePet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_PetStoreServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'GetPet': grpc.unary_unary_rpc_method_handler(servicer.GetPet, request_deserializer=pet_dot_v1_dot_pet__pb2.GetPetRequest.FromString, response_serializer=pet_dot_v1_dot_pet__pb2.GetPetResponse.SerializeToString), 'PutPet': grpc.unary_unary_rpc_method_handler(servicer.PutPet, request_deserializer=pet_dot_v1_dot_pet__pb2.PutPetRequest.FromString, response_serializer=pet_dot_v1_dot_pet__pb2.PutPetResponse.SerializeToString), 'DeletePet': grpc.unary_unary_rpc_method_handler(servicer.DeletePet, request_deserializer=pet_dot_v1_dot_pet__pb2.DeletePetRequest.FromString, response_serializer=pet_dot_v1_dot_pet__pb2.DeletePetResponse.SerializeToString), 'PurchasePet': grpc.unary_unary_rpc_method_handler(servicer.PurchasePet, request_deserializer=pet_dot_v1_dot_pet__pb2.PurchasePetRequest.FromString, response_serializer=pet_dot_v1_dot_pet__pb2.PurchasePetResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('pet.v1.PetStoreService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class PetStoreService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetPet(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pet.v1.PetStoreService/GetPet', pet_dot_v1_dot_pet__pb2.GetPetRequest.SerializeToString, pet_dot_v1_dot_pet__pb2.GetPetResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PutPet(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pet.v1.PetStoreService/PutPet', pet_dot_v1_dot_pet__pb2.PutPetRequest.SerializeToString, pet_dot_v1_dot_pet__pb2.PutPetResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeletePet(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pet.v1.PetStoreService/DeletePet', pet_dot_v1_dot_pet__pb2.DeletePetRequest.SerializeToString, pet_dot_v1_dot_pet__pb2.DeletePetResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PurchasePet(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pet.v1.PetStoreService/PurchasePet', pet_dot_v1_dot_pet__pb2.PurchasePetRequest.SerializeToString, pet_dot_v1_dot_pet__pb2.PurchasePetResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)