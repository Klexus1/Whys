import json
from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from core.serializers import *
from core.models import *
from core import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.apps import apps
from django.db.models import ForeignKey



def get_fk_model(model, fieldname):
    """Returns None if not foreignkey, otherswise the relevant model"""
    print(model)
    print(model._meta)
    field_object = model._meta.get_field_by_name(fieldname)

    # if not m2m and direct and isinstance(field_object, ForeignKey):
    #     return True
    return None


class ImportDataView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # records_that_couldnt_be_executed = {}
        models = apps.get_app_config('core').get_models().gi_frame.f_locals["self"].models
        model_names = []
        for i in range(0, len(list(models.items()))):
            model_names.append(str(list(models.items())[i][0]))
        available_serializers = []
        for name, obj in inspect.getmembers(serializers):
            if inspect.isclass(obj) and "Serializer" in name:
                for model_name in model_names:
                    if model_name in name.lower():
                        available_serializers.append((name, obj))
        available_serializers = list(set(available_serializers))
        data = request.data
        # ii = 0

        for record in data:
            if list(record.keys())[0].lower() not in model_names:
                return Response({"message": f"Model {list(record.keys())[0]} not supported."},
                                status=status.HTTP_400_BAD_REQUEST)
            # todo co když špatně velká písmena ve jméně modelu
            try:
                the_model_name = list(record.keys())[0]
                try:
                    the_serializer = None
                    for serializer in available_serializers:
                        if the_model_name in (serializer[0]) and (serializer[1].Meta.model.__name__).lower() == the_model_name.lower():
                            the_serializer = serializer[1]

                    try:
                        ser = the_serializer(data=record[the_model_name])
                        if ser.is_valid():
                            ser.save()
                        else:
                            id = record[the_model_name]["id"]
                            try:
                                the_model = [modell[1] for modell in list(models.items()) if modell[0].lower() == the_model_name.lower()][0]
                                obj = the_model.objects.get(id=id)
                                obj.__dict__.update(record[the_model_name])
                                obj.save(force_update=True)
                            except:
                                Response({
                                    "message": f"Failed to update a db record for model {the_model_name} for object with id {record[the_model_name][id]}."},
                                    status=status.HTTP_400_BAD_REQUEST)

                    except:
                        return Response({
                                            "message": f"Failed to create a db record for model {the_model_name} with attributes {record[the_model_name]}."},
                                        status=status.HTTP_400_BAD_REQUEST)


                except:
                    return Response({"message": "Model does not exits."}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"message": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Import successful."},
                        status=status.HTTP_201_CREATED)
