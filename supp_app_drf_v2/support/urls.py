from django.urls import path
from support.views import ListCreateTicketAPIView, ListAllTicketAPIView, \
                          ListUpdateTicketAPIView, CommentCreateAPIView


# Ticket
urlpatterns = [
    path('ticket/', ListCreateTicketAPIView.as_view()),
    path('ticket/support/', ListAllTicketAPIView.as_view()),
    path('ticket/support/<int:pk>/', ListUpdateTicketAPIView.as_view()),
]


# Comments
urlpatterns += [
    path('comment/', CommentCreateAPIView.as_view()),
]
