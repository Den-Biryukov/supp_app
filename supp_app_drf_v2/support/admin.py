from django.contrib import admin
from support.models import Support, Ticket, Comment


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ticket_name', 'description', 'decided_status',
                    'unsolved_status', 'frozen_status')
    list_filter = ('decided_status', 'unsolved_status', 'frozen_status')


class SupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_support')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ticket', 'content', 'parent')
    list_filter = ('user',)


admin.site.register(Support, SupportAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comment, CommentAdmin)
