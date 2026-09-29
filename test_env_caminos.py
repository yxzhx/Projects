"""
Laboratorio: Caminos mínimos — Dijkstra y Bellman-Ford
Universidad Complutense de Madrid — Flujos en Redes (3º Matemáticas)

ENTORNO DE PRUEBAS
Ejecutad este fichero con vuestra implementación completada.

Uso:
    python test_env_caminos.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time

# ─── Importar helpers ────────────────────────────────────────────
from helpers_caminos import (
    create_problem_dijkstra,
    create_problem_bellman_ford,
    create_problem_negative_cycle,
    draw_graph, draw_solution,
    animate_algorithm,
    verify_result,
    get_all_edges, get_all_nodes,
    reconstruct_path,
)

# ─── Importar implementación del alumno ──────────────────────────
try:
    from lab_template_caminos import dijkstra, bellman_ford # type: ignore
    STUDENT_IMPL = True
except Exception as e:
    print(f"[!] No se pudo cargar lab_template_caminos.py: {e}")
    STUDENT_IMPL = False


# ══════════════════════════════════════════════════════════════════
# TABLA DE RESULTADOS
# ══════════════════════════════════════════════════════════════════

def print_header(text):
    w = 70
    print(f"\n{'═' * w}")
    print(f"  {text}")
    print(f"{'═' * w}")


def print_result_table(rows, title=""):
    """rows = [(algo, dist, path, steps, time, ok), ...]"""
    if title:
        print(f"\n  {title}")
    print(f"  {'─' * 65}")
    print(f"  {'Algoritmo':<18} {'Distancia':<12} {'Pasos':<8} {'Tiempo':<10} {'Camino'}")
    print(f"  {'─' * 65}")
    for algo, dist, path, n_steps, elapsed, ok in rows:
        marker = '✓' if ok else '✗'
        dstr = f'{dist:g}' if dist is not None else 'N/A'
        pstr = ' → '.join(path) if path else 'N/A'
        if len(pstr) > 35:
            pstr = pstr[:32] + '...'
        print(f"  [{marker}] {algo:<15} {dstr:<12} {n_steps:<8} {elapsed:<10.4f} {pstr}")
    print(f"  {'─' * 65}")


# ══════════════════════════════════════════════════════════════════
# PROBLEMA 1: DIJKSTRA
# ══════════════════════════════════════════════════════════════════

def run_problem_1(fig, gs_row):
    prob = create_problem_dijkstra()
    print_header(f"PROBLEMA 1: {prob['name']}")
    print(f"  {prob['description']}")
    print(f"  Origen: {prob['source']},  Destino: {prob['target']}")
    print(f"  Solución esperada: dist = {prob['optimal_dist']}, "
          f"camino = {prob['optimal_path']}")

    rows = []

    # ── Dijkstra del alumno ──────────────────────────────────────
    result_dij = None
    if STUDENT_IMPL:
        try:
            t0 = time.time()
            result_dij = dijkstra(prob['graph'], prob['source'], prob['target'])
            elapsed = time.time() - t0

            ok = verify_result(result_dij, prob['optimal_dist'],
                               prob['optimal_path'], 'P1', 'Dijkstra')

            d_target = result_dij['distances'].get(prob['target'])
            rows.append(('Dijkstra', d_target, result_dij.get('path'),
                         len(result_dij.get('steps', [])), elapsed, ok))
        except Exception as e:
            print(f"  [✗] Error en Dijkstra: {e}")
            import traceback; traceback.print_exc()
            rows.append(('Dijkstra', None, None, 0, 0, False))

    # ── Bellman-Ford del alumno (comparativa) ────────────────────
    if STUDENT_IMPL:
        try:
            t0 = time.time()
            result_bf = bellman_ford(prob['graph'], prob['source'], prob['target'])
            elapsed = time.time() - t0

            d_target = result_bf['distances'].get(prob['target'])
            ok_bf = (d_target is not None and
                     abs(d_target - prob['optimal_dist']) < 1e-6)
            rows.append(('Bellman-Ford', d_target, result_bf.get('path'),
                         len(result_bf.get('steps', [])), elapsed, ok_bf))
            if ok_bf:
                print(f"  [✓] P1/Bellman-Ford: distancia correcta = {d_target}")
            else:
                print(f"  [✗] P1/Bellman-Ford: distancia = {d_target}")
        except Exception as e:
            print(f"  [✗] Error en Bellman-Ford (P1): {e}")
            rows.append(('Bellman-Ford', None, None, 0, 0, False))

    print_result_table(rows, "Comparativa P1")

    # ── Gráficas ─────────────────────────────────────────────────
    ax_graph = fig.add_subplot(gs_row[0])
    ax_sol = fig.add_subplot(gs_row[1])

    draw_graph(prob['graph'], prob['pos'], ax=ax_graph,
               title='P1: Grafo — Red de mensajería')

    if result_dij and result_dij.get('path'):
        draw_solution(prob['graph'], prob['pos'], result_dij['path'],
                      result_dij['distances'], prob['source'], prob['target'],
                      ax=ax_sol, title='P1: Camino mínimo (Dijkstra)')
    else:
        draw_graph(prob['graph'], prob['pos'], ax=ax_sol,
                   title='P1: Solución no disponible')

    # ── Animación ────────────────────────────────────────────────
    if result_dij and result_dij.get('steps'):
        animate_algorithm(
            prob['graph'], prob['pos'], result_dij['steps'],
            result_dij.get('path'), prob['source'], prob['target'],
            filename='dijkstra_p1.gif', algorithm_name='Dijkstra',
            fps=1, hold_last=3
        )

    return result_dij


# ══════════════════════════════════════════════════════════════════
# PROBLEMA 2: BELLMAN-FORD
# ══════════════════════════════════════════════════════════════════

def run_problem_2(fig, gs_row):
    prob = create_problem_bellman_ford()
    print_header(f"PROBLEMA 2: {prob['name']}")
    print(f"  {prob['description']}")
    print(f"  Origen: {prob['source']},  Destino: {prob['target']}")
    print(f"  Solución esperada: dist = {prob['optimal_dist']}, "
          f"camino = {prob['optimal_path']}")

    rows = []

    # ── Dijkstra del alumno (debería fallar) ─────────────────────
    result_dij_wrong = None
    if STUDENT_IMPL:
        try:
            t0 = time.time()
            result_dij_wrong = dijkstra(prob['graph'], prob['source'], prob['target'])
            elapsed = time.time() - t0

            d_target = result_dij_wrong['distances'].get(prob['target'])
            ok = (d_target is not None and
                  abs(d_target - prob['optimal_dist']) < 1e-6)
            rows.append(('Dijkstra ⚠', d_target, result_dij_wrong.get('path'),
                         len(result_dij_wrong.get('steps', [])), elapsed, ok))
            if not ok:
                print(f"  [!] P2/Dijkstra produce distancia = {d_target} "
                      f"(esperada {prob['optimal_dist']}) — comportamiento esperado")
            else:
                print(f"  [?] P2/Dijkstra coincide — revisar grafo")
        except Exception as e:
            print(f"  [!] Error en Dijkstra (P2): {e}")
            rows.append(('Dijkstra ⚠', None, None, 0, 0, False))

    # ── Bellman-Ford del alumno ──────────────────────────────────
    result_bf = None
    if STUDENT_IMPL:
        try:
            t0 = time.time()
            result_bf = bellman_ford(prob['graph'], prob['source'], prob['target'])
            elapsed = time.time() - t0

            ok = verify_result(result_bf, prob['optimal_dist'],
                               prob['optimal_path'], 'P2', 'Bellman-Ford')

            d_target = result_bf['distances'].get(prob['target'])
            neg_cycle = result_bf.get('has_negative_cycle', None)
            rows.append(('Bellman-Ford', d_target, result_bf.get('path'),
                         len(result_bf.get('steps', [])), elapsed, ok))
            if neg_cycle:
                print(f"  [!] Bellman-Ford detecta ciclo negativo — "
                      f"no debería en este problema")
            else:
                print(f"  [✓] Bellman-Ford: sin ciclo negativo (correcto)")
        except Exception as e:
            print(f"  [✗] Error en Bellman-Ford (P2): {e}")
            import traceback; traceback.print_exc()
            rows.append(('Bellman-Ford', None, None, 0, 0, False))

    print_result_table(rows, "Comparativa P2 — Dijkstra vs Bellman-Ford")

    # ── Gráficas ─────────────────────────────────────────────────
    ax_graph = fig.add_subplot(gs_row[0])
    ax_sol = fig.add_subplot(gs_row[1])

    # Resaltar aristas negativas
    neg_edges = [(u, v) for u, v, w in get_all_edges(prob['graph']) if w < 0]
    node_colors_neg = {prob['source']: '#42a5f5', prob['target']: '#ef5350'}
    draw_graph(prob['graph'], prob['pos'], ax=ax_graph,
               title='P2: Red de distribución (arcos negativos en naranja)',
               highlight_edges=neg_edges,
               highlight_nodes=node_colors_neg)

    if result_bf and result_bf.get('path'):
        draw_solution(prob['graph'], prob['pos'], result_bf['path'],
                      result_bf['distances'], prob['source'], prob['target'],
                      ax=ax_sol, title='P2: Camino mínimo (Bellman-Ford)')
    else:
        draw_graph(prob['graph'], prob['pos'], ax=ax_sol,
                   title='P2: Solución no disponible')

    # ── Animación ────────────────────────────────────────────────
    if result_bf and result_bf.get('steps'):
        animate_algorithm(
            prob['graph'], prob['pos'], result_bf['steps'],
            result_bf.get('path'), prob['source'], prob['target'],
            filename='bellman_ford_p2.gif', algorithm_name='Bellman-Ford',
            fps=1, hold_last=3
        )

    return result_bf


# ══════════════════════════════════════════════════════════════════
# PROBLEMA 3: DETECCIÓN DE CICLO NEGATIVO (ARBITRAJE)
# ══════════════════════════════════════════════════════════════════

def run_problem_3(fig, gs_row):
    prob = create_problem_negative_cycle()
    print_header(f"PROBLEMA 3: {prob['name']}")
    print(f"  {prob['description']}")
    print(f"  Origen: {prob['source']}")
    print(f"  Ciclo negativo esperado: {prob['has_negative_cycle']}")

    # ── Bellman-Ford del alumno ──────────────────────────────────
    result_bf = None
    if STUDENT_IMPL:
        try:
            t0 = time.time()
            # target = source (no buscamos camino, solo detectar ciclo)
            result_bf = bellman_ford(prob['graph'], prob['source'], prob['source'])
            elapsed = time.time() - t0

            neg_cycle = result_bf.get('has_negative_cycle', False)
            n_steps = len(result_bf.get('steps', []))

            if neg_cycle == prob['has_negative_cycle']:
                print(f"  [✓] P3/Bellman-Ford: has_negative_cycle = {neg_cycle} (correcto)")
            else:
                print(f"  [✗] P3/Bellman-Ford: has_negative_cycle = {neg_cycle} "
                      f"(esperado {prob['has_negative_cycle']})")
            print(f"      Pasadas realizadas: {n_steps}")
            print(f"      Tiempo: {elapsed:.4f}s")

        except Exception as e:
            print(f"  [✗] Error en Bellman-Ford (P3): {e}")
            import traceback; traceback.print_exc()

    # ── Tabla de tasas ───────────────────────────────────────────
    if prob.get('rates'):
        print(f"\n  Tasas de cambio originales:")
        for (u, v), r in sorted(prob['rates'].items()):
            w = -np.log(r)
            print(f"    {u:>3} → {v:<3}:  tasa = {r:>10.4f},  "
                  f"peso = -ln({r:.4f}) = {w:>8.4f}")

    # ── Gráficas ─────────────────────────────────────────────────
    ax_graph = fig.add_subplot(gs_row[0])
    ax_info = fig.add_subplot(gs_row[1])

    draw_graph(prob['graph'], prob['pos'], ax=ax_graph,
               title='P3: Grafo de divisas (w = −ln r)')

    # Panel informativo
    ax_info.axis('off')
    info_lines = [
        f"Problema 3: Detección de arbitraje",
        f"",
        f"Ciclo EUR → USD → GBP → EUR",
    ]
    if prob.get('rates'):
        r1 = prob['rates'][('EUR', 'USD')]
        r2 = prob['rates'][('USD', 'GBP')]
        r3 = prob['rates'][('GBP', 'EUR')]
        prod = r1 * r2 * r3
        info_lines += [
            f"  {r1:.2f} × {r2:.2f} × {r3:.2f} = {prod:.5f}",
            f"  Producto > 1 → arbitraje",
            f"",
            f"Pesos: −ln({r1:.2f}) − ln({r2:.2f}) − ln({r3:.2f})",
            f"     = {-np.log(r1):.4f} + {-np.log(r2):.4f} + {-np.log(r3):.4f}",
            f"     = {-np.log(prod):.4f} < 0 → ciclo negativo",
        ]
    if result_bf:
        info_lines += [
            f"",
            f"Resultado Bellman-Ford:",
            f"  has_negative_cycle = {result_bf.get('has_negative_cycle', '?')}",
            f"  pasadas = {len(result_bf.get('steps', []))}",
        ]
    ax_info.text(0.05, 0.95, '\n'.join(info_lines),
                 transform=ax_info.transAxes, fontsize=9,
                 verticalalignment='top', fontfamily='monospace',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#f5f5f5',
                           edgecolor='#ccc'))
    ax_info.set_title('P3: Análisis de arbitraje', fontsize=10, fontweight='bold')

    return result_bf


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════

def run_tests():
    if not STUDENT_IMPL:
        print("\n[!] No se encontró la implementación del alumno.")
        print("    Completad lab_template_caminos.py y ejecutad de nuevo.")
        return

    fig = plt.figure(figsize=(16, 18))
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.25)

    # ── Problema 1 ───────────────────────────────────────────────
    run_problem_1(fig, [gs[0, 0], gs[0, 1]])

    # ── Problema 2 ───────────────────────────────────────────────
    run_problem_2(fig, [gs[1, 0], gs[1, 1]])

    # ── Problema 3 ───────────────────────────────────────────────
    run_problem_3(fig, [gs[2, 0], gs[2, 1]])

    # ── Guardar ──────────────────────────────────────────────────
    fig.suptitle("Laboratorio Caminos Mínimos — Dijkstra y Bellman-Ford",
                 fontsize=14, fontweight='bold', y=0.98)

    plt.savefig('resultados_caminos.pdf', bbox_inches='tight', dpi=150)
    plt.savefig('resultados_caminos.png', bbox_inches='tight', dpi=150)
    print(f"\n{'═' * 70}")
    print(f"  [✓] Resultados guardados:")
    print(f"      resultados_caminos.pdf")
    print(f"      resultados_caminos.png")
    print(f"      dijkstra_p1.gif     (si Dijkstra implementado)")
    print(f"      bellman_ford_p2.gif  (si Bellman-Ford implementado)")
    print(f"{'═' * 70}")

    plt.show()


if __name__ == '__main__':
    run_tests()
