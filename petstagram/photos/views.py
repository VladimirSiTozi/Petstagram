from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from petstagram.common.forms import CommentForm
from petstagram.photos.forms import PhotoAddForm, PhotoEditForm
from petstagram.photos.models import Photo


class AddPhotoPageView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoAddForm
    template_name = 'photos/photo-add-page.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        # photo.save()
        # form.save_m2m()
        return super().form_valid(form)


class EditPhotoPageView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    template_name = 'photos/photo-edit-page.html'
    form_class = PhotoEditForm

    def test_func(self):
        photo = get_object_or_404(Photo, slug=self.kwargs['pk'])
        return self.request.user == photo.user

    def get_success_url(self):
        return reverse_lazy(
            'photo-details',
            kwargs={'pk': self.kwargs['pk']}
        )


class PhotoDetailsView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photos/photo-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['likes'] = self.object.like_set.all()
        context['comments'] = self.object.comment_set.all()
        context['comment_form'] = CommentForm
        self.object.has_liked = self.object.like_set.filter(user=self.request.user).exists()

        return context


@login_required
def delete_photo(request, pk: int):
    photo = Photo.objects.get(pk=pk)

    if request.user == photo.user:
        photo.delete()
    return redirect('home-page')
