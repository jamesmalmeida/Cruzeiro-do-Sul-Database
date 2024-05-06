from django.urls import path
from database import views

# from .views import upload_xdi

urlpatterns = [
    # path('upload/', upload_xdi, name='upload_xdi'),
    path('', views.index, name='index'),
    path('experiments/', views.experiment_list, name='experiments'),
    path('experiments/<int:pk>', views.experiment_detail, name='experiment-detail'),
    path('experiments/<int:pk>/delete/', views.DeleteExperiment.as_view(), name='experiment-delete'),
    path('experiments/<int:pk>/file=<str:string>', views.file_response, name='file-response'),
    path('search-data/', views.search_data, name='search-data'),
    path('search-data/result/', views.search_result, name='result'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('accounts/<int:pk>/update/', views.ChangeAccountView.as_view(), name='account-update'),
    #path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/', views.sign_up, name = 'signup'),
    path('user-data/', views.user_data_list, name='user-data'),
    # path('add-experiment/', views.AddExperiment.as_view(), name='add-experiment'),
    path('add-experiment/', views.AddExperiment, name='add-experiment'),
    path('add-element/', views.AddElement.as_view(), name='add-element'),
    path('add-beamline/', views.AddBeamline.as_view(), name='add-beamline'),
    path('add-facility/', views.AddFacility.as_view(), name='add-facility'),
    path('normalization/', views.normalize_file, name='normalization'),
    #path('normalization/result', views.AddNormalization.as_view(), name='normalization'),
    #path('upload/', normalize_file, name='normalize_file'),
    path('normalization/chart', views.plotly_chart, name='plotly_chart'),
    #path('upload/', views.plot_graph, name='plot_graph'),
    #path('result/<path:plot_file_path>/', views.plot_result, name='plot_result'),
    path('comparison/', views.spectra_comparison, name='comparison'),
    path('comparison/chart', views.plotly_chart, name='plotly_chart')
]