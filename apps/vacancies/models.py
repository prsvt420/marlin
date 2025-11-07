from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from apps.vacancies.choices import ExperienceLevel, WorkSchedule


class Vacancy(models.Model):
    """Model representing a job vacancy.

    Each record stores information about a single job opening:
    title, descriptions, professional area, location, work schedule,
    experience requirements, salary range, and activity status.

    Attributes:
        title (CharField): Vacancy title.
        short_description (TextField): Brief introduction about the vacancy.
        description (TextField): Detailed vacancy description with HTML markup.
        professional_area (ForeignKey): Professional field.
        city (ForeignKey): City and region where the vacancy is located.
        work_schedule (CharField): Work schedule (full-time, part-time, etc.).
        experience_level (CharField): Required work experience level.
        salary_from (PositiveIntegerField): Minimum salary.
        salary_to (PositiveIntegerField): Maximum salary.
        is_active (BooleanField): Whether the vacancy is active and visible.
        created_at (DateTimeField): Date and time when the vacancy was created.
        updated_at (DateTimeField): Date and time when the vacancy was last
        updated.
    """

    title = models.CharField(
        max_length=255,
        verbose_name="заголовок",
        help_text="Заголовок вакансии.",
    )
    short_description = models.TextField(
        verbose_name="краткое описание",
        help_text="Вступительный текст о вакансии (обычный текст).",
    )
    description = models.TextField(
        verbose_name="описание",
        help_text="Подробное описание вакансии "
        "(HTML-разметка, используйте div, ul, h3, li).",
    )
    professional_area = models.ForeignKey(
        to="ProfessionalArea",
        on_delete=models.CASCADE,
        related_name="vacancies",
        verbose_name="профессиональная область",
        help_text="Профессиональная область вакансии.",
    )
    city = models.ForeignKey(
        to="City",
        on_delete=models.CASCADE,
        related_name="vacancies",
        verbose_name="город и регион",
        help_text="Город и регион размещения вакансии.",
    )
    work_schedule = models.CharField(
        max_length=10,
        choices=WorkSchedule.choices,
        default=WorkSchedule.FULL_TIME,
        verbose_name="график работы",
        help_text="Предполагаемый режим работы.",
    )
    experience_level = models.CharField(
        max_length=10,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.NO_EXPERIENCE,
        verbose_name="опыт работы",
        help_text="Требуемый для работы опыт.",
    )
    salary_from = models.PositiveIntegerField(
        verbose_name="зарплата от",
        help_text="Минимальная зарплата.",
        null=True,
        blank=True,
    )
    salary_to = models.PositiveIntegerField(
        verbose_name="зарплата до",
        help_text="Максимальная зарплата.",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="активна",
        help_text="Определяет, активна ли вакансия.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания",
        help_text="Дата и время добавления вакансии.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="дата обновления",
        help_text="Дата и время последнего обновления вакансии.",
    )

    class Meta:  # noqa: D106
        db_table = "vacancies_vacancy"
        db_table_comment = "Таблица с информацией о вакансиях"
        verbose_name = "вакансия"
        verbose_name_plural = "вакансии"
        ordering = (
            "-created_at",
            "title",
        )

    def __str__(self) -> str:
        """Return a string representation of the vacancy.

        Returns:
            str: Vacancy title with city.
        """
        return f"{self.title} / {self.city}"

    def get_formatted_salary(self) -> str:
        """Return a formatted string representation of the salary range.

        Returns:
            str: Formatted salary range in format "X – Y", "от X",
            "до Y" or empty string if not specified.
        """
        if self.salary_from and self.salary_to:
            return f"{self.salary_from} – {self.salary_to}"
        elif self.salary_from:
            return f"от {self.salary_from}"
        elif self.salary_to:
            return f"до {self.salary_to}"
        return ""

    def clean(self) -> None:
        """Validate vacancy data."""
        super().clean()
        if self.salary_from and self.salary_to:
            if self.salary_from >= self.salary_to:
                raise ValidationError(
                    {
                        "salary_to": "Верхняя граница зарплаты "
                        "должна быть больше нижней"
                    }
                )

    def get_absolute_url(self) -> str:
        """Return the absolute URL for the vacancy detail page.

        Uses the vacancy id to reverse the URL named
        'vacancies:vacancy_detail'.

        Returns:
            str: The URL of the vacancy detail page.
        """
        return reverse("vacancies:vacancy_detail", kwargs={"pk": self.pk})


class ProfessionalArea(models.Model):
    """Model representing a professional field or industry.

    Each record stores information about a specific professional area.

    Attributes:
        name (CharField): Name of the professional area.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="название",
        help_text="Название профессиональной области.",
    )

    class Meta:  # noqa: D106
        db_table = "vacancies_professional_area"
        db_table_comment = "Таблица с информацией о профессиональных областях"
        verbose_name = "профессиональная область"
        verbose_name_plural = "профессиональные области"
        ordering = ("name",)

    def __str__(self) -> str:
        """Return a string representation of the professional area.

        Returns:
            str: Professional area name.
        """
        return f"{self.name}"


class City(models.Model):
    """Model representing a city with optional regional affiliation.

    Each record stores information about a city that can be linked to a region.

    Attributes:
        name (CharField): Name of the city.
        region (ForeignKey): Region to which the city belongs (optional).
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="название",
        help_text="Название города.",
    )
    region = models.ForeignKey(
        to="Region",
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name="регион",
        help_text="Регион, к которому относится город.",
        null=True,
        blank=True,
    )

    class Meta:  # noqa: D106
        db_table = "vacancies_city"
        db_table_comment = "Таблица с информацией о городах"
        verbose_name = "город"
        verbose_name_plural = "города"
        ordering = ("name",)

    def __str__(self) -> str:
        """Return a string representation of the city.

        Returns:
            str: City name with region if available.
        """
        if self.region:
            return f"г. {self.name}, {self.region.name}"
        return f"г. {self.name}"


class Region(models.Model):
    """Model representing a geographical region.

    Each record stores information about a region that can contain
    multiple cities.

    Attributes:
        name (CharField): Name of the region.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="название",
        help_text="Название региона.",
    )

    class Meta:  # noqa: D106
        db_table = "vacancies_region"
        db_table_comment = "Таблица с информацией о регионах"
        verbose_name = "регион"
        verbose_name_plural = "регионы"
        ordering = ("name",)

    def __str__(self) -> str:
        """Return a string representation of the region.

        Returns:
            str: Region name.
        """
        return f"{self.name}"
