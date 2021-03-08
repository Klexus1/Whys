from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from django.core.exceptions import FieldError

from core.serializers import *
from core.models import *
from core import serializers


class ImportDataView(APIView):
    """
    Api endpoint that allows products to be imported
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        errors = []  # logs errors if needed
        records_that_couldnt_be_executed = []  # records that couldn't be executed in first two iterations
        models = apps.get_app_config('core').get_models().gi_frame.f_locals["self"].models  # get all available models
        model_names = []  # stores model names
        for i in range(0, len(list(models.items()))):
            model_names.append(str(list(models.items())[i][0]))
        available_serializers = []  # stores serializer names
        for name, obj in inspect.getmembers(serializers):
            if inspect.isclass(obj) and "Serializer" in name:
                for model_name in model_names:
                    if model_name in name.lower():
                        available_serializers.append((name, obj))
        available_serializers = list(set(available_serializers))
        data = request.data
        for ii in range(0, 3):
            """
            the for loop iterates over the records 3 times
            
            it does so as some records come before those they actually reference via FK relationships and wouldn't be 
            otherwise handled
            """
            if ii in [1, 2]:
                if not records_that_couldnt_be_executed:
                    """ if all records handled earlier, exit"""
                    return Response({"message": "Import successful."},
                                    status=status.HTTP_201_CREATED)
                data = records_that_couldnt_be_executed
                records_that_couldnt_be_executed = []
            for record in data:
                """ checks if record's key (model name) is valid """
                if list(record.keys())[0].lower() not in model_names:
                    return Response({"message": f"Model {list(record.keys())[0]} not supported."},
                                    status=status.HTTP_400_BAD_REQUEST)
                try:
                    the_model_name = list(record.keys())[0]
                    try:
                        the_serializer = None
                        for serializer in available_serializers:
                            """
                            checks if app has a serializer for the model in question (assumes naming conventions are stuck to; "ModelNameSerializer" 
                            """
                            if the_model_name in (serializer[0]) and (
                            serializer[1].Meta.model.__name__).lower() == the_model_name.lower():
                                the_serializer = serializer[1]

                        try:
                            ser = the_serializer(data=record[the_model_name])
                            if ser.is_valid():
                                """ if serializer for recognised model is valid, save instance"""
                                ser.save()
                            elif ii in [0, 1]:
                                """ otherwise add it to the queue for next iteration, if any """
                                records_that_couldnt_be_executed.append(
                                    {list(record.keys())[0]: record[the_model_name]})
                            else:
                                try:
                                    """
                                    if last iteration, check if object with given id already exists in its db table
                                    if it does, update it. 
                                    doesn't work for m2m rel
                                    """
                                    obj_id = record[the_model_name]["id"]
                                    the_model = [modell[1] for modell in list(models.items()) if
                                                 modell[0].lower() == the_model_name.lower()][0]
                                    the_model.objects.filter(id=obj_id).update(**record[the_model_name])
                                except FieldError:
                                    """
                                    is m2m field on the model, update (patch) of records must be handled separately
                                    in this case only Product model involves m2m
                                    if a new model with m2m rel to be imported, following block must be duplicated and adjusted accordingly 
                                    """
                                    try:
                                        obj_id = record[the_model_name]["id"]
                                        catalog = Catalog.objects.get(id=obj_id)
                                        if "products_ids" in record[the_model_name].keys():
                                            product_ids = record[the_model_name].pop("products_ids")
                                            catalog.products_ids.clear()
                                            for id in product_ids:
                                                catalog.products_ids.add(Product.objects.get(id=id))
                                        if "attributes_ids" in record[the_model_name].keys():
                                            attributes_ids = record[the_model_name].pop("attributes_ids")
                                            catalog.attributes_ids.clear()
                                            for id in attributes_ids:
                                                catalog.attributes_ids.add(Attribute.objects.get(id=id))
                                        catalog.save()
                                        catalog.__dict__.update(**record[the_model_name])
                                        catalog.save()
                                    except Exception as e:
                                        return Response({
                                            "message": f"Failed to update a db record for model {the_model_name} for object with id {record[the_model_name][obj_id]}."},
                                            status=status.HTTP_400_BAD_REQUEST)
                                except:
                                    return Response({
                                        "message": f"Failed to update a db record for model {the_model_name} for object with id {record[the_model_name][obj_id]}."},
                                        status=status.HTTP_400_BAD_REQUEST)

                        except Exception as e:
                            errors.append(e)
                            return Response({
                                "message": f"Failed to create a db record for model {the_model_name} with attributes {record[the_model_name]}."},
                                status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        errors.append(e)
                        return Response({"message": "Model does not exits."}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    errors.append(e)
                    return Response({"message": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Import successful."},
                        status=status.HTTP_201_CREATED)
