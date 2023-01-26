from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:myid>/", views.quiz, name="quiz"),
    #path("<int:myid>/", views.privatequiz, name="privatequiz"),
    #path("<int:myid>/", views.privatequiz, name="privatequiz"),
    path('<int:myid>/data/', views.quiz_data_view, name='quiz-data'),
    path('<int:myid>/save/', views.save_quiz_view, name='quiz-save'),
    
    path("signup/", views.Signup, name="signup"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

    path('add_quiz/', views.add_quiz, name='add_quiz'),
    path('add_question/', views.add_question, name='add_question'),
    path('add_options/<int:myid>/', views.add_options, name='add_options'),
    path('add_integer/<int:myid>/', views.add_integer, name='add_integer'),
    path('add_boolean/<int:myid>/', views.add_boolean, name='add_boolean'),

    path('results/', views.results, name='results'),
    path('results_list/', views.ResultsList.as_view(), name='results_list'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('delete_question/<int:myid>/', views.delete_question, name='delete_question'),
    path('delete_result/<int:myid>/', views.delete_result, name='delete_result'),

    path('social/signup/', views.signup_redirect, name='signup_redirect'),
]