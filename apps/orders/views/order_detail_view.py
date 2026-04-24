from typing import Any, Dict, List, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from apps.orders.choices import OrderStatus
from apps.orders.models import Order
from apps.orders.selectors import OrderSelector


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "orders/order_detail.html"
    context_object_name = "order"
    ORDER_STATUS_FLOW = [
        OrderStatus.PENDING,
        OrderStatus.CONFIRMED,
        OrderStatus.ASSEMBLING,
        OrderStatus.SHIPPED,
        OrderStatus.COMPLETED,
    ]
    ORDER_STATUS_DICT = dict(OrderStatus.choices)

    def get_object(self, queryset: Optional[QuerySet[Order]] = None) -> Order:
        order_number: str = self.kwargs["order_number"]
        order: Optional[Order] = OrderSelector().get_order_by_number(
            order_number=order_number
        )

        if not order or not order.user == self.request.user:
            raise Http404

        return order

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": f"{_('Order')}",
                "url": reverse_lazy(
                    viewname="orders:detail",
                    kwargs={"order_number": self.object.number},
                ),
            },
        ]

        is_cancelled: bool = self.object.order_status == "cancelled"
        current_idx: int = (
            self.ORDER_STATUS_FLOW.index(self.object.order_status)
            if not is_cancelled
            else 0
        )

        steps: List[Dict[str, Any]] = []
        for idx, key in enumerate(self.ORDER_STATUS_FLOW):
            if is_cancelled and idx == 1:
                steps.append({"label": ["cancelled"], "state": "cancelled"})
            elif is_cancelled and idx == 0:
                steps.append(
                    {"label": self.ORDER_STATUS_DICT[key], "state": "done"}
                )
            elif is_cancelled:
                steps.append(
                    {"label": self.ORDER_STATUS_DICT[key], "state": "pending"}
                )
            elif idx < current_idx:
                steps.append(
                    {"label": self.ORDER_STATUS_DICT[key], "state": "done"}
                )
            elif idx == current_idx:
                steps.append(
                    {"label": self.ORDER_STATUS_DICT[key], "state": "current"}
                )
            else:
                steps.append(
                    {"label": self.ORDER_STATUS_DICT[key], "state": "pending"}
                )

        order_status_progress_percent = (
            current_idx if not is_cancelled else 1
        ) * 20

        context["order_status_steps"] = steps
        context["order_status_progress_percent"] = (
            order_status_progress_percent
        )

        return context
