from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
import kandidat
from kandidat.models import Kandidat
from kandidat.serializers import KandidatSerializer
from rest_framework.decorators import api_view
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@api_view(['GET', 'POST', 'DELETE'])
def kandidaten_list(request):
    # GET Liste der Kandidaten, POST einen neuen Kandidaten, DELETE alle Kandidaten
    if request.method == 'GET':
        kandidat = Kandidat.objects.all()

        Vorname = request.query_params.get('Vorname', None)
        if Vorname is not None:
            kandidat = kandidat.filter(title__icontains=Vorname)

        kandidat_serializer = KandidatSerializer(kandidat, many=True)
        return JsonResponse(kandidat_serializer.data, safe=False)
        # safe=False' für die Serialisierung von Objekten

    elif request.method == 'POST':
        print("kandidat: ",request.data)
        kandidat_serializer = KandidatSerializer(data=request.data)
        if kandidat_serializer.is_valid():
            kandidat_serializer.save()
            return JsonResponse(kandidat_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(kandidat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Kandidat.objects.all().delete()
        return JsonResponse({'message': '{} candidates were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def kandidaten_detail(request, pk):
    # Suche nach Kandidaten durch pk (id)
    try:
        kandidat = Kandidat.objects.get(pk=pk)
    except Kandidat.DoesNotExist:
        return JsonResponse({'message': 'The candidate does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # GET / PUT / DELETE candidate
    if request.method == 'GET':
        kandidat_serializer = KandidatSerializer(kandidat)
        return JsonResponse(kandidat_serializer.data)

    elif request.method == 'PUT':
        kandidat_serializer = KandidatSerializer(kandidat,data=request.data)
        if kandidat_serializer.is_valid():
            kandidat_serializer.save()
            return JsonResponse(kandidat_serializer.data)
        return JsonResponse(kandidat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        kandidat.delete()
        return JsonResponse({'message': 'candidate was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def kandidaten_list_erwachsene(request):
    # GET alle erwachsenen Kandidaten
    kandidat = Kandidat.objects.filter(is_adult=True)
    if request.method == 'GET':
        kandidat_serializer = KandidatSerializer(kandidat, many=True)
        return JsonResponse(kandidat_serializer.data, safe=False)

def home(request):

    return render(request,'kandidat/layout.html')

def kandidat_add(request):

    return render(request,'kandidat/kandidat-add.html',{'current':'add'})

def kandidat_update(request,id):

    kandidat = ""

    try:
        kandidat = Kandidat.objects.get(id=id)
    except Kandidat.DoesNotExist:
        return redirect('kandidat-all')



    return render(request,'kandidat/kandidat-update.html',{'current':'update',"id":id,"candidat":kandidat})


#die Funktion, um alle Benutzer und den ersten Benutzer in der Liste zurückzugeben

def kandidat_all(request,id):

    candidats = Kandidat.objects.all()
    if str(id).isnumeric():
        try :
            single = Kandidat.objects.get(id=id)
        except Kandidat.DoesNotExist:
            return redirect('kandidat-add')
    else:
        id = Kandidat.objects.first().id
    current = Kandidat.objects.get(id=id).Vorname
    return render(request,'kandidat/kandidat-all.html',{'current':current,"id":id,"candidats":candidats,"single":single})

#Funktion, um einen bestimmten zurückzugeben

def kandidat_home(request):

    candidats = Kandidat.objects.all()
    try:
        id = Kandidat.objects.first().id
    except AttributeError:
        return render(request,'kandidat/kandidat-all.html',{"current":False,"candidats":[],"single":[],"id":1})
    single = id = Kandidat.objects.first()
    return render(request,'kandidat/kandidat-all.html',{'current':'all',"id":id,"candidats":candidats,"single":single})

def kandidat_delete(request,id):

    try:
        Kandidat.objects.filter(id=id).delete()
        return redirect('kandidat-home')
    except Kandidat.DoesNotExist:
        return redirect('kandidat-home')

def kandidat_delete_all(request):

    delete = Kandidat.objects.all().delete()

    return redirect("kandidat-home")
