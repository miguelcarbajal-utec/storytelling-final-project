# 📊 Proyecto Final: Observatorio SIDPOL — Data Storytelling (CMT8002)

> **Materia:** Comunicación efectiva y storytelling con datos — Ciclo 1  
> **Docentes:** David Chira (Componente Técnico / Storytelling) · Martín Alcandré (Comunicación y Liderazgo)  
> **Repositorio Colaborativo:** GitHub (cuenta institucional UTEC — carpeta raíz `final-project/`)  
> **Hub del Vault (Obsidian):** [[ciclo-1/data-storytelling/Index - Data Storytelling|Volver al Índice de Data Storytelling]]

---

## 📚 Documentos y Artefactos del Proyecto

- [📋 Indicaciones Oficiales y Ejemplos](./Proyecto%20Final%20-%20Indicaciones.md)
- [📏 Rúbrica de Evaluación (Martín Alcandré & David Chira)](./Rubrica_CMT8002.md)
- [❓ Listado de Preguntas de Negocio (P1–P6)](./Posibles%20Preguntas.md)
- [🎨 Maqueta en Excalidraw (Pág. 1 Exploratorio + Pág. 2 Aclaratorio)](./presentacion/Maqueta.excalidraw)
- [🔍 Auditoría y Hallazgos Detectados](./hallazgos/00_Resumen_Hallazgos.md)
- [💻 Prototipo Streamlit (`app/app.py`)](./app/app.py)

---

## 🧭 Contexto del Proyecto y Modelo de Datos

- **Tema:** **Observatorio SIDPOL** — Análisis de Denuncias Policiales en Perú (`2018–2026`, con `2026*` comparable de enero a octubre).
- **Volumen consolidado:** `378,187` registros en tabla de hechos (`7,614,774` denuncias acumuladas).
- **Arquitectura de Datos (Modelo Estrella en `app/dataset/`):**
  - `Fact_Denuncias.csv`: métricas de denuncias, casos resueltos, tiempo de respuesta (min), pérdida económica (PEN) y bandera `Estado_Emergencia`.
  - `Dim_Calendario.csv` (`106` periodos, incluye bandera `Es_Comparable_Ene_Oct`), `Dim_Ubicacion.csv` (`1,840` distritos con `Poblacion_Estimada`), `Dim_Modalidad.csv` (`7` modalidades), `Dim_Franja_Horaria.csv` (`4` franjas) y `Dim_Canal.csv` (`2` canales).

---

## 🛠️ Decisiones de Arquitectura y Stack Técnico

> Registro de acuerdos técnicos del equipo *(actualizado al 22 de noviembre de 2026)*.

| Componente | Decisión | Justificación / Rol en el Proyecto | Estado |
| :--- | :--- | :--- | :--- |
| **Interfaz / Dashboards** | **Streamlit + Plotly** | Construcción de los dashboards **Exploratorio (Pág. 1)** y **Aclaratorio / Storytelling (Pág. 2)** con control preciso de jerarquía visual, color focal y títulos accionables. | 🔄 Prototipo Pág. 1 implementado |
| **Motor Analítico** | **DuckDB** | Lectura y agregaciones SQL sobre los CSV del modelo estrella para evitar múltiples `.merge()` en memoria y acelerar consultas filtradas. | ⏳ Pendiente migrar `app.py` (hoy usa Pandas) |
| **Dataset Base** | **Modelo Estrella CSV limpio** | 6 archivos normalizados en `app/dataset/` con **0 nulos** en cruces referenciales. | ✅ Completado |
| **Colaboración y Versionado** | **GitHub (Cuenta UTEC)** | Subida completa de `final-project/` como repositorio compartido para que todo el equipo aporte mediante ramas/PRs. | 🔄 En preparación para push |

### 💡 Alineación con la Rúbrica
- **Componente Técnico (David Chira):** Asegurar que cada pregunta (`P1`–`P6`) tenga visualización clara, corregir los bugs de la Página 1, cubrir las brechas detectadas (`P2` mensual 2026 vs 2025, `P4` tasa por 10,000 hab. + detalle distrital, `P6` comparativa Estado de Emergencia) e implementar la Página 2 (4 pasos de Data Storytelling). Ver detalle en [02_Brechas_Preguntas_Maqueta_Rubrica.md](./hallazgos/02_Brechas_Preguntas_Maqueta_Rubrica.md).
- **Comunicación y Liderazgo (Martín Alcandré):** Documentar aquí las decisiones clave (elección de Streamlit + DuckDB, flujo de trabajo en GitHub UTEC, validación cruzada de cifras entre equipo de datos y desarrollo) como insumos concretos para la reflexión final de 3 minutos.

---

## 👥 Bitácora de Coordinación y Avance (*Team Log*)

### 📌 Estado actual (22 Nov 2026)
- [x] Exportación de indicaciones, imágenes de ejemplo y rúbrica unificada al vault.
- [x] Limpieza, normalización y modelado estrella de los 6 CSV de SIDPOL (`app/dataset/`).
- [x] Redacción de preguntas de negocio (`Posibles Preguntas.md`, `P1`–`P6`).
- [x] Diseño de maqueta de 2 páginas (`presentacion/Maqueta.excalidraw`).
- [x] Primer prototipo funcional de Página 1 en Streamlit (`app/app.py`) + auditoría completa en `hallazgos/`.
- [ ] **En curso:** Subir `final-project/` a GitHub (cuenta UTEC) para trabajo colaborativo.
- [ ] **Siguiente sprint:**
  1. Corregir bugs P0 en `app/app.py` (tasa de resolución, KPIs dinámicos y tooltips).
  2. Migrar carga/consultas a **DuckDB** y actualizar `app/requirements.txt`.
  3. Resolver brechas `P2`, `P4` y `P6` e implementar la **Página 2 (Dashboard Aclaratorio)**.
  4. Armar la presentación PPT (contexto del dataset, preguntas, maqueta y guion de sustentación).

### 📝 Registro de Acuerdos y Decisiones
- **2026-11-22 (10:54) — Acuerdo de Stack:** Se define **Streamlit + DuckDB** como stack del proyecto.
- **2026-11-22 (11:30) — Avance paralelo:** El equipo entregó los CSV limpios en modelo estrella (`app/dataset/`), el borrador de preguntas `P1`–`P6`, la maqueta en Excalidraw y el prototipo inicial de Página 1 en Streamlit.
- **2026-11-22 (12:02) — Auditoría y Repositorio Compartido:** Se documentaron los hallazgos técnicos y brechas en `hallazgos/` y se prepara `final-project/` (con `.gitignore`) para subirlo a GitHub bajo la cuenta UTEC.

---

## 🗂️ Estructura Actual del Repositorio (`final-project/`)

```text
final-project/
├── .gitignore                            # Ignora .DS_Store, .venv, __pycache__, etc.
├── 00_Plan_y_Decisiones.md               # Plan maestro, stack, bitácora y enlaces
├── Proyecto Final - Indicaciones.md      # Consigna y ejemplos visuales del docente
├── Rubrica_CMT8002.md                    # Rúbrica oficial (Martín Alcandré & David Chira)
├── Posibles Preguntas.md                 # Preguntas de negocio P1–P6
├── hallazgos/                            # Auditoría técnica, brechas y cifras base
│   ├── 00_Resumen_Hallazgos.md
│   ├── 01_Bugs_y_Deuda_Tecnica_App.md
│   ├── 02_Brechas_Preguntas_Maqueta_Rubrica.md
│   └── 03_Resumen_Dataset_y_Metricas_Base.md
├── app/                                  # Aplicación Streamlit (+ migración a DuckDB)
│   ├── app.py
│   ├── main.py                           # (Por eliminar: plantilla PyCharm)
│   ├── requirements.txt
│   └── dataset/                          # 6 CSV del modelo estrella SIDPOL (~18.6 MB total)
├── presentacion/                         # Maqueta Excalidraw y futura PPT
│   └── Maqueta.excalidraw
├── imagenes/                             # Imágenes de ejemplo extraídas de indicaciones
└── data/                                 # Carpeta vacía (evaluar consolidar con app/dataset)
```
