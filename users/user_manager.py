from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Normalize the email address by lowercasing the domain part of it
        email = self.normalize_email(email)

        # Create a new user instance
        user = self.model(email=email, **extra_fields)

        # Set the user's password
        user.set_password(password)

        # Save the user to the database
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create a regular user with the provided email and password
        user = self.create_user(email=email, password=password, **extra_fields)

        # Set additional fields for the superuser
        user.is_staff = True
        user.is_superuser = True

        # Save the user to the database
        user.save()

        return user