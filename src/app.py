import os
import json
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from controllers.metrics import generate_charts

from main import analizar
from controllers.data_loader import load_messages, load_patterns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

VIEWS_DIR = os.path.join(BASE_DIR, "views")
app = Flask(__name__, static_folder=VIEWS_DIR, static_url_path="")

@app.route("/")
def index():
    return send_from_directory(VIEWS_DIR, "index.html")

@app.route("/api/graficas/<path:filename>")
def serve_graficas(filename):
    ruta_mockups = os.path.join(BASE_DIR, "..", "docs", "mockups")
    return send_from_directory(ruta_mockups, filename)

@app.route("/api/patrones", methods=["GET"])
def get_patrones():
    ruta = os.path.join(DATA_DIR, "patterns.csv")
    if not os.path.exists(ruta):
        return jsonify([])
    patrones = load_patterns(ruta)
    return jsonify(patrones)


@app.route("/api/ejecutar", methods=["POST"])
def ejecutar():
    algoritmo = request.form.get("algoritmo", "kmp")

    if "mensajes" in request.files and request.files["mensajes"].filename:
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as tmp:
            request.files["mensajes"].save(tmp.name)
            ruta_temporal = tmp.name
        try:
            mensajes = load_messages(ruta_temporal)
        finally:
            os.remove(ruta_temporal)
    else:
        mensajes = load_messages(os.path.join(DATA_DIR, "messages.csv"))

    patrones_json = request.form.get("patrones")
    if patrones_json:
        patrones = json.loads(patrones_json)
    else:
        patrones = load_patterns(os.path.join(DATA_DIR, "patterns.csv"))

    if not mensajes:
        return jsonify({"error": "No hay mensajes para analizar."}), 400
    if not patrones:
        return jsonify({"error": "No hay patrones configurados."}), 400

    tiempos_totales, alertas = analizar(mensajes, patrones, algoritmo=algoritmo)
    generate_charts(tiempos_totales, alertas)
    
    resultado = {
        "total_mensajes": len(mensajes),
        "coincidencias": len(alertas),
        "tiempo_ms": round(tiempos_totales[algoritmo] * 1000, 4),
        "tiempos_totales_ms": {k: round(v * 1000, 4) for k, v in tiempos_totales.items()},
        "algoritmo": algoritmo.upper(),
        "alertas": [
            {
                "id": a["id"],
                "patron": a["patron"],
                "categoria": a["categoria"],
                "nivel": a["nivel"],
                "posicion": a["posicion"],
                "sugerencia": a["sugerencia"],
                "algoritmo": a["algoritmo"]
            }
            for a in alertas
        ]
    }
    return jsonify(resultado)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
