from django.urls import path

from petstagram.common import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('like/<int:photo_id>/', views.likes_func, name='like'),
    path('share/<int:photo_id>/', views.share_func, name='share'),
    path('comment<int:photo_id>/', views.comment_func, name='comment')

]
