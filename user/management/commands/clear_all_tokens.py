from django.core.management.base import BaseCommand
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class Command(BaseCommand):
    help = 'Clears all outstanding tokens and the token blacklist'

    def handle(self, *args, **options):
        # Revoke outstanding tokens
        OutstandingToken.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully revoked all outstanding tokens'))

        # Clear token blacklist
        BlacklistedToken.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared the token blacklist'))
