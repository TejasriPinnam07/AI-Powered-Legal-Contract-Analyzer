import streamlit as st 
import os
from datetime import datetime

def reset_analysis_state():
    """Reset all analysis-related session state variables"""
    st.session_state['analysis_done'] = False
    st.session_state.pop('clauses', None)
    st.session_state.pop('clause_types', None)
    st.session_state.pop('summary', None)
    st.session_state.pop('importance_filter', None)

def show_sidebar():
    with st.sidebar:
        st.image("assets/logo.png", width=80)
        st.markdown(f"**Welcome, {st.session_state.get('username', 'Guest')}**")

        st.markdown("---")

        # File uploader (keep existing code)
        uploaded_file = st.file_uploader(
            "Upload Contract Document",
            type=["pdf", "docx", "txt"],
            help="Upload your legal contract in PDF, Word, or text format",
            key="file_uploader"
        )

        if uploaded_file:
            reset_analysis_state()
            file_path = os.path.join("uploads", uploaded_file.name)
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.session_state['uploaded_file'] = file_path
            st.session_state['current_file'] = uploaded_file.name
            st.success(f"📄 {uploaded_file.name} uploaded successfully!")

        st.markdown("---")

        if 'uploaded_file' in st.session_state:
            st.subheader("Filter Clauses")
            filter_options = ["All", "Standard", "Important", "Risky"]
            st.session_state.setdefault("type_filter", "All")

            new_value=st.selectbox(
                "Filter by Clause Type",
                filter_options,
                index=filter_options.index(st.session_state["type_filter"])
                
            )

            if st.session_state.type_filter != new_value:
                st.session_state["type_filter"] = new_value
                st.rerun()

        st.markdown("---")
        st.caption(f"© {datetime.now().year} LegaLens | v2.1")

__all__ = ['show_sidebar']
