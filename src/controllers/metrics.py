import matplotlib.pyplot as plt
import os

def generate_charts(tiempos, alertas):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(base_dir, "..", "..", "docs", "mockups")
    
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)

    plt.figure(figsize=(8, 5))
    algos = ['KMP', 'Boyer-Moore']
    valores = [tiempos['kmp'], tiempos['bm']]
    plt.bar(algos, valores, color=['#e63946', '#2d2d3d'])
    plt.title('Eficiencia Algorítmica (Tiempo Total)')
    plt.ylabel('Segundos')
    
    rendimiento_file = os.path.join(docs_path, "reporte_rendimiento.png")
    plt.savefig(rendimiento_file)
    plt.close()

    if alertas:
        categorias = {}
        for a in alertas:
            cat = a['categoria']
            categorias[cat] = categorias.get(cat, 0) + 1
        
        plt.figure(figsize=(7, 7))
        plt.pie(categorias.values(), labels=categorias.keys(), autopct='%1.1f%%', 
                colors=['#e63946', '#f97316', '#a855f7', '#6366f1'])
        plt.title('Distribución de Riesgos Detectados')
        
        categorias_file = os.path.join(docs_path, "reporte_categorias.png")
        plt.savefig(categorias_file)
        plt.close()
    
    print(f"-> Gráficas generadas exitosamente en: {docs_path}")