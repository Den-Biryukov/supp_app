from supp_app_drf_v2.celery import app
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from supp_app_drf_v2 import settings
from support.models import Ticket


list_of_admins_and_supports = [user for user in get_user_model().objects.all() if user.is_staff]


def is_user_support():
    users = get_user_model().objects.all()
    for user in users:
        if hasattr(user, 'supports'):
            if user.supports.is_support == True:
                list_of_admins_and_supports.append(user)


@app.task(bind=True)
def send_mail_func(self, user_id, ticket_status):
    user = get_user_model().objects.get(id=user_id)
    mail_subject = "ticket status"

    STATUS = ['unsolved', 'solved', 'frozen']

    message = f"Dear {user.username}, your ticket status was changed to {STATUS[int(ticket_status)]}."
    to_email = user.email
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
    return f"email was sent to {to_email}"


@app.task(bind=True)
def send_beat_mail_tickets(self):
    users = get_user_model().objects.all()
    mail_subject = "Some statistic"
    is_user_support()
    for user in users:
        if user not in list_of_admins_and_supports:
            ticket_count = Ticket.objects.filter(user=user).count()

            unsolved_tickets = Ticket.objects.filter(user=user,
                                                     status=0).count()
            decided_tickets = Ticket.objects.filter(user=user,
                                                    status=1).count()
            frozen_tickets = Ticket.objects.filter(user=user,
                                                   status=2).count()

            send_mail(
                subject=mail_subject,
                message=f'Dear {user.username}, You have in total {ticket_count} tickets. '
                        f'Count of unsolved tickets is {unsolved_tickets}. '
                        f'Count of decided tickets is {decided_tickets}. '
                        f'Count of frozen tickets is {frozen_tickets}. '
                        f'Thank you for using our app!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=True,
            )

    return f'email was sent to users'
