
import os
import streamlit as st
import pandas as pd
import base64
import re
import time
from typing import List, Dict
from utils.document_parser import parse_document, split_into_clauses
from utils.ner_model import extract_entities
from utils.classifier import classify_clauses
from utils.summarizer import generate_summary

def clean_display_text(text: str) -> str:
    text = re.sub(r'(\[REDACTED\]\s*){2,}', '[REDACTED]', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:5000] + "..." if len(text) > 5000 else text

def analyze_contract():
    if 'uploaded_file' not in st.session_state:
        st.info("📁 Please upload a contract document to begin analysis")
        return

    if not validate_uploaded_file():
        return

    if 'current_file' in st.session_state:
        st.subheader(f"Analyzing: `{st.session_state.current_file}`")

    if not st.session_state.get('analysis_done', False):
        with st.spinner("🔍 Analyzing contract content..."):
            try:
                perform_contract_analysis()
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                if "PDF" in str(e):
                    st.warning("Ensure the PDF is not scanned or password-protected")
                return

    if 'clauses' in st.session_state:
        display_analysis_results()

def validate_uploaded_file() -> bool:
    if not hasattr(st.session_state, 'uploaded_file'):
        return False

    valid_extensions = ('.pdf', '.docx', '.txt')
    file_path = st.session_state.uploaded_file

    if not isinstance(file_path, str) or not file_path.lower().endswith(valid_extensions):
        st.error("⚠️ Unsupported file format. Please upload PDF, DOCX, or TXT")
        return False

    if not os.path.exists(file_path):
        st.error("⚠️ File not found. Please upload again")
        return False

    return True

def perform_contract_analysis():
    start_time = time.time()

    text = parse_document(st.session_state.uploaded_file)
    raw_clauses = split_into_clauses(text)

    processed_clauses = []
    for clause in raw_clauses:
        if not clause.strip():
            continue

        display_text = clean_display_text(clause)
        processed_clause = {
            'text': display_text,
            'entities': [],
            'type': 'General'
        }

        if st.session_state.get('extract_entities', True):
            try:
                entities = extract_entities(display_text)
                processed_clause['entities'] = [
                    {'text': ent[0], 'label': ent[1]} 
                    for ent in entities
                ]
            except Exception as e:
                st.warning(f"Entity extraction failed for a clause: {str(e)}")

        if st.session_state.get('classify_clauses', True):
            try:
                classification = classify_clauses(display_text)
                processed_clause['type'] = classification.get('type', 'General')
            except Exception as e:
                st.warning(f"Classification failed for a clause: {str(e)}")
                processed_clause['type'] = 'General'

        processed_clauses.append(processed_clause)

    if st.session_state.get('summarize', True):
        full_text = " ".join(c['text'] for c in processed_clauses)
        try:
            st.session_state['summary'] = generate_summary(full_text)
        except Exception as e:
            st.warning(f"Summary generation failed: {str(e)}")
            st.session_state['summary'] = "Summary unavailable"

    st.session_state.update({
        'clauses': processed_clauses,
        'analysis_done': True
    })

    st.success(f"Analysis completed in {time.time()-start_time:.1f} seconds")

def apply_filters(clauses: List[Dict]) -> List[Dict]:
    if 'type_filter' not in st.session_state:
        st.session_state.type_filter = "All"

    current_filter = st.session_state.type_filter
    if current_filter == "All":
        return clauses

    return [c for c in clauses if c.get('type') == current_filter]

def display_analysis_results():
    if 'summary' in st.session_state:
        with st.expander("📝 Document Summary", expanded=True):
            st.markdown(f"""
            <div style='padding: 1rem; background: #f8f9fa; border-radius: 8px; line-height: 1.6;'>
                {st.session_state['summary']}
            </div>
            """, unsafe_allow_html=True)
            if st.button("💾 Download Summary"):
                st.markdown(create_download_link(
                    st.session_state['summary'],
                    "summary.txt",
                    "text/plain"
                ), unsafe_allow_html=True)

    filtered_clauses = apply_filters(st.session_state['clauses'])

    tab1, tab2 = st.tabs(["📜 Clause View", "📊 Analysis"])
    with tab1:
        display_clause_view(filtered_clauses)
    with tab2:
        display_analysis_view(filtered_clauses)

def display_clause_view(clauses: List[Dict]):
    for clause in clauses:
        if not is_complete_clause(clause['text']):
            continue

        border_color = {
            'Risky': '#ff4444',
            'Important': '#ffbb33',
            'Standard': '#00C851',
            'Unknown': '#aaaaaa'
        }.get(clause.get('type', 'Unknown'), '#aaaaaa')

        with st.container():
            st.markdown(f"""
                <div style='border-left: 4px solid {border_color}; padding: 1rem; margin: 1rem 0; background: #f8f9fa; border-radius: 0 8px 8px 0; line-height: 1.6;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                        <strong>{clause.get('type', 'Clause')}</strong>
                        <span style='background: {border_color}; color: white; padding: 0.2rem 0.8rem; border-radius: 12px; font-size: 0.8rem;'>
                            {clause.get('type', 'Unknown')}
                        </span>
                    </div>
                    <div style='margin: 0.5rem 0;'>{clause['text']}</div>
            """, unsafe_allow_html=True)

            if clause.get('entities'):
                render_entities(clause['entities'])

            st.markdown("</div>", unsafe_allow_html=True)

def render_entities(entities: List[Dict]):
    with st.expander("🔍 Identified Entities", expanded=False):
        cols = st.columns(4)
        for i, entity in enumerate(entities):
            color = {
                'PARTY': '#4285F4',
                'DATE': '#EA4335',
                'AMOUNT': '#FBBC05',
                'TERM': '#34A853',
                'LAW': '#9C27B0',
                'GOVERNING_LAW': '#9C27B0'
            }.get(entity['label'], '#9E9E9E')

            with cols[i % 4]:
                st.markdown(
                    f"<span style='background: {color}; color: white; padding: 2px 8px; border-radius: 8px; font-size: 0.8em;'>{entity['text']} ({entity['label']})</span>",
                    unsafe_allow_html=True
                )

def is_complete_clause(text: str) -> bool:
    text = text.strip()
    return len(text) > 30 and len(text.split()) > 5 and not re.match(r'^[-\d\s]+$', text)

def display_analysis_view(clauses: List[Dict]):
    st.subheader("Clause Distribution")
    type_counts = {
        'Standard': len([c for c in clauses if c.get('type') == 'Standard']),
        'Important': len([c for c in clauses if c.get('type') == 'Important']),
        'Risky': len([c for c in clauses if c.get('type') == 'Risky'])
    }
    cols = st.columns(3)
    cols[0].metric("Standard", type_counts['Standard'])
    cols[1].metric("Important", type_counts['Important'])
    cols[2].metric("Risky", type_counts['Risky'])

    st.subheader("All Clauses")
    df = pd.DataFrame([{
        'Clause': c['text'][:200] + ('...' if len(c['text']) > 200 else ''),
        'Type': c.get('type', 'Unknown'),
        'Entities': ', '.join([e['text'] for e in c.get('entities', [])])
    } for c in clauses])
    st.dataframe(df)

    if st.button("💾 Export to CSV"):
        st.markdown(create_download_link(
            df.to_csv(index=False),
            "contract_analysis.csv",
            "text/csv"
        ), unsafe_allow_html=True)

def create_download_link(data: str, filename: str, mime: str) -> str:
    b64 = base64.b64encode(data.encode()).decode()
    return f'<a href="data:{mime};base64,{b64}" download="{filename}">Download {filename}</a>'
