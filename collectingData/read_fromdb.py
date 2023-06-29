import sqlite3
import pandas as pd

def read_data_from_database(db_file, table_name, columns):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Überprüfen, ob die Tabelle existiert
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    table_exists = cursor.fetchone()
    if not table_exists:
        print(f"Die Tabelle '{table_name}' existiert nicht in der Datenbank.")
        conn.close()
        return

    # Spaltennamen in eine kommagetrennte Zeichenkette umwandeln
    columns_str = ", ".join(columns)

    # Daten auslesen
    cursor.execute(f"SELECT {columns_str} FROM {table_name}")
    rows = cursor.fetchall()

    # DataFrame erstellen
    df = pd.DataFrame(rows, columns=columns)


    conn.close()

# Beispielaufruf
db_file = 'vegan_products.db'  # Pfad zur SQLite-Datenbankdatei
table_name = 'products'  # Name der Tabelle in der Datenbank
columns = ['id', 'name', 'ingredients']  # Liste der gewünschten Spaltennamen

read_data_from_database(db_file, table_name, columns)
