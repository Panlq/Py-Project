import grpc

from api.gen.pb.pet.v1 import pet_pb2
from api.gen.pb.pet.v1 import pet_pb2_grpc

class PetStoreClient(object):
    def __init__(self, *args, **kwargs):
        self.host = "localhost"
        self.port = 50001
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.port)
        )
        self.client = pet_pb2_grpc.PetStoreServiceStub(self.channel)

    def get_pet(self, pet_id: str):
        msg = pet_pb2.GetPetRequest(pet_id=pet_id)
        print(msg)
        return self.client.GetPet(msg)


if __name__ == '__main__':
    client = PetStoreClient()
    result = client.get_pet("hello-jon")
    print(result)
