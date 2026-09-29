"""
Laboratorio: Caminos mínimos — Dijkstra y Bellman-Ford
UCM — Flujos en Redes (3.º Matemáticas)

Completad las dos funciones. No modificar helpers_caminos.py.
Ejecutad test_env_caminos.py para comprobar los resultados.
"""

from typing import Dict, List, Tuple, Optional
from helpers_caminos import reconstruct_path, get_all_nodes


# ─────────────────────────────────────────────────────────────────
# FUNCIÓN 1: DIJKSTRA
# ─────────────────────────────────────────────────────────────────

def dijkstra(graph: Dict[str, Dict[str, float]], source: str, target: str) -> dict:
    todos = get_all_nodes(graph)
    dist = {j: float('inf') for j in todos}
    dist[source] = 0
    prev = {j: None for j in todos}
    if source in graph:
        for j, peso in graph[source].items():
            dist[j] = peso
            prev[j] = source
    P = {source}
    T = set(todos)
    T.discard(source)
    paso = []
    while T:
        k = min(T, key=lambda j: dist[j])
        # si el camino mínimo es infinito, el bucle se para pues los nodos de T son inalcanzables
        if dist[k] == float('inf'):
            break
        P.add(k)
        T.remove(k)
        paso.append({'current': k, 'distancias': dict(dist), 'predecessors': dict(prev), 'visited': set(P)})
        if k == target:
            break
        if k in graph:
            for j, d_kj in graph[k].items():
                if j in T and dist[k] + d_kj < dist[j]:
                    dist[j] = dist[k] + d_kj
                    prev[j] = k
    path = reconstruct_path(prev, source, target)
    return {'distances': dist, 'predecessors': prev, 'path': path, 'steps': paso}
    pass


# ─────────────────────────────────────────────────────────────────
# FUNCIÓN 2: BELLMAN-FORD
# ─────────────────────────────────────────────────────────────────

def bellman_ford(graph: Dict[str, Dict[str, float]], source: str, target: str) -> dict:
    V = get_all_nodes(graph)
    n = len(V)
    dist = {j: float('inf') for j in V}
    dist[source] = 0
    prev = {j: None for j in V}
    if source in graph:
        for j, peso in graph[source].items():
            dist[j] = peso
            prev[j] = source
    paso = []  # paso es una lista donde guardo los registros
    for t in range(n-1):
        updated_edges = []
        cambio = False
        for k in graph:
            for j, d_kj in graph[k].items():
                if dist[k] + d_kj < dist[j]:
                    dist[j] = dist[k] + d_kj
                    prev[j] = k
                    updated_edges.append((k, j))
                    cambio = True
        paso.append({'iteration': t+1, 'distances': dict(dist), 'predecessors': dict(prev),
                     'updated_edges': updated_edges})
        if not cambio:
            break
    has_negative_cycle = False
    for k in graph:
        for j, d_kj in graph[k].items():
            if dist[k] + d_kj < dist[j]:
                has_negative_cycle = True
                break
        if has_negative_cycle:
            break
    path = reconstruct_path(prev, source, target)
    return {'distances': dist, 'predecessors': prev, 'path': path, 'steps': paso,
            'has_negative_cycle': has_negative_cycle}
    pass


# ─────────────────────────────────────────────────────────────────
# REFLEXIÓN (responder aquí como comentario)
# ─────────────────────────────────────────────────────────────────
#
# P1. Ejecutad Dijkstra sobre el Problema 2 (arcos negativos).
#     ¿Qué camino devuelve y con qué coste? ¿Por qué falla?
#     ¿Qué nodo se marca como permanente prematuramente?
#
# P1: Nos devuelve Madrid -> Guadalajara -> Cuenca -> Valencia, con un coste de 11.
#      Falló porque al ver el peso de Guadalajara menor que el de Toledo decidió tomar el de Guadalajara.
#      El problema fue cuando Toledo tenía un peso negativo, por lo que no pudo rectificarse.
#       Dijkstra toma el primer peso más barato y no vuelve a mirar otra vez.
#       Además, el algoritmo trabaja con pesos positivos y mayores que cero, que a medida que busca un camino
#       asume que el coste total va ser mayor.
#       Por tanto, la no previsión de un peso negativo provocó que se dejará de buscar un camino óptimo.
#       Se marcó prematuramente a Guadalajara.

# P2. Comparad el número de comprobaciones de arcos de Dijkstra
#     y Bellman-Ford en el Problema 1. ¿Por qué Dijkstra necesita
#     menos? Relacionad con O(n^2) frente a O(n^3).
#
# P2:Dijkstra asume que no hay pesos negativos y se pone encontrar un camino,
#      mientras que Bellman-Ford necesita comprobar todo el grafo entero p para ester seguro.
#     Dijkstra tiene O(n^2) pues evalua en cada nodo n uno sola vez y comprueba sus conexiones con los otros nodos,
#     hasta n conexiones. De modo que es una operacion de n.n = n^2.
#       Bellman-Ford tiene O(n^3) pues debe recorrer cada nodo y el grafo completo,
#       sumándole que también revisa cada arista y los pesos negativos, la operación de comprobar todo eso
#        aumenta más que O(n^2).

# P3. En el Problema 3, la transformación w = -ln(r) exige r > 0.
#     ¿Es razonable? Si Bellman-Ford no detecta ciclo negativo,
#     ¿significa que no hay ninguna oportunidad de beneficio, o solo
#     que no hay arbitraje sin riesgo? Razonad la diferencia.
#
# P3: Es razonable pues estamos trabajando con valores monetarios positivos reales, que nunca son ceros ni negativos.
#     Por tanto, la fórmula funciona siempre.
#     Significa que no hay dinero gratis e instantáneo. La diferencia se encuentra en que "arbitraje" comprueba si
#     puedes cambiar monedas en círculo en ese mismo instante para ganar sin riesgo.
#     Si no encuentra un ciclo, es que ese atajo fácil no existe. Mientras que en el caso de
#     "especulación", sigues pudiendo comprar hoy y esperar que mañana valga más.
#     Pero para ello necesitas tiempo y tomar el riesgo de perder.
#
# P4. ¿Qué ocurre si aplicáis Bellman-Ford al Problema 1?
#     ¿Resultado correcto? ¿Cuántas pasadas antes de la convergencia
#     anticipada vs. iteraciones de Dijkstra?
#
# P4: Si aplicamos Bellman-Ford obtenemos lo mismo que Dijkstra, que es 14 por tanto correcto.
#     Bellman sólo se necesito 2 iteraciones para obtener el resultado, pues comprobó todo el grafo el primera y en la
#      segunda al no haber una distancia que pudiese mejorar paró.
#      Dijkstra necesito 7 iteraciones pues necesitaba comprobar, evaluar y cerrar en cada nodo hasta
#      llegar el nodo final.

# OPCIONAL. Suponed que cada conversión de divisas tiene una comisión
# fija de c euros. ¿Cómo modificaríais los pesos? ¿Sigue siendo
# válida la transformación logarítmica? Si no, proponed alternativa.
#
# OPCIONAL: Como nos quita c euros fijos podemos cambiar el tasa de cambio r por una nueva que tenga tambien la
#           comision. Entonces, sea K la cantidad de dinero que queremos cambiar de divisa, K·r-c. Obtenemos la divisa
#           monetaria cambiada final. Como queremos saber la tasa que ha variado con la comision, lo dividmos por K,
#           obteniendo r_nuevo = r - c/K. Luego, deja de funcionar la transformación logarítmica, pues no podemos
#           separar la resta dentro de un logaritmo o en el peor de los casos que r < c/K.
#           Para resolver el problema podemos convertir la comisión c en una comisión porcentual, de manera que basta
#           con ver el porcentaje que nos quita y multiplicarlo por la tasa de cambio. De esta forma, podemos mantener
#           la estructura que tenemos.
