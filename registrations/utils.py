import os
import random
import string
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings

def generate_unique_ticket_id():
    """Generates a unique ticket format e.g. EVT-2026-98A4B2"""
    from registrations.models import Ticket
    prefix = "EVT-2026-"
    while True:
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        ticket_id = f"{prefix}{random_suffix}"
        if not Ticket.objects.filter(ticket_id=ticket_id).exists():
            return ticket_id

def create_ticket_qr_code(ticket):
    """
    Generates a QR code image containing ticket details and assigns it to ticket.qr_code ImageField.
    """
    qr_data = (
        f"EventHub Digital Ticket\n"
        f"Ticket ID: {ticket.ticket_id}\n"
        f"Event: {ticket.registration.event.title}\n"
        f"Participant: {ticket.registration.participant.get_full_name() or ticket.registration.participant.username}\n"
        f"Date: {ticket.registration.event.date}\n"
        f"Location: {ticket.registration.event.location}"
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#6D28D9", back_color="#FFFFFF")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    file_name = f"qr_{ticket.ticket_id}.png"
    
    ticket.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
