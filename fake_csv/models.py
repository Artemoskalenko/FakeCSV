from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Schema(models.Model):
    STRING_CHARACTER_CHOICES = (
        ("'", "Quote(')"),
        ("\"", "Double-quote(\")")
    )
    SEPARATOR_CHOICES = (
        (",", "Comma(,)"),
        (" ", "Space( )"),
        (";", "Semicolon(;)")
    )

    name = models.CharField(max_length=100)
    separator = models.CharField(max_length=1, choices=SEPARATOR_CHOICES,
                                 default=";", verbose_name="Column separator")
    string_character = models.CharField(max_length=1,
                                        choices=STRING_CHARACTER_CHOICES,
                                        default='"')
    modified = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Схема"
        verbose_name_plural = "Схемы"


class Column(models.Model):
    TYPES_CHOICES = (
                        ("Full name", "Full name"),
                        ("Job", "Job"),
                        ("Email", "Email"),
                        ("Domain name", "Domain name"),
                        ("Phone number", "Phone number"),
                        ("Company name", "Company name"),
                        ("Text", "Text"),
                        ("Integer", "Integer"),
                        ("Address", "Address"),
                        ("Date", "Date")
    )

    schema_id = models.ForeignKey(Schema, on_delete=models.CASCADE)
    order = models.IntegerField()
    name = models.CharField(max_length=100)
    type = models.CharField(choices=TYPES_CHOICES, max_length=100)
    from_num = models.IntegerField(verbose_name="from", blank=True, null=True)
    to_num = models.IntegerField(verbose_name="to", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('order', 'schema_id')
        verbose_name = "Колонка"
        verbose_name_plural = "Колонки"


class DataSet(models.Model):
    STATUS_CHOICES = (
                        ("Ready", "Ready"),
                        ("Processing", "Processing"),
    )

    schema_id = models.ForeignKey(Schema, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    file = models.FileField(upload_to="csv_files", blank=True, null=True)
    rows = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    def save_file(self, *args, **kwargs):
        filename = kwargs['filename']
        path = kwargs['path']
        with open(path, "r") as f:
            self.file.save(filename, f)
        return

