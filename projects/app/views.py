from django.shortcuts import render
import json
import csv
import os
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import JsonResponse
from rest_framework import status
from django.core.files.uploadedfile import UploadedFile
from .config import *

@api_view(['GET'])
def upload_page(request):
    print("Upload page loaded")
    return render(request, 'update.html')
  
    
# @api_view(['POST'])
# # @parser_classes([MultiPartParser, FormParser])  
# def upload_csv_api(request: Request):
#     file: UploadedFile = request.FILES.get('file')  
#     if not file:
#         return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
#     UPLOAD_DIR = os.path.join(settings.BASE_DIR, "uploads")  
#     if not os.path.exists(UPLOAD_DIR):
#         os.makedirs(UPLOAD_DIR)
#     file_path = os.path.join(UPLOAD_DIR, file.name) 
#     try:
#         decoded_file = file.read().decode("utf-8").splitlines()
#         reader = csv.DictReader(decoded_file)
#         csv_data = list(reader) 
#     except Exception as e:
#         return JsonResponse({"error" : "Error parsing the cdv file"})    
#     print(f"File name :- {file.name}")
#     with open(file_path, 'wb+') as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)
#     return JsonResponse({
#         "message" : f"File stored {file.name}",
#         "csv_data": csv_data
#     })        



@api_view(['POST'])
def upload_csv_api(request):
    file: UploadedFile = request.FILES.get('file')  
    if not file:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Save file in `uploads` directory
    UPLOAD_DIR = os.path.join(settings.BASE_DIR, "uploads")  
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.name) 

    try:
        decoded_file = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)
        csv_data = list(reader)  

        if not csv_data:
            return JsonResponse({"error": "CSV file is empty"}, status=400)

        # Extract headers (column names)
        headers = list(csv_data[0].keys())
        table_name = "uploaded_csv_data"

        # Connect to PostgreSQL
        conn = db_connection()
        if not conn:
            return JsonResponse({"error": "Failed to connect to the database"}, status=500)
        
        cursor = conn.cursor()

        # Create table with `id SERIAL PRIMARY KEY`
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY, 
            {', '.join([f'"{col}" TEXT' for col in headers])}
        );
        """
        cursor.execute(create_table_query)

        # Insert data into table
        for row in csv_data:
            columns = ', '.join([f'"{col}"' for col in headers])
            values = ', '.join(["%s" for _ in headers])
            insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING id;'
            cursor.execute(insert_query, tuple(row.values()))

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        return JsonResponse({"error": f"Error processing the CSV file: {str(e)}"}, status=400)    

    # Save the file
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return JsonResponse({
        "message": f"File stored: {file.name}",
        "csv_data": csv_data
    })


@api_view(['PUT'])
def update_csv_row(request, row_id):
    data = request.data  # JSON Data for update
    
    if not data:
        return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Dynamically create UPDATE query
        set_clause = ", ".join([f'"{col}" = %s' for col in data.keys()])
        values = list(data.values()) + [row_id]

        update_query = f'UPDATE uploaded_csv_data SET {set_clause} WHERE id = %s;'
        cursor.execute(update_query, values)

        conn.commit()
        cursor.close()
        conn.close()

        return Response({"message": "Row updated successfully"})

    except Exception as e:
        return Response({"error": f"Error updating row: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)







@api_view(['POST'])
def signup_api(request):
    data: dict = json.loads(request.body)
    print("\n\nSIGN UP PAGE LOADED")
    user_name: str = data.get("email")
    password: str = data.get("password")
    print(f"User :-  {user_name}")
    print(f"Password :- {password}")
    return JsonResponse({"message" : "Data stored"})




@api_view(['GET'])
def signup_page(request):
    return render(request, "signup.html")



@api_view(['POST'])
def login_api(request):
    data: dict = json.loads(request.body)
    print("\n\nLOGIN PAGE LOADED")
    user_name: str = data.get("email")
    password: str = data.get("password")
    print(f"User :-  {user_name}")
    print(f"Password :- {password}")
    return JsonResponse({"message" : "Data stored"})




@api_view(['GET'])
def login_page(request):
    return render(request, "login.html")



    # return JsonResponse({"message" : "server is active"})

@api_view(['GET'])
def test_server(request):
    return JsonResponse({"message" : "server is active"})