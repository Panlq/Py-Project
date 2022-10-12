# -*- coding: utf-8 -*-
# Generated by https://github.com/verloop/twirpy/protoc-gen-twirpy.  DO NOT EDIT!
# source: pet/v1/pet.proto

from google.protobuf import symbol_database as _symbol_database

from twirp.base import Endpoint
from twirp.server import TwirpServer
from twirp.client import TwirpClient

_sym_db = _symbol_database.Default()

class PetStoreServiceServer(TwirpServer):

	def __init__(self, *args, service, server_path_prefix="/twirp"):
		super().__init__(service=service)
		self._prefix = F"{server_path_prefix}/pet.v1.PetStoreService"
		self._endpoints = {
			"GetPet": Endpoint(
				service_name="PetStoreService",
				name="GetPet",
				function=getattr(service, "GetPet"),
				input=_sym_db.GetSymbol("pet.v1.GetPetRequest"),
				output=_sym_db.GetSymbol("pet.v1.GetPetResponse"),
			),
			"PutPet": Endpoint(
				service_name="PetStoreService",
				name="PutPet",
				function=getattr(service, "PutPet"),
				input=_sym_db.GetSymbol("pet.v1.PutPetRequest"),
				output=_sym_db.GetSymbol("pet.v1.PutPetResponse"),
			),
			"DeletePet": Endpoint(
				service_name="PetStoreService",
				name="DeletePet",
				function=getattr(service, "DeletePet"),
				input=_sym_db.GetSymbol("pet.v1.DeletePetRequest"),
				output=_sym_db.GetSymbol("pet.v1.DeletePetResponse"),
			),
			"PurchasePet": Endpoint(
				service_name="PetStoreService",
				name="PurchasePet",
				function=getattr(service, "PurchasePet"),
				input=_sym_db.GetSymbol("pet.v1.PurchasePetRequest"),
				output=_sym_db.GetSymbol("pet.v1.PurchasePetResponse"),
			),
		}

class PetStoreServiceClient(TwirpClient):

	def GetPet(self, *args, ctx, request, server_path_prefix="/twirp", **kwargs):
		return self._make_request(
			url=F"{server_path_prefix}/pet.v1.PetStoreService/GetPet",
			ctx=ctx,
			request=request,
			response_obj=_sym_db.GetSymbol("pet.v1.GetPetResponse"),
			**kwargs,
		)

	def PutPet(self, *args, ctx, request, server_path_prefix="/twirp", **kwargs):
		return self._make_request(
			url=F"{server_path_prefix}/pet.v1.PetStoreService/PutPet",
			ctx=ctx,
			request=request,
			response_obj=_sym_db.GetSymbol("pet.v1.PutPetResponse"),
			**kwargs,
		)

	def DeletePet(self, *args, ctx, request, server_path_prefix="/twirp", **kwargs):
		return self._make_request(
			url=F"{server_path_prefix}/pet.v1.PetStoreService/DeletePet",
			ctx=ctx,
			request=request,
			response_obj=_sym_db.GetSymbol("pet.v1.DeletePetResponse"),
			**kwargs,
		)

	def PurchasePet(self, *args, ctx, request, server_path_prefix="/twirp", **kwargs):
		return self._make_request(
			url=F"{server_path_prefix}/pet.v1.PetStoreService/PurchasePet",
			ctx=ctx,
			request=request,
			response_obj=_sym_db.GetSymbol("pet.v1.PurchasePetResponse"),
			**kwargs,
		)