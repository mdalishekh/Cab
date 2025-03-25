from django.urls import path
from .views import *

urlpatterns = [
    # Pages route
    # path('', name='sign-up'),
    path('sign-up', signup_page,  name='sign-up'),
    path('login',login_page ,name='login'),
    path('upload',upload_page, name='upload-file'),
    
    # APIs route
    path('signup-api/', signup_api,name='sign-up'),
    path('login-api/',login_api ,name='login'),
    path('upload-api/', upload_csv_api, name='upload-file'),
    path('update-csv-row/<int:row_id>/', update_csv_row, name='update_csv_row'),
    path('test', test_server)
]
