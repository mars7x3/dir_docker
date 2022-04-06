from django.urls import path

from .views import *


urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('resume/<int:resume_id>/', ResumeDetailView.as_view(), name='resume'),
    path('add_resume/', add_resume, name='add_resume'),
    path('update_resume/<int:pk>/', ResumeUpdateView.as_view(), name='update'),
    path('delete_resume/<int:pk>/', ResumeDeleteView.as_view(), name='delete'),
    path('resumes/', ResumeHome.as_view(), name='resume_home'),
    path('works/', WorkHome.as_view(), name='work_home'),
    path('search/', SearchListView.as_view(), name='search'),
    path('resume/send/<int:pk>/', reviews, name='send_review'),
    path('comment_delete/<int:pk>/', delete_comment, name='delete_comment'),
    path('<str:slug>/', FilterHome.as_view(), name='filter')
    
]


