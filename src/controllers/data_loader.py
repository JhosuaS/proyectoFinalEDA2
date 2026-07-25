import csv
import os

def load_messages(csv_path):
    """
    Carga el archivo CSV de mensajes. Debe contener la columna 'mensaje'.
    """
    messages = []
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No existe el archivo: {csv_path}")

    with open(csv_path, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if "mensaje" not in reader.fieldnames:
            raise ValueError("El CSV de mensajes debe contener una columna llamada 'mensaje'.")
        for row in reader:
            messages.append(row)
    return messages

def load_patterns(csv_path):
    """
    Carga el archivo CSV de patrones con las columnas requeridas por el proyecto.
    """
    patterns = []
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No existe el archivo: {csv_path}")

    with open(csv_path, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        # Se cambió 'descripcion' por 'categoria' para coincidir con la fuente [3]
        columnas_requeridas = {
            "patron",
            "nivel_alerta",
            "categoria",
            "sugerencia_accion"
        }

        if not columnas_requeridas.issubset(set(reader.fieldnames)):
            raise ValueError(
                f"El CSV de patrones no tiene el formato esperado. "
                f"Columnas detectadas: {reader.fieldnames}"
            )

        for row in reader:
            patterns.append(row)
    return patterns


def add_pattern(csv_path, patron, nivel, categoria, sugerencia):
    """
    Agrega un nuevo patrón respetando el orden de columnas del proyecto [2].
    """
    campos = ["patron", "categoria", "nivel_alerta", "sugerencia_accion"]
    
    archivo_nuevo = (
        not os.path.exists(csv_path)
        or os.path.getsize(csv_path) == 0
    )

    with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=campos)
        if archivo_nuevo:
            writer.writeheader()

        writer.writerow({
            "patron": patron,
            "categoria": categoria,
            "nivel_alerta": nivel,
            "sugerencia_accion": sugerencia
        })

def update_pattern(csv_path, patron_original, nuevo_patron, nivel, categoria, sugerencia):
    """
    Actualiza un patrón existente usando la columna 'categoria' [1, 3].
    """
    patterns = load_patterns(csv_path)
    encontrado = False
    for row in patterns:
        if row["patron"] == patron_original:
            row["patron"] = nuevo_patron
            row["nivel_alerta"] = nivel
            row["categoria"] = categoria 
            row["sugerencia_accion"] = sugerencia
            encontrado = True

    if encontrado:
        save_patterns(csv_path, patterns)

def delete_pattern(csv_path, patron):
    patterns = load_patterns(csv_path)
    patterns = [p for p in patterns if p["patron"] != patron]
    save_patterns(csv_path, patterns)


def save_patterns(csv_path, patterns):
    """
    Sobrescribe el archivo CSV con la lista de patrones actualizada.
    """
    campos = ["patron", "categoria", "nivel_alerta", "sugerencia_accion"]
    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=campos)
        writer.writeheader()
        writer.writerows(patterns)


def find_pattern(csv_path, patron):
    try:
        patterns = load_patterns(csv_path)
        for row in patterns:
            if row["patron"].lower() == patron.lower():
                return row
    except Exception:
        return None
    return None