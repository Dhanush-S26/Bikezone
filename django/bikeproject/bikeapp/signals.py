# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from django.template.loader import render_to_string
# from django.core.mail import EmailMultiAlternatives
# from django.db import transaction
# from .models import Booking,Testride
# import logging

# logger = logging.getLogger(__name__)
# User = get_user_model()

# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     """Send welcome email when a new user is created."""
#     if not created:
#         return
#     user = instance
#     if not user.email:
#         logger.info("No email for user %s — skipping welcome email.", user)
#         return

#     def _send():
#         subject = f"Welcome to {getattr(settings, 'SITE_NAME', 'Our site')}"
#         context = {'user': user, 'site_name': getattr(settings, 'SITE_NAME', 'BikeZone')}
#         text_body = render_to_string('emails/welcome_email.txt', context)
#         html_body = render_to_string('emails/welcome_email.html', context)

#         msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, [user.email])
#         msg.attach_alternative(html_body, "text/html")
#         try:
#             msg.send()
#             logger.info("Welcome email sent to %s", user.email)
#         except Exception as e:
#             logger.exception("Failed to send welcome email to %s: %s", user.email, e)

#     # Ensure the email is only sent after the DB transaction commits
#     _send()
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from .models import Booking, Testride, BikeCollections
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


# ------------------------------------------------------
# 1. Welcome email when a new user registers
# ------------------------------------------------------
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if not created:
        return
    user = instance
    if not user.email:
        logger.info("No email for user %s — skipping welcome email.", user)
        return

    def _send():
        subject = f"Welcome to {getattr(settings, 'SITE_NAME', 'BikeZone')}"
        context = {'user': user, 'site_name': getattr(settings, 'SITE_NAME', 'BikeZone')}
        text_body = render_to_string('emails/welcome_email.txt', context)
        html_body = render_to_string('emails/welcome_email.html', context)

        msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, [user.email])
        msg.attach_alternative(html_body, "text/html")
        try:
            msg.send()
            logger.info("✅ Welcome email sent to %s", user.email)
        except Exception as e:
            logger.exception("❌ Failed to send welcome email to %s: %s", user.email, e)

    transaction.on_commit(_send)


# ------------------------------------------------------
# 2. Booking confirmation email
# ------------------------------------------------------
@receiver(post_save, sender=Booking)
def send_booking_confirmation(sender, instance, created, **kwargs):
    if not created:
        return
    booking = instance
    if not booking.email:
        logger.info("No email for booking %s — skipping confirmation email.", booking.id)
        return

    def _send():
        subject = "Your Bike Booking is Confirmed!"

        # 🔹 Get the price of the selected bike
        bike_price = None
        try:
            bike = BikeCollections.objects.get(name=booking.prefered_bike)
            bike_price = bike.price
        except BikeCollections.DoesNotExist:
            logger.warning("Bike %s not found in collections.", booking.prefered_bike)

        # 🔹 Pass price into the email context
        context = {
            'booking': booking,
            'bike_price': bike_price,
        }

        text_body = render_to_string('emails/booking_confirmation.txt', context)
        html_body = render_to_string('emails/booking_confirmation.html', context)

        msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, [booking.email])
        msg.attach_alternative(html_body, "text/html")
        try:
            msg.send()
            logger.info("✅ Booking confirmation email sent to %s", booking.email)
        except Exception as e:
            logger.exception("❌ Failed to send booking email to %s: %s", booking.email, e)

    transaction.on_commit(_send)


# ------------------------------------------------------
# 3. Test-ride confirmation email
# ------------------------------------------------------
@receiver(post_save, sender=Testride)
def send_testride_confirmation(sender, instance, created, **kwargs):
    if not created:
        return

    ride = instance  # this is the newly created test ride

    if not ride.email:
        logger.info("No email for testride %s — skipping confirmation email.", ride.id)
        return

    def _send():
        subject = "Your Test-Ride is Confirmed!"
        
        # ✅ Make sure the context key matches your template
        context = {
            'testride': ride,  # this key must be 'testride'
            'user': ride.username,  # optional if you want to show username separately
            'bike_price': 1000  # you can pass dynamic price if needed
        }

        text_body = render_to_string('emails/testride_confirmation.txt', context)
        html_body = render_to_string('emails/testride_confirmation.html', context)

        msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, [ride.email])
        msg.attach_alternative(html_body, "text/html")
        try:
            msg.send()
            logger.info("✅ Test-ride confirmation email sent to %s", ride.email)
        except Exception as e:
            logger.exception("❌ Failed to send testride email to %s: %s", ride.email, e)

    transaction.on_commit(_send)

