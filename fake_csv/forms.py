from django import forms

from .models import Schema, Column


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ['name', 'separator', 'string_character']

    def __init__(self, *args, **kwargs):
        super(SchemaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['name', 'type', 'from_num', 'to_num', 'order']

    def __init__(self, *args, **kwargs):
        super(ColumnForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



