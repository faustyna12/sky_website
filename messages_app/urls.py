from django.urls import path
from . import views             

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'), #inbox page
    path('sent/', views.sent_messages, name='sent_messages'),#sent messages page
    path('message/<int:message_id>/', views.view_message, name='view_message'),#view message page
    path('compose/', views.compose_message, name='compose_message'),#compose message page
    path('drafts/', views.drafts, name='drafts'),#drafts page
    path('edit_draft/<int:message_id>/', views.edit_draft, name='edit_draft'),#edit draft page

]