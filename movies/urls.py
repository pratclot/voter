from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path('polls/', views.PollsView.as_view(), name='polls'),
    path('polls/<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
    path('polls/<int:pk>/results/', views.PollResultsView.as_view(),
         name='poll_results'),
    path('polls/<int:poll_id>/vote2/', views.vote2, name='vote2'),
]