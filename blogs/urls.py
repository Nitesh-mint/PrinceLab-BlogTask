from django.urls import path
from . import views

urlpatterns = [
        path('', views.Home.as_view(), name='bloghome'),
        path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
        path('post/<int:pk>/like', views.like_posts, name='like_post'),
        path('post/<int:pk>/comment', views.PostCommentView.as_view(), name="post_comment"),
        path('post/<int:pk>/edit-comment', views.EditCommentView.as_view(), name="edit_comment"),
        ]
