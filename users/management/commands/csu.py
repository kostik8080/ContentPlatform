from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            phone="+79280096181",
            email="kostik80_80@mail.ru",
            first_name="admin",
            last_name="admin",
            is_staff=True,
            is_superuser=True,

        )

        user.set_password("12345")
        user.save()
