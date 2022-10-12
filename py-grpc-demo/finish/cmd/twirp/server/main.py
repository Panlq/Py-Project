
from twirp.asgi import TwirpASGIApp
from twirp.exceptions import InvalidArgument

from api.gen.pb.pet.v1 import pet_pb2
from api.gen.pb.pet.v1.pet_twirp import PetStoreServiceServer


class PetStoreService(object):
    def GetPet(self, context, request):
        if len(request.pet_id) != 36:
            raise InvalidArgument(argument="pet_id", error=" must be 36 characters")
        
        return pet_pb2.GetPetResponse(pet=pet_pb2.Pet(
            name="hell jon",
            pet_id=request.pet_id,
            pet_type=pet_pb2.PET_TYPE_CAT
        ))

    def PutPet(self, context, request):
        pass

    def DeletePet(self, context, request):
        pass

    def PurchasePet(self, context, request):
        pass



service = PetStoreServiceServer(service=PetStoreService())
app = TwirpASGIApp()
app.add_service(service)

