# 🔍 Hallazgos y Auditoría Técnica — Observatorio SIDPOL

> **Fecha de revisión:** 22 de noviembre de 2026  
> **Alcance:** Revisión de `app/app.py`, `app/requirements.txt`, `app/dataset/`, `Posibles Preguntas.md`, `presentacion/Maqueta.excalidraw` y alineación con `Rubrica_CMT8002.md`.  
> **Volver al Plan:** [00_Plan_y_Decisiones.md](../00_Plan_y_Decisiones.md)

---

## 📂 Documentos en esta carpeta

1. **[01_Bugs_y_Deuda_Tecnica_App.md](./01_Bugs_y_Deuda_Tecnica_App.md)** — Bugs detectados en `app/app.py` (cálculos, textos hardcodeados, tooltips), migración pendiente a DuckDB y limpieza del repositorio.
2. **[02_Brechas_Preguntas_Maqueta_Rubrica.md](./02_Brechas_Preguntas_Maqueta_Rubrica.md)** — Matriz de trazabilidad entre las 6 preguntas de negocio (`P1`–`P6`), la maqueta en Excalidraw, la app actual y los criterios de la rúbrica.
3. **[03_Resumen_Dataset_y_Metricas_Base.md](./03_Resumen_Dataset_y_Metricas_Base.md)** — Esquema verificado del modelo estrella (`Fact_Denuncias.csv` + 5 dimensiones), integridad referencial y métricas globales de referencia para validar DuckDB.

---

## 🎯 Backlog Priorizado para el Equipo

### 🔴 Prioridad 0 — Corrección de Bugs Críticos (`app/app.py`)
- [ ] **Corregir gráfico `modal_fig` (`L367`):** Actualmente grafica `% participación del total` (`share`) en lugar de `% tasa de resolución` (`Casos_Resueltos / Cantidad_Denuncias`).
- [ ] **Eliminar hardcodes y typo en KPIs (`L286-305`):**
  - Corregir `"Extensión: 9.4% (mín.)"` → dinámico según filtros + ortografía `"Extorsión"`.
  - Corregir formato de pérdida económica (`S/ 4,093 M`) y subtítulo dinámico de pico anual.
  - Usar `emergency_time` (ya calculado en `L270-274`) en lugar de `"±0.0 min en Emergencia"`.
- [ ] **Corregir tooltip de `annual_fig` (`L346`):** Cambiar `"% resuelto"` por `"% denuncia digital"` y limpiar asignaciones repetidas de `annual["color"]` (`L314-320`).

### 🟠 Prioridad 1 — Brechas de Preguntas de Negocio (`P1`–`P6`)
- [ ] **P2 (Estacionalidad mensual 2026 vs 2025):** Agregar visualización o vista comparativa mensual 2026 vs mismo periodo 2025 (Ene–Oct).
- [ ] **P4 (Riesgo por 10,000 hab. y drill-down distrital):** Aprovechar `Poblacion_Estimada` de `Dim_Ubicacion.csv` para mostrar tasa por cada 10,000 habitantes y habilitar el detalle distrital (1,840 distritos) prometido en el subtítulo.
- [ ] **P6 (Evaluación Estado de Emergencia):** Agregar comparativa explícita de **tiempo de respuesta** y **tasa de resolución** entre zonas con y sin Estado de Emergencia.

### 🟡 Prioridad 2 — Arquitectura DuckDB + Página 2 (Storytelling)
- [ ] Agregar `duckdb` a `app/requirements.txt` y migrar `load_data()` + agregaciones a consultas SQL con DuckDB.
- [ ] Implementar la **Página 2: Dashboard Aclaratorio** diseñada en `presentacion/Maqueta.excalidraw` (evolución indexada Base 2018=100, brecha de resolución y pérdida económica de Estafa/Extorsión, y bloque de acción recomendada en los 3 focos críticos).

### 🟢 Prioridad 3 — Higiene del Repositorio GitHub
- [ ] Eliminar plantilla vacía `app/main.py` de PyCharm.
- [ ] Consolidar el uso de `app/dataset/` vs `data/` para no confundir rutas entre compañeros.
