from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

import pytz
from django.utils.timezone import localtime

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like
from petstagram.photos.models import Photo


def home_page(request):
    all_photos = Photo.objects.all().order_by('-date_of_publication')
    timezone = pytz.timezone('Etc/GMT-3')
    comment_form = CommentForm()
    search_form = SearchForm(request.GET)

    for photo in all_photos:
        photo.date_of_publication = localtime(photo.date_of_publication, timezone)

    if search_form.is_valid():
        if search_form.cleaned_data['pet_name']:
            all_photos = all_photos.filter(
                tagged_pets__name__icontains=search_form.cleaned_data['pet_name']
            )

    context = {
        'all_photos': all_photos,
        'comment_form': comment_form,
        'search_form': search_form,
    }

    return render(request, 'common/home-page.html', context)


def likes_func(request, photo_id: int):
    liked_object = Like.objects.filter(to_photo=photo_id).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo_id=photo_id)
        like.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


def share_func(request, photo_id: int):
    copy(request.META.get('HTTP_HOST') + resolve_url('photo-details', photo_id))
    # HTTP_HOST = https://127.0.0.1 + photo/<int:pk/

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


def comment_func(request, photo_id: int):
    if request.POST:
        photo = Photo.objects.get(pk=photo_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_photo = photo
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')
