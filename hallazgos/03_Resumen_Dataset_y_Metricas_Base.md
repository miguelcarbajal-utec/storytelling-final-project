# 🗄️ Resumen del Dataset y Métricas Base (SIDPOL 2018–2026)

> **Ubicación actual:** [`../app/dataset/`](../app/dataset/)  
> **Propósito:** Servir como referencia única del esquema y cifras reales para validar las consultas SQL en **DuckDB** y evitar valores hardcodeados en la aplicación.

---

## 1. Esquema del Modelo Estrella

| Tabla | Archivo | Filas | Columnas |
| :--- | :--- | ---: | :--- |
| **Hechos** | `Fact_Denuncias.csv` | 378,187 | `ID_Denuncia`, `Fecha_Key`, `UBIGEO_HECHO`, `ID_Modalidad`, `ID_Franja`, `ID_Canal`, `Estado_Emergencia`, `Cantidad_Denuncias`, `Casos_Resueltos`, `Tiempo_Respuesta_Min`, `Perdida_Economica_PEN` |
| **Calendario** | `Dim_Calendario.csv` | 106 | `Fecha_Key`, `Anio`, `Mes`, `Nombre_Mes`, `Mes_Corto`, `Anio_Mes`, `Trimestre`, `Semestre`, `Es_Comparable_Ene_Oct` |
| **Ubicación** | `Dim_Ubicacion.csv` | 1,840 | `UBIGEO_HECHO`, `Departamento`, `Provincia`, `Distrito`, `Poblacion_Estimada`, `Pais` |
| **Modalidad** | `Dim_Modalidad.csv` | 7 | `ID_Modalidad`, `Modalidad`, `Grupo_Delito` |
| **Franja Horaria** | `Dim_Franja_Horaria.csv` | 4 | `ID_Franja`, `Franja_Horaria`, `Turno_Corto`, `Orden_Franja` |
| **Canal** | `Dim_Canal.csv` | 2 | `ID_Canal`, `Canal_Denuncia` |

### Validación de Integridad Referencial
- **Cruces verificados (`LEFT JOIN`):** **0 valores nulos** en `Anio`, `Departamento`, `Modalidad`, `Canal_Denuncia` y `Turno_Corto` tras unir `Fact_Denuncias` con las 5 dimensiones (normalizando `UBIGEO_HECHO` a 6 dígitos con ceros a la izquierda).

---

## 2. Métricas Globales de Referencia (Sin Filtros)

Valores exactos calculados directamente sobre los CSV en `app/dataset/`:

| Indicador | Valor Exacto | Valor Formateado Sugerido |
| :--- | :--- | :--- |
| **Denuncias totales** | `7,614,774` | `7.61 M` |
| **Casos resueltos** | `1,788,568` | `1.79 M` |
| **Tasa global de resolución** | `23.4881%` | `23.5%` |
| **Pérdida económica estimada** | `S/ 4,092,674,311` | `S/ 4,093 M` |
| **Tiempo prom. respuesta (ponderado)** | `40.01 min` | `40.0 min` |
| **Tiempo prom. respuesta (Emergencia = 1)** | `32.29 min` | `32.3 min` |
| **Tiempo prom. respuesta (Sin Emergencia = 0)** | `42.17 min` | `42.2 min` |

> **Nota sobre KPI 4 en `app.py` / `Maqueta.excalidraw`:** El promedio global ponderado es **40.0 min**, mientras que en zonas en Estado de Emergencia es **32.3 min** (y fuera de emergencia **42.2 min**). Conviene revisar la maqueta (`46.7 min` vs `40.0 min`) para alinear las cifras exactas con el dataset actual.

---

## 3. Desglose Verificado por Modalidad

| Modalidad | Denuncias | Casos Resueltos | Tasa Resolución | Pérdida Económica (PEN) |
| :--- | ---: | ---: | ---: | ---: |
| **Otros** | 2,802,011 | 616,825 | 22.01% | S/ 635,709,000 |
| **Violencia contra la mujer e integrantes** | 2,208,353 | 752,475 | 34.07% | S/ 0 |
| **Hurto** | 1,517,822 | 274,894 | 18.11% | S/ 1,174,651,000 |
| **Robo** | 727,061 | 102,972 | 14.16% | S/ 941,685,900 |
| **Estafa** | 230,458 | 25,921 | 11.25% | S/ 685,779,100 |
| **Extorsión** | 118,737 | 11,123 | 9.37% | S/ 542,967,700 |
| **Secuestro** | 10,332 | 4,358 | 42.18% | S/ 111,881,200 |
