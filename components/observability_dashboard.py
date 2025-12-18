import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def show_observability_dashboard():
    """Display professional Splunk observability dashboard."""

    st.markdown('<div class="observability-page-active"></div>', unsafe_allow_html=True)

    # Use container to isolate dashboard content and prevent leaking
    with st.container():
        st.title("Splunk Observability Dashboard")
        st.markdown("*USF Concierge - Production Monitoring*")

        st.info("""
        **Demo Dashboard:** Provides a glimpse at a Splunk dashboard. The numbers are sample data, but the layout mirrors what’s wired up through the Splunk logger.
        """)

        # Metrics row
        st.subheader("System Health Pulse")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Requests/min",
                value="47",
                delta="+5%",
                help="Total request throughput"
            )

        with col2:
            st.metric(
                label="P95 Latency",
                value="1.2s",
                delta="-0.3s",
                delta_color="inverse",
                help="95th percentile response time"
            )

        with col3:
            st.metric(
                label="Error Rate",
                value="0.8%",
                delta="-0.2%",
                delta_color="inverse",
                help="Percentage of failed requests"
            )

        with col4:
            st.metric(
                label="RAG Quality Score",
                value="0.78",
                delta="+0.05",
                help="Average cross-encoder relevance score"
            )

        st.divider()

        # Charts section
        col1, col2 = st.columns(2)

        # Generate mock data for last 24 hours
        dates = pd.date_range(end=datetime.now(), periods=24, freq='h')

        with col1:
            st.subheader("Request Volume Over Time")
            st.caption("Every question and regenerate request flowing through the app")

            df_requests = pd.DataFrame({
                'Time': dates,
                'Requests': np.random.randint(30, 80, 24)
            })
            st.line_chart(df_requests.set_index('Time'))

        with col2:
            st.subheader("RAG Retrieval Quality")
            st.caption("How confident the reranker feels about the retrieved chunks")

            df_quality = pd.DataFrame({
                'Time': dates,
                'Avg Score': np.random.uniform(0.6, 0.9, 24)
            })
            st.line_chart(df_quality.set_index('Time'))

        # Second row of charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Response Latency Percentiles")
            st.caption("Median vs. tail latency for the end‑to‑end response time")

            df_latency = pd.DataFrame({
                'Time': dates,
                'P50': np.random.uniform(800, 1200, 24),
                'P95': np.random.uniform(1500, 2500, 24)
            })
            st.line_chart(df_latency.set_index('Time'))

        with col2:
            st.subheader("Database Query Performance")
            st.caption("Supabase reads/writes measured inside the database client")

            df_db = pd.DataFrame({
                'Time': dates,
                'Duration (ms)': np.random.uniform(30, 120, 24)
            })
            st.area_chart(df_db.set_index('Time'))

        st.divider()

        # Event category breakdown
        st.subheader("Event Distribution by Category")
        st.caption("What the Splunk logger is actually capturing")

        col1, col2 = st.columns([2, 1])

        with col1:
            event_data = pd.DataFrame({
                'Category': ['Request', 'RAG', 'LLM', 'API', 'Database', 'MCP', 'Security', 'Agent'],
                'Count': [640, 480, 220, 160, 130, 110, 40, 25]
            })
            st.bar_chart(event_data.set_index('Category'), height=300)

        with col2:
            st.markdown("**Event Categories**")
            st.markdown("""
            **Request** – every question, regenerate, or error captured in `app.py`  
            **RAG** – the retrieval journey: search, rerank, neighbor fetch, pipeline complete  
            **LLM** – token usage and latency for the Azure Phi-4 calls  
            **API** – Gmail, Calendar, and Hugging Face calls plus their metadata  
            **Database** – Supabase reads/writes (sessions, messages, audit logs)  
            **MCP** – tool calls routed through the MCP server/client  
            **Security** – sanitization, injection checks, content-filter blocks  
            **Agent** – email/meeting assistant clicks inside the Streamlit UI
            """)

        st.divider()

        st.subheader("Production Infrastructure")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Observability Stack**")
            impl_data = {
                "Component": [
                    "Event Collector",
                    "Transport",
                    "Instrumented Modules",
                    "Event Categories",
                    "Fallback / Resilience"
                ],
                "Status": [
                    "The shared Splunk logger handles batching + timing and feeds every module data safely",
                    "Events stream into Splunk’s HTTP collector (with retries and a fallback file) ",
                    "From chat orchestration to Google tools, every layer calls the same logging helper",
                    "We treat requests, RAG, LLMs, APIs, database ops, MCP I/O, security, and UI actions as first-class data sources",
                    "If HEC is unreachable we drop into a local log so nothing silently disappears"
                ]
            }
            df_impl = pd.DataFrame(impl_data)
            st.dataframe(
                df_impl,
                hide_index=True,
                width="stretch",
                column_config={
                    "Component": st.column_config.TextColumn("Component", width="small"),
                    "Status": st.column_config.TextColumn("Status", width="large")
                }
            )

        with col2:
            st.markdown("**What We Watch For**")
            perf_data = {
                "Optimization": [
                    "Session/Message Cache",
                    "Rerank Cache",
                    "Neighbor Batching",
                    "MCP Metrics",
                    "API Metadata"
                ],
                "Impact": [
                      "Warm caches keep Supabase quiet between chat polls",
                      "The reranker stays fast by skipping repeat query/doc pairs",
                      "Neighbor lookups run as one bundled query instead of dozens",
                      "Every MCP tool call is timed and labeled so slow tools stand out",
                      "API logs capture recipient, status, and duration for clear audit trails"
                  ]
            }
            df_perf = pd.DataFrame(perf_data)
            st.dataframe(
                df_perf,
                hide_index=True,
                width="stretch",
                column_config={
                    "Optimization": st.column_config.TextColumn("Optimization", width="small"),
                    "Impact": st.column_config.TextColumn("Impact", width="large")
                }
            )
