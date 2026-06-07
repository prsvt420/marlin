from django import forms

from apps.reviews.models import ProductReview


class ProductReviewForm(forms.ModelForm):

    class Meta:
        model = ProductReview
        fields = ("rating",)
