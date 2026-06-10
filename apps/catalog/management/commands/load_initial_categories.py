from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.catalog.models import Category


class Command(BaseCommand):
    help = "Load initial categories if the category table is empty."

    def handle(self, *args: Any, **options: Any) -> None:
        if Category.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Categories already exist. Fixture loading skipped."
                )
            )
            return

        call_command(
            "loaddata",
            "init/categories.json",
            verbosity=options["verbosity"],
        )
        self.stdout.write(
            self.style.SUCCESS("Initial categories loaded successfully.")
        )
