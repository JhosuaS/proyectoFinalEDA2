import csv
import os


# ==========================================
# CARGAR MENSAJES
# ==========================================

def load_messages(csv_path):
    """
    Carga cualquier archivo CSV de mensajes.

    Debe contener al menos una columna llamada:
        mensaje

    Opcionalmente puede tener:
        id_mensaje
    """

    messages = []

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No existe el archivo: {csv_path}")

    with open(csv_path, mode="r", newline="", encoding="utf-8-sig") as file:

        reader = csv.DictReader(file)

        if "mensaje" not in reader.fieldnames:
            raise ValueError(
                "El CSV de mensajes debe contener una columna llamada 'mensaje'."
            )

        for row in reader:
            messages.append(row)

    return messages


# ==========================================
# CARGAR PATRONES
# ==========================================

def load_patterns(csv_path):
    """
    Carga cualquier archivo CSV de patrones.

    Columnas esperadas:

    patron
    nivel_alerta
    descripcion
    sugerencia_accion
    """

    patterns = []

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No existe el archivo: {csv_path}")

    with open(csv_path, mode="r", newline="", encoding="utf-8-sig") as file:

        reader = csv.DictReader(file)

        columnas = {
            "patron",
            "nivel_alerta",
            "descripcion",
            "sugerencia_accion"
        }

        if not columnas.issubset(set(reader.fieldnames)):
            raise ValueError(
                "El CSV de patrones no tiene el formato esperado."
            )

        for row in reader:
            patterns.append(row)

    return patterns


# ==========================================
# AGREGAR PATRÓN
# ==========================================

def add_pattern(csv_path,
                patron,
                nivel,
                descripcion,
                sugerencia):
    """
    Agrega un patrón al CSV seleccionado.
    """

    campos = [
        "patron",
        "nivel_alerta",
        "descripcion",
        "sugerencia_accion"
    ]

    archivo_nuevo = (
        not os.path.exists(csv_path)
        or os.path.getsize(csv_path) == 0
    )

    with open(csv_path,
              mode="a",
              newline="",
              encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=campos)

        if archivo_nuevo:
            writer.writeheader()

        writer.writerow({
            "patron": patron,
            "nivel_alerta": nivel,
            "descripcion": descripcion,
            "sugerencia_accion": sugerencia
        })


# ==========================================
# EDITAR PATRÓN
# ==========================================

def update_pattern(csv_path,
                   patron_original,
                   nuevo_patron,
                   nivel,
                   descripcion,
                   sugerencia):

    patterns = load_patterns(csv_path)

    for row in patterns:

        if row["patron"] == patron_original:

            row["patron"] = nuevo_patron
            row["nivel_alerta"] = nivel
            row["descripcion"] = descripcion
            row["sugerencia_accion"] = sugerencia

    save_patterns(csv_path, patterns)


# ==========================================
# ELIMINAR PATRÓN
# ==========================================

def delete_pattern(csv_path, patron):

    patterns = load_patterns(csv_path)

    patterns = [
        p for p in patterns
        if p["patron"] != patron
    ]

    save_patterns(csv_path, patterns)


# ==========================================
# GUARDAR PATRONES
# ==========================================

def save_patterns(csv_path, patterns):

    campos = [
        "patron",
        "nivel_alerta",
        "descripcion",
        "sugerencia_accion"
    ]

    with open(csv_path,
              mode="w",
              newline="",
              encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=campos)

        writer.writeheader()

        writer.writerows(patterns)


# ==========================================
# BUSCAR PATRÓN
# ==========================================

def find_pattern(csv_path, patron):

    patterns = load_patterns(csv_path)

    for row in patterns:

        if row["patron"].lower() == patron.lower():
            return row

    return None
