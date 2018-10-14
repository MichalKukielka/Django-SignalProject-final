import os
from django.core.exceptions import ValidationError


def validate_input_file_extension(value):

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mat', '.json', '.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension!')

def validate_results_file_extension(value):

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.json']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension!')
