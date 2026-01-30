from datetime import datetime


class CustomVariables:
    # SEVICE_AVAILABLE = {
    #     "prometheus-metrics": "http://localhost:5000/prometheus",
    #     "prometheus": "http://localhost:9090",
    #     "grafana": "http://localhost:3000",
    #     "jupyterlab": "http://localhost:8888",
    #     "airflow": "http://localhost:8082",
    #     "kafka": "http://localhost:8081",
    #     "flask": "http://localhost:5000/routes",
    #     "elasticsearch": "http://localhost:9200",
    #     "kibana": "http://localhost:5601",
    #     "elasticvue": "http://localhost:8080",
    # }
    SERVICE_AVAILABLE = {
        "flask": "http://localhost:5000",
        "prometheus-metrics": "http://localhost:5000/prometheus",
        "prometheus": "http://localhost:9090",
        "grafana": "http://localhost:3000",
        "elasticsearch": "http://localhost:9200",
        "elasticvue": "http://localhost:8080",
        "kafka-ui": "http://localhost:8081",
        "airflow": "http://localhost:8082",
        "jupyterlab": "http://localhost:8888",
        "postgres": "localhost:5433",  # Port zewnętrzny, który zmapowałeś (5433:5432)
    }

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Service Dashboard</title>
        <style>
            body { font-family: sans-serif; background: #f4f7f6; padding: 40px; }
            .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h2 { border-bottom: 2px solid #333; padding-bottom: 10px; color: #333; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { text-align: left; padding: 12px; border-bottom: 1px solid #ddd; }
            th { background-color: #f8f9fa; text-transform: uppercase; font-size: 12px; color: #666; }
            tr:hover { background-color: #f1f1f1; }
            .status-pill { padding: 4px 8px; border-radius: 12px; font-size: 11px; background: #e1f5fe; color: #01579b; font-weight: bold; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🛠️ Project Infrastructure Dashboard</h2>
            <table>
                <thead>
                    <tr>
                        <th>Service Name</th>
                        <th>Status</th>
                        <th>External URL / Address</th>
                    </tr>
                </thead>
                <tbody>
                    {% for name, url in services.items() %}
                    <tr>
                        <td><strong>{{ name | capitalize }}</strong></td>
                        <td><span class="status-pill">Active</span></td>
                        <td><a href="{{ url if 'http' in url else '#' }}" target="_blank">{{ url }}</a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """


def render_pretty_table(df, filename):
    """
    Zamienia DataFrame w nowoczesną, interaktywną tabelę HTML.
    """
    # Generowanie podstawowej tabeli przez Pandas
    html_table = df.to_html(classes="table table-striped table-hover table-borderless align-middle", index=False)

    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
            <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css">
            <style>
                body {{ background-color: #f4f7f9; padding: 2rem; font-family: 'Inter', sans-serif; }}
                .card {{ border: none; border-radius: 15px; box-shadow: 0 8px 30px rgba(0,0,0,0.05); overflow: hidden; }}
                .card-header {{ background: linear-gradient(45deg, #2c3e50, #000000); color: white; padding: 1.5rem; border: none; }}
                
                /* Własne stylowanie pasów (zebra) */
                .table-striped>tbody>tr:nth-of-type(odd)>* {{
                    --bs-table-accent-bg: rgba(13, 110, 253, 0.03); /* Bardzo delikatny błękit dla nieparzystych */
                    color: #495057;
                }}
                
                .table thead {{ 
                    background-color: #f8f9fa; 
                    color: #333;
                    text-transform: uppercase; 
                    font-size: 0.85rem; 
                    letter-spacing: 0.05rem;
                    border-bottom: 2px solid #dee2e6;
                }}
                
                .table-hover tbody tr:hover {{ 
                    background-color: #e9ecef !important; 
                    transition: 0.2s; 
                }}
            </style>
        </head>
        <body>
            <div class="container-fluid">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h4 class="mb-0">📋 Arkusz: {filename}</h4>
                        <span class="badge bg-info">{len(df)} rekordów</span>
                    </div>
                    <div class="card-body p-4">
                        <div class="table-responsive">
                            {html_table}
                        </div>
                    </div>
                </div>
            </div>
            
            <script src="https://code.jquery.com/jquery-3.7.0.js"></script>
            <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
            <script src="https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js"></script>
            <script>
                $(document).ready(function() {{
                    $('.table').DataTable({{
                        "pageLength": 15,
                        "lengthMenu": [[5, 10, 15, 25, 50, -1], [5, 10, 15, 25, 50, "Wszystkie"]],
                        // "language": {{
                        //     "url": "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pl.json"
                        // }}
                    }});
                }});
            </script>
        </body>
    </html>
    """


def to_prometheus_time(dt_str):
    """Konwertuje datę na timestamp (sekundy), co jest jedyną formą liczbową daty w Promu."""
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.timestamp()
    except:
        return None
