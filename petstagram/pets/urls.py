from django.urls import path, include

from petstagram.pets import views

urlpatterns = [
    path('add/', views.AddPetView.as_view(), name='add-pet'),
    path('<str:username>/pet/<slug:pet_slug>/', include([
        path('', views.PetDetailsPage.as_view(), name='pet-details'),
        path('edit/', views.EditPetView.as_view(), name='edit-pet'),
        path('delete/', views.DeletePetView.as_view(), name='delete-pet'),
    ])),
]
