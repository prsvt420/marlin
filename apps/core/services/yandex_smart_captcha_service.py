from typing import Any, Dict, Optional

import requests
from django.http import HttpRequest
from ipware import get_client_ip

from config import settings


class YandexSmartCaptchaService:

    def validate_captcha(self, request: HttpRequest) -> bool:
        token: Optional[str] = request.POST.get("smart-token")

        if not token:
            return False

        client_ip: str = get_client_ip(request=request)[0]

        try:
            response: requests.Response = requests.get(
                url=settings.YANDEX_SMART_CAPTCHA_VALIDATE_URL,
                params={
                    "secret": settings.YANDEX_SMART_CAPTCHA_SERVER_KEY,
                    "token": token,
                    "ip": client_ip,
                },
                timeout=1,
            )
            response.raise_for_status()

            response_json: Dict[str, Any] = response.json()
            return response_json.get("status") == "ok"
        except (requests.RequestException, ValueError):
            return False
