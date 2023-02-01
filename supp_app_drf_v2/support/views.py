from rest_framework import generics
from support.models import Ticket, Comment
from support.permissions import IsUser, IsAdminOrSupport
from support.serializers import TicketListSerializer, TicketCreateSerializer, \
                                TicketForSupportSerializer, UpdateTicketForSupportSerializer, \
                                CommentListSerializer, CommentSerializer
from .pagination import ListPagination
from .tasks import send_mail_func
from rest_framework.permissions import IsAuthenticated


class ListCreateTicketAPIView(generics.ListCreateAPIView):

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    permission_classes = (IsUser,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TicketListSerializer
        else:
            return TicketCreateSerializer


class ListAllTicketAPIView(generics.ListAPIView):
    permission_classes = (IsAdminOrSupport,)
    pagination_class = ListPagination
    serializer_class = TicketForSupportSerializer
    queryset = Ticket.objects.all().select_related('user')


class ListUpdateTicketAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdminOrSupport,)
    queryset = Ticket.objects.all().select_related('user')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TicketForSupportSerializer
        else:
            return UpdateTicketForSupportSerializer

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user_id = Ticket.objects.get(id=pk).user.id
        ticket_status = request.data['status']
        send_mail_func.delay(user_id, ticket_status)
        return self.update(request, *args, **kwargs)


class CommentCreateAPIView(generics.ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentListSerializer
        else:
            return CommentSerializer

    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
