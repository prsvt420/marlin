from __future__ import annotations

from typing import Any, Optional

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(raw_password=password)  # type: ignore
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email=email, password=password, **extra_fields)
