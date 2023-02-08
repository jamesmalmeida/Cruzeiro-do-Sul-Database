from django.urls import path
from database import views


urlpatterns = [
    path('', views.index, name='index'),
    path('experiments/', views.ExperimentListView.as_view(), name='experiments'),
    path('experiments/<int:pk>', views.ExperimentDetailView.as_view(), name='experiment-detail'),
    path('experiments/<int:pk>/file=<str:string>', views.file_response, name='file-response'),
    path('search-xas/', views.search_xas, name='search-xas'),
    path('search-xrd/', views.search_xrd, name='search-xrd'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('create-account/', views.create_account, name='create-account'),
    path('upload-data/', views.upload_data, name='upload-data'),
]