from ui.styles import load_styles
import streamlit as st
import pandas as pd
import time
import json

from core.extraction import (
    extract_text,
    extract_clauses,
    extract_entities,
    classify_contract
)
from core.analysis import (
    detect_risks,
    assign_risk_scores,
    detect_ambiguities,
    analyze_sentiment
)
from core.generation import generate_explanation, suggest_alternatives
from core.export import create_pdf
from core.audit import log_audit, load_audit_logs

st.set_page_config(page_title="Contract Analysis Tool", layout="wide")
load_styles()

st.title("Contract Analysis & Risk Assessment Tool")
st.caption("Analyze and assess risk seamlessely with Gen AI powered tool.")

# Sidebar
with st.sidebar:
    st.header("Actions")

    uploaded = st.file_uploader(
        "Upload Contract (PDF, DOCX, TXT)",
        ["pdf", "docx", "txt"]
    )

    if uploaded:
        st.success("File uploaded successfully.")

    st.metric("Total Analyses", len(load_audit_logs()))

    with st.expander("Recent Audit Logs"):
        logs = load_audit_logs()[-5:]
        for log in logs:
            if "time" in log:
                st.write(f"{log['time'][:19]}: {log['action']} - {log['detail']}")
            else:
                st.write(f"N/A: {log.get('action')} - {log.get('detail')}")


# Main analysis flow
if uploaded:
    progress_bar = st.progress(0)

    with st.spinner("Analyzing contract..."):
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)

        text = extract_text(uploaded, uploaded.name.split(".")[-1])

    progress_bar.empty()

    if text.strip():
        log_audit("UPLOAD", uploaded.name)

        clauses = extract_clauses(text)
        entities = extract_entities(text)
        risks = detect_risks(clauses)
        scores, overall = assign_risk_scores(risks)
        ambiguities = detect_ambiguities(clauses)
        ctype = classify_contract(text)
        sentiment = analyze_sentiment(text)

        explanations = []
        analysis = {
            "summary": {
                "type": ctype,
                "risk": overall,
                "sentiment": sentiment,
                "ambiguities": len(ambiguities)
            },
            "entities": entities,
            "risks": risks
        }

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Summary", "Clauses", "Risks", "Compare", "Export"]
        )

        # SUMMARY TAB
        with tab1:
            st.subheader("Contract Summary")

            st.markdown(f"""
<div class="label">Contract Type</div>
<div class="value">{ctype}</div><br>

<div class="label">Parties</div>
<div class="value">{', '.join(entities['Parties']) or 'Not detected'}</div><br>

<div class="label">Dates</div>
<div class="value">{', '.join(entities['Dates']) or 'Not detected'}</div><br>

<div class="label">Amounts</div>
<div class="value">{', '.join(entities['Amounts']) or 'Not detected'}</div><br>

<div class="label">Jurisdiction</div>
<div class="value">{', '.join(entities['Jurisdiction']) or 'Not detected'}</div>
""", unsafe_allow_html=True)

            def risk_class(r):
                return (
                    "risk-high" if r == "High"
                    else "risk-medium" if r == "Medium"
                    else "risk-low"
                )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Risk Level</div>
                    <div class="metric-value {risk_class(overall)}">{overall}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Ambiguities</div>
                    <div class="metric-value">{len(ambiguities)}</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Sentiment</div>
                    <div class="metric-value value">{sentiment}</div>
                </div>
                """, unsafe_allow_html=True)

        # CLAUSES TAB
        with tab2:
            st.subheader("Clause Analysis")

            search = st.text_input("Search Clauses")
            filtered_clauses = (
                [c for c in clauses if search.lower() in c.lower()]
                if search else clauses[:10]
            )

            for i, clause in enumerate(filtered_clauses):
                st.markdown(f"**Clause {i+1}**")
                st.write(clause)

                exp = generate_explanation(clause)
                explanations.append(f"Clause {i+1}: {exp}")

                st.info(exp)

                if clause in ambiguities:
                    st.warning("Potential ambiguity detected.")

                st.success(suggest_alternatives(clause))

        # RISKS TAB
        with tab3:
            st.subheader("Risk Assessment")
            st.metric("Overall Risk", overall)

            risk_data = {k: len(v) for k, v in risks.items()}
            st.bar_chart(
                pd.DataFrame.from_dict(
                    risk_data,
                    orient="index",
                    columns=["Count"]
                )
            )

            for cat, items in risks.items():
                if items:
                    with st.expander(cat):
                        for c in items:
                            cls = (
                                "risk-high" if scores.get(c) == "High"
                                else "risk-medium" if scores.get(c) == "Medium"
                                else "risk-low"
                            )
                            st.markdown(
                                f"<p class='{cls}'>- {c} ({scores.get(c)})</p>",
                                unsafe_allow_html=True
                            )

        # COMPARE TAB
        with tab4:
            st.subheader("Compare Contracts")

            uploaded2 = st.file_uploader(
                "Upload Second Contract",
                ["pdf", "docx", "txt"],
                key="compare_upload"
            )

            if uploaded2:
                text2 = extract_text(uploaded2, uploaded2.name.split(".")[-1])

                if text2.strip():
                    ctype2 = classify_contract(text2)
                    risks2 = detect_risks(extract_clauses(text2))
                    _, overall2 = assign_risk_scores(risks2)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**First Contract**")
                        st.write(f"Type: {ctype}")
                        st.write(f"Risk: {overall}")

                    with col2:
                        st.markdown("**Second Contract**")
                        st.write(f"Type: {ctype2}")
                        st.write(f"Risk: {overall2}")

        # EXPORT TAB
        with tab5:
            st.subheader("Export & Save")

            if st.button("Save Analysis as JSON"):
                st.download_button(
                    "Download JSON",
                    json.dumps(analysis, indent=2),
                    "analysis.json",
                    "application/json"
                )
                log_audit("SAVE", "JSON Exported")

            if st.button("Generate PDF Report"):
                pdf = create_pdf(
                    summary=json.dumps(analysis, indent=2),
                    explanations=explanations,
                    risks=risks,
                    entities=entities,
                    ambiguities=ambiguities,
                    sentiment=sentiment
                )
                st.download_button(
                    "Download PDF",
                    pdf,
                    "contract_analysis.pdf",
                    "application/pdf"
                )
