# 📊 Observatorio SIDPOL — Proyecto Final de Data Storytelling (CMT8002)

Análisis exploratorio y narrativa visual con datos (**Data Storytelling**) sobre denuncias policiales registradas en el Sistema de Denuncias Policiales (**SIDPOL**, Perú, periodo **2018–2026\***).

> **Curso:** CMT8002 – Comunicación efectiva y storytelling con datos  
> **Docentes:** David Chira *(Componente Técnico / Storytelling)* · Martín Alcandré *(Comunicación y Liderazgo)*  
> **Planificación y bitácora:** [`00_Plan_y_Decisiones.md`](./00_Plan_y_Decisiones.md) · **Auditoría técnica:** [`hallazgos/00_Resumen_Hallazgos.md`](./hallazgos/00_Resumen_Hallazgos.md)

---

## 🎯 Entregables del Proyecto

1. **Presentación (`presentacion/`):** Contexto del dataset, listado de preguntas de negocio ([`Posibles Preguntas.md`](./Posibles%20Preguntas.md)) y maqueta de diseño ([`presentacion/Maqueta.excalidraw`](./presentacion/Maqueta.excalidraw)).
2. **Dashboard Exploratorio (`app/` — Página 1):** Exploración interactiva por año, región, modalidad y canal para responder las preguntas de negocio.
3. **Dashboard Aclaratorio (`app/` — Página 2, en desarrollo):** Narrativa enfocada en el hallazgo central (*explosión de Extorsión y Estafa vs. caída del Robo tradicional, brecha de resolución y focalización en 3 focos críticos*).

---

## 🛠️ Stack Tecnológico

- **Frontend / Dashboards:** Python + [Streamlit](https://streamlit.io/) + [Plotly](https://plotly.com/python/)
- **Motor Analítico:** [DuckDB](https://duckdb.org/) *(en migración desde Pandas para consultar directamente los CSV del modelo estrella mediante SQL)*
- **Prototipado / Maqueta:** Excalidraw

---

## 🚀 Cómo ejecutar la aplicación en local

> **Importante:** Ejecuta `streamlit run app.py` desde la carpeta `app/`, ya que el código carga el dataset usando la ruta relativa `dataset/`.

```bash
# 1. Clonar el repositorio
git clone https://github.com/miguelcarbajal-utec/storytelling-final-project.git
cd storytelling-final-project/app

# 2. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate        # En macOS / Linux
# .venv\Scripts\activate         # En Windows (PowerShell/CMD)

# 3. Instalar dependencias y lanzar Streamlit
pip install -r requirements.txt
streamlit run app.py
```

---

## 🗄️ Modelo de Datos (`app/dataset/`)

El dataset consolidado sigue un **modelo estrella** con **378,187** registros de hechos (**7,614,774** denuncias acumuladas, periodo `2018–2026*`, con `*2026` comparable de enero a octubre):

| Archivo | Tipo | Filas | Descripción |
| :--- | :--- | ---: | :--- |
| `Fact_Denuncias.csv` | Hechos | 378,187 | Denuncias, casos resueltos, tiempo de respuesta (min), pérdida económica (PEN) y bandera `Estado_Emergencia`. |
| `Dim_Calendario.csv` | Dimensión | 106 | Periodos mensuales (`2018–2026`) y bandera `Es_Comparable_Ene_Oct`. |
| `Dim_Ubicacion.csv` | Dimensión | 1,840 | `UBIGEO_HECHO`, departamento, provincia, distrito y `Poblacion_Estimada`. |
| `Dim_Modalidad.csv` | Dimensión | 7 | Modalidad delictiva y agrupación (`Grupo_Delito`). |
| `Dim_Franja_Horaria.csv` | Dimensión | 4 | Franjas horarias (`Madrugada`, `Mañana`, `Tarde`, `Noche`). |
| `Dim_Canal.csv` | Dimensión | 2 | Canal de registro (`Denuncia Digital` vs. `Presencial Comisaría`). |

---

## 🗂️ Estructura del Repositorio

```text
storytelling-final-project/
├── README.md                              # Guía general del proyecto
├── 00_Plan_y_Decisiones.md                # Plan maestro, acuerdos técnicos y bitácora del equipo
├── Proyecto Final - Indicaciones.md       # Consigna oficial y ejemplos visuales
├── Rubrica_CMT8002.md                     # Rúbrica de evaluación de ambos docentes
├── Posibles Preguntas.md                  # Preguntas de negocio (P1–P6)
├── hallazgos/                             # Auditoría de bugs, brechas y métricas verificadas
│   ├── 00_Resumen_Hallazgos.md
│   ├── 01_Bugs_y_Deuda_Tecnica_App.md
│   ├── 02_Brechas_Preguntas_Maqueta_Rubrica.md
│   └── 03_Resumen_Dataset_y_Metricas_Base.md
├── app/                                   # Aplicación Streamlit
│   ├── app.py
│   ├── requirements.txt
│   └── dataset/                           # 6 CSV del modelo estrella SIDPOL
├── presentacion/                          # Maqueta Excalidraw y futura presentación PPT
│   └── Maqueta.excalidraw
├── imagenes/                              # Imágenes de referencia de las indicaciones
└── data/                                  # Notas auxiliares de validación de datos
```

---

## 📌 Estado Actual y Próximos Pasos

Consulta el tablero detallado en [`hallazgos/00_Resumen_Hallazgos.md`](./hallazgos/00_Resumen_Hallazgos.md):

1. **P0 — Correcciones en `app/app.py`:** Corregir cálculo de `% Casos Resueltos` en el gráfico por modalidad, reemplazar KPIs *hardcodeados* (typo `"Extensión"` y `"±0.0 min en Emergencia"`) y ajustar tooltips.
2. **P1 — Brechas frente a `P1`–`P6`:** Añadir comparativa mensual `2026 vs. 2025` (`P2`), tasa por cada `10,000` habitantes + detalle distrital (`P4`) y comparativa explícita con/sin `Estado_Emergencia` (`P6`).
3. **P2 — DuckDB + Página 2:** Migrar la carga y agregaciones a **DuckDB** e implementar el **Dashboard Aclaratorio** según `presentacion/Maqueta.excalidraw`.

---

## 🤝 Flujo de Trabajo Colaborativo (Git)

Para evitar conflictos en `main`:

```bash
git checkout main
git pull origin main
git checkout -b feat/nombre-de-tu-tarea
# ... realiza tus cambios y commits ...
git push -u origin feat/nombre-de-tu-tarea
```

Luego abre un **Pull Request** hacia `main` en GitHub describiendo brevemente qué resuelve el cambio.
