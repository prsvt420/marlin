from typing import Dict

from django.utils.translation import gettext_lazy as _

from apps.catalog.dataclasses import OrderingOption

ORDERING_OPTIONS: Dict[str, OrderingOption] = {
    "": OrderingOption(None, _("Default")),
    "price_asc": OrderingOption("final_price", _("Cheapest first")),
    "price_desc": OrderingOption("-final_price", _("Most expensive first")),
    "discount": OrderingOption("-discount", _("By discount amount")),
}
