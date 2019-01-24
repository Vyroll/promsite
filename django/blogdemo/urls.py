from django.urls import path

from . import views

app_name = 'blogdemo'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('createpost/', views.CreatePostView.as_view(), name='createpost'),
    path('createcomment/<int:pk>/', views.CreateCommentView.as_view(), name='createcomment'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('post/<int:pk>/edit/', views.EditPostView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='post_delete'),
]