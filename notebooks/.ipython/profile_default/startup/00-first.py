try:
    from IPython import get_ipython

    ipython = get_ipython()
    if ipython:
        ipython.run_line_magic("load_ext", "sparksql_magic")
        # Tutaj możesz dodać automatyczne przypisanie sesji spark,
        # jeśli jest już dostępna w przestrzeni nazw.
except Exception as e:
    print(f"Błąd autostartu: {e}")
