# import Flask
from flask import Flask
import csv
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)


def get_dataset_dimensions(filename):
    try:
        with open(filename, 'r',encoding="utf8") as file:
            reader = csv.reader(file)
            rows = sum(1 for row in reader)
            file.seek(0)
            columns = len(next(reader))
    except FileNotFoundError:
        print("File not found.")
        return None

    return rows, columns


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(filename)
            df = pd.read_csv(filename)
            duplicates = df.duplicated() * 100
            dimensions = get_dataset_dimensions(filename)
            dup_name = len(df.columns) == len(set(df.columns))
            if dimensions is not None:
                rows, columns = dimensions
                null_values = df.isnull().mean() * 100
                result_df = pd.DataFrame({
                    'Number of Rows': [rows],
                    'Number of Columns': [columns],
                    'Number of Duplicates in Rows': [duplicates],
                    '% of Null Values': [null_values],
                    'No Duplicate Column name found':[dup_name]
                })
                result_table = result_df.to_html(index=False)
                return render_template('result.html', result_table=result_table)
            else:
                return "File not found."
    return render_template('upload.html')


# if _name_ == '_main_':


if __name__ == "__main__":
    app.run(debug=True)
