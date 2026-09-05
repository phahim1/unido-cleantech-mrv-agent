# UNIDO Cleantech MRV Agent (`unido-cleantech-mrv-agent`)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Standards: IEEE P7802 | ISO 50001](https://img.shields.io/badge/Standards-IEEE%20P7802%20%7C%20ISO%2050001-green.svg)]()
[![SDG Alignment: 7 | 9 | 13](https://img.shields.io/badge/UN%20SDGs-7%20%7C%209%20%7C%2013-blue.svg)]()

> **An Open-Source Multi-Agent Digital MRV & Adaptive Climate Impact Engine for Industrial MSMEs in Developing Nations**

---

## Executive Overview

`unido-cleantech-mrv-agent` is an open-source, industrial-grade decision-support and Measurement, Reporting, and Verification (MRV) platform designed to support UNIDO's **Global Cleantech Innovation Programme (GCIP)**, **Climate Technology Centre and Network (CTCN)**, and **Adaptation SME Innovation Facility (ASIF)**.

The framework ingests industrial energy and thermal telemetry, executes multi-agent analytics across power systems efficiency and climate adaptation risk, and computes greenhouse gas (GHG) reductions (`tCO₂e`) and GEF/GCF Core Indicator outputs.

```text
[ Industrial IoT ]
        │
        ▼
[ ISO/IEC 17025 Data Validation Pipeline ]
        │
        ▼
[ Multi-Agent MRV Engine ]
        │
        ├───────────────┬───────────────────┐
        ▼               ▼                   ▼
[ Power Systems ] [ Climate MRV ] [ Adaptation Risk ]
[    Agent      ] [    Agent    ] [     Agent      ]
        │               │                   │
        │               │                   │
 ISO 50001 /        IEEE P7802 /       Thermal /
 Kigali / VFD       IPCC Tier-2        Derating
 Analytics          Accounting         Analysis
        │               │                   │
        └───────────────┴───────────────────┘
                        │
                        ▼
             [ UNIDO / GEF / GCF Reports ]
```

---

## Key Features & UNIDO SDG Alignment

* **Automated Digital MRV (IEEE P7802-aligned):** Replaces static manual reporting with continuous data ingestion and calculation of avoided emissions for industrial equipment such as high-efficiency cooling systems, heat pumps, and VFD retrofits.
* **Power Quality & ISO 50001 Analytics:** Evaluates voltage unbalance, power factor, total harmonic distortion (THD), and mechanical-to-electrical efficiency losses.
* **Low-GWP & Kigali Amendment Support:** Provides logic for calculating baseline-to-project refrigerant transition emissions, including direct refrigerant leakage and indirect energy-related emissions.
* **Climate Vulnerability & Adaptation Scoring:** Simulates asset derating under elevated ambient temperatures to support thermal resilience planning for MSMEs.
* **Tamper-Evident Verification:** Hashes audit outputs using cryptographic logs and supports distributed-ledger verification workflows.

| UN Sustainable Development Goal                  | Application in Repository                                                                          |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| **SDG 7: Affordable & Clean Energy**             | Optimizes energy efficiency (`kWh/unit`) in industrial drives and HVAC systems.                    |
| **SDG 9: Industry, Innovation & Infrastructure** | Enables developing-country MSMEs to integrate digital IoT and AI-driven predictive maintenance.    |
| **SDG 13: Climate Action**                       | Provides verifiable `tCO₂e` reduction tracking for climate-finance and impact-reporting workflows. |

---

## Mathematical & Engineering Formulation

### 1. Avoided Emissions Calculation (`tCO₂e`)

The net greenhouse gas mitigation (`ΔE_total`) achieved by an industrial cleantech intervention is calculated using baseline/project accounting logic:

$$
\Delta E_{\text{total}}
=
\left[
\left(
E_{\text{base, elec}}
-
E_{\text{proj, elec}}
\right)
\times
EF_{\text{grid}}(t)
\right]
+
\left[
\sum_k
\left(
L_{\text{base},k}
-
L_{\text{proj},k}
\right)
\times
GWP_k
\right]
\times 10^{-3}
$$

Where:

* `E_base,elec` and `E_proj,elec` are baseline and project electrical energy consumption (`kWh`).
* `EF_grid(t)` is the applicable grid emission factor (`kg CO₂e/kWh`).
* `L_base,k` and `L_proj,k` are baseline and project refrigerant leakage quantities (`kg`) for refrigerant `k`.
* `GWP_k` is the applicable 100-year Global Warming Potential of refrigerant `k`.

### 2. Temperature Derating & Adaptation Risk Factor

Thermal stress impact on industrial electrical machinery efficiency (`η_actual`) and asset availability (`A_risk`) is represented by:

$$
\eta_{\text{actual}}
=
\eta_{\text{rated}}
\times
\left[
1
-
\alpha
\cdot
\max
\left(
0,
T_{\text{ambient}}
-
T_{\text{rated}}
\right)
\right]
$$

$$
A_{\text{risk}}
=
1
-
\frac{\text{MTTR}}
{\text{MTBF}
\times
e^{-\beta
(T_{\text{ambient}}
-
T_{\text{threshold}})}}
$$

Where:

* `α` is the thermal derating coefficient (`% / °C`).
* `T_ambient` and `T_rated` are ambient operating and rated temperatures (`°C`).
* `MTTR` represents Mean Time To Repair.
* `MTBF` represents Mean Time Between Failures.
* `β` represents the temperature sensitivity coefficient.

---

## Quickstart Guide

### Prerequisites

* Python 3.11+
* Docker & Docker Compose
* Git

### Local Installation

```bash
# Clone the repository
git clone https://github.com/fahimullah-khanzada/unido-cleantech-mrv-agent.git

# Enter the repository
cd unido-cleantech-mrv-agent

# Create and activate virtual environment
python3 -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running with Docker

```bash
docker-compose up --build
```

Access the Streamlit Dashboard at:

```text
http://localhost:8501
```

Access the FastAPI documentation at:

```text
http://localhost:8000/docs
```

---

## Quick Example Usage (Python API)

```python
from src.agents.power_engineering import PowerEngineeringAgent
from src.agents.climate_mrv import ClimateMRVAgent

# Initialize agents
power_agent = PowerEngineeringAgent()
mrv_agent = ClimateMRVAgent(grid_ef_kg_kwh=0.52)

# Example telemetry for a 75 kW industrial pump VFD retrofit
telemetry_data = {
    "voltage_v": 400,
    "current_a": 120,
    "power_factor": 0.82,
    "operating_hours": 4200,
    "vfd_installed": True
}

# Analyze power-system efficiency
power_metrics = power_agent.analyze_efficiency(telemetry_data)

# Calculate avoided emissions
mrv_results = mrv_agent.compute_avoided_emissions(
    baseline_kwh=315000,
    project_kwh=220500,
    refrigerant_leakage_saved_kg=12.5,
    gwp=1430  # Example: R-134a
)

print(
    f"Annual Avoided Emissions: "
    f"{mrv_results['total_avoided_tco2e']:.2f} tCO2e"
)

print(
    f"GEF Core Indicator 6.2 Contribution: "
    f"{mrv_results['gef_indicator_6_2_tco2e']:.2f} tCO2e"
)
```

---

## Repository Structure

```text
unido-cleantech-mrv-agent/
├── data/
│   ├── reference/          # Grid emission factors and reference data
│   └── samples/            # Sample industrial telemetry datasets
│
├── docs/
│   ├── architecture/       # System architecture diagrams
│   └── mappings/           # UNIDO / GEF / GCF KPI mappings
│
├── src/
│   ├── agents/
│   │   ├── power_engineering.py
│   │   ├── climate_mrv.py
│   │   └── adaptation_risk.py
│   │
│   ├── ingestion/          # FastAPI endpoints and data validation
│   ├── mrv_core/           # MRV formulas, calculations and hashing
│   └── reporting/          # Streamlit UI and report generation
│
└── tests/                  # PyTest engineering and MRV validation suite
```

---

## Verification & Testing

Execute the complete unit-test suite with coverage:

```bash
pytest tests/ -v --cov=src
```

The test suite is intended to validate:

* Engineering calculations
* Power-quality metrics
* Energy-efficiency calculations
* GHG/MRV calculations
* Refrigerant emission calculations
* Climate adaptation and thermal-risk calculations
* Cryptographic verification outputs

---

## Verification Philosophy

The platform is designed around four principles:

1. **Measurement** — ingest structured industrial telemetry and reference data.
2. **Calculation** — apply transparent engineering and emissions-accounting methodologies.
3. **Verification** — preserve calculation provenance through validation and tamper-evident records.
4. **Reporting** — translate technical outputs into decision-ready climate and energy indicators.

This architecture is intended to provide a traceable digital pathway from industrial measurement data to climate-impact reporting.

---

## Future Roadmap & Technical Scaling

### 1. WebMCP & Distributed Multi-Agent Protocols
* **Autonomous Agent Collaboration:** Upgrade agent communications to the WebMCP (Model Context Protocol) standard, allowing the **Power Systems**, **Climate MRV**, and **Adaptation Risk** agents to run as autonomous, decentralized microservices.
* **LLM-Driven Diagnostic Reasoning:** Integrate open-source Small Language Models (SLMs) locally to generate natural-language technical audit summaries and operational recommendations for plant engineers based on real-time telemetry anomalies.

### 2. DLT & Tamper-Evident Audit Trails (Hedera Network Integration)
* **Cryptographic Verification:** Anchor high-frequency telemetry hashes and calculated $tCO_2e$ reduction records directly to open-source Distributed Ledger Technology (Hedera Consensus Service).
* **Automated Smart Contracts:** Enable programmable performance-based grant disbursements from climate funds (GEF/GCF) triggered automatically upon reaching verified $tCO_2e$ reduction thresholds.

### 3. Edge-AI & Industrial Protocol Ingestion
* **Direct Modbus / MQTT Industrial Gateway:** Package the ingestion engine into lightweight Docker/WebAssembly microservices capable of running on edge hardware (e.g., Raspberry Pi / industrial PLCs) inside factory environments with offline data caching.
* **Predictive Maintenance for Motor Systems:** Incorporate Fourier Transform (FFT) vibration analysis and harmonic distortion degradation modeling to forecast mechanical motor failures prior to grid-stress events.

### 4. Advanced Regulatory & Standards Expansion
* **ISO/IEC 17025 Automated Compliance Checks:** Build automated measurement uncertainty models ($\pm U$) directly into telemetry ingestion to meet strict laboratory calibration standards for multilateral funding claims.
* **CBAM & Scope 3 Industrial Supply Chain Tracking:** Expand emission factor accounting to support the European Union’s Carbon Border Adjustment Mechanism (CBAM), enabling developing-country MSME exporters to verify embodied carbon content.

---

## Disclaimer

This repository is an **open-source research and decision-support prototype**. References to UNIDO programmes, GEF/GCF indicators, ISO standards, IEEE standards, the Kigali Amendment, IPCC methodologies, or other international frameworks do not imply endorsement, certification, accreditation, or official affiliation unless explicitly stated.

Actual MRV, GHG accounting, climate-finance reporting, certification, or regulatory submissions should be performed or validated by appropriately authorized professionals and according to the applicable methodology and jurisdiction.

---

## License

Distributed under the MIT License. See `LICENSE` for details.
