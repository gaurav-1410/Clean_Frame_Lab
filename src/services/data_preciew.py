from flask import Blueprint, render_template, request
import pandas as pd
import io

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files['dataset']
    
    if not file:
        return "No file uploaded", 400

    filename = file.filename.lower()

    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        elif filename.endswith('.json'):
            df = pd.read_json(file)
        else:
            return "Unsupported file format", 400
    except Exception as e:
        return f"Error reading file: {e}", 400

    rows, cols = df.shape
    null_val = df.isna().sum()
    head = df.head().to_html(classes='table-bordered table-dark', index=False)
    buf = io.StringIO()
    df.info(buf=buf)
    infom = buf.getvalue()
    duplicate = df.duplicated().sum()
    num_summary = df.describe().reset_index().rename(columns={'index': 'Statistic'}).to_html(classes='table-bordered table-dark', index=False)
    cat_summary = df.describe(include = 'object').reset_index().rename(columns={'index': 'Statistic'}).to_html(classes='table-bordered table-dark', index=False)

    return render_template('data_preview.html', rows = rows, cols = cols, null_val = null_val, head = head, infom = infom, duplicate = duplicate, num_describe = num_summary, cat_describe = cat_summary)
