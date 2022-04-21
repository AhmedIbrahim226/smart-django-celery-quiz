from django.urls import path

from . import views


urlpatterns = [
    path('sign/up/', views.sign_up, name='signup-view'),
    # path('sign/in/', views.login_view, name='login-view'),
    
    path('add/quiz/', views.create_quiz, name='add-quiz'),
    path('response_code/', views.generate_code),

    path('delete/unanswerd/quiz/<id>/', views.delete_unanswered_quiz, name='delete-unanswerd-quiz'),
    
    path('quiz/my-quizes/', views.my_quizes, name='my-quizes-view'),
    path('quiz/my-quizes/edit/<id>/', views.edit_quiz, name='edit-quiz'),
    path('response_id/', views.response_id),
    
    path('quiz/my-quizes/quiz-question/<id>/', views.quiz_questions, name='quiz-question'),
    
    path('quiz/my-quizes/quiz-question/<quiz_id>/question/edit/<question_id>/', views.edit_question, name='edit-question'),
    path('quiz/my-quizes/quiz-question/<quiz_id>/question/delete/<question_id>/', views.delete_question, name='delete-question'),

    
    path('reports/', views.quizes_report_view, name='reports-view'),
    path('report/<id>/', views.report_view, name='report'),

    
    path('logout/', views.lgout_view, name='logout-view'),
]