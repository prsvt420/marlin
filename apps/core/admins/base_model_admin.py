from unfold.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    list_per_page = 25
    empty_value_display = "—"
    list_filter_submit = True
