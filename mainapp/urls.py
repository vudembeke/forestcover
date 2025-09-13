from django.urls import path
from mainapp import views

urlpatterns = [
    path('',views.index,name='index'),
    path('prediction/',views.prediction,name='prediction'),
    path('api/forest/<int:forest_id>/', views.get_forest_data),
    path('api/documentation/',views.documentation,name="apidocumentation"),
    path('api/forest/<int:forest_id>/update/', views.update_forest_data, name='update_forest_data'),
   

]
