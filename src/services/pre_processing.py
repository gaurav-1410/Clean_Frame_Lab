from data_preview import df
from flask import render_template, Blueprint, current_app, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.pyplot as plt
import io, base64

upload_pre_process = Blueprint('plot_features', __name__)

@upload_pre_process.route('/plot_features', methods=['GET'])
def plot_features_route():
    df = current_app.config.get('DF')
    if df is None:
        return "No dataset uploaded yet!", 400

    cat_vars = df.select_dtypes(include=['object']).columns.tolist()
    num_vars = df.select_dtypes(include=['float', 'int']).columns.tolist()

    selected_col = request.args.get("col")
    selected_col2 = request.args.get("col2")
    graph_type = request.args.get("graph_type")
    col_types = df.dtypes.apply(lambda x: "num" if pd.api.types.is_numeric_dtype(x) else "cat").to_dict()

    plot_html = None

    if (selected_col or selected_col2) and graph_type:
        if selected_col and not selected_col2:
            col_type = col_types[selected_col]
            if col_type == "cat":
                if graph_type == "bar":
                    count_df = df[selected_col].value_counts().reset_index()
                    count_df.columns = [selected_col, 'Count']
                    fig = px.bar(count_df, x=selected_col, y="Count",
                                title=f"Bar Plot: {selected_col}")
                    plot_html = pio.to_html(fig, full_html=False)

                elif graph_type == "pie":
                    fig = px.pie(df, names=selected_col, title=f"Pie Chart: {selected_col}")
                    plot_html = pio.to_html(fig, full_html=False)

                elif graph_type == "mosaic":
                    plt.figure(figsize=(6, 4))
                    mosaic(df, [selected_col])
                    buf = io.BytesIO()
                    plt.savefig(buf, format="png")
                    buf.seek(0)
                    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                    plot_html = f'<img src="data:image/png;base64,{img_b64}"/>'
                    
            elif col_type == "num":
                if graph_type == "hist":
                    fig = px.histogram(df, x=selected_col,
                                    title=f"Histogram of {selected_col}")
                    plot_html = pio.to_html(fig, full_html=False)
                elif graph_type == "box":
                    fig = px.box(df, y=selected_col,
                                title=f"Box Plot of {selected_col}")
                    plot_html = pio.to_html(fig, full_html=False)
                elif graph_type == "scatter":
                    fig = px.scatter(df, x=df.index, y=selected_col,
                                    title=f"Scatter of {selected_col}")
                    plot_html = pio.to_html(fig, full_html=False)

        elif selected_col2 and not selected_col:
            col_type = col_types[selected_col2]
            if col_type == "cat":
                if graph_type == "bar":
                    fig = px.bar(df[selected_col2].value_counts().reset_index(),
                                 x="index", y=selected_col2,
                                 title=f"Bar Plot of {selected_col2}")
                    plot_html = pio.to_html(fig, full_html=False)
                elif graph_type == "pie":
                    fig = px.pie(df, names=selected_col2,
                                 title=f"Pie Chart of {selected_col2}")
                    plot_html = pio.to_html(fig, full_html=False)
            elif col_type == "num":
                if graph_type == "hist":
                    fig = px.histogram(df, x=selected_col2,
                                       title=f"Histogram of {selected_col2}")
                    plot_html = pio.to_html(fig, full_html=False)
                elif graph_type == "box":
                    fig = px.box(df, y=selected_col2,
                                 title=f"Box Plot of {selected_col2}")
                    plot_html = pio.to_html(fig, full_html=False)
                elif graph_type == "scatter":
                    fig = px.scatter(df, x=df.index, y=selected_col2,
                                     title=f"Scatter of {selected_col2}")
                    plot_html = pio.to_html(fig, full_html=False)

        elif selected_col and selected_col2:
            type1, type2 = col_types[selected_col], col_types[selected_col2]

            if (type1 == "cat" and type2 == "num") or (type1 == "num" and type2 == "cat"):
                cat_col = selected_col if type1 == "cat" else selected_col2
                num_col = selected_col if type1 == "num" else selected_col2

                if graph_type == "cat_box":
                    fig = px.box(df, x=cat_col, y=num_col,
                                 title=f"Box Plot of {num_col} by {cat_col}")
                    plot_html = pio.to_html(fig, full_html=False)
                elif graph_type == "violin":
                    fig = px.violin(df, x=cat_col, y=num_col, box=True,
                                    title=f"Violin Plot of {num_col} by {cat_col}")
                    plot_html = pio.to_html(fig, full_html=False)
                elif graph_type == "bar_error":
                    fig = px.bar(df, x=cat_col, y=num_col, error_y="size",
                                 title=f"Bar Plot with Error Bars ({num_col} by {cat_col})")
                    plot_html = pio.to_html(fig, full_html=False)

            elif type1 == "num" and type2 == "num":
                if graph_type == "num_scatter":
                    fig = px.scatter(df, x=selected_col, y=selected_col2,
                                     title=f"Scatter Plot: {selected_col} vs {selected_col2}")
                    plot_html = pio.to_html(fig, full_html=False)
                elif graph_type == "num_line":
                    fig = px.line(df, x=selected_col, y=selected_col2,
                                  title=f"Line Plot: {selected_col} vs {selected_col2}")
                    plot_html = pio.to_html(fig, full_html=False)
                elif graph_type == "corr":
                    corr_val = df[[selected_col, selected_col2]].corr().iloc[0, 1]
                    fig = px.imshow(df[[selected_col, selected_col2]].corr(),
                                    text_auto=True, aspect="auto",
                                    title=f"Correlation Heatmap (ρ = {corr_val:.2f})")
                    plot_html = pio.to_html(fig, full_html=False)

    return render_template("pre_processing.html",
                           columns=df.columns.tolist(),
                           cat_vars=cat_vars,
                           num_vars=num_vars,
                           plot_html=plot_html,
                           selected_col=selected_col,
                           selected_col2=selected_col2,
                           graph_type=graph_type)
