from data_preview import df
from flask import render_template, Blueprint, current_app, request
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

    selected_col = request.args.get("col")
    plot_html = None

    if selected_col:
        if selected_col in cat_vars:
            count_df = df[selected_col].value_counts().reset_index()
            count_df.columns = [selected_col, 'Count']
            fig = px.bar(count_df, x=selected_col, y="Count",
                         title=f"Categorical Distribution: {selected_col}")
            plot_html = pio.to_html(fig, full_html=False)

        elif selected_col in num_vars:
            fig = px.histogram(df, x=selected_col, nbins=30,
                               title=f"Numerical Distribution: {selected_col}")
            plot_html = pio.to_html(fig, full_html=False)

    return render_template("pre_processing.html",
                           cat_vars=cat_vars,
                           num_vars=num_vars,
                           plot_html=plot_html,
                           selected_col=selected_col)