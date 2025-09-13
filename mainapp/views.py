

from django.shortcuts import render
from rest_framework.decorators import api_view


from django.http import HttpResponse,JsonResponse,response


import json
# views.py

from .models import Forest, ForestData
from .serializers import ForestSerializer, ForestDataSerializer
from rest_framework.views import APIView



# Create your views here.
def index(request):
    return render(request,'index.html')

def prediction(request):
    return render(request,'prediction.html')

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Forest, ForestData
from .serializers import ForestSerializer

def get_forest_data(request, forest_id):
    # Get the forest object (only retrieve the name field)
    forest = get_object_or_404(Forest.objects.only('forest_name'), id=forest_id)

    # Get start_year and end_year from query parameters (if they exist)
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')

    # Build the queryset for ForestData
    forest_data_qs = ForestData.objects.filter(forest_id=forest_id).only(
        'ndvi', 'area', 'density', 'change', 'year'
    ).order_by('year')

    # If start_year and end_year are provided, filter by them
    if start_year and end_year:
        # Ensure they are integers
        try:
            start_year = int(start_year)
            end_year = int(end_year)
            forest_data_qs = forest_data_qs.filter(year__gte=start_year, year__lte=end_year)
        except ValueError:
            return JsonResponse({"error": "Invalid start_year or end_year"}, status=400)

    # Serialize the data using the ForestSerializer
    serializer = ForestSerializer({
        "forest_name": forest.forest_name,
        "data": forest_data_qs
    })

    # Return the JSON response
    return JsonResponse(serializer.data, json_dumps_params={'indent': 2})

def documentation(request):
    return render(request,"documentation.html")



@api_view(['POST'])
def update_forest_data(request, forest_id):
    # Try to get the forest by ID, if not found, return a 404 error
    try:
        forest = Forest.objects.get(id=forest_id)
    except Forest.DoesNotExist:
        raise NotFound("Forest not found.")
    
    # Get the 'data' from the request body
    data = request.data.get('data', [])
    
    if not data:
        return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Process each entry in the incoming data
    for entry in data:
        year = entry.get('year')
        if not year:
            return Response({"error": "Year is required for each data entry."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if ForestData for the specific year already exists
        forest_data, created = ForestData.objects.update_or_create(
            forest=forest, 
            year=year,
            defaults={
                'ndvi': entry.get('ndvi'),
                'area': entry.get('area'),
                'density': entry.get('density'),
                'change': entry.get('change')
            }
        )
        
        # If the record was created, you may want to return the created data for confirmation
        if created:
            # Optionally: Return a response saying the data was created
            print(f"Created data for {forest.forest_name} in year {year}")

    # Return success response
    return Response({"message": "Forest data updated successfully"}, status=status.HTTP_200_OK)







  
