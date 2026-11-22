# 📏 Brechas: Preguntas de Negocio vs. Maqueta vs. App vs. Rúbrica

> **Fuentes contrastadas:** [`../Posibles Preguntas.md`](../Posibles%20Preguntas.md) · [`../presentacion/Maqueta.excalidraw`](../presentacion/Maqueta.excalidraw) · [`../app/app.py`](../app/app.py) · [`../Rubrica_CMT8002.md`](../Rubrica_CMT8002.md)

La rúbrica técnica de **David Chira** asigna **25%** a que *"Todos los gráficos de la maqueta responden a las preguntas del negocio; cada pregunta cuenta con al menos una visualización que la resuelve con claridad"*.

---

## 1. Matriz de Trazabilidad (`P1`–`P6`)

| Pregunta | Enfoque | En Maqueta (`Excalidraw`) | En `app/app.py` | Estado / Acción Requerida |
| :--- | :--- | :--- | :--- | :--- |
| **P1** | Total denuncias por año, proporción canal digital vs presencial, tasa global de resolución y pérdida económica | ✅ KPIs + Gráfico Evolución Anual (Pág. 1) | ⚠️ Parcial (Pág. 1) | Corregir formato de pérdida (`S/ 4,093 M`), tooltip de `% denuncia digital` y hacer explícita la proporción **Digital vs Presencial** (ej. en subtítulo o tooltip). |
| **P2** | Evolución **mensual** de denuncias en **2026 vs mismo periodo 2025** (estacionalidad) | ❌ No presente (Pág. 2 muestra serie *anual* indexada Ene–Oct 2018–2026) | ❌ No presente | **Brecha:** Incorporar gráfico de líneas mensual `Ene–Oct 2025` vs `Ene–Oct 2026` (aprovechando `Es_Comparable_Ene_Oct = 1` en `Dim_Calendario.csv`) tanto en la maqueta como en la app. |
| **P3** | Modalidades con mayor volumen vs modalidades con mayor **impacto económico** | ✅ Pág. 1 (volumen + resolución) y Pág. 2 (pérdida `Estafa S/ 686 M`, `Extorsión S/ 543 M`) | ⚠️ Solo Pág. 1 (con bug de share vs resolución) | Corregir tasa de resolución en Pág. 1 y construir Pág. 2 en `app.py` mostrando el daño económico por modalidad. |
| **P4** | Regiones y distritos líderes en volumen absoluto **y riesgo relativo por cada 10,000 hab.** | ⚠️ Parcial (Top 6 regiones por volumen; menciona drill-through distrital sin maqueta de tasa per cápita) | ⚠️ Solo Top 6 regiones por volumen | **Brecha:** Usar `Poblacion_Estimada` de `Dim_Ubicacion.csv` para calcular `(Denuncias / Poblacion_Estimada) * 10000` (con filtro/toggle Volumen vs Tasa x 10k hab.) e implementar detalle distrital interactivo. |
| **P5** | Franjas horarias donde se concentran las principales modalidades (turnos de patrullaje) | ✅ Heatmap Modalidad × Franja Horaria (Pág. 1) | ✅ Heatmap implementado | Validar consistencia cuando se apliquen filtros (manejo de filas vacías si se filtra una sola modalidad). |
| **P6** | Variación de **tiempo promedio de respuesta** y **tasa de resolución** en Estado de Emergencia vs sin declaratoria | ⚠️ Solo texto resumen en KPI 4 (`40.0 min en Emergencia`) | ❌ Roto (`±0.0 min` fijo; sin tasa de resolución comparada) | **Brecha:** Agregar comparativa clara (tarjeta o mini-gráfico) de **Con Estado de Emergencia vs Sin Declaratoria** mostrando tanto **tiempo promedio de respuesta** (`32.3 min` vs `42.2 min`) como **tasa de resolución**. |

---

## 2. Revisión de la Página 2 (Dashboard Aclaratorio) frente a los 4 Pasos de Storytelling

La Página 2 diseñada en `Maqueta.excalidraw` está **muy bien alineada** con la rúbrica de David Chira (*Aplicación de los 4 primeros pasos del Data Storytelling*):
1. **Paso 1 (Mensaje y acción):** Título accionable claro (*"Crear unidades especializadas en Extorsión y Estafa..."*) + caja explícita de *ACCIÓN RECOMENDADA (FOCALIZACIÓN)*.
2. **Paso 2 (Gráfico adecuado):**
   - Líneas indexadas (`Base 2018 = 100`, periodo comparable `Ene–Oct`) para evidenciar el quiebre de tendencia (`Extorsión 7.6x`, `Estafa 4.4x` vs `Robo -47%`).
   - Barras horizontales ordenadas para resaltar la brecha de resolución (`9.4%` y `11.2%` vs promedio `23.5%`) y daño económico (`S/ 1,229 M` conjuntos).
3. **Paso 3 (Eliminar desorden):** Sin cuadrículas innecesarias, etiquetas directas en series y jerarquía limpia en dos bloques.
4. **Paso 4 (Capturar atención):** Uso intencional de color focal (rojo/acento solo en Extorsión y Estafa; gris/azul apagado en el resto de modalidades).

> **Pendiente clave:** Llevar esta Página 2 de `Maqueta.excalidraw` a código funcional en `app/app.py` (calculando dinámicamente todos los índices y cifras con DuckDB para evitar inconsistencias con los datos reales).

---

## 3. Recordatorio para la Rúbrica de Martín Alcandré (Sustentación)

Además de los gráficos, preparar evidencia concreta para la reflexión de ~3 minutos:
- **Acuerdos clave:** Definición del modelo estrella de SIDPOL, reparto entre limpieza/normalización del dataset y desarrollo en **Streamlit + DuckDB**.
- **Dificultades/decisiones:** Por qué se eligió Streamlit + DuckDB (reproducibilidad, consultas SQL rápidas sobre `378k` registros, control fino del diseño para aplicar los principios de storytelling) y cómo resolvieron la comparabilidad de `2026` incompleto (`Ene–Oct`).
