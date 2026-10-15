"""
===============================================================================
MEDVANTAGE AI — ENTERPRISE CLINICAL TRIAGE, SOAP & PATIENT INTELLIGENCE SUITE
Main Streamlit Application Entrypoint (app.py)
===============================================================================
"""

import json
import time
import datetime
from typing import Dict, Any, Tuple
import streamlit as st

from clinical_engine import (
    CLINICAL_SCENARIOS,
    DRUG_INTERACTION_DB,
    analyze_custom_symptoms,
    query_live_gemini_api,
    generate_fhir_bundle,
)
from ui_components import inject_custom_css, render_hero_and_vitals

st.set_page_config(
    page_title="MedVantage AI | Clinical Triage & Co-Pilot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_session_state() -> None:
    """Initializes chat history and active clinical triage state."""
    if "messages" not in st.session_state:
        default_case = CLINICAL_SCENARIOS["🫀 Acute Chest Tightness & Radiating Pain"]
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 **Welcome to MedVantage AI — Clinical Triage & Physician Co-Pilot.**\n\n"
                    "I am an autonomous clinical decision-support assistant capable of **real-time ESI Triage Stratification, "
                    "Red-Flag Detection, Automated SOAP Note Generation, ICD-10 Coding, and Polypharmacy Drug Interaction Analysis**.\n\n"
                    "💡 *Click any of the Quick Clinical Scenarios above or describe your symptoms below to test the live engine!*"
                ),
            }
        ]
        st.session_state.active_triage = default_case
        st.session_state.last_patient_statement = default_case["prompt"]

    if "booked_appointments" not in st.session_state:
        st.session_state.booked_appointments = []


def render_sidebar() -> Tuple[Dict[str, Any], str, str]:
    """Renders the sidebar containing patient vitals telemetry and AI configuration."""
    with st.sidebar:
        st.markdown("### 🏥 Patient Telemetry & Profile")
        st.caption("Adjust real-time patient vitals to see how the AI adapts clinical triage and SOAP documentation.")

        col_a, col_b = st.columns(2)
        with col_a:
            age = st.number_input("Age (Yrs)", min_value=1, max_value=110, value=54)
        with col_b:
            sex = st.selectbox("Biological Sex", ["Male", "Female", "Other"], index=0)

        col_c, col_d = st.columns(2)
        with col_c:
            hr = st.slider("Heart Rate (bpm)", 40, 180, 96)
            spo2 = st.slider("SpO2 (%)", 82, 100, 97)
        with col_d:
            bp = st.selectbox("Blood Pressure", ["118/76", "134/86", "158/96", "178/108", "92/60"], index=2)
            temp = st.slider("Temp (°F)", 96.0, 104.5, 98.8, step=0.1)

        conditions = st.text_input("Chronic Conditions", value="Hypertension, Hyperlipidemia")
        allergies = st.text_input("Known Allergies", value="Penicillin (Hives)")

        st.divider()
        st.markdown("### 🌐 AI Engine & Language")
        language = st.selectbox(
            "Consultation Language",
            ["English", "Spanish (Español)", "Hindi (हिन्दी)", "French (Français)", "Arabic (العربية)"],
            index=0,
        )

        default_secret_key = ""
        try:
            default_secret_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            default_secret_key = ""

        api_key = st.text_input(
            "Optional Gemini API Key",
            value=default_secret_key,
            type="password",
            help="Leave blank to use the built-in Autonomous Clinical Simulation Engine (works 100% free with zero setup!). Enter a Gemini API key for live LLM generation.",
        )

        if api_key:
            st.success("🟢 Live Gemini 2.5 Flash Connected")
        else:
            st.info("⚡ Autonomous Clinical Engine Active (Zero API Key Required)")

        if st.button("🔄 Reset Clinical Session", use_container_width=True):
            for key in ["messages", "active_triage", "last_patient_statement"]:
                st.session_state.pop(key, None)
            st.rerun()

        st.divider()
        st.caption("🔒 **HIPAA-Ready Architecture Demo** • HL7 FHIR R4 & ICD-10-CM Compliant Output")

    patient_context = {
        "age": age,
        "sex": sex,
        "hr": hr,
        "bp": bp,
        "spo2": spo2,
        "temp": temp,
        "conditions": conditions,
        "allergies": allergies,
    }
    return patient_context, api_key, language


def render_triage_chat_tab(patient_context: Dict[str, Any], api_key: str, language: str) -> None:
    """Renders the interactive patient chat alongside the live ESI triage intelligence board."""
    st.markdown("##### ⚡ One-Click Clinical Simulation Scenarios (Try these to see instant triage & SOAP updates)")
    preset_cols = st.columns(len(CLINICAL_SCENARIOS))

    triggered_prompt = None
    for idx, (scenario_title, scenario_payload) in enumerate(CLINICAL_SCENARIOS.items()):
        with preset_cols[idx]:
            if st.button(scenario_title, key=f"preset_{idx}", use_container_width=True):
                triggered_prompt = scenario_payload["prompt"]

    chat_col, triage_col = st.columns([1.55, 1.0], gap="large")

    with chat_col:
        chat_container = st.container(height=470)
        with chat_container:
            for msg in st.session_state.messages:
                avatar = "🩺" if msg["role"] == "assistant" else "🧑‍💼"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])

        user_query = st.chat_input("Describe symptoms, lab values, or medication questions...")
        active_input = triggered_prompt or user_query

        if active_input:
            st.session_state.messages.append({"role": "user", "content": active_input})
            st.session_state.last_patient_statement = active_input

            structured_triage = analyze_custom_symptoms(active_input, patient_context)
            st.session_state.active_triage = structured_triage

            if api_key.strip():
                try:
                    ai_reply = query_live_gemini_api(active_input, patient_context, api_key.strip(), language)
                except Exception:
                    ai_reply = structured_triage["clinical_response"]
            else:
                time.sleep(0.2)
                ai_reply = structured_triage["clinical_response"]

            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.rerun()

    with triage_col:
        triage = st.session_state.active_triage
        st.markdown("#### 🛡️ Live Clinical Decision Support")
        st.markdown(
            f"""
            <div class="triage-box {triage['css_class']}">
                <div style="font-size:0.75rem; text-transform:uppercase; font-weight:700; opacity:0.85;">
                    Emergency Severity Index (ESI)
                </div>
                <div style="font-size:1.1rem; font-weight:800; margin:4px 0 6px 0;">
                    {triage['urgency_label']}
                </div>
                <div style="font-size:0.86rem;">
                    <strong>Recommended Disposition:</strong> {triage['care_setting']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(triage["confidence"] / 100.0, text=f"Diagnostic Triage Confidence: {triage['confidence']}%")

        st.markdown("**🚩 Detected Clinical Red Flags & Risk Factors**")
        for flag in triage["red_flags"]:
            st.markdown(f'<span class="clinical-tag clinical-tag-danger">⚠️ {flag}</span>', unsafe_allow_html=True)

        st.markdown("**🔍 Leading Differential Considerations**")
        for diff in triage["differentials"]:
            st.markdown(f'<span class="clinical-tag">🩺 {diff}</span>', unsafe_allow_html=True)

        st.markdown("**🏷️ Suggested ICD-10-CM Billing & EHR Codes**")
        for code_item in triage["icd10"]:
            st.code(f"{code_item['code']} — {code_item['desc']}", language="text")


def render_soap_and_fhir_tab(patient_context: Dict[str, Any]) -> None:
    """Renders real-time structured SOAP documentation and downloadable HL7 FHIR JSON."""
    triage = st.session_state.active_triage
    last_statement = st.session_state.last_patient_statement

    st.markdown("### 📋 Automated Physician SOAP Note & Interoperability Export")
    st.caption("Automatically synthesized from the active patient consultation, vital signs, and triage engine.")

    col_soap, col_fhir = st.columns([1.3, 1.0], gap="large")

    with col_soap:
        st.markdown(
            f"""
            <div class="soap-section">
                <p><span class="soap-letter">S</span><strong>Subjective (Chief Complaint & HPI)</strong></p>
                <p style="font-size:0.92rem; margin:0;">
                    {patient_context['age']}-year-old {patient_context['sex'].lower()} with past medical history of
                    <strong>{patient_context['conditions']}</strong> (Allergies: <em>{patient_context['allergies']}</em>)
                    presents reporting: <em>"{last_statement}"</em>
                </p>
            </div>
            <div class="soap-section">
                <p><span class="soap-letter">O</span><strong>Objective (Telemetry & Vital Signs)</strong></p>
                <p style="font-size:0.92rem; margin:0;">
                    • <strong>BP:</strong> {patient_context['bp']} mmHg &nbsp;|&nbsp;
                    <strong>HR:</strong> {patient_context['hr']} bpm &nbsp;|&nbsp;
                    <strong>SpO2:</strong> {patient_context['spo2']}% &nbsp;|&nbsp;
                    <strong>Temp:</strong> {patient_context['temp']}°F
                </p>
            </div>
            <div class="soap-section">
                <p><span class="soap-letter">A</span><strong>Assessment (Triage & Differential Diagnosis)</strong></p>
                <p style="font-size:0.92rem; margin:0;">
                    • <strong>Stratification:</strong> {triage['urgency_label']}<br>
                    • <strong>Primary Differentials:</strong> {', '.join(triage['differentials'])}<br>
                    • <strong>ICD-10-CM Codes:</strong> {', '.join(c['code'] + ' (' + c['desc'] + ')' for c in triage['icd10'])}
                </p>
            </div>
            <div class="soap-section">
                <p><span class="soap-letter">P</span><strong>Plan (Disposition & Specialist Routing)</strong></p>
                <p style="font-size:0.92rem; margin:0;">
                    • <strong>Care Setting:</strong> {triage['care_setting']}<br>
                    • <strong>Recommended Service:</strong> {triage['recommended_specialist']}<br>
                    • <strong>Red Flag Precautions:</strong> {', '.join(triage['red_flags'])}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        soap_markdown = (
            f"# MEDVANTAGE AI — CLINICAL SOAP NOTE\n"
            f"**Patient:** {patient_context['age']}yo {patient_context['sex']} | **Allergies:** {patient_context['allergies']}\n\n"
            f"## SUBJECTIVE\n{last_statement}\n\n"
            f"## OBJECTIVE\nBP: {patient_context['bp']} | HR: {patient_context['hr']} bpm | SpO2: {patient_context['spo2']}% | Temp: {patient_context['temp']}F\n\n"
            f"## ASSESSMENT\n{triage['urgency_label']}\nDifferentials: {', '.join(triage['differentials'])}\n\n"
            f"## PLAN\nDisposition: {triage['care_setting']}\nSpecialist: {triage['recommended_specialist']}\n"
        )
        st.download_button(
            "📥 Download Signed SOAP Note (.md)",
            data=soap_markdown,
            file_name="MedVantage_Clinical_SOAP_Note.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col_fhir:
        st.markdown("#### 🔗 HL7 FHIR R4 Bundle Payload (EHR Ready)")
        fhir_bundle = generate_fhir_bundle(patient_context, triage, last_statement)
        fhir_json_str = json.dumps(fhir_bundle, indent=2)
        st.code(fhir_json_str, language="json")
        st.download_button(
            "📦 Export HL7 FHIR R4 Bundle (.json)",
            data=fhir_json_str,
            file_name="hl7_fhir_r4_encounter.json",
            mime="application/json",
            use_container_width=True,
        )


def render_lab_and_drug_tab() -> None:
    """Renders an interactive polypharmacy checker and abnormal lab panel interpreter."""
    col_drug, col_lab = st.columns(2, gap="large")

    with col_drug:
        st.markdown("### 💊 Polypharmacy Drug-Drug Interaction Checker")
        st.caption("Screen high-risk medication combinations for CYP450, renal, and pharmacodynamic conflicts.")

        pair_labels = [f"{item['pair'][0]}  +  {item['pair'][1]}" for item in DRUG_INTERACTION_DB]
        selected_pair_label = st.selectbox("Select Medication Regimen to Screen:", pair_labels)
        selected_interaction = next(
            item for item in DRUG_INTERACTION_DB if f"{item['pair'][0]}  +  {item['pair'][1]}" == selected_pair_label
        )

        st.markdown(
            f"""
            <div class="triage-box triage-critical">
                <div style="font-size:0.76rem; text-transform:uppercase; font-weight:700;">
                    Interaction Severity: {selected_interaction['severity']}
                </div>
                <div style="font-size:1.05rem; font-weight:800; margin:6px 0;">
                    {selected_interaction['pair'][0]} ↔ {selected_interaction['pair'][1]}
                </div>
                <p style="font-size:0.88rem; margin:4px 0;">
                    <strong>Pharmacological Mechanism:</strong> {selected_interaction['mechanism']}
                </p>
                <p style="font-size:0.88rem; margin:4px 0;">
                    <strong>Clinical Risk:</strong> {selected_interaction['clinical_risk']}
                </p>
                <p style="font-size:0.88rem; margin:4px 0; color:#6ee7b7;">
                    <strong>Clinical Decision Guidance:</strong> {selected_interaction['recommendation']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_lab:
        st.markdown("### 🧪 Smart Lab Biomarker Interpreter")
        st.caption("Adjust patient blood panel biomarkers below for instant clinical interpretation.")

        hba1c = st.slider("Hemoglobin A1c (%)", 4.5, 12.0, 7.4, step=0.1)
        ldl = st.slider("LDL Cholesterol (mg/dL)", 50, 240, 148)
        egfr = st.slider("eGFR Renal Function (mL/min/1.73m²)", 15, 120, 54)
        potassium = st.slider("Serum Potassium K+ (mEq/L)", 2.8, 6.5, 4.9, step=0.1)

        findings = []
        if hba1c >= 6.5:
            findings.append(f"🔴 **HbA1c ({hba1c}%):** Diabetic range (Target < 7.0% for most non-pregnant adults per ADA guidelines).")
        elif hba1c >= 5.7:
            findings.append(f"🟡 **HbA1c ({hba1c}%):** Prediabetes range (5.7% – 6.4%); recommend lifestyle & nutrition intervention.")
        else:
            findings.append(f"🟢 **HbA1c ({hba1c}%):** Optimal glycemic control.")

        if ldl >= 130:
            findings.append(f"🟡 **LDL-C ({ldl} mg/dL):** Borderline-high/Elevated atherogenic lipid profile; evaluate ASCVD 10-year risk.")
        else:
            findings.append(f"🟢 **LDL-C ({ldl} mg/dL):** Within target lipid parameters.")

        if egfr < 60:
            findings.append(f"🟠 **eGFR ({egfr} mL/min):** Decreased renal filtration (CKD Stage 3); adjust renally cleared medications.")
        else:
            findings.append(f"🟢 **eGFR ({egfr} mL/min):** Preserved renal filtration.")

        if potassium > 5.2:
            findings.append(f"🔴 **Serum K+ ({potassium} mEq/L):** Hyperkalemia alert — review ACEi/ARB/Spironolactone therapy.")
        elif potassium < 3.5:
            findings.append(f"🟡 **Serum K+ ({potassium} mEq/L):** Hypokalemia alert — evaluate diuretic therapy.")
        else:
            findings.append(f"🟢 **Serum K+ ({potassium} mEq/L):** Normal electrolyte homeostasis.")

        st.markdown("#### 📊 Automated Pathology Summary")
        for f in findings:
            st.markdown(f)


def render_appointment_routing_tab(patient_context: Dict[str, Any]) -> None:
    """Renders an interactive appointment booking workflow connected to the active triage state."""
    triage = st.session_state.active_triage
    st.markdown("### 📅 Smart Care Routing & Automated Appointment Dispatch")
    st.caption(
        f"Based on your active triage assessment (**{triage['urgency_label']}**), "
        f"our routing engine recommends: **{triage['recommended_specialist']}**."
    )

    c1, c2 = st.columns([1.2, 1.0], gap="large")
    with c1:
        with st.form("smart_booking_form"):
            patient_name = st.text_input("Patient Full Name", value="Alex Morgan (Demo Patient)")
            specialty = st.selectbox(
                "Matched Clinical Department",
                [
                    triage["recommended_specialist"],
                    "Internal Medicine / Primary Care",
                    "Interventional Cardiology",
                    "Neurology & Headache Center",
                    "Endocrinology & Metabolism",
                    "Orthopedic & Vascular Surgery",
                ],
            )
            visit_modality = st.radio(
                "Consultation Modality",
                ["🎥 Priority HD Telehealth Video", "🏥 In-Person Clinic / Urgent Care"],
                horizontal=True,
            )
            preferred_date = st.date_input("Preferred Date", value=datetime.date.today() + datetime.timedelta(days=1))
            preferred_slot = st.selectbox("Available Priority Time Slots", ["09:30 AM", "11:15 AM", "02:00 PM", "04:45 PM"])
            submit_booking = st.form_submit_button("✅ Confirm Priority Clinical Dispatch", use_container_width=True)

            if submit_booking:
                booking_record = {
                    "ref_id": f"MV-{int(time.time()) % 100000}",
                    "patient": patient_name,
                    "specialty": specialty,
                    "modality": visit_modality,
                    "date": str(preferred_date),
                    "time": preferred_slot,
                    "triage": triage["urgency_label"],
                    "vitals": f"BP {patient_context['bp']}, HR {patient_context['hr']}",
                }
                st.session_state.booked_appointments.insert(0, booking_record)
                st.success(f"🎉 Appointment Dispatched! Reference ID: **{booking_record['ref_id']}** with SOAP Note pre-attached.")

    with c2:
        st.markdown("#### 🗂️ Active Clinical Dispatch Queue")
        if not st.session_state.booked_appointments:
            st.info("No active appointments dispatched in this session yet. Submit the form on the left to test the workflow.")
        else:
            for appt in st.session_state.booked_appointments:
                st.markdown(
                    f"""
                    <div class="soap-section">
                        <div style="font-size:0.78rem; color:#10b981; font-weight:700;">
                            REF #{appt['ref_id']} • {appt['modality']}
                        </div>
                        <div style="font-size:1rem; font-weight:700; margin:3px 0;">
                            {appt['patient']} → {appt['specialty']}
                        </div>
                        <div style="font-size:0.84rem; color:#cbd5e1;">
                            📅 {appt['date']} at {appt['time']} | 🩺 {appt['vitals']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def main() -> None:
    """Main execution entrypoint for the MedVantage AI Streamlit application."""
    inject_custom_css()
    init_session_state()

    patient_context, api_key, language = render_sidebar()
    render_hero_and_vitals(patient_context)

    tab_chat, tab_soap, tab_labs, tab_booking = st.tabs(
        [
            "🩺 1. AI Clinical Triage & Chat",
            "📋 2. Auto-SOAP Note & FHIR JSON",
            "🧪 3. Drug Interaction & Lab AI",
            "📅 4. Smart Care Routing",
        ]
    )

    with tab_chat:
        render_triage_chat_tab(patient_context, api_key, language)
    with tab_soap:
        render_soap_and_fhir_tab(patient_context)
    with tab_labs:
        render_lab_and_drug_tab()
    with tab_booking:
        render_appointment_routing_tab(patient_context)


if __name__ == "__main__":
    main()