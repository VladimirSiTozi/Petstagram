from django.shortcuts import render


def add_pet(request):
    return render(request, 'pets/pet-add-page.html')


def delete_pet(request, username: str, pet_slug: str):
    return render(request, 'pets/pet-delete-page.html')


def pet_details(request, username: str, pet_slug: str):
    return render(request, 'pets/pet-details-page.html')


def edit_pet(request, username: str, pet_slug: str):
    return render(request, 'pets/pet-edit-page.html')