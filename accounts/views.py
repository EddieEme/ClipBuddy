from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.urls import reverse


User = get_user_model()

# Password Reset Request View
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)  # Query CustomUser model
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                 # Debugging output for uid and token
                print(f"UID: {uid}, Token: {token}")

                # Ensure the correct use of reverse with uid and token
                reset_link = request.build_absolute_uri(reverse("accounts:password_reset_confirm", kwargs={"uidb64": uid, "token": token}))

                # Debugging output for reset link
                print(f"Reset link: {reset_link}")

                # Send email
                subject = "Password Reset Request"
                message = render_to_string("accounts/password_reset_email.html", {
                    "user": user,
                    "domain": request.get_host(),
                    "protocol": "https" if request.is_secure() else "http",
                    "uidb64": uid,
                    "token": token,
                })
                send_mail(subject, message, "noreply@example.com", [user.email])

                messages.success(request, "Password reset link has been sent to your email.")
            except User.DoesNotExist:
                messages.error(request, "No user found with this email.")

            return redirect("accounts:password_reset")  # Ensure correct namespace

    else:
        form = PasswordResetForm()

    return render(request, "accounts/password_reset_form.html", {"form": form})


# Password Reset Done View
def password_reset_done(request):
    return render(request, "accounts/password_reset_done.html")


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been successfully reset.")
                return redirect("accounts:password_reset_complete")  # Ensure namespace is correct
        else:
            form = SetPasswordForm(user)

        return render(request, "accounts/password_reset_confirm.html", {"form": form})

    messages.error(request, "The password reset link is invalid or has expired.")
    return redirect("accounts:password_reset")


# Password Reset Complete View
def password_reset_complete(request):
    messages.success(request, "Your password has been successfully reset. You can now log in with your new password.")
    return redirect(reverse('clipapp:login'))
