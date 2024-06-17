from django import forms

from menenger.models import Content


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})


class ContentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Content

        exclude = ('author', 'count_views', 'published',)


class PublishedContentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Content
        fields = ('published',)

