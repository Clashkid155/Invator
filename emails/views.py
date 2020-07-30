from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage, BadHeaderError
from django.contrib.auth.decorators import login_required
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from root.settings import SENDGRID_API_KEY
from django.conf import settings
from .models import Emails
from .forms import EmailsForm

'''
def send_email(subject, message, sender, recipient, attach):
	email = EmailMessage(
			subject,
			message,
			sender,
			recipient
		)
	email.attach(attach.name, attach.read(), attach.content_type)
	return email
'''

#@login_required
def email_invoice(request):
	form = EmailsForm()
	if request.method == "POST":
		form = EmailsForm(request.POST, request.FILES)
		if form.is_valid():
			print("Form works!")
			subject = f'Message from {form.cleaned_data["name"]}'
			message = form.cleaned_data["message"]
			sender = settings.EMAIL_HOST_USER
			recipient = form.cleaned_data["recipient"]
			files = request.FILES.getlist("attach")
			try:
				mail = EmailMessage(subject, message, sender, [recipient])
				for f in files:
					mail.attach(f.name, f.read(), f.content_type)
				mail.send()
				sg = SendGridAPIClient(SENDGRID_API_KEY)
				sg.send(mail)
			except BadHeaderError:
				return HttpResponse("Invalid header found!")
			return HttpResponse("Success... Your email has been sent!")
	return render(request, "emails.html", {'form': form})



