# 🐛 Bugs y Deuda Técnica en `app/app.py`

> **Archivo auditado:** [`../app/app.py`](../app/app.py) (505 líneas) y [`../app/requirements.txt`](../app/requirements.txt)

---

## 1. Bugs Funcionales y de Datos

### 🔴 Bug 1: `modal_fig` muestra `% de participación` en lugar de `% Casos Resueltos`
- **Ubicación:** `app/app.py`, líneas `362–383` (y tarjeta en `475–481`).
- **Problema:** El título y subtítulo dicen *"Volumen y Tasa de Resolución por Modalidad"* y *"Etiqueta derecha: % Casos Resueltos"*, pero el cálculo actual es:
  ```python
  mod["share"] = mod["Cantidad_Denuncias"] / mod_total * 100
  ```
  Esto muestra qué porcentaje del total de denuncias representa cada delito (ej. `Otros ≈ 36.8%`), en lugar de la tasa de resolución (`Casos_Resueltos / Cantidad_Denuncias * 100`), que según el dataset real y la maqueta debe ser:
  - `Secuestro`: **42.2%**
  - `Violencia F.`: **34.1%**
  - `Otros`: **22.0%**
  - `Hurto`: **18.1%**
  - `Robo`: **14.2%**
  - `Estafa`: **11.2%**
  - `Extorsión`: **9.4%**
- **Solución:** Agregar `Casos_Resueltos` en el `groupby("Modalidad")` y calcular `mod["resolution_rate"] = mod["Casos_Resueltos"] / mod["Cantidad_Denuncias"] * 100`.

### 🔴 Bug 2: KPIs con textos estáticos (*hardcoded*) y error tipográfico
- **Ubicación:** `app/app.py`, líneas `277–305`.
- **Detalle por KPI:**
  1. **KPI 2 (`TASA DE RESOLUCIÓN`, `L289`):** Dice `'Extensión: 9.4% (mín.)'` — tiene un typo (*Extensión* por *Extorsión*) y permanece fijo aunque el usuario filtre por otra modalidad, región o año. Debe calcularse dinámicamente sobre `filtered` (ej. mostrando la modalidad con menor tasa dentro de la selección actual).
  2. **KPI 3 (`PÉRDIDA ECONÓMICA EST.`, `L295–296`):**
     - `f'S/ {loss / 1_000_000:.3f} M'` imprime `S/ 4092.674 M` (sin separador de miles y con 3 decimales, diferente a `S/ 4,093 M` en la maqueta). Conviene formatear como `f"S/ {loss / 1_000_000:,.0f} M"`.
     - El subtítulo `'Pico en 2023: S/ 691 M'` está fijo; debe calcularse dinámicamente con el año de mayor pérdida dentro de `filtered`.
  3. **KPI 4 (`TIEMPO PROM. RESPUESTA`, `L303`):**
     - Imprime literalmente `'±0.0 min en Emergencia'`.
     - La variable `emergency_time` se calcula en `L270–274`, pero **nunca se utiliza**. En los datos globales: el promedio general es `40.0 min` y en Estado de Emergencia es `32.3 min` (`-7.7 min` respecto al promedio o `-9.9 min` frente a `42.2 min` sin emergencia).

### 🟠 Bug 3: Tooltip contradictorio en `annual_fig` y código muerto
- **Ubicación:** `app/app.py`, líneas `308–348`.
- **Problema:**
  - En `L309–313`, `annual["rate"]` calcula correctamente el `% de Denuncia Digital` (`ID_Canal == 1`), consistente con el subtítulo (`L469`: *Línea celeste: % Denuncia Digital*).
  - Sin embargo, el `hovertemplate` en `L346` dice `"%{x}: %{y:.1f}% resuelto<extra></extra>"`. Debe decir `% denuncia digital`.
  - En `L314–320`, `annual["color"]` se asigna 3 veces seguidas; las líneas `314–317` son código muerto sobrescrito por `L318–320`.

### 🟡 Bug 4: Promesa de Drill-through no implementada
- **Ubicación:** `app/app.py`, línea `487`.
- **Problema:** El subtítulo indica *"Clic derecho en región para Drill-through a detalle distrital (1,840 distritos)"*, pero el gráfico es estático (solo muestra Top 6 regiones) y Streamlit no soporta drill-through por clic derecho de Power BI de forma nativa.
- **Alternativa en Streamlit:** Usar `st.plotly_chart(..., on_select="rerun")` o un selector complementario de Departamento/Provincia/Distrito con tabla/gráfico de detalle distrital.

---

## 2. Deuda Técnica y Arquitectura

1. **Falta integrar DuckDB:**
   - `app/requirements.txt` solo lista `pandas`, `streamlit` y `plotly`. Falta agregar `duckdb`.
   - `load_data()` (`L16–45`) carga los 6 CSV completos en memoria y realiza 5 `.merge()` con Pandas en lugar de consultar con DuckDB (`read_csv_auto` o vistas en una conexión cacheada `@st.cache_resource`).
   - El filtrado y las agregaciones pueden ejecutarse vía SQL parametrizado en DuckDB, reduciendo consumo de RAM y simplificando consultas complejas (como evolución indexada Base 2018=100 o tasas por 10,000 habitantes).
2. **Falta Página 2 (Dashboard Aclaratorio — Storytelling):**
   - `app.py` solo implementa la **Página 1 · Exploratorio**.
   - Falta implementar la **Página 2 · Aclaratorio** diseñada en `presentacion/Maqueta.excalidraw` (navegación multipágina con `st.tabs`, `st.segmented_control` o páginas de Streamlit).
3. **Limpieza de archivos del proyecto:**
   - `app/main.py` contiene la plantilla por defecto de PyCharm (`print_hi('PyCharm')`) y debe eliminarse para no confundir el punto de entrada (`streamlit run app.py`).
   - Definir una única ruta de datos (`app/dataset/` vs `data/` en la raíz de `final-project/`) y documentarla en el `README`.
