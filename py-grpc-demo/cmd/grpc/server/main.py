import grpc
from concurrent import futures

from api.gen.pb.pet.v1 import pet_pb2
from api.gen.pb.pet.v1 import pet_pb2_grpc

class PetStoreService(pet_pb2_grpc.PetStoreServiceServicer):
    def __init__(self, *args, **kwargs):
        pass

    def GetPet(self, request, context):
        print("get request", request)
        print(f'Hello I am up and running received "{request.pet_id}" message from you')
        
        return pet_pb2.GetPetResponse(pet=pet_pb2.Pet(
            name="hello jon",
            pet_id=request.pet_id,
            pet_type=pet_pb2.PET_TYPE_CAT
        ))



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pet_pb2_grpc.add_PetStoreServiceServicer_to_server(PetStoreService(), server)
    server.add_insecure_port('[::]:50001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
