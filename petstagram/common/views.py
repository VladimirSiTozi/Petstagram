from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView
from pyperclip import copy

import pytz
from django.utils.timezone import localtime

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like
from petstagram.photos.models import Photo


class HomePageView(ListView):
    model = Photo
    template_name = 'common/home-page.html'
    context_object_name = 'all_photos'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['search_form'] = SearchForm(self.request.GET)

        user = self.request.user

        for photo in context['all_photos']:
            photo.has_liked = photo.like_set.filter(user=user).exists() if user.is_authenticated else False

        return context

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date_of_publication')  # get all objects
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            queryset = queryset.filter(  # filter the objects
                tagged_pets__name__icontains=pet_name
            )

        return queryset  # return new queryset


@login_required
def likes_func(request, photo_id: int):
    liked_object = Like.objects.filter(
        to_photo=photo_id,
        user=request.user
    ).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo_id=photo_id, user=request.user)
        like.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


def share_func(request, photo_id: int):
    copy(request.META.get('HTTP_HOST') + resolve_url('photo-details', photo_id))
    # HTTP_HOST = https://127.0.0.1 + photo/<int:pk/

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


@login_required
def comment_func(request, photo_id: int):
    if request.POST:
        photo = Photo.objects.get(pk=photo_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')
