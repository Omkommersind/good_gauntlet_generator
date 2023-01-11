import csv
import sys


def seed_objects_from_csv(file_path: str, model):
    if model.objects.exists():
        sys.stdout.write("%s data exists [OK]\n" % model._meta.model_name)
        return

    with open(file_path, newline='', encoding='utf-8') as csv_file:
        rows = csv.reader(csv_file, delimiter=',', quotechar='"')
        rows_iterator = iter(rows)
        header_row = next(rows_iterator, [])
        headers = [col_name for col_name in header_row]
        cols_count = len(headers)
        objects = []

        for i, row in enumerate(rows_iterator):
            object_data = {}
            for j in range(cols_count):
                data = row[j]
                if data == '':
                    data = None

                object_data[headers[j]] = data
            objects.append(model(**object_data))

        try:
            model.objects.bulk_create(objects)
            sys.stdout.write("%s data seed successful [OK]\n" % model._meta.model_name)
        except Exception as ex:
            sys.stdout.write("Error seed %s : %s [ERROR]\n" % (model._meta.model_name, ex))
