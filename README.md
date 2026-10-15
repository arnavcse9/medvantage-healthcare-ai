# 🩺 MedVantage AI — Enterprise Clinical Triage & Physician Co-Pilot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-10b981.svg)
![HL7 FHIR R4](https://img.shields.io/badge/HL7_FHIR-R4_Compliant-3b82f6.svg)
![ICD-10-CM](https://img.shields.io/badge/Coding-ICD--10--CM-f59e0b.svg)

**MedVantage AI** is a modular Healthcare AI Clinical Decision Support, ESI Triage, and Automated Physician Documentation (SOAP + HL7 FHIR R4) platform built with Python and Streamlit.

## ✨ Key Enterprise Capabilities
- **🚨 Real-Time ESI (Emergency Severity Index) Triage Engine:** Stratifies patient symptoms from ESI Level 1 (Immediate/Emergent) to Level 5 with red-flag detection and confidence scoring.
- **📋 Automated SOAP Note & ICD-10-CM Generator:** Converts unstructured patient conversations and telemetry vitals into structured Subjective, Objective, Assessment, and Plan notes.
- **🔗 HL7 FHIR R4 Interoperability Export:** Generates downloadable FHIR R4 JSON bundles (`Patient`, `Observation`, `ClinicalImpression`) ready for EHR/EMR integration.
- **💊 Polypharmacy Drug-Drug Interaction & Lab Biomarker Analyzer:** Screens high-risk medication pairs and interprets HbA1c, LDL-C, eGFR, and Serum Potassium levels.
- **⚡ Dual-Engine Architecture:** Works out-of-the-box with a Zero-Key Autonomous Clinical Engine for instant live demonstrations, or connects dynamically to Google Gemini 2.5 Flash.

## 🗂️ Modular Repository Architecture
```text
├── app.py                  # Main Streamlit application entrypoint
├── clinical_engine.py      # ESI triage, ICD-10 coding, FHIR R4 & Gemini API engine
├── ui_components.py        # Custom CSS styling & patient telemetry UI components
├── requirements.txt        # Production dependencies for Streamlit Cloud
├── .streamlit/config.toml  # Custom dark-emerald healthcare SaaS theme
└── README.md               # Project documentation
```

## 🚀 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```