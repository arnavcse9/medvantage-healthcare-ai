"""
===============================================================================
MEDVANTAGE AI — CLINICAL UI & TELEMETRY STYLING MODULE
Module: ui_components.py
===============================================================================
"""

from typing import Dict, Any
import streamlit as st


def inject_custom_css() -> None:
    """Injects modern clinical SaaS styling, glassmorphic cards, and ESI badges."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .med-hero {
            background: linear-gradient(135deg, #0f172a 0%, #0f3d3e 55%, #065f46 100%);
            border-radius: 18px;
            padding: 1.65rem 2rem;
            color: #f8fafc;
            border: 1px solid rgba(16, 185, 129, 0.3);
            box-shadow: 0 12px 32px -8px rgba(6, 95, 70, 0.35);
            margin-bottom: 1.25rem;
        }
        .med-hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.18);
            border: 1px solid rgba(52, 211, 153, 0.45);
            color: #6ee7b7;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 4px 12px;
            border-radius: 999px;
            margin-bottom: 0.6rem;
        }
        .med-hero h1 {
            font-size: 1.85rem;
            font-weight: 800;
            margin: 0 0 0.35rem 0;
            color: #ffffff;
            letter-spacing: -0.02em;
        }
        .med-hero p {
            font-size: 0.95rem;
            color: #cbd5e1;
            margin: 0;
            line-height: 1.5;
        }
        .vital-card {
            background: rgba(30, 41, 59, 0.55);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 14px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.75rem;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }
        .vital-card:hover {
            border-color: rgba(16, 185, 129, 0.55);
            transform: translateY(-2px);
        }
        .vital-label {
            font-size: 0.73rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #94a3b8;
            font-weight: 600;
            margin-bottom: 0.2rem;
        }
        .vital-value {
            font-size: 1.35rem;
            font-weight: 800;
            color: #10b981;
            font-family: 'JetBrains Mono', monospace;
        }
        .vital-sub {
            font-size: 0.75rem;
            color: #cbd5e1;
        }
        .triage-box {
            border-radius: 14px;
            padding: 1.15rem 1.25rem;
            margin-bottom: 1rem;
            border-left: 6px solid;
        }
        .triage-critical {
            background: rgba(239, 68, 68, 0.12);
            border-left-color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.35);
            border-left-width: 6px;
        }
        .triage-urgent {
            background: rgba(245, 158, 11, 0.12);
            border-left-color: #f59e0b;
            border: 1px solid rgba(245, 158, 11, 0.35);
            border-left-width: 6px;
        }
        .triage-moderate {
            background: rgba(59, 130, 246, 0.12);
            border-left-color: #3b82f6;
            border: 1px solid rgba(59, 130, 246, 0.35);
            border-left-width: 6px;
        }
        .triage-routine {
            background: rgba(16, 185, 129, 0.12);
            border-left-color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.35);
            border-left-width: 6px;
        }
        .clinical-tag {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 600;
            margin-right: 6px;
            margin-bottom: 6px;
            background: rgba(16, 185, 129, 0.14);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .clinical-tag-danger {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.35);
        }
        .soap-section {
            background: rgba(15, 23, 42, 0.45);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.85rem;
        }
        .soap-letter {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 8px;
            background: #10b981;
            color: #06281e;
            font-weight: 800;
            margin-right: 8px;
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero_and_vitals(patient_context: Dict[str, Any]) -> None:
    """Renders the executive header and 4-column live vital signs monitor."""
    st.markdown(
        """
        <div class="med-hero">
            <div class="med-hero-badge">🩺 Enterprise Healthcare AI • HL7 FHIR R4 & ICD-10 Integrated</div>
            <h1>MedVantage AI — Autonomous Clinical Triage & Physician Co-Pilot</h1>
            <p>
                Next-generation multimodal healthcare assistant combining <strong>ESI Risk Stratification</strong>,
                <strong>Automated SOAP Documentation</strong>, <strong>Polypharmacy Drug-Interaction Screening</strong>,
                and <strong>Smart Care Routing</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    v1, v2, v3, v4 = st.columns(4)
    with v1:
        st.markdown(
            f"""
            <div class="vital-card">
                <div class="vital-label">❤️ Heart Rate (ECG)</div>
                <div class="vital-value">{patient_context['hr']} BPM</div>
                <div class="vital-sub">{'Normal Sinus Rhythm' if 60 <= patient_context['hr'] <= 100 else 'Tachycardia / Alert'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with v2:
        st.markdown(
            f"""
            <div class="vital-card">
                <div class="vital-label">🩸 Arterial Blood Pressure</div>
                <div class="vital-value">{patient_context['bp']}</div>
                <div class="vital-sub">Mean Arterial Pressure Tracked</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with v3:
        st.markdown(
            f"""
            <div class="vital-card">
                <div class="vital-label">🫁 Pulse Oximetry (SpO2)</div>
                <div class="vital-value">{patient_context['spo2']}%</div>
                <div class="vital-sub">{'Normoxic Baseline' if patient_context['spo2'] >= 95 else 'Hypoxemia Warning'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with v4:
        st.markdown(
            f"""
            <div class="vital-card">
                <div class="vital-label">🌡️ Core Temperature</div>
                <div class="vital-value">{patient_context['temp']} °F</div>
                <div class="vital-sub">{'Afebrile' if patient_context['temp'] < 100.4 else 'Febrile State Detected'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )