import json
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Any, Dict, List

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, DecimalField, Q, Sum, Value
from django.db.models.functions import Coalesce, TruncDate
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.carts.choices import CartStatus
from apps.carts.models import Cart
from apps.catalog.models import Product
from apps.orders.choices import OrderStatus, PaymentStatus
from apps.orders.models import Order, OrderItem

DASHBOARD_DAYS = 30
MONEY_OUTPUT_FIELD: DecimalField = DecimalField(
    max_digits=14,
    decimal_places=2,
)


def _format_currency(value: Decimal) -> str:
    formatted = f"{value:,.2f}".replace(",", " ").replace(".", ",")
    return f"{formatted} ₽"


def _period_start(today: date) -> datetime:
    start_date = today - timedelta(days=DASHBOARD_DAYS - 1)
    return timezone.make_aware(
        datetime.combine(start_date, time.min),
        timezone.get_current_timezone(),
    )


def _empty_money() -> Value:
    return Value(Decimal("0.00"), output_field=MONEY_OUTPUT_FIELD)


def _chart_data(
    *,
    labels: List[str],
    values: List[float | int],
    label: str,
    color: str,
    suffix: str = "",
) -> str:
    return json.dumps(
        {
            "labels": labels,
            "datasets": [
                {
                    "label": label,
                    "data": values,
                    "borderColor": color,
                    "backgroundColor": color,
                    "displayYAxis": True,
                    "suffixYAxis": suffix,
                    "maxTicksXLimit": 10,
                }
            ],
        },
        ensure_ascii=False,
    )


def _daily_series(
    *,
    today: date,
    rows: Dict[date, Decimal | int],
) -> tuple[List[str], List[Decimal | int]]:
    days = [
        today - timedelta(days=offset)
        for offset in reversed(range(DASHBOARD_DAYS))
    ]
    labels = [day.strftime("%d.%m") for day in days]
    values = [rows.get(day, 0) for day in days]
    return labels, values


def _get_dashboard_data() -> Dict[str, Any]:
    today = timezone.localdate()
    today_start = timezone.make_aware(
        datetime.combine(today, time.min),
        timezone.get_current_timezone(),
    )
    period_start = _period_start(today)

    period_orders = Order.objects.filter(created_at__gte=period_start)
    paid_filter = Q(payment_status=PaymentStatus.PAID) & ~Q(
        order_status=OrderStatus.CANCELLED
    )

    period_summary = period_orders.aggregate(
        orders=Count("id"),
        revenue=Coalesce(
            Sum("total_price", filter=paid_filter),
            _empty_money(),
            output_field=MONEY_OUTPUT_FIELD,
        ),
        average_order=Coalesce(
            Avg("total_price", filter=paid_filter),
            _empty_money(),
            output_field=MONEY_OUTPUT_FIELD,
        ),
        cancelled=Count(
            "id",
            filter=Q(order_status=OrderStatus.CANCELLED),
        ),
    )
    today_summary = Order.objects.filter(
        created_at__gte=today_start
    ).aggregate(
        orders=Count("id"),
        revenue=Coalesce(
            Sum("total_price", filter=paid_filter),
            _empty_money(),
            output_field=MONEY_OUTPUT_FIELD,
        ),
    )

    carts_summary = Cart.objects.filter(
        created_at__gte=period_start
    ).aggregate(
        total=Count("id"),
        converted=Count(
            "id",
            filter=Q(cart_status=CartStatus.CONVERTED),
        ),
        active=Count(
            "id",
            filter=Q(cart_status=CartStatus.ACTIVE),
        ),
    )
    conversion = (
        round(carts_summary["converted"] / carts_summary["total"] * 100, 1)
        if carts_summary["total"]
        else 0
    )

    daily_orders = {
        row["day"]: row["total"]
        for row in period_orders.annotate(
            day=TruncDate(
                "created_at",
                tzinfo=timezone.get_current_timezone(),
            )
        )
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    }
    daily_revenue = {
        row["day"]: row["total"]
        for row in period_orders.filter(paid_filter)
        .annotate(
            day=TruncDate(
                "created_at",
                tzinfo=timezone.get_current_timezone(),
            )
        )
        .values("day")
        .annotate(
            total=Coalesce(
                Sum("total_price"),
                _empty_money(),
                output_field=MONEY_OUTPUT_FIELD,
            )
        )
        .order_by("day")
    }
    chart_labels, order_values = _daily_series(
        today=today,
        rows=daily_orders,
    )
    revenue_labels, revenue_values = _daily_series(
        today=today,
        rows=daily_revenue,
    )

    status_counts = {
        row["order_status"]: row["total"]
        for row in period_orders.values("order_status").annotate(
            total=Count("id")
        )
    }
    total_orders = period_summary["orders"]
    status_rows = []
    for status, label in OrderStatus.choices:
        count = status_counts.get(status, 0)
        share = round(count / total_orders * 100, 1) if total_orders else 0
        status_rows.append([str(label), count, f"{share}%"])

    top_products = (
        OrderItem.objects.filter(
            order__created_at__gte=period_start,
            order__payment_status=PaymentStatus.PAID,
        )
        .exclude(order__order_status=OrderStatus.CANCELLED)
        .values("product_name_snapshot")
        .annotate(
            sold_quantity=Sum("quantity"),
            revenue=Sum("total_price"),
        )
        .order_by("-revenue")[:5]
    )
    top_product_rows = [
        [
            row["product_name_snapshot"],
            row["sold_quantity"],
            _format_currency(row["revenue"]),
        ]
        for row in top_products
    ]

    low_stock_products = Product.objects.filter(
        is_active=True,
        stock__lte=10,
    ).order_by("stock", "name")[:5]
    low_stock_rows = [
        [
            product.name,
            product.stock,
            str(product.get_unit_type_display()),
        ]
        for product in low_stock_products
    ]

    latest_orders = Order.objects.select_related("user").all()[:8]
    latest_order_rows = [
        [
            order.number,
            order.user.email,
            str(order.get_order_status_display()),
            _format_currency(order.total_price),
            timezone.localtime(order.created_at).strftime("%d.%m.%Y %H:%M"),
        ]
        for order in latest_orders
    ]

    metrics = [
        {
            "title": _("Revenue today"),
            "value": _format_currency(today_summary["revenue"]),
            "description": _("%(count)s orders")
            % {"count": today_summary["orders"]},
            "icon": "payments",
        },
        {
            "title": _("Revenue for 30 days"),
            "value": _format_currency(period_summary["revenue"]),
            "description": _("%(count)s orders")
            % {"count": period_summary["orders"]},
            "icon": "monitoring",
        },
        {
            "title": _("Average order"),
            "value": _format_currency(period_summary["average_order"]),
            "description": _("Paid orders for 30 days"),
            "icon": "receipt_long",
        },
        {
            "title": _("New users"),
            "value": get_user_model()
            .objects.filter(date_joined__gte=period_start)
            .count(),
            "description": _("For the last 30 days"),
            "icon": "person_add",
        },
        {
            "title": _("Cart conversion"),
            "value": f"{conversion}%",
            "description": _("%(count)s converted carts")
            % {"count": carts_summary["converted"]},
            "icon": "shopping_cart_checkout",
        },
        {
            "title": _("Active carts"),
            "value": carts_summary["active"],
            "description": _("%(count)s cancelled orders")
            % {"count": period_summary["cancelled"]},
            "icon": "shopping_cart",
        },
    ]

    return {
        "metrics": metrics,
        "orders_chart": _chart_data(
            labels=chart_labels,
            values=[int(value) for value in order_values],
            label=str(_("Orders")),
            color="var(--color-primary-600)",
        ),
        "revenue_chart": _chart_data(
            labels=revenue_labels,
            values=[float(value) for value in revenue_values],
            label=str(_("Revenue")),
            color="var(--color-green-600)",
            suffix="₽",
        ),
        "status_table": {
            "headers": [_("Status"), _("Orders"), _("Share")],
            "rows": status_rows,
        },
        "top_products_table": {
            "headers": [_("Product"), _("Quantity"), _("Revenue")],
            "rows": top_product_rows,
        },
        "low_stock_table": {
            "headers": [_("Product"), _("Stock"), _("Unit")],
            "rows": low_stock_rows,
        },
        "latest_orders_table": {
            "headers": [
                _("Number"),
                _("Customer"),
                _("Status"),
                _("Total"),
                _("Created"),
            ],
            "rows": latest_order_rows,
        },
    }


def dashboard_callback(
    request: HttpRequest,
    context: Dict[str, Any],
) -> Dict[str, Any]:
    if not request.user.has_perm("orders.view_order"):
        context["dashboard"] = None
        return context

    context["dashboard"] = _get_dashboard_data()
    return context
