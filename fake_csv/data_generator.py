import csv
from random import randint

from fake_csv.models import Schema, DataSet, Column
from fake_csv.faker import get_fake_data


def generate_csv_file(schema_id, rows, dataset_id):
    """
    The function generates a CSV file.
    Saves the file to an instance of the DataSet class, returns nothing.
    """
    schema = Schema.objects.get(id=schema_id)
    columns = Column.objects.filter(schema_id=schema).order_by('order')
    columns_names = [column.name for column in columns]
    separator = schema.separator
    string_character = schema.string_character
    filename = f'dataset{dataset_id}_schema{schema_id}.csv'
    with open('media/csv_files/' + filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, quotechar=string_character, quoting=csv.QUOTE_NONNUMERIC, delimiter=separator)
        writer.writerow(columns_names)
        for line_number in range(rows):
            fake_data = []
            for column in columns:
                fake_data.append(get_fake_data(column.type, column.from_num, column.to_num))
            writer.writerow(fake_data)

    dataset = DataSet.objects.get(id=dataset_id)
    dataset.save_file(path=f'media/csv_files/{filename}', filename=filename)
    dataset.status = 'Ready'
    dataset.save()
    return dataset.file.url
