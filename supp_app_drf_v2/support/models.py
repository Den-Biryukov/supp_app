from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Support(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='supports')
    is_support = models.BooleanField(default=False, verbose_name='support status')

    def __str__(self):
        if self.is_support:
            return f'{self.user} - is support'
        else:
            return f'{self.user} - is not support'

    class Meta:
        verbose_name_plural = 'List of Supports'
        ordering = ['user']


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    STATUS = [
        (0, 'unsolved'),
        (1, 'solved'),
        (2, 'frozen')
    ]

    status = models.PositiveSmallIntegerField(choices=STATUS, blank=False, default=0)

    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ticket_name}'

    class Meta:
        unique_together = ('user', 'ticket_name')
        verbose_name_plural = 'List of Tickets'
        ordering = ['user', 'ticket_name']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    parent = models.ForeignKey('self', verbose_name='parent', on_delete=models.CASCADE,
                               blank=True, null=True, related_name='children')
    time_create = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} - comment on - {self.ticket}'


class Meta:
    verbose_name_plural = 'comments'
    ordering = ['user', 'ticket']
