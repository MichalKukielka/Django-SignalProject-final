from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .validators import validate_input_file_extension, validate_results_file_extension
import os


class InputSignal(models.Model):

    name = models.CharField(max_length=512)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    adnotations = models.TextField(blank=True, null=True)
    amplitude_unit = models.CharField(max_length=64)
    sample_rate = models.FloatField(validators=[MinValueValidator(0.0000000001)])
    input_file = models.FileField(upload_to='signals/', null=False, validators=[validate_input_file_extension])
    results_file = models.FileField(upload_to='results/', default='results/results_template.json',null=True, blank=True, validators=[validate_results_file_extension])
    add_date = models.DateTimeField(default=datetime.now)
    last_edit_date = models.DateTimeField(auto_now=True)


    objects = models.Manager()


    def delete(self):
        self.input_file.delete()
        if os.path.basename(self.results_file.name) != 'results_template.json':
            self.results_file.delete()
        super().delete()

    def __str__(self):
        return self.name

    def add_date_pretty(self):
        return self.add_date.strftime('%b %e %Y')

    def last_edit_date_pretty(self):
        return self.add_date.strftime('%H:%M:%S %b %e %Y')
