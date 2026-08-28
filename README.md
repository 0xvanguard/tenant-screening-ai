# 🏠 Tenant Screening AI

**Analiza y evalúa inquilinos potenciales automáticamente**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)

---

## 📋 Descripción

Tenant Screening AI es una herramienta que analiza perfiles de inquilinos y genera recomendaciones automáticas basadas en ingresos, estabilidad laboral, historial crediticio y otros factores.

### ✨ Características

- 📊 **Análisis automático** - Evalúa inquilinos en segundos
- 💰 **Ratio ingreso/renta** - Calcula capacidad de pago
- 🏢 **Estabilidad laboral** - Analiza tipo y duración del empleo
- ⚠️ **Red flags** - Detecta señales de alerta
- ✅ **Factores positivos** - Resalta fortalezas del inquilino
- 📋 **Condiciones** - Genera condiciones de aprobación
- 🔌 **API REST** - Fácil integración
- 🌐 **Web UI** - Interfaz interactiva

---

## 🚀 Instalación

```bash
git clone https://github.com/0xvanguard/tenant-screening-ai.git
cd tenant-screening-ai
pip install -r requirements.txt
python src/api.py
```

---

## 📖 Uso

### API

```bash
curl -X POST http://localhost:9002/api/screen \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@email.com",
    "phone": "+52 55 1234 5678",
    "monthly_income": 5000,
    "monthly_rent": 1500,
    "employment_status": "employed",
    "employer": "Google México",
    "employment_duration_months": 24,
    "credit_score": 750
  }'
```

### Web UI

Abre http://localhost:9002 en tu navegador.

---

## 📊 Ejemplos

| Inquilino | Riesgo | Recomendación |
|-----------|--------|---------------|
| Ingreso alto, empleo estable | ✅ LOW | APROBADO |
| Ingreso medio, empleo temporal | ⚠️ MEDIUM | CON CONDICIONES |
| Ingreso bajo, mal historial | ❌ HIGH | REVISIÓN |

---

**Desarrollado por [0xvanguard](https://github.com/0xvanguard)**
