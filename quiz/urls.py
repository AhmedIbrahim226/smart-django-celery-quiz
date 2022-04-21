from django.urls import path
from . import views



urlpatterns = [
    path('quizes/', views.quiz_view, name='quiz-view'),
    path('response/code/', views.check_quiz_code_response),

    path('questions/<quiz_id>/', views.question_view, name='questions'),


    path('get-quiz-degree/', views.get_quiz_degree),
    path('reports/', views.reports_views, name='quiz-reports-view'),

    path('report/<id>/', views.student_report, name='report-view'),
]
