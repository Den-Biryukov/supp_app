from rest_framework import serializers
from .models import Ticket, Comment


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterCommentSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CommentListSerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(read_only=True)
    children = RecursiveSerializer(many=True)

    def get_username(self, obj):
        return obj.user.username + ' - Support'

    user = serializers.SerializerMethodField('get_username')

    class Meta:
        list_serializer_class = FilterCommentSerializer
        model = Comment
        fields = ('user', 'content', 'time_create', 'children')


class CommentSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    time_create = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class TicketListSerializer(serializers.ModelSerializer):

    comments = CommentListSerializer(many=True)

    class Meta:
        model = Ticket
        fields = ('ticket_name', 'description', 'time_create', 'comments')


class TicketCreateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = ('ticket_name', 'description', 'user')


class TicketForSupportSerializer(serializers.ModelSerializer):

    def get_id_and_username(self, obj):
        return {'id': obj.user.id, 'username': obj.user.username}

    user = serializers.SerializerMethodField('get_id_and_username')

    status = serializers.SerializerMethodField()

    unsolved_tickets_count = serializers.SerializerMethodField()
    decided_tickets_count = serializers.SerializerMethodField()
    frozen_tickets_count = serializers.SerializerMethodField()

    comments = CommentListSerializer(many=True)

    time_create = serializers.DateTimeField(read_only=True)

    def get_status(self, instance):

        if Ticket.objects.filter(user__ticket=instance,
                                 unsolved_status=True):
            return 'unsolved'
        elif Ticket.objects.filter(user__ticket=instance,
                                   decided_status=True):
            return 'decided'
        else:
            return 'frozen'

    def get_unsolved_tickets_count(self, instance):

        return Ticket.objects.filter(user__ticket=instance,
                                     unsolved_status=True).count()

    def get_decided_tickets_count(self, instance):

        return Ticket.objects.filter(user__ticket=instance,
                                     decided_status=True).count()

    def get_frozen_tickets_count(self, instance):

        return Ticket.objects.filter(user__ticket=instance,
                                     frozen_status=True).count()

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'ticket_name', 'description', 'time_create', 'status',
                  'unsolved_tickets_count', 'decided_tickets_count',
                  'frozen_tickets_count', 'comments')


class UpdateTicketForSupportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('decided_status', 'unsolved_status', 'frozen_status')
