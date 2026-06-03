# 🏥 Panel de Seguridad — HR/HAE Tlajomulco

Dashboard interactivo para el sistema de gestión de **Eventos Adversos, Cuasifallas y Centinelas** del Hospital Regional de Alta Especialidad Tlajomulco de Zúñiga (ISSSTE).

---

## 🚀 Instalación y uso

### 1. Requisitos
- Python 3.9 o superior
- pip

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el dashboard
```bash
streamlit run app.py
```

Se abrirá automáticamente en: **http://localhost:8501**

---

## 📌 Funcionalidades

| Pestaña | Contenido |
|---------|-----------|
| 📊 Resumen | KPIs, distribución por tipo, estado e incidente |
| 📈 Tendencias | Línea semanal, heatmap día×hora, distribución por día |
| 🗺️ Por Área | Barras apiladas, treemap de subáreas, mapa de riesgo |
| 📋 Registros | Tabla buscable, descarga CSV |
| ⚙️ Calidad | Prevenibilidad, tiempo de resolución, semáforo de riesgo |

### Filtros globales (sidebar)
- Rango de fechas
- Área hospitalaria
- Tipo de evento (Adverso / Centinela / Cuasifalla)
- Estado (Enviado / En Revisión / Cerrado)

---

## 🔌 Conectar datos reales

El archivo `app.py` genera datos de ejemplo en la función `generar_datos()`.
Para usar datos reales, reemplázala con:

```python
@st.cache_data
def cargar_datos():
    # Opción 1: desde Excel/CSV exportado del sistema
    df = pd.read_excel("eventos.xlsx")
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    return df

df_full = cargar_datos()
```

Las columnas esperadas son:
`Código, Paciente, Fecha, Tipo, Incidente, Área, Subárea, Estado, Gravedad, Prevenible, Reportador, Días_resol`

---

## 🎨 Personalización
Los colores institucionales están definidos como variables CSS al inicio de `app.py`:
- `--guinda: #6B1A2B`
- `--gold: #B8860B`

---

*v1.0 · 2026 — Panel de Seguridad del Paciente*
