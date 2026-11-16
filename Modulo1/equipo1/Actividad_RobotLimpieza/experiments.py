"""Barrido de experimentos para analizar el efecto del número de agentes.

Genera dos experimentos sobre una habitación de 20x20 con 50 % de celdas
sucias:

* Experimento A: tiempo máximo amplio (20 000 pasos) para medir cuánto
  tardan en limpiar todo y cuántos movimientos hacen.
* Experimento B: tiempo máximo corto (300 pasos) para comparar el
  porcentaje de celdas limpias cuando no da tiempo de terminar.

Los resultados se guardan en ``resultados/`` como CSV y gráficas PNG.

Uso:
    python experiments.py
"""

import csv
import statistics
from pathlib import Path

import matplotlib.pyplot as plt

from model import CleaningModel

CARPETA_RESULTADOS = Path(__file__).resolve().parent / "resultados"
ANCHO = 20
ALTO = 20
PORCENTAJE_SUCIO = 0.5
AGENTES = (1, 2, 4, 8, 16, 32, 64)
REPETICIONES = 30
TIEMPO_AMPLIO = 20000
TIEMPO_CORTO = 300
AGENTES_CURVAS = (1, 2, 4, 8, 16)

# Paleta categórica fija (orden constante, nunca ciclada).
COLORES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4")
COLOR_PRINCIPAL = COLORES[0]
COLOR_REJILLA = "#e1e0d9"
COLOR_EJE = "#c3c2b7"
COLOR_TEXTO = "#3d3d3a"


def correr_barrido(tiempo_maximo):
    """Corre todas las combinaciones de agentes y repeticiones.

    Args:
        tiempo_maximo: Pasos máximos de cada simulación.

    Returns:
        Lista de diccionarios, uno por corrida.
    """
    filas = []
    for num_agentes in AGENTES:
        for repeticion in range(REPETICIONES):
            modelo = CleaningModel(
                width=ANCHO,
                height=ALTO,
                num_agents=num_agentes,
                dirty_fraction=PORCENTAJE_SUCIO,
                max_steps=tiempo_maximo,
                rng=1000 * num_agentes + repeticion,
            )
            resultado = modelo.run()
            resultado["repeticion"] = repeticion
            filas.append(resultado)
    return filas


def guardar_csv(filas, nombre):
    """Escribe las corridas en un archivo CSV."""
    ruta = CARPETA_RESULTADOS / nombre
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)


def resumir(filas, campo):
    """Calcula media, desviación estándar, mínimo y máximo por agentes.

    Args:
        filas: Corridas producidas por ``correr_barrido``.
        campo: Nombre de la métrica a resumir.

    Returns:
        Diccionario ``{agentes: (media, desviacion, minimo, maximo)}``.
    """
    resumen = {}
    for num_agentes in AGENTES:
        valores = [f[campo] for f in filas if f["agents"] == num_agentes]
        resumen[num_agentes] = (
            statistics.mean(valores),
            statistics.stdev(valores),
            min(valores),
            max(valores),
        )
    return resumen


def preparar_ejes(eje, titulo, etiqueta_y):
    """Aplica un estilo sobrio y consistente a una gráfica."""
    eje.set_title(titulo, loc="left", fontsize=11, color=COLOR_TEXTO)
    eje.set_ylabel(etiqueta_y, color=COLOR_TEXTO)
    eje.grid(axis="y", color=COLOR_REJILLA, linewidth=0.8)
    eje.set_axisbelow(True)
    for lado in ("top", "right", "left"):
        eje.spines[lado].set_visible(False)
    eje.spines["bottom"].set_color(COLOR_EJE)
    eje.tick_params(colors=COLOR_TEXTO, length=0)


def graficar_metrica(resumen, titulo, etiqueta_y, archivo, log_y=False):
    """Gráfica de línea de la media con banda de una desviación estándar."""
    figura, eje = plt.subplots(figsize=(6.4, 3.6))
    medias = [resumen[a][0] for a in AGENTES]
    desviaciones = [resumen[a][1] for a in AGENTES]
    eje.fill_between(
        AGENTES,
        [m - d for m, d in zip(medias, desviaciones)],
        [m + d for m, d in zip(medias, desviaciones)],
        color=COLOR_PRINCIPAL, alpha=0.15, linewidth=0,
    )
    eje.plot(AGENTES, medias, color=COLOR_PRINCIPAL, linewidth=2,
             marker="o", markersize=6)
    eje.set_xscale("log", base=2)
    if log_y:
        eje.set_yscale("log")
        marcas = [200, 500, 1000, 2000, 5000, 10000]
        eje.set_yticks(marcas, [f"{m:,}" for m in marcas])
        eje.minorticks_off()
    eje.set_xticks(AGENTES, [str(a) for a in AGENTES])
    eje.set_xlabel("Número de agentes", color=COLOR_TEXTO)
    preparar_ejes(eje, titulo, etiqueta_y)
    figura.tight_layout()
    figura.savefig(CARPETA_RESULTADOS / archivo, dpi=200)
    plt.close(figura)


def graficar_porcentaje_final(resumen, archivo):
    """Barras del porcentaje limpio al terminar el tiempo corto."""
    figura, eje = plt.subplots(figsize=(6.4, 3.6))
    posiciones = range(len(AGENTES))
    medias = [resumen[a][0] for a in AGENTES]
    eje.bar(posiciones, medias, color=COLOR_PRINCIPAL, width=0.6)
    for x, media in zip(posiciones, medias):
        eje.text(x, media + 1.5, f"{media:.1f} %", ha="center",
                 fontsize=8, color=COLOR_TEXTO)
    eje.set_xticks(list(posiciones), [str(a) for a in AGENTES])
    eje.set_ylim(0, 108)
    eje.set_xlabel("Número de agentes", color=COLOR_TEXTO)
    preparar_ejes(eje, f"Celdas limpias tras {TIEMPO_CORTO} pasos",
                  "Celdas limpias (%)")
    figura.tight_layout()
    figura.savefig(CARPETA_RESULTADOS / archivo, dpi=200)
    plt.close(figura)


def graficar_curvas_limpieza(archivo):
    """Evolución del porcentaje limpio en el tiempo para varios agentes."""
    figura, eje = plt.subplots(figsize=(6.4, 3.6))
    for color, num_agentes in zip(COLORES, AGENTES_CURVAS):
        modelo = CleaningModel(
            width=ANCHO, height=ALTO, num_agents=num_agentes,
            dirty_fraction=PORCENTAJE_SUCIO,
            max_steps=TIEMPO_AMPLIO, rng=42,
        )
        modelo.run()
        datos = modelo.datacollector.get_model_vars_dataframe()
        eje.plot(datos.index, datos["CleanPercentage"], color=color,
                 linewidth=2, label=f"{num_agentes} agente(s)")
    eje.set_xscale("symlog", linthresh=100)
    eje.set_xlabel("Paso de tiempo (escala logarítmica después de 100)",
                   color=COLOR_TEXTO)
    eje.legend(frameon=False, fontsize=8, loc="lower right")
    preparar_ejes(eje, "Porcentaje de celdas limpias a lo largo del tiempo",
                  "Celdas limpias (%)")
    figura.tight_layout()
    figura.savefig(CARPETA_RESULTADOS / archivo, dpi=200)
    plt.close(figura)


def imprimir_tabla(resumen_tiempo, resumen_movimientos, resumen_corto):
    """Muestra en consola la tabla resumen usada en el informe."""
    tiempo_uno = resumen_tiempo[1][0]
    print("agentes | pasos (media ± de) | min-max | aceleración | "
          "movimientos (media ± de) | mov/agente | % limpio "
          f"t={TIEMPO_CORTO}")
    for a in AGENTES:
        media_t, de_t, min_t, max_t = resumen_tiempo[a]
        media_m, de_m, _, _ = resumen_movimientos[a]
        print(f"{a:7d} | {media_t:8.0f} ± {de_t:6.0f} | "
              f"{min_t:5.0f}-{max_t:5.0f} | {tiempo_uno / media_t:5.2f} | "
              f"{media_m:9.0f} ± {de_m:6.0f} | {media_m / a:8.0f} | "
              f"{resumen_corto[a][0]:6.2f} ± {resumen_corto[a][1]:.2f}")


def main():
    """Ejecuta ambos experimentos y genera tablas y gráficas."""
    CARPETA_RESULTADOS.mkdir(exist_ok=True)

    filas_amplio = correr_barrido(TIEMPO_AMPLIO)
    guardar_csv(filas_amplio, "experimento_a_tiempo_amplio.csv")
    filas_corto = correr_barrido(TIEMPO_CORTO)
    guardar_csv(filas_corto, "experimento_b_tiempo_corto.csv")

    sin_terminar = [f for f in filas_amplio if not f["all_clean"]]
    print(f"Corridas sin terminar en el experimento A: {len(sin_terminar)}")

    resumen_tiempo = resumir(filas_amplio, "steps")
    resumen_movimientos = resumir(filas_amplio, "moves")
    resumen_corto = resumir(filas_corto, "clean_percentage")
    imprimir_tabla(resumen_tiempo, resumen_movimientos, resumen_corto)

    graficar_metrica(resumen_tiempo, "Tiempo hasta limpiar toda la habitación",
                     "Pasos (escala log)", "tiempo_vs_agentes.png", log_y=True)
    graficar_metrica(resumen_movimientos,
                     "Movimientos totales de todos los agentes",
                     "Movimientos", "movimientos_vs_agentes.png")
    graficar_porcentaje_final(resumen_corto, "limpio_tiempo_corto.png")
    graficar_curvas_limpieza("curvas_limpieza.png")


if __name__ == "__main__":
    main()
