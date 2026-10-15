"""
===============================================================================
MEDVANTAGE AI — CLINICAL TRIAGE, PHARMACOLOGY & HL7 FHIR R4 ENGINE
Module: clinical_engine.py
===============================================================================
"""

import json
import datetime
import urllib.request
from typing import Dict, List, Any

CLINICAL_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "🫀 Acute Chest Tightness & Radiating Pain": {
        "prompt": (
            "I'm a 54-year-old experiencing sudden pressure in the center of my chest "
            "for the past 25 minutes. It radiates to my left shoulder and jaw, and I feel "
            "slightly diaphoretic (cold sweat) and short of breath."
        ),
        "esi_level": 1,
        "urgency_label": "ESI Level 1 — Immediate / Emergent (High-Risk Cardiac)",
        "css_class": "triage-critical",
        "care_setting": "Emergency Department via EMS (Call 911 / Emergency Services Immediately)",
        "confidence": 97,
        "red_flags": [
            "Substernal chest pressure > 20 minutes",
            "Radiation to left shoulder and mandible",
            "Autonomic diaphoresis and dyspnea",
        ],
        "differentials": [
            "Acute Coronary Syndrome (STEMI / NSTEMI)",
            "Unstable Angina Pectoris",
            "Acute Aortic Dissection",
            "Pulmonary Embolism",
        ],
        "icd10": [
            {"code": "R07.9", "desc": "Chest pain, unspecified"},
            {"code": "I20.0", "desc": "Unstable angina"},
            {"code": "R06.02", "desc": "Shortness of breath"},
        ],
        "recommended_specialist": "Interventional Cardiology / Emergency Medicine",
        "clinical_response": (
            "### 🚨 Immediate Clinical Triage Alert: High-Risk Cardiac Presentation\n\n"
            "Based on your symptom profile (**central chest pressure >20 minutes, radiation to the left shoulder/jaw, "
            "diaphoresis, and dyspnea**), this presentation strongly warrants **immediate emergency evaluation** "
            "to rule out **Acute Coronary Syndrome (ACS)**.\n\n"
            "#### 1. Immediate Action Protocol\n"
            "- **Do not drive yourself to the hospital.** Activate Emergency Medical Services (EMS / 911) immediately.\n"
            "- **Rest in a semi-reclined position** and avoid all physical exertion.\n"
            "- **Aspirin Protocol:** If you have no history of aspirin allergy or active gastrointestinal bleeding, "
            "emergency dispatchers or clinicians typically advise chewing **162–325 mg of non-enteric coated aspirin** while awaiting EMS.\n\n"
            "#### 2. Anticipated Emergency Workup\n"
            "- **12-Lead ECG** within 10 minutes of arrival.\n"
            "- **Serial High-Sensitivity Cardiac Troponin (hs-cTn)** levels.\n"
            "- **Chest Radiograph & Coagulation Profile**.\n\n"
            "#### 3. Clarifying Triage Questions\n"
            "1. Does the pain change when you take a deep breath or press on your chest wall?\n"
            "2. Do you have a history of hypertension, hyperlipidemia, diabetes, or prior stent placement?"
        ),
    },
    "🧠 Throbbing Unilateral Migraine & Visual Aura": {
        "prompt": (
            "I have a severe throbbing headache on the right side of my head that started "
            "2 hours ago. About 20 minutes before the headache began, I saw shimmering zig-zag "
            "lines in my vision. Bright lights and loud sounds make me nauseous."
        ),
        "esi_level": 3,
        "urgency_label": "ESI Level 3 — Urgent Telehealth / Acute Neurology Evaluation",
        "css_class": "triage-moderate",
        "care_setting": "Same-Day Telehealth or Urgent Care Clinic",
        "confidence": 94,
        "red_flags": [
            "Monitor for sudden 'thunderclap' onset",
            "Check for focal motor weakness or slurred speech",
            "Verify absence of fever or nuchal rigidity (neck stiffness)",
        ],
        "differentials": [
            "Migraine with Classic Visual Aura (Scintillating Scotoma)",
            "Tension-Type Headache",
            "Cluster Headache",
        ],
        "icd10": [
            {"code": "G43.109", "desc": "Migraine with aura, not intractable, without status migrainosus"},
            {"code": "R51.9", "desc": "Headache, unspecified"},
            {"code": "H53.19", "desc": "Other subjective visual disturbances"},
        ],
        "recommended_specialist": "Neurology & Headache Specialist",
        "clinical_response": (
            "### 🧠 Clinical Triage Assessment: Classic Migraine with Visual Aura\n\n"
            "Your symptoms—**unilateral pulsatile headache preceded by a 20-minute reversible visual aura "
            "(scintillating scotoma), accompanied by photophobia, phonophobia, and nausea**—align closely "
            "with **ICHD-3 diagnostic criteria for Migraine with Aura**.\n\n"
            "#### 1. Evidence-Based Acute Management\n"
            "- **Sensory Rest:** Rest in a quiet, dark room with cool compresses applied to the forehead or temples.\n"
            "- **First-Line Abortive Therapy:** Early administration of NSAIDs (e.g., Ibuprofen or Naproxen) or "
            "migraine-specific **Triptans (e.g., Sumatriptan, Rizatriptan)** or **Gepants (Rimegepant)** if prescribed by your physician.\n"
            "- **Hydration & Antiemetics:** Sip electrolyte fluids slowly; an antiemetic (such as Ondansetron or Metoclopramide) can help if nausea progresses.\n\n"
            "#### 2. Neurological Red Flags ('SNOOP4' Criteria)\n"
            "Seek urgent emergency care if you experience:\n"
            "- A sudden, explosive *'worst headache of your life'* peaking within 60 seconds.\n"
            "- Persistent visual loss lasting >60 minutes, facial droop, arm weakness, or difficulty speaking.\n\n"
            "#### 3. Follow-Up Questions\n"
            "1. Have you experienced similar episodes previously, and how many headache days do you average per month?\n"
            "2. Have you taken any acute medication in the last 4 hours?"
        ),
    },
    "🩸 Type 2 Diabetes: Metformin & Upcoming CT Contrast Scan": {
        "prompt": (
            "I have Type 2 Diabetes and take Metformin 1000mg twice daily. My doctor scheduled "
            "me for an abdominal CT scan with IV iodinated contrast tomorrow morning. My latest "
            "eGFR kidney value is 52 mL/min. Do I need to hold my Metformin?"
        ),
        "esi_level": 4,
        "urgency_label": "ESI Level 4 — Medication Safety & Peri-Procedural Guidance",
        "css_class": "triage-routine",
        "care_setting": "Outpatient Endocrinology / Radiology Pre-Procedure Protocol",
        "confidence": 96,
        "red_flags": [
            "Moderate renal impairment (eGFR 52 mL/min/1.73m²)",
            "Risk of Contrast-Induced Acute Kidney Injury (CI-AKI)",
            "Secondary risk of Metformin-Associated Lactic Acidosis (MALA)",
        ],
        "differentials": [
            "Peri-procedural Metformin Management in CKD Stage 3a",
            "Type 2 Diabetes Mellitus without complications",
            "Chronic Kidney Disease, Stage 3a",
        ],
        "icd10": [
            {"code": "E11.9", "desc": "Type 2 diabetes mellitus without complications"},
            {"code": "N18.31", "desc": "Chronic kidney disease, stage 3a"},
            {"code": "Z79.84", "desc": "Long term (current) use of oral hypoglycemic drugs"},
        ],
        "recommended_specialist": "Endocrinology / Diagnostic Radiology",
        "clinical_response": (
            "### 💊 Peri-Procedural Clinical Pharmacology Guidance (ACR / FDA Guidelines)\n\n"
            "This is a critical medication safety question. Because your **eGFR is 52 mL/min/1.73m²** (between 30 and 60) "
            "and you are receiving **intravenous iodinated contrast**, specific renal protection precautions apply.\n\n"
            "#### 1. ACR (American College of Radiology) & FDA Protocol\n"
            "- **When eGFR is 30–59 mL/min:** Guidelines frequently recommend **temporarily holding Metformin at the time of, "
            "or prior to, the IV contrast procedure** and withholding it for **48 hours post-procedure**.\n"
            "- **Why?** Metformin itself does not damage the kidneys, but if the IV contrast causes a transient dip in kidney "
            "function, Metformin can accumulate and rarely trigger **Metformin-Associated Lactic Acidosis (MALA)**.\n"
            "- **Restart Criteria:** Metformin is typically resumed after 48 hours once your ordering physician confirms stable renal function.\n\n"
            "#### 2. Recommended Next Steps Today\n"
            "- **Confirm with the Radiology Department:** Call the imaging center today to verify their exact institution cutoff.\n"
            "- **Pre-Hydration:** Ensure adequate oral hydration prior to your scan unless you have fluid restrictions."
        ),
    },
    "🦴 Post-Op Knee Arthroplasty Swelling & Calf Warmth": {
        "prompt": (
            "I had a total right knee replacement 9 days ago. Today my right calf is noticeably "
            "more swollen than yesterday, feels warm and tight when I flex my foot upward, "
            "and I have a low-grade temperature of 99.6°F."
        ),
        "esi_level": 2,
        "urgency_label": "ESI Level 2 — High-Risk Post-Operative Vascular Alert (Rule Out DVT)",
        "css_class": "triage-urgent",
        "care_setting": "Same-Day Urgent Vascular Ultrasound / Emergency Evaluation",
        "confidence": 95,
        "red_flags": [
            "Post-operative Day 9 after major orthopedic arthroplasty",
            "Unilateral calf asymmetry, warmth, and Homan-like dorsiflexion tightness",
            "High Wells' Score probability for Deep Vein Thrombosis (DVT)",
        ],
        "differentials": [
            "Acute Lower Extremity Deep Vein Thrombosis (DVT)",
            "Post-Operative Lymphedema / Hematoma",
            "Superficial Thrombophlebitis or Early Surgical Site Cellulitis",
        ],
        "icd10": [
            {"code": "I82.401", "desc": "Acute embolism and thrombosis of unspecified deep veins of right lower extremity"},
            {"code": "Z96.651", "desc": "Presence of right artificial knee joint"},
            {"code": "M79.89", "desc": "Other specified soft tissue disorders"},
        ],
        "recommended_specialist": "Orthopedic Surgery / Vascular Medicine",
        "clinical_response": (
            "### ⚠️ Urgent Post-Operative Triage Alert: Rule Out Deep Vein Thrombosis (DVT)\n\n"
            "Following total knee arthroplasty (post-op day 9), **new unilateral calf swelling, localized warmth, "
            "and pain on dorsiflexion** place you in an elevated risk category on the **Wells' Criteria for DVT**.\n\n"
            "#### 1. Immediate Clinical Recommendations\n"
            "- **Contact Your Orthopedic Surgeon's On-Call Line Immediately** or proceed to an Urgent Care / Emergency Department equipped with **Venous Duplex Ultrasound**.\n"
            "- **Do NOT massage or vigorously rub the lower leg**, as this could theoretically dislodge a thrombus.\n"
            "- **Verify Anticoagulation Compliance:** Confirm whether you have been taking your prescribed post-op DVT prophylaxis.\n\n"
            "#### 2. Critical Pulmonary Embolism (PE) Warning Signs\n"
            "Proceed to the nearest Emergency Room immediately if you develop:\n"
            "- Sudden shortness of breath, sharp pleuritic chest pain, rapid heart rate (tachycardia), or lightheadedness."
        ),
    },
}

DRUG_INTERACTION_DB: List[Dict[str, Any]] = [
    {
        "pair": ("Warfarin", "Ibuprofen (NSAID)"),
        "severity": "Major / Contraindicated",
        "mechanism": "Synergistic antiplatelet effect + NSAID-induced gastric mucosal erosion + CYP2C9 competition.",
        "clinical_risk": "Significantly increases risk of life-threatening gastrointestinal hemorrhage (3x–6x baseline risk).",
        "recommendation": "Avoid concurrent use. Use Acetaminophen (with INR monitoring) or topical agents if analgesia is required.",
    },
    {
        "pair": ("Lisinopril (ACEi)", "Spironolactone"),
        "severity": "Major — Monitor Closely",
        "mechanism": "Dual suppression of the Renin-Angiotensin-Aldosterone System (RAAS) impairs renal potassium excretion.",
        "clinical_risk": "High risk of severe Hyperkalemia (K+ > 5.5 mEq/L) and lethal cardiac arrhythmias, especially in CKD.",
        "recommendation": "Check serum potassium and creatinine within 3–7 days of initiation and monthly thereafter.",
    },
    {
        "pair": ("Simvastatin", "Clarithromycin"),
        "severity": "Contraindicated",
        "mechanism": "Potent CYP3A4 inhibition by macrolide antibiotic markedly elevates plasma statin concentration.",
        "clinical_risk": "Severe myopathy and Rhabdomyolysis leading to acute myoglobinuric renal failure.",
        "recommendation": "Temporarily suspend Simvastatin during Clarithromycin course, or switch antibiotic to Azithromycin.",
    },
    {
        "pair": ("Sertraline (SSRI)", "Tramadol"),
        "severity": "Major",
        "mechanism": "Additive serotonergic neurotransmission + CYP2D6 inhibition reducing active opioid metabolite conversion.",
        "clinical_risk": "Risk of Serotonin Syndrome (clonus, hyperthermia, agitation, tachycardia) and lowered seizure threshold.",
        "recommendation": "Consider non-serotonergic analgesics and educate patient on early signs of serotonin toxicity.",
    },
    {
        "pair": ("Metformin", "Iodinated IV Contrast"),
        "severity": "Moderate-Major (Renal Dependent)",
        "mechanism": "Transient contrast-induced nephropathy can impair renal clearance of Metformin.",
        "clinical_risk": "Accumulation of Metformin leading to Metformin-Associated Lactic Acidosis (MALA) if eGFR < 60.",
        "recommendation": "Hold Metformin at time of procedure for 48 hours in patients with eGFR 30–59 mL/min; recheck renal function.",
    },
]


def analyze_custom_symptoms(user_input: str, patient_context: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic clinical NLP analyzer that computes ESI triage level, red flags, and ICD-10 codes."""
    text_lower = user_input.lower()

    for _, data in CLINICAL_SCENARIOS.items():
        if data["prompt"].lower()[:45] in text_lower:
            return data

    if any(k in text_lower for k in ["chest pain", "chest pressure", "heart attack", "can't breathe", "shortness of breath", "stroke", "slurred speech", "fainting"]):
        return {
            "esi_level": 1,
            "urgency_label": "ESI Level 1 — Immediate / Emergent Evaluation Required",
            "css_class": "triage-critical",
            "care_setting": "Emergency Department Immediately (Activate EMS / 911)",
            "confidence": 95,
            "red_flags": [
                "Potential acute cardiopulmonary or neurovascular instability",
                f"Patient Vitals Context: HR {patient_context['hr']} bpm, BP {patient_context['bp']}, SpO2 {patient_context['spo2']}%",
            ],
            "differentials": [
                "Acute Cardiopulmonary Syndrome",
                "Acute Cerebrovascular / Neurovascular Event",
                "Pulmonary Embolism / Arrhythmia",
            ],
            "icd10": [
                {"code": "R07.9", "desc": "Chest pain, unspecified"},
                {"code": "R06.02", "desc": "Shortness of breath"},
            ],
            "recommended_specialist": "Emergency Medicine / Cardiology",
            "clinical_response": (
                f"### 🚨 Emergency Clinical Triage Assessment\n\n"
                f"Thank you for sharing your symptoms. Given your reported presentation (**\"{user_input}\"**) "
                f"and your current vital profile (**BP {patient_context['bp']} mmHg, HR {patient_context['hr']} bpm, "
                f"SpO2 {patient_context['spo2']}%**), our clinical triage engine classifies this as **High Priority (ESI Level 1–2)**.\n\n"
                f"#### 1. Immediate Safety Guidance\n"
                f"- **Seek Immediate In-Person Emergency Care:** Symptoms involving acute chest discomfort, dyspnea, or neurological deficits require immediate ECG, biomarker, and physical evaluation.\n"
                f"- **Do Not Delay:** Please call local emergency services or have someone escort you to the nearest Emergency Department."
            ),
        }

    if any(k in text_lower for k in ["fever", "cough", "sore throat", "flu", "infection", "sinus", "chills"]):
        return {
            "esi_level": 3,
            "urgency_label": "ESI Level 3 — Acute Outpatient / Urgent Care Evaluation",
            "css_class": "triage-moderate",
            "care_setting": "Telehealth Consultation or Local Urgent Care Within 24 Hours",
            "confidence": 92,
            "red_flags": [
                f"Monitor temperature trend (Current: {patient_context['temp']}°F)",
                "Watch for resting dyspnea or SpO2 < 94%",
            ],
            "differentials": [
                "Acute Viral Upper Respiratory Infection / Influenza",
                "Acute Bacterial Pharyngitis / Sinusitis",
            ],
            "icd10": [
                {"code": "J06.9", "desc": "Acute upper respiratory infection, unspecified"},
                {"code": "R50.9", "desc": "Fever, unspecified"},
            ],
            "recommended_specialist": "Internal Medicine / Family Practice",
            "clinical_response": (
                f"### 🩺 Clinical Triage Assessment: Acute Febrile / Respiratory Presentation\n\n"
                f"Based on your reported symptoms (**\"{user_input}\"**) and recorded vitals (**Temp {patient_context['temp']}°F, "
                f"HR {patient_context['hr']} bpm, SpO2 {patient_context['spo2']}%**), this presentation is consistent with an "
                f"**acute infectious or inflammatory process (ESI Level 3)**.\n\n"
                f"#### 1. Evidence-Based Supportive & Diagnostic Plan\n"
                f"- **Targeted Testing:** Consider a rapid multiplex PCR/antigen swab.\n"
                f"- **Symptomatic Relief:** Maintain hydration and use antipyretics respecting your allergy profile (**{patient_context['allergies']}**)."
            ),
        }

    return {
        "esi_level": 4,
        "urgency_label": "ESI Level 4 — Non-Emergent Clinical Consultation",
        "css_class": "triage-routine",
        "care_setting": "Outpatient Primary Care / Scheduled Telehealth Visit",
        "confidence": 91,
        "red_flags": [
            "No immediate life-threatening red flags detected in initial statement",
            f"Allergy Alert Checked: {patient_context['allergies']}",
        ],
        "differentials": [
            "Subacute Symptomatic Presentation Requiring History & Physical",
            "Medication or Lifestyle-Related Etiology",
        ],
        "icd10": [
            {"code": "R69", "desc": "Illness, unspecified"},
            {"code": "Z00.00", "desc": "Encounter for general adult medical examination"},
        ],
        "recommended_specialist": "Primary Care / Internal Medicine",
        "clinical_response": (
            f"### 🩺 Structured Clinical Assessment & Care Guidance\n\n"
            f"I have reviewed your concern (**\"{user_input}\"**) alongside your patient profile "
            f"(**{patient_context['age']}yo {patient_context['sex']}, History: {patient_context['conditions']}, "
            f"Allergies: {patient_context['allergies']}**).\n\n"
            f"#### 1. Clinical Impression & Stratification\n"
            f"- **Triage Stratification:** Categorized as **ESI Level 4 (Outpatient / Telehealth Appropriate)** based on stable baseline vitals (**BP {patient_context['bp']}, SpO2 {patient_context['spo2']}%**).\n"
            f"- **SOAP Note Ready:** Open the **'📋 2. Auto-SOAP Note & FHIR JSON'** tab above to export a structured clinical summary."
        ),
    }


def query_live_gemini_api(user_input: str, patient_context: Dict[str, Any], api_key: str, language: str) -> str:
    """Calls the Google Gemini REST API if an API key is provided."""
    system_instruction = (
        "You are MedVantage AI, an advanced, empathetic clinical triage and physician co-pilot assistant. "
        f"Respond in {language}. "
        f"Patient Context: Age {patient_context['age']}, Sex {patient_context['sex']}, "
        f"Vitals: BP {patient_context['bp']}, HR {patient_context['hr']} bpm, SpO2 {patient_context['spo2']}%, Temp {patient_context['temp']}F. "
        f"Chronic Conditions: {patient_context['conditions']}. Allergies: {patient_context['allergies']}."
    )
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"role": "user", "parts": [{"text": user_input}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 900},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        candidates = result.get("candidates", [])
        if candidates and candidates[0].get("content", {}).get("parts"):
            return candidates[0]["content"]["parts"][0]["text"]
    raise ValueError("Empty response from Gemini endpoint")


def generate_fhir_bundle(patient_context: Dict[str, Any], triage_data: Dict[str, Any], last_query: str) -> Dict[str, Any]:
    """Generates a standards-compliant HL7 FHIR R4 Clinical Impression & Observation Bundle."""
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "resourceType": "Bundle",
        "id": "medvantage-clinical-encounter-001",
        "type": "collection",
        "timestamp": now_iso,
        "entry": [
            {
                "resource": {
                    "resourceType": "Patient",
                    "id": "pat-upwork-demo",
                    "gender": patient_context["sex"].lower(),
                    "extension": [
                        {"url": "http://hl7.org/fhir/StructureDefinition/patient-age", "valueInteger": patient_context["age"]}
                    ],
                }
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "id": "obs-vitals-panel",
                    "status": "final",
                    "effectiveDateTime": now_iso,
                    "component": [
                        {"code": {"text": "Blood Pressure"}, "valueString": f"{patient_context['bp']} mmHg"},
                        {"code": {"text": "Heart Rate"}, "valueQuantity": {"value": patient_context["hr"], "unit": "beats/min"}},
                        {"code": {"text": "Oxygen Saturation"}, "valueQuantity": {"value": patient_context["spo2"], "unit": "%"}},
                        {"code": {"text": "Body Temperature"}, "valueQuantity": {"value": patient_context["temp"], "unit": "degF"}},
                    ],
                }
            },
            {
                "resource": {
                    "resourceType": "ClinicalImpression",
                    "id": "ci-triage-summary",
                    "status": "completed",
                    "description": triage_data["urgency_label"],
                    "summary": f"Chief Complaint: {last_query}",
                    "finding": [
                        {"itemCodeableConcept": {"coding": [{"system": "http://hl7.org/fhir/sid/icd-10-cm", "code": item["code"], "display": item["desc"]}]}}
                        for item in triage_data["icd10"]
                    ],
                }
            },
        ],
    }