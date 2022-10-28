
from twirp.context import Context
from twirp.exceptions import TwirpServerException

from api.gen.pb.pet.v1 import pet_pb2
from api.gen.pb.pet.v1 import pet_twirp


client = pet_twirp.PetStoreServiceClient("http://localhost:3000")

try:
    response = client.GetPet(ctx=Context(), request=pet_pb2.GetPetRequest(pet_id="1243"))
    print(response)

except TwirpServerException as e:
    print(e.code, e.message, e.meta, e.to_dict())
