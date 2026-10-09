from getpass import getpass

from django.core.management.base import BaseCommand, CommandError

from apps.users.models import User


class Command(BaseCommand):
    help = "Create the default local admin account for dashboard access."

    def handle(self, *args, **options):
        email = "admin@skillbase.local"
        password = getpass("Password: ")
        password_confirmation = getpass("Password (again): ")

        if not password:
            raise CommandError("Password cannot be empty.")
        if password != password_confirmation:
            raise CommandError("The two passwords did not match.")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "role": "admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if not created:
            user.role = "admin"
            user.is_staff = True
            user.is_superuser = True

        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin account ready for email: {email}"
            )
        )
