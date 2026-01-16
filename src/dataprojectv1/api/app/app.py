from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from flask import url_for

import os
import json
from flask import Response
from datetime import datetime
import logging
from datetime import datetime
import pandas as pd

from .utils import render_pretty_table
from .utils import to_prometheus_time

app = Flask(__name__)
metrics = PrometheusMetrics(app)

METRICS_FOLDER = "/app/prometheus_metrics"  # Dostosuj ścieżkę do swojego kontenera

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")


@app.route("/")
def index():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Hello, World! <br> {current_time}"


@app.route("/routes2", methods=["GET"])
def list_routes2():
    output = []
    for rule in app.url_map.iter_rules():
        methods = ", ".join(rule.methods)
        output.append(f"{rule.endpoint:20s} {methods:20s} {rule}")
    return "<pre>" + "\n".join(output) + "</pre>"


@app.route("/routes", methods=["GET"])
def list_routes():
    import urllib.parse

    links = []
    # Pobieramy wszystkie reguły z mapy URL Flaska
    for rule in app.url_map.iter_rules():
        # Pomijamy endpointy, które wymagają argumentów (np. <id>) dla prostoty listy
        # oraz endpointy czysto techniczne (np. 'static')
        if "GET" in rule.methods and len(rule.arguments) == 0:
            url = url_for(rule.endpoint, _external=False)
            links.append(f'<li><a href="{url}">{url}</a> (endpoint: {rule.endpoint})</li>')

    html = f"""
    <html>
        <head><title>API Map</title></head>
        <body>
            <h1>🚀 DataProject V1.0 - Available Endpoints</h1>
            <ul>
                {"".join(sorted(links))}
            </ul>
            <hr>
            <p><i>Tryb: Debug | Mentor IT</i></p>
        </body>
    </html>
    """
    return html


@app.route("/filescsv")
def filescsv():
    filespath = "/app/filescsv"

    if not os.path.exists(filespath):
        logger.error(f"Directory not found: {filespath}")
        return {"error": "Path not found"}, 404

    fileslist = os.listdir(filespath)
    logger.info(f"This is an info message: Filelist: {fileslist}")

    data = []
    for idx, file in enumerate(fileslist):
        name, extension = os.path.splitext(file)
        timestamp = datetime.fromtimestamp(os.path.getmtime(os.path.join(filespath, file))).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        data.append([idx, f"<a href='/filescsv/{file}'>{name}</a>", extension, timestamp])

    df = pd.DataFrame(data, columns=["id", "namefile", "extension", "timestamp"])
    df = df.sort_values(by=["extension", "namefile"])

    html = customize_df_html(df)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Reading CSV files: <br> {current_time} <br> {html}"


def customize_file_content(
    content,
    background_color="#f9f9f9",
    padding="10px",
    border="1px solid #ddd",
    font_family="monospace",
    font_size="14px",
):
    return f"""
    <pre style='background-color: {background_color}; padding: {padding}; border: {border}; font-family: {font_family}; font-size: {font_size};'>
    {content}
    </pre>
    """


@app.route("/filescsv/<filename>")
def view_csv_file(filename):
    filespath = "/app/filescsv"
    filepath = os.path.join(filespath, filename)

    if not os.path.exists(filepath):
        return f"File {filename} not found.", 404

    # with open(filepath, 'r') as file:
    #     content = file.read()

    # logger.info(f"Viewing content of file: {filename}")
    # customized_content = customize_file_content(content)
    # return f"<h2>Content of {filename}</h2>{customized_content}"
    try:
        # Read CSV to Pandas
        df = pd.read_csv(filepath)

        # Convert to HTML with Bootstrap classes for a nice appearance
        html_table = df.to_html(classes="table table-striped table-hover", index=False)

        return render_pretty_table(df, filename)
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        return f"Error processing file: {str(e)}", 500


@app.route("/filesjson")
def filesjson():
    filespath = "/app/filesjson"
    fileslist = os.listdir(filespath)
    logger.info(f"This is an info message: Filelist filesjson: {fileslist}")

    data = []
    for idx, file in enumerate(fileslist):
        name, extension = os.path.splitext(file)
        timestamp = datetime.fromtimestamp(os.path.getmtime(os.path.join(filespath, file))).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        # data.append([idx, f"<a href='/filesjson/{file}'>{name}</a>", extension, timestamp])
        data.append([idx, f"<a href='/filesjson/{file}'>{file}</a>", extension, timestamp])

    df = pd.DataFrame(data, columns=["id", "namefile", "extension", "timestamp"])
    df = df.sort_values(by=["extension", "namefile"])

    html = customize_df_html(df)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Reading Json files: <br> {current_time} <br> {html}"


@app.route("/filesjson/<filename>")
def view_json_file(filename):
    filespath = "/app/filesjson"
    # filepath = os.path.join(filespath, f"{filename}.json")
    filepath = os.path.join(filespath, f"{filename}")

    if not os.path.exists(filepath):
        return f"File {filename}.json not found.", 404

    # with open(filepath, 'r') as file:
    #     content = file.read()

    # logger.info(f"Viewing content of file: {filename}.json")
    # customized_content = customize_file_content(content)
    # # return f"<h2>Content of {filename}.json</h2>{customized_content}"
    # return f"{content}"
    try:
        # Read CSV to Pandas
        df = pd.read_json(filepath)

        # Convert to HTML with Bootstrap classes for a nice appearance
        html_table = df.to_html(classes="table table-striped table-hover", index=False)

        return render_pretty_table(df, filename)
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        return f"Error processing file: {str(e)}", 500


def customize_df_html(
    df, header_bg_color="#f2f2f2", even_row_bg_color="#f9f9f9", odd_row_bg_color="#ffffff", font_weight="bold"
):
    styles = [
        dict(selector="th", props=[("font-weight", font_weight), ("background-color", header_bg_color)]),
        dict(selector="tr:nth-child(even)", props=[("background-color", even_row_bg_color)]),
        dict(selector="tr:nth-child(odd)", props=[("background-color", odd_row_bg_color)]),
    ]
    return df.style.set_table_styles(styles).to_html()


@app.route("/prometheus")
def get_custom_prometheus_data():
    output = []
    if not os.path.exists(METRICS_FOLDER):
        return Response("# Folder nie istnieje", status=200, mimetype="text/plain")

    for filename in os.listdir(METRICS_FOLDER):
        if filename.endswith(".json"):
            metric_name = os.path.splitext(filename)[0].replace("-", "_").replace(".", "_")
            file_path = os.path.join(METRICS_FOLDER, filename)

            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                    # Budowanie stringa etykiet: {key1="val1", key2="val2"}
                    labels = []
                    for key, value in data.items():
                        clean_key = key.replace("-", "_").replace(" ", "_")
                        # Wartości w etykietach muszą być stringami w cudzysłowie
                        labels.append(f'{clean_key}="{value}"')

                    labels_str = "{" + ",".join(labels) + "}"

                    # Wynik: nazwa_metki{etykiety} 1
                    output.append(f"# HELP {metric_name} Metadata from {filename}")
                    output.append(f"# TYPE {metric_name} gauge")
                    output.append(f"{metric_name}{labels_str} 1")

            except Exception as e:
                logger.error(f"Błąd pliku {filename}: {e}")

    return Response("\n".join(output) + "\n", mimetype="text/plain")


@app.route("/bronze")
def filesbronze():
    filespath = "../bronze"
    fileslist = os.listdir(filespath)
    logger.info(f"This is an info message: Filelist bronze: {fileslist}")

    data = []
    for idx, file in enumerate(fileslist):
        name, extension = os.path.splitext(file)
        timestamp = datetime.fromtimestamp(os.path.getmtime(os.path.join(filespath, file))).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        data.append([idx, name, extension, timestamp])

    df = pd.DataFrame(data, columns=["id", "namefile", "extension", "timestamp"])
    df = df.sort_values(by=["extension", "namefile"])

    html = customize_df_html(df)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Reading bronze files <br> {current_time} <br> {html}"


@app.route("/silver")
def filessilver():
    filespath = "../silver"
    fileslist = os.listdir(filespath)
    logger.info(f"This is an info message: Filelist silver: {fileslist}")

    data = []
    for idx, file in enumerate(fileslist):
        name, extension = os.path.splitext(file)
        timestamp = datetime.fromtimestamp(os.path.getmtime(os.path.join(filespath, file))).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        data.append([idx, name, extension, timestamp])

    df = pd.DataFrame(data, columns=["id", "namefile", "extension", "timestamp"])
    df = df.sort_values(by=["extension", "namefile"])

    html = customize_df_html(df)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Reading silver files <br> {current_time} <br> {html}"


@app.route("/gold")
def filesgold():
    filespath = "../gold"
    fileslist = os.listdir(filespath)
    logger.info(f"This is an info message: Filelist gold: {fileslist}")

    data = []
    for idx, file in enumerate(fileslist):
        name, extension = os.path.splitext(file)
        timestamp = datetime.fromtimestamp(os.path.getmtime(os.path.join(filespath, file))).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        data.append([idx, name, extension, timestamp])

    df = pd.DataFrame(data, columns=["id", "namefile", "extension", "timestamp"])
    df = df.sort_values(by=["extension", "namefile"])

    html = customize_df_html(df)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Reading gold files <br> {current_time} <br> {html}"


@app.route("/scripts")
def filesscripts():
    filespath = "../scripts"
    fileslist = os.listdir(filespath)
    logger.info(f"This is an info message: Filelist scripts: {fileslist}")

    data = []
    for idx, file in enumerate(fileslist):
        name, extension = os.path.splitext(file)
        timestamp = datetime.fromtimestamp(os.path.getmtime(os.path.join(filespath, file))).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        data.append([idx, name, extension, timestamp])

    df = pd.DataFrame(data, columns=["id", "namefile", "extension", "timestamp"])
    df = df.sort_values(by=["extension", "namefile"])

    html = customize_df_html(df)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Reading scripts files <br> {current_time} <br> {html}"


@app.route("/dockervolume")
def filessdockervolume():
    filespath = "../docker_volume"
    fileslist = os.listdir(filespath)
    logger.info(f"This is an info message: Filelist docker_volume: {fileslist}")

    data = []
    for idx, file in enumerate(fileslist):
        name, extension = os.path.splitext(file)
        timestamp = datetime.fromtimestamp(os.path.getmtime(os.path.join(filespath, file))).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        data.append([idx, name, extension, timestamp])

    df = pd.DataFrame(data, columns=["id", "namefile", "extension", "timestamp"])
    df = df.sort_values(by=["extension", "namefile"])

    html = customize_df_html(df)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Reading docker_volume files <br> {current_time} <br> {html}"


@app.route("/routes")
def show_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"<a href='{rule.rule}'>{rule.endpoint}: {rule.rule}</a>")
    return "<br>".join(routes)


def files_list(path):
    fileslist = os.listdir(path)
    return fileslist


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
