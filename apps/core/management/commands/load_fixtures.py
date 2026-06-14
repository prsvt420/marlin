from pathlib import Path
from runpy import run_path
from typing import Any, Dict, List, Optional, Tuple

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

FIXTURE_PATHS: Tuple[str, ...] = (
    "init/categories.json",
    "demo/products.json",
    "demo/product_nutritions.json",
    "demo/product_images.json",
    "demo/users.json",
    "demo/carts.json",
    "demo/cart_items.json",
    "demo/orders.json",
    "demo/order_items.json",
    "demo/product_reviews.json",
)

RELATED_FIXTURES_GENERATOR: Path = (
    Path(settings.BASE_DIR)
    / "fixtures"
    / "demo"
    / "generate_users_orders_reviews.py"
)


class Command(BaseCommand):
    help = "Generate related demo fixtures and load all project fixtures."

    def handle(self, *args: Any, **options: Any) -> None:
        self._generate_related_fixtures()
        self._validate_fixture_files()

        call_command(
            "loaddata",
            *FIXTURE_PATHS,
            verbosity=options["verbosity"],
        )

        self.stdout.write(
            self.style.SUCCESS("All fixtures loaded successfully.")
        )

    def _generate_related_fixtures(self) -> None:
        if not RELATED_FIXTURES_GENERATOR.is_file():
            raise CommandError(
                "Fixture generator not found: " f"{RELATED_FIXTURES_GENERATOR}"
            )

        namespace: Dict[str, Any] = run_path(str(RELATED_FIXTURES_GENERATOR))
        generator: Optional[Any] = namespace.get("main")
        if not callable(generator):
            raise CommandError(
                "Fixture generator does not expose a callable main()."
            )

        generator()
        self.stdout.write("Related demo fixtures generated.")

    def _validate_fixture_files(self) -> None:
        fixture_root: Path = Path(settings.BASE_DIR) / "fixtures"
        missing_files: List[str] = [
            fixture_path
            for fixture_path in FIXTURE_PATHS
            if not (fixture_root / fixture_path).is_file()
        ]
        if missing_files:
            missing_list: str = ", ".join(missing_files)
            raise CommandError(f"Fixture files not found: {missing_list}")
