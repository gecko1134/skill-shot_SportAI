"""
SportAI Board Governance Module
Board management, compliance, reporting, and meeting tools
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List

def run(context: Dict[str, Any]):
    """Main board governance execution"""
    
    st.markdown('<div class="main-header">⚖️ Board Governance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Board management, compliance, and reporting</div>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Board Overview",
        "📄 Documents",
        "🗓️ Meetings",
        "📊 Reports"
    ])
    
    with tab1:
        show_board_overview(context)
        
    with tab2:
        show_documents(context)
        
    with tab3:
        show_meetings(context)
        
    with tab4:
        show_board_reports(context)

def show_board_overview(context: Dict[str, Any]):
    """Board overview dashboard"""
    
    st.markdown("### 📊 Board Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("DSCR (Debt Service)", "1.42", "+0.08")
        st.caption("Target: >1.25")
        
    with col2:
        st.metric("Cash Reserves", "$485K", "+$42K")
        st.caption("3.4 months operating")
        
    with col3:
        st.metric("Utilization Rate", "87.3%", "+5.2%")
        st.caption("Target: 90%")
        
    with col4:
        st.metric("Net Revenue (YTD)", "$1.24M", "+$185K")
        st.caption("vs Budget: +12%")
    
    st.divider()
    
    # Board structure
    st.markdown("### 👥 Board Structure")
    
    board_members = get_board_members()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(
            pd.DataFrame(board_members),
            use_container_width=True,
            hide_index=True
        )
        
    with col2:
        st.markdown("#### Committee Assignments")
        committees = {
            "Finance": 4,
            "Development": 3,
            "Operations": 3,
            "Governance": 2
        }
        
        for committee, count in committees.items():
            st.markdown(f"**{committee}:** {count} members")
    
    # Compliance status
    st.divider()
    st.markdown("### ✅ Compliance Status")
    
    compliance_items = [
        {"Item": "Annual Financial Audit", "Status": "Complete", "Due Date": "2025-03-31", "Progress": 100},
        {"Item": "IRS Form 990", "Status": "In Progress", "Due Date": "2025-11-15", "Progress": 60},
        {"Item": "Board Meeting Minutes", "Status": "Current", "Due Date": "Ongoing", "Progress": 100},
        {"Item": "Conflict of Interest Forms", "Status": "Complete", "Due Date": "Annual", "Progress": 100},
        {"Item": "Insurance Review", "Status": "Pending", "Due Date": "2025-12-01", "Progress": 25},
    ]
    
    df_compliance = pd.DataFrame(compliance_items)
    
    st.dataframe(
        df_compliance,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Progress": st.column_config.ProgressColumn(
                "Progress",
                format="%d%%",
                min_value=0,
                max_value=100
            )
        }
    )
    
    # Action items
    st.divider()
    st.markdown("### 📝 Board Action Items")
    
    action_items = [
        {"Item": "Review Q4 financial projections", "Assigned": "Finance Committee", "Due": "2025-10-25", "Priority": "High"},
        {"Item": "Approve sponsorship policy updates", "Assigned": "Development Committee", "Due": "2025-11-01", "Priority": "Medium"},
        {"Item": "Review facility expansion feasibility", "Assigned": "Operations Committee", "Due": "2025-11-15", "Priority": "High"},
    ]
    
    for item in action_items:
        priority_color = "#ef4444" if item['Priority'] == "High" else "#f59e0b" if item['Priority'] == "Medium" else "#10b981"
        st.markdown(f"""
        <div style="background: #f9fafb; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 4px solid {priority_color};">
        <strong>{item['Item']}</strong><br>
        Assigned: {item['Assigned']} | Due: {item['Due']} | Priority: {item['Priority']}
        </div>
        """, unsafe_allow_html=True)

def show_documents(context: Dict[str, Any]):
    """Board documents and policies"""
    
    st.markdown("### 📄 Board Documents")
    
    # Document categories
    doc_categories = {
        "Governing Documents": [
            {"Name": "Articles of Incorporation", "Last Updated": "2023-01-15", "Version": "1.2"},
            {"Name": "Bylaws", "Last Updated": "2024-06-20", "Version": "2.1"},
            {"Name": "Conflict of Interest Policy", "Last Updated": "2024-01-10", "Version": "1.5"},
        ],
        "Financial Documents": [
            {"Name": "2024 Annual Budget", "Last Updated": "2024-01-05", "Version": "1.0"},
            {"Name": "Q3 2024 Financial Statement", "Last Updated": "2024-10-05", "Version": "1.0"},
            {"Name": "Investment Policy", "Last Updated": "2023-09-15", "Version": "1.1"},
        ],
        "Meeting Records": [
            {"Name": "September 2024 Meeting Minutes", "Last Updated": "2024-09-18", "Version": "Final"},
            {"Name": "August 2024 Meeting Minutes", "Last Updated": "2024-08-21", "Version": "Final"},
            {"Name": "July 2024 Meeting Minutes", "Last Updated": "2024-07-17", "Version": "Final"},
        ],
        "Policies & Procedures": [
            {"Name": "Sponsorship Policy", "Last Updated": "2024-05-12", "Version": "2.0"},
            {"Name": "Pricing Policy & Guardrails", "Last Updated": "2024-08-01", "Version": "1.3"},
            {"Name": "Community Access Policy", "Last Updated": "2024-03-15", "Version": "1.0"},
        ]
    }
    
    for category, documents in doc_categories.items():
        with st.expander(f"📁 {category} ({len(documents)} documents)"):
            df = pd.DataFrame(documents)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col2:
                if st.button(f"📥 Download All", key=f"download_{category}"):
                    st.success(f"Downloading {category}...")
    
    # Upload new document
    st.divider()
    st.markdown("#### ➕ Upload Document")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        doc_category = st.selectbox("Category", list(doc_categories.keys()))
        
    with col2:
        doc_name = st.text_input("Document Name")
        
    with col3:
        uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'xlsx'])
    
    if st.button("📤 Upload Document") and doc_name and uploaded_file:
        st.success(f"✅ '{doc_name}' uploaded successfully!")
        context['audit_log']('document_uploaded', {'name': doc_name, 'category': doc_category})

def show_meetings(context: Dict[str, Any]):
    """Board meeting management"""
    
    st.markdown("### 🗓️ Board Meetings")
    
    # Upcoming meetings
    st.markdown("#### 📅 Upcoming Meetings")
    
    upcoming_meetings = [
        {
            "Date": "2025-10-28",
            "Time": "6:00 PM",
            "Type": "Regular Board Meeting",
            "Location": "Skill Shot - Conference Room",
            "Agenda Items": 5,
            "RSVP": "7/9"
        },
        {
            "Date": "2025-11-15",
            "Time": "12:00 PM",
            "Type": "Finance Committee",
            "Location": "Virtual - Zoom",
            "Agenda Items": 3,
            "RSVP": "3/4"
        }
    ]
    
    for meeting in upcoming_meetings:
        with st.expander(f"📌 {meeting['Date']} - {meeting['Type']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **Date:** {meeting['Date']} at {meeting['Time']}  
                **Location:** {meeting['Location']}  
                **Agenda Items:** {meeting['Agenda Items']}  
                **RSVP Status:** {meeting['RSVP']}
                """)
                
                if st.button("📋 View Full Agenda", key=f"agenda_{meeting['Date']}"):
                    show_meeting_agenda(meeting['Date'])
                    
            with col2:
                st.markdown("#### Quick Actions")
                if st.button("✅ RSVP", key=f"rsvp_{meeting['Date']}"):
                    st.success("RSVP confirmed")
                if st.button("📧 Email Board", key=f"email_{meeting['Date']}"):
                    st.success("Email sent")
    
    # Meeting history
    st.divider()
    st.markdown("#### 📚 Meeting History")
    
    meeting_history = [
        {"Date": "2024-09-16", "Type": "Regular Board", "Attendance": "9/9", "Minutes": "Approved"},
        {"Date": "2024-08-19", "Type": "Regular Board", "Attendance": "8/9", "Minutes": "Approved"},
        {"Date": "2024-07-15", "Type": "Regular Board", "Attendance": "9/9", "Minutes": "Approved"},
        {"Date": "2024-06-17", "Type": "Regular Board", "Attendance": "7/9", "Minutes": "Approved"},
    ]
    
    st.dataframe(pd.DataFrame(meeting_history), use_container_width=True, hide_index=True)
    
    # Create new meeting
    st.divider()
    st.markdown("#### ➕ Schedule New Meeting")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        meeting_date = st.date_input("Meeting Date")
        meeting_time = st.time_input("Start Time")
        
    with col2:
        meeting_type = st.selectbox("Meeting Type", [
            "Regular Board Meeting",
            "Special Board Meeting",
            "Finance Committee",
            "Development Committee",
            "Operations Committee"
        ])
        
    with col3:
        meeting_location = st.selectbox("Location", [
            "Skill Shot - Conference Room",
            "Virtual - Zoom",
            "Hybrid"
        ])
    
    if st.button("📅 Schedule Meeting"):
        st.success(f"✅ {meeting_type} scheduled for {meeting_date}")
        context['audit_log']('meeting_scheduled', {
            'date': str(meeting_date),
            'type': meeting_type
        })

def show_meeting_agenda(meeting_date: str):
    """Display meeting agenda"""
    st.markdown(f"#### Agenda - {meeting_date}")
    
    agenda_items = [
        "1. Call to Order",
        "2. Approval of Previous Minutes",
        "3. Financial Report - Q3 2024",
        "4. Sponsorship Update & New Proposals",
        "5. Facility Utilization Analysis",
        "6. Old Business",
        "7. New Business",
        "8. Executive Session (if needed)",
        "9. Adjournment"
    ]
    
    for item in agenda_items:
        st.markdown(f"- {item}")

def show_board_reports(context: Dict[str, Any]):
    """Board reporting and packet generation"""
    
    st.markdown("### 📊 Board Reports")
    
    # Report templates
    st.markdown("#### 📋 Available Reports")
    
    reports = [
        {
            "Name": "Monthly Financial Summary",
            "Description": "P&L, balance sheet, cash flow, and budget variance",
            "Frequency": "Monthly",
            "Last Generated": "2024-10-01"
        },
        {
            "Name": "Quarterly Board Packet",
            "Description": "Complete board packet with all financials and metrics",
            "Frequency": "Quarterly",
            "Last Generated": "2024-10-01"
        },
        {
            "Name": "Annual Report",
            "Description": "Comprehensive annual report for stakeholders",
            "Frequency": "Annual",
            "Last Generated": "2024-03-15"
        },
        {
            "Name": "Sponsorship Performance",
            "Description": "Sponsorship revenue, renewals, and pipeline",
            "Frequency": "Monthly",
            "Last Generated": "2024-10-05"
        }
    ]
    
    for report in reports:
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.markdown(f"**{report['Name']}**")
            st.caption(report['Description'])
            
        with col2:
            st.caption(f"📅 {report['Frequency']}")
            st.caption(f"Last: {report['Last Generated']}")
            
        with col3:
            if st.button("📄 Generate", key=f"gen_{report['Name']}"):
                generate_board_report(context, report['Name'])
    
    st.divider()
    
    # Custom report builder
    st.markdown("#### 🔧 Custom Report Builder")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.multiselect(
            "Include Sections",
            [
                "Executive Summary",
                "Financial Overview",
                "Utilization Metrics",
                "Revenue Analysis",
                "Sponsorship Update",
                "Membership Stats",
                "Capital Projects",
                "Risk Assessment"
            ],
            default=["Executive Summary", "Financial Overview"]
        )
        
    with col2:
        date_range = st.selectbox(
            "Date Range",
            ["Current Month", "Last Quarter", "Year to Date", "Custom"]
        )
        
        format_type = st.selectbox(
            "Output Format",
            ["PDF", "Excel", "PowerPoint", "All"]
        )
    
    if st.button("🎨 Generate Custom Report", type="primary"):
        st.success("✅ Custom report generated successfully!")
        st.info("Report available for download")
        context['audit_log']('custom_report_generated', {'format': format_type})
    
    # Key metrics summary
    st.divider()
    st.markdown("#### 📈 Key Metrics (Board View)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Financial Health**")
        fig_financial = create_financial_health_chart()
        st.plotly_chart(fig_financial, use_container_width=True)
        
    with col2:
        st.markdown("**Operational Performance**")
        fig_operational = create_operational_chart()
        st.plotly_chart(fig_operational, use_container_width=True)

# Helper functions

def get_board_members() -> List[Dict]:
    """Get board member information"""
    return [
        {
            "Name": "John Anderson",
            "Position": "Board Chair",
            "Committee": "Finance, Governance",
            "Term Expires": "2026-12-31",
            "Attendance": "100%"
        },
        {
            "Name": "Sarah Mitchell",
            "Position": "Vice Chair",
            "Committee": "Development, Operations",
            "Term Expires": "2025-12-31",
            "Attendance": "95%"
        },
        {
            "Name": "David Chen",
            "Position": "Treasurer",
            "Committee": "Finance",
            "Term Expires": "2027-12-31",
            "Attendance": "100%"
        },
        {
            "Name": "Emily Rodriguez",
            "Position": "Secretary",
            "Committee": "Governance",
            "Term Expires": "2026-12-31",
            "Attendance": "100%"
        },
        {
            "Name": "Michael Brown",
            "Position": "Director",
            "Committee": "Operations",
            "Term Expires": "2025-12-31",
            "Attendance": "89%"
        }
    ]

def generate_board_report(context: Dict[str, Any], report_name: str):
    """Generate board report"""
    st.success(f"✅ '{report_name}' generated successfully!")
    st.info("📥 Report available for download as PDF and Excel")
    
    # Show preview
    with st.expander("📄 Report Preview"):
        st.markdown(f"""
        ### {report_name}
        **Generated:** {datetime.now().strftime('%B %d, %Y')}
        
        #### Executive Summary
        - Total Revenue (MTD): $142,500
        - Utilization Rate: 87.3%
        - Active Memberships: 847
        - Sponsorship Value: $385,000
        
        #### Financial Highlights
        - DSCR: 1.42
        - Cash Reserves: $485,000
        - Operating Margin: 12.3%
        
        *Full report attached as PDF*
        """)
    
    context['audit_log']('report_generated', {'report': report_name})

def create_financial_health_chart():
    """Create financial health indicators chart"""
    categories = ['DSCR', 'Cash\nReserves', 'Revenue\nGrowth', 'Margin']
    values = [95, 85, 92, 88]  # Percentages of target
    targets = [100, 100, 100, 100]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=targets,
        name='Target',
        marker_color='lightgray',
        opacity=0.3
    ))
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        name='Actual',
        marker_color=['#10b981' if v >= 90 else '#f59e0b' if v >= 75 else '#ef4444' for v in values],
        text=[f'{v}%' for v in values],
        textposition='outside'
    ))
    
    fig.update_layout(
        height=300,
        barmode='overlay',
        yaxis_title="% of Target",
        yaxis_range=[0, 110],
        showlegend=True
    )
    
    return fig

def create_operational_chart():
    """Create operational metrics chart"""
    metrics = ['Utilization', 'Member\nSatisfaction', 'Staff\nEfficiency', 'Safety']
    scores = [87, 92, 85, 98]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=metrics,
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.3)',
        line=dict(color='#3b82f6', width=2),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        height=300,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False
    )
    
    return fig
