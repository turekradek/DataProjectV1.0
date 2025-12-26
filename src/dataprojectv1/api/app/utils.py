


def render_pretty_table(df, filename):
    """
    Zamienia DataFrame w nowoczesną, interaktywną tabelę HTML.
    """
    # Generowanie podstawowej tabeli przez Pandas
    html_table = df.to_html(classes='table table-striped table-hover table-borderless align-middle', index=False)
    
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