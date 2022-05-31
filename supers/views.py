from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . serializers import SuperSerializer
from . models import Super
from super_types.models import SuperType


@api_view(['GET', 'POST'])
def supers_list(request):
    if request.method == 'GET':
        super_type_name = request.query_params.get('Super_Type')
        if super_type_name:
            queryset = Super.objects.filter(super_type__type=super_type_name)
            serializer = SuperSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            heroes = Super.objects.filter(super_type_id=1)
            heroes_serializer = SuperSerializer(heroes, many=True)
            villians = Super.objects.filter(super_type_id=2)
            villians_serializer = SuperSerializer(villians, many=True)

            custom_dictionary = {
                "heroes": heroes_serializer.data,
                "villians": villians_serializer.data
            }
            return Response(custom_dictionary)

    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def super_detail(request, pk):
    super = get_object_or_404(Super, pk=pk)

    if request.method == 'GET':
        serializer = SuperSerializer(super)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SuperSerializer(super, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
