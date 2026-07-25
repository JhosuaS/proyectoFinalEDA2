import time
import os
from controllers.data_loader import load_messages, load_patterns
from controllers.kmp_matcher import kmp
from controllers.bm_matcher import bm
from controllers.utils import normalize_text
from controllers.metrics import generate_charts


def analizar(mensajes, patrones, algoritmo='kmp'):
    tiempos_totales = {"kmp": 0.0, "bm": 0.0}
    alertas_detectadas = []

    for msg_data in mensajes:
        texto_norm = normalize_text(msg_data['mensaje'])

        for p_data in patrones:
            patron_norm = normalize_text(p_data['patron'])

            t_ini = time.perf_counter()
            pos_kmp = kmp(texto_norm, patron_norm)
            tiempos_totales["kmp"] += (time.perf_counter() - t_ini)

            t_ini = time.perf_counter()
            pos_bm = bm(texto_norm, patron_norm)
            tiempos_totales["bm"] += (time.perf_counter() - t_ini)

            posiciones = pos_kmp if algoritmo == 'kmp' else pos_bm

            if posiciones:
                alertas_detectadas.append({
                    "id": msg_data['id_mensaje'],
                    "patron": p_data['patron'],
                    "categoria": p_data['categoria'],
                    "nivel": p_data['nivel_alerta'],
                    "posicion": posiciones,
                    "sugerencia": p_data['sugerencia_accion'],
                    "algoritmo": algoritmo.upper()
                })

    return tiempos_totales, alertas_detectadas


def main():
    print("Iniciando...")
    base_path = os.path.dirname(os.path.abspath(__file__))
    path_msg = os.path.join(base_path, "data", "messages.csv")
    path_pat = os.path.join(base_path, "data", "patterns.csv")

    print("SISTEMA DE DETECCIÓN SAFE-TEXT")

    try:
        mensajes = load_messages(path_msg)
        patrones = load_patterns(path_pat)
        if not mensajes or not patrones:
            print("Error: Los archivos están vacíos.")
            return
    except FileNotFoundError:
        print("Error: No se encontraron los archivos CSV en /data.")
        return

    tiempos_totales, alertas_detectadas = analizar(mensajes, patrones, algoritmo='kmp')

    print(f"\n{'ID':<5} | {'Patrón':<18} | {'Categoría':<18} | {'Posiciones':<12}")
    print("-" * 65)
    for res in alertas_detectadas[:20]:
        print(f"{res['id']:<5} | {res['patron']:<18} | {res['categoria']:<18} | {str(res['posicion']):<12}")

    generate_charts(tiempos_totales, alertas_detectadas)

    print("\nRESUMEN DE INTERVENCIÓN RECOMENDADA")
    for a in alertas_detectadas[:5]:
        print(f"[{a['nivel'].upper()}] {a['categoria']}: {a['sugerencia']}")


if __name__ == "__main__":
    main()
