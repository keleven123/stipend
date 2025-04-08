import pandas as pd

def import_consumption(csv_file, ConsumptionRecord=None):
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        ConsumptionRecord.objects.update_or_create(
            student_id=row['学号'],
            defaults={
                'last_month_total': row['月总消费'],
                'canteen_avg': row['日均食堂消费']
            }
        )