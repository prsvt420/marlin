from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django_resized import ResizedImageField

from apps.core.models import BaseModel


class Category(BaseModel):  # type: ignore
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
        verbose_name=_("parent"),
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("name"),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_("slug"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("description"),
    )
    image = ResizedImageField(
        size=(1024, 1024),
        crop=None,
        quality=80,
        force_format="WEBP",
        upload_to="category_images/",
        keep_meta=False,
        blank=True,
        null=True,
        verbose_name=_("image"),
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("sort order"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=pgettext_lazy("feminine", "active"),
    )

    class Meta:
        db_table = "catalog_category"
        db_table_comment = "Table containing product categories."
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ("sort_order", "name")

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="catalog:product-list",
            kwargs={"category_slug": self.slug},
        )
