from data_preview import df
from flask import render_template, Blueprint, current_app
import pandas as pd
import plotly.express as px
import plotly.io as pio

upload_pre_process = Blueprint('plot_features', __name__)

@upload_pre_process.route('/plot_features', methods=['GET'])
def plot_features_route():
    df = current_app.config.get('DF')
    if df is None:
        return "No dataset uploaded yet!", 400

    cat_vars = df.select_dtypes(include=['object']).columns.tolist()
    num_vars = df.select_dtypes(include=['float', 'int']).columns.tolist()

    plot_htmls = []

    for col in cat_vars:
        count_df = df[col].value_counts().reset_index()
        count_df.columns = [col, 'Count']
        fig = px.bar(
            count_df,
            x=col, y="Count",
            title=f"Categorical Distribution: {col}",
            labels={col: col, "Count": "Count"}
        )
        plot_html = pio.to_html(fig, full_html=False)
        plot_htmls.append(plot_html)

    for col in num_vars:
        fig = px.histogram(
            df, x=col,
            nbins=30,
            title=f"Numerical Distribution: {col}",
            labels={col: col}
        )
        plot_html = pio.to_html(fig, full_html=False)
        plot_htmls.append(plot_html)

    return render_template('pre_processing.html', 
                           plot_htmls = plot_htmls
                        )