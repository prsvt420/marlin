from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

FIXTURE_DIR = Path(__file__).resolve().parent
PRODUCTS_PATH = FIXTURE_DIR / "products.json"
USERS_PATH = FIXTURE_DIR / "users.json"
CARTS_PATH = FIXTURE_DIR / "carts.json"
CART_ITEMS_PATH = FIXTURE_DIR / "cart_items.json"
ORDERS_PATH = FIXTURE_DIR / "orders.json"
ORDER_ITEMS_PATH = FIXTURE_DIR / "order_items.json"
REVIEWS_PATH = FIXTURE_DIR / "product_reviews.json"

ORDER_SIZE = 12


@dataclass(frozen=True)
class UserSpec:
    last_name: str
    first_name: str
    middle_name: str
    email: str
    address: str

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.middle_name}"


USERS = [
    UserSpec(
        "Иванов",
        "Александр",
        "Сергеевич",
        "alexander.ivanov@example.com",
        "г. Иркутск, ул. Ленина, д. 18, кв. 42",
    ),
    UserSpec(
        "Смирнова",
        "Елена",
        "Андреевна",
        "elena.smirnova@example.com",
        "г. Иркутск, ул. Байкальская, д. 107, кв. 15",
    ),
    UserSpec(
        "Кузнецов",
        "Дмитрий",
        "Олегович",
        "dmitry.kuznetsov@example.com",
        "г. Иркутск, ул. Советская, д. 58, кв. 21",
    ),
    UserSpec(
        "Попова",
        "Анна",
        "Викторовна",
        "anna.popova@example.com",
        "г. Иркутск, мкр. Университетский, д. 46, кв. 8",
    ),
    UserSpec(
        "Васильев",
        "Максим",
        "Игоревич",
        "maxim.vasiliev@example.com",
        "г. Иркутск, ул. Карла Либкнехта, д. 121, кв. 36",
    ),
    UserSpec(
        "Петрова",
        "Мария",
        "Алексеевна",
        "maria.petrova@example.com",
        "г. Иркутск, ул. Декабрьских Событий, д. 85, кв. 14",
    ),
    UserSpec(
        "Соколов",
        "Артём",
        "Михайлович",
        "artem.sokolov@example.com",
        "г. Иркутск, ул. Трилиссера, д. 92, кв. 27",
    ),
    UserSpec(
        "Михайлова",
        "Ольга",
        "Романовна",
        "olga.mikhailova@example.com",
        "г. Иркутск, ул. Красноказачья, д. 74, кв. 19",
    ),
    UserSpec(
        "Новиков",
        "Илья",
        "Павлович",
        "ilya.novikov@example.com",
        "г. Иркутск, ул. Лермонтова, д. 275, кв. 51",
    ),
    UserSpec(
        "Фёдорова",
        "Наталья",
        "Дмитриевна",
        "natalia.fedorova@example.com",
        "г. Иркутск, ул. Ржанова, д. 45/3, кв. 24",
    ),
    UserSpec(
        "Морозов",
        "Егор",
        "Владимирович",
        "egor.morozov@example.com",
        "г. Иркутск, ул. Ядринцева, д. 29, кв. 11",
    ),
    UserSpec(
        "Волкова",
        "Татьяна",
        "Сергеевна",
        "tatiana.volkova@example.com",
        "г. Иркутск, ул. Александра Невского, д. 99/2, кв. 43",
    ),
    UserSpec(
        "Алексеев",
        "Никита",
        "Андреевич",
        "nikita.alekseev@example.com",
        "г. Иркутск, ул. Верхняя Набережная, д. 165/4, кв. 30",
    ),
    UserSpec(
        "Лебедева",
        "Светлана",
        "Олеговна",
        "svetlana.lebedeva@example.com",
        "г. Иркутск, ул. Партизанская, д. 112, кв. 17",
    ),
    UserSpec(
        "Семёнов",
        "Кирилл",
        "Александрович",
        "kirill.semenov@example.com",
        "г. Иркутск, ул. Пискунова, д. 142/5, кв. 9",
    ),
    UserSpec(
        "Егорова",
        "Ирина",
        "Валерьевна",
        "irina.egorova@example.com",
        "г. Иркутск, ул. Омулевского, д. 20/1, кв. 48",
    ),
    UserSpec(
        "Павлов",
        "Михаил",
        "Евгеньевич",
        "mikhail.pavlov@example.com",
        "г. Иркутск, ул. Марата, д. 31, кв. 6",
    ),
    UserSpec(
        "Козлова",
        "Виктория",
        "Ильинична",
        "victoria.kozlova@example.com",
        "г. Иркутск, ул. Крылатый, д. 7, кв. 22",
    ),
    UserSpec(
        "Степанов",
        "Роман",
        "Денисович",
        "roman.stepanov@example.com",
        "г. Иркутск, ул. Сибирская, д. 23, кв. 33",
    ),
    UserSpec(
        "Николаева",
        "Ксения",
        "Максимовна",
        "ksenia.nikolaeva@example.com",
        "г. Иркутск, ул. Рабочего Штаба, д. 78, кв. 12",
    ),
    UserSpec(
        "Орлов",
        "Андрей",
        "Константинович",
        "andrey.orlov@example.com",
        "г. Иркутск, ул. Розы Люксембург, д. 217, кв. 45",
    ),
    UserSpec(
        "Андреева",
        "Дарья",
        "Павловна",
        "daria.andreeva@example.com",
        "г. Иркутск, ул. Седова, д. 65А, кв. 18",
    ),
    UserSpec(
        "Макаров",
        "Владислав",
        "Сергеевич",
        "vladislav.makarov@example.com",
        "г. Иркутск, ул. Гоголя, д. 53, кв. 29",
    ),
    UserSpec(
        "Захарова",
        "Юлия",
        "Игоревна",
        "yulia.zakharova@example.com",
        "г. Иркутск, ул. Мухиной, д. 10, кв. 37",
    ),
    UserSpec(
        "Зайцев",
        "Денис",
        "Анатольевич",
        "denis.zaitsev@example.com",
        "г. Иркутск, ул. Маршала Конева, д. 38, кв. 10",
    ),
    UserSpec(
        "Беляева",
        "Алина",
        "Романовна",
        "alina.belyaeva@example.com",
        "г. Иркутск, ул. Клары Цеткин, д. 14, кв. 26",
    ),
    UserSpec(
        "Громов",
        "Станислав",
        "Юрьевич",
        "stanislav.gromov@example.com",
        "г. Иркутск, ул. Поленова, д. 35, кв. 7",
    ),
    UserSpec(
        "Тихонова",
        "Екатерина",
        "Вадимовна",
        "ekaterina.tikhonova@example.com",
        "г. Иркутск, ул. 4-я Советская, д. 49, кв. 16",
    ),
    UserSpec(
        "Крылов",
        "Арсений",
        "Петрович",
        "arseniy.krylov@example.com",
        "г. Иркутск, ул. Дальневосточная, д. 144, кв. 31",
    ),
    UserSpec(
        "Комарова",
        "Вероника",
        "Александровна",
        "veronika.komarova@example.com",
        "г. Иркутск, ул. Багратиона, д. 54/1, кв. 20",
    ),
]


def fixture_timestamp(value: datetime) -> str:
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def write_fixture(path: Path, data: list[dict]) -> None:
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    temporary_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def build_users() -> list[dict]:
    users = []
    joined_at = datetime(2026, 1, 10, 7, 0, tzinfo=timezone.utc)
    for index, spec in enumerate(USERS, start=1):
        date_joined = joined_at + timedelta(days=index * 2, hours=index % 7)
        users.append(
            {
                "model": "accounts.user",
                "pk": index,
                "fields": {
                    "password": "!",  # noqa: S105
                    "last_login": None,
                    "is_superuser": False,
                    "email": spec.email,
                    "phone_number": f"+7900000{index:04d}",
                    "first_name": spec.first_name,
                    "last_name": spec.last_name,
                    "middle_name": spec.middle_name,
                    "is_staff": False,
                    "is_active": True,
                    "date_joined": fixture_timestamp(date_joined),
                    "groups": [],
                    "user_permissions": [],
                },
            }
        )
    return users


def review_count(product_pk: int) -> int:
    return 6 + ((product_pk * 7 + 3) % 20)


def review_rating(product_pk: int, user_pk: int) -> int:
    score = (product_pk * 29 + user_pk * 17) % 100
    if score < 2:
        return 1
    if score < 7:
        return 2
    if score < 18:
        return 3
    if score < 58:
        return 4
    return 5


def review_assignments(
    products: list[dict],
) -> dict[int, list[tuple[int, int]]]:
    assignments: dict[int, list[tuple[int, int]]] = defaultdict(list)
    user_count = len(USERS)
    for product in products:
        product_pk = int(product["pk"])
        count = review_count(product_pk)
        start = (product_pk * 11) % user_count
        for offset in range(count):
            user_pk = (start + offset * 7) % user_count + 1
            rating = review_rating(product_pk, user_pk)
            assignments[user_pk].append((product_pk, rating))
    return assignments


def order_quantity(product: dict, user_pk: int) -> Decimal:
    fields = product["fields"]
    if fields.get("weight_step") is not None:
        step = Decimal(fields["weight_step"])
        if step >= Decimal("1.00"):
            multipliers = (Decimal("1"), Decimal("1"), Decimal("2"))
        elif step >= Decimal("0.50"):
            multipliers = (Decimal("1"), Decimal("2"), Decimal("3"))
        else:
            multipliers = (Decimal("2"), Decimal("5"), Decimal("10"))

        return (
            step * multipliers[(int(product["pk"]) + user_pk) % 3]
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    return (Decimal("1.00"), Decimal("1.00"), Decimal("2.00"))[
        (int(product["pk"]) + user_pk) % 3
    ]


def build_related_fixtures(
    products: list[dict],
) -> tuple[list[dict], list[dict], list[dict], list[dict], list[dict]]:
    products_by_pk = {int(item["pk"]): item for item in products}
    assignments = review_assignments(products)
    carts = []
    cart_items = []
    orders = []
    order_items = []
    reviews = []
    order_pk = 1
    cart_item_pk = 1
    order_item_pk = 1
    review_pk = 1
    order_base = datetime(2026, 6, 2, 9, 0, tzinfo=timezone.utc)

    for user_pk, purchases in sorted(assignments.items()):
        user = USERS[user_pk - 1]
        purchases.sort(key=lambda item: item[0])
        for chunk_index in range(0, len(purchases), ORDER_SIZE):
            chunk = purchases[
                chunk_index : chunk_index + ORDER_SIZE  # noqa: E203
            ]
            order_created_at = order_base + timedelta(
                minutes=(order_pk - 1) * 90
            )
            total_price = Decimal("0.00")
            pending_items = []

            for product_pk, rating in chunk:
                product = products_by_pk[product_pk]
                quantity = order_quantity(product, user_pk)
                price = Decimal(product["fields"]["final_price"])
                line_total = (price * quantity).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                )
                total_price += line_total
                pending_items.append(
                    (product_pk, product, quantity, price, line_total, rating)
                )

            delivery_method = (
                "courier" if (order_pk + user_pk) % 3 else "pickup"
            )
            cart_created_at = order_created_at - timedelta(
                hours=2 + (order_pk % 5)
            )
            cart_updated_at = order_created_at - timedelta(minutes=5)
            carts.append(
                {
                    "model": "carts.cart",
                    "pk": order_pk,
                    "fields": {
                        "created_at": fixture_timestamp(cart_created_at),
                        "updated_at": fixture_timestamp(cart_updated_at),
                        "user": user_pk,
                        "cart_status": "converted",
                    },
                }
            )
            order_timestamp = fixture_timestamp(order_created_at)
            orders.append(
                {
                    "model": "orders.order",
                    "pk": order_pk,
                    "fields": {
                        "created_at": order_timestamp,
                        "updated_at": order_timestamp,
                        "user": user_pk,
                        "cart": order_pk,
                        "order_status": "completed",
                        "delivery_method": delivery_method,
                        "delivery_address": (
                            user.address
                            if delivery_method == "courier"
                            else ""
                        ),
                        "payment_status": "paid",
                        "payment_method": (
                            "online" if order_pk % 2 else "on_delivery"
                        ),
                        "comment": "",
                        "recipient_name": user.full_name,
                        "recipient_email": user.email,
                        "recipient_phone_number": f"+7900000{user_pk:04d}",
                        "total_price": f"{total_price:.2f}",
                        "number": f"ORD-2026-{order_pk:06d}",
                    },
                }
            )

            for (
                product_pk,
                product,
                quantity,
                price,
                line_total,
                rating,
            ) in pending_items:
                cart_item_created_at = cart_created_at + timedelta(
                    minutes=cart_item_pk % 90
                )
                cart_items.append(
                    {
                        "model": "carts.cartitem",
                        "pk": cart_item_pk,
                        "fields": {
                            "created_at": fixture_timestamp(
                                cart_item_created_at
                            ),
                            "updated_at": fixture_timestamp(cart_updated_at),
                            "cart": order_pk,
                            "product": product_pk,
                            "quantity": f"{quantity:.2f}",
                            "price_snapshot": f"{price:.2f}",
                            "total_price": f"{line_total:.2f}",
                        },
                    }
                )
                item_timestamp = fixture_timestamp(
                    order_created_at + timedelta(minutes=order_item_pk % 45)
                )
                order_items.append(
                    {
                        "model": "orders.orderitem",
                        "pk": order_item_pk,
                        "fields": {
                            "created_at": item_timestamp,
                            "updated_at": item_timestamp,
                            "order": order_pk,
                            "product": product_pk,
                            "quantity": f"{quantity:.2f}",
                            "product_name_snapshot": product["fields"][
                                "name_ru"
                            ],
                            "price_snapshot": f"{price:.2f}",
                            "total_price": f"{line_total:.2f}",
                        },
                    }
                )
                review_created_at = order_created_at + timedelta(
                    days=2 + (product_pk + user_pk) % 18,
                    minutes=review_pk % 50,
                )
                reviews.append(
                    {
                        "model": "reviews.productreview",
                        "pk": review_pk,
                        "fields": {
                            "created_at": fixture_timestamp(review_created_at),
                            "updated_at": fixture_timestamp(review_created_at),
                            "user": user_pk,
                            "product": product_pk,
                            "rating": rating,
                        },
                    }
                )
                cart_item_pk += 1
                order_item_pk += 1
                review_pk += 1
            order_pk += 1

    return carts, cart_items, orders, order_items, reviews


def main() -> None:
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    users = build_users()
    carts, cart_items, orders, order_items, reviews = build_related_fixtures(
        products
    )
    write_fixture(USERS_PATH, users)
    write_fixture(CARTS_PATH, carts)
    write_fixture(CART_ITEMS_PATH, cart_items)
    write_fixture(ORDERS_PATH, orders)
    write_fixture(ORDER_ITEMS_PATH, order_items)
    write_fixture(REVIEWS_PATH, reviews)
    print(
        f"Generated {len(users)} users, {len(carts)} carts, "
        f"{len(cart_items)} cart items, {len(orders)} orders, "
        f"{len(order_items)} order items and {len(reviews)} reviews"
    )


if __name__ == "__main__":
    main()
