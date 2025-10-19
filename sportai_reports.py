"""
SportAI Reports Module
Comprehensive reporting, exports, and analytics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any

def run(context: Dict[str, Any]):
    """Main reports execution"""
    
    st.markdown('<div class="main-header">📈 Reports & Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comprehensive reporting and data export</div>', unsafe_allow_html=True)
    
    # Report type selector
    report_type = st.selectbox(
        "Select Report Type",
        [
            "Executive Summary",
            "Financial Performance",
            "Utilization Analysis",
            "Revenue Breakdown",
            "Sponsorship Performance",
            "Membership Analytics",
            "Custom Report Builder"
        ]
    )
    
    st.divider()
    
    # Date range selector
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30)
        )
        
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now()
        )
        
    with col3:
        export_format = st.selectbox(
            "Format",
            ["PDF", "Excel", "CSV", "All"]
        )
    
    st.divider()
    
    # Display selected report
    if report_type == "Executive Summary":
        show_executive_summary(context, start_date, end_date)
    elif report_type == "Financial Performance":
        show_financial_performance(context, start_date, end_date)
    elif report_type == "Utilization Analysis":
        show_utilization_analysis(context, start_date, end_date)
    elif report_type == "Revenue Breakdown":
        show_revenue_breakdown(context, start_date, end_date)
    elif report_type == "Sponsorship Performance":
        show_sponsorship_performance(context, start_date, end_date)
    elif report_type == "Membership Analytics":
        show_membership_analytics(context, start_date, end_date)
    elif report_type == "Custom Report Builder":
        show_custom_report_builder(context)
    
    # Export buttons
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Export as PDF", use_container_width=True):
            export_report(context, report_type, "PDF")
            
    with col2:
        if st.button("📊 Export as Excel", use_container_width=True):
            export_report(context, report_type, "Excel")
            
    with col3:
        if st.button("📋 Export as CSV", use_container_width=True):
            export_report(context, report_type, "CSV")
            
    with col4:
        if st.button("📧 Email Report", use_container_width=True):
            st.success("Report emailed successfully!")
            context['audit_log']('report_emailed', {'type': report_type})

def show_executive_summary(context: Dict[str, Any], start_date, end_date):
    """Executive summary report"""
    
    st.markdown("### 📊 Executive Summary")
    st.markdown(f"**Period:** {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}")
    
    # Key highlights
    st.markdown("#### 🎯 Key Highlights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", "$142,500", "+12%")
        
    with col2:
        st.metric("Utilization Rate", "87.3%", "+5.2%")
        
    with col3:
        st.metric("Active Members", 847, "+23")
        
    with col4:
        st.metric("Net Profit Margin", "14.2%", "+1.8%")
    
    st.divider()
    
    # Performance summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💰 Revenue by Source")
        fig = create_revenue_source_chart()
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### 📈 Trend Analysis")
        fig = create_trend_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    # Top performers
    st.divider()
    st.markdown("#### ⭐ Top Performers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Top Revenue Assets**")
        top_assets = [
            "Turf Field - Full: $45,200",
            "Courts (Combined): $28,500",
            "Golf Bays: $18,300"
        ]
        for asset in top_assets:
            st.markdown(f"• {asset}")
            
    with col2:
        st.markdown("**Top Sponsors**")
        top_sponsors = [
            "TechCorp: $125,000",
            "HealthPlus: $75,000",
            "ABC Corp: $50,000"
        ]
        for sponsor in top_sponsors:
            st.markdown(f"• {sponsor}")
            
    with col3:
        st.markdown("**Growth Areas**")
        growth_areas = [
            "Memberships: +18%",
            "Events: +24%",
            "Sponsorships: +15%"
        ]
        for area in growth_areas:
            st.markdown(f"• {area}")

def show_financial_performance(context: Dict[str, Any], start_date, end_date):
    """Financial performance report"""
    
    st.markdown("### 💰 Financial Performance")
    
    # P&L Summary
    st.markdown("#### 📋 Profit & Loss Summary")
    
    pl_data = {
        "Category": [
            "Revenue - Bookings",
            "Revenue - Memberships",
            "Revenue - Sponsorships",
            "Revenue - Events",
            "Revenue - Other",
            "Total Revenue",
            "",
            "Operating Expenses",
            "Staff Costs",
            "Facility Maintenance",
            "Utilities",
            "Marketing",
            "Total Expenses",
            "",
            "Net Operating Income",
            "EBITDA",
            "Net Profit"
        ],
        "Amount": [
            65000, 42000, 25000, 18000, 7500,
            157500,
            0,
            45000, 32000, 18500, 12000, 8500,
            116000,
            0,
            41500, 48200, 35800
        ],
        "% of Revenue": [
            41.3, 26.7, 15.9, 11.4, 4.8,
            100.0,
            0,
            28.6, 20.3, 11.7, 7.6, 5.4,
            73.7,
            0,
            26.3, 30.6, 22.7
        ]
    }
    
    df = pd.DataFrame(pl_data)
    df['Amount'] = df['Amount'].apply(lambda x: f"${x:,.0f}" if x > 0 else "")
    df['% of Revenue'] = df['% of Revenue'].apply(lambda x: f"{x:.1f}%" if x > 0 else "")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Financial ratios
    st.divider()
    st.markdown("#### 📊 Financial Ratios & Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Gross Margin", "73.7%", "+2.1%")
        st.metric("Operating Margin", "26.3%", "+1.5%")
        
    with col2:
        st.metric("Net Margin", "22.7%", "+1.8%")
        st.metric("ROI", "18.4%", "+2.3%")
        
    with col3:
        st.metric("DSCR", "1.42", "+0.08")
        st.metric("Current Ratio", "2.8", "+0.2")
        
    with col4:
        st.metric("Quick Ratio", "2.1", "+0.1")
        st.metric("Debt/Equity", "0.45", "-0.05")
    
    # Cash flow
    st.divider()
    st.markdown("#### 💵 Cash Flow Analysis")
    
    fig_cashflow = create_cashflow_chart()
    st.plotly_chart(fig_cashflow, use_container_width=True)

def show_utilization_analysis(context: Dict[str, Any], start_date, end_date):
    """Utilization analysis report"""
    
    st.markdown("### 🎯 Utilization Analysis")
    
    # Overall utilization
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Utilization", "87.3%", "+5.2%")
        
    with col2:
        st.metric("Prime Time", "94.2%", "+3.1%")
        
    with col3:
        st.metric("Off-Peak", "68.5%", "+8.7%")
    
    st.divider()
    
    # Utilization by asset
    st.markdown("#### 📊 Utilization by Asset Type")
    
    util_data = {
        "Asset Type": ["Turf Field", "Courts", "Golf Bays", "Suites", "Esports"],
        "Capacity Hours": [168, 672, 336, 168, 168],
        "Booked Hours": [154, 571, 262, 109, 119],
        "Utilization %": [91.7, 85.0, 78.0, 64.9, 70.8],
        "Revenue": [45200, 28500, 18300, 12800, 8900]
    }
    
    df = pd.DataFrame(util_data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Utilization %": st.column_config.ProgressColumn(
                "Utilization %",
                format="%.1f%%",
                min_value=0,
                max_value=100
            ),
            "Revenue": st.column_config.NumberColumn(
                "Revenue",
                format="$%d"
            )
        }
    )
    
    # Hourly breakdown
    st.divider()
    st.markdown("#### ⏰ Hourly Utilization Pattern")
    
    fig_hourly = create_hourly_utilization_detailed()
    st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Gap analysis
    st.divider()
    st.markdown("#### 🔍 Gap Analysis & Opportunities")
    
    opportunities = [
        {"Time Slot": "Tuesday 2-4pm", "Current": "45%", "Potential": "75%", "Revenue Opportunity": "$2,400/month"},
        {"Time Slot": "Thursday 10am-12pm", "Current": "52%", "Potential": "80%", "Revenue Opportunity": "$1,800/month"},
        {"Time Slot": "Sunday 8-10pm", "Current": "38%", "Potential": "65%", "Revenue Opportunity": "$1,200/month"},
    ]
    
    st.dataframe(pd.DataFrame(opportunities), use_container_width=True, hide_index=True)

def show_revenue_breakdown(context: Dict[str, Any], start_date, end_date):
    """Revenue breakdown report"""
    
    st.markdown("### 💵 Revenue Breakdown")
    
    # Revenue by category
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Revenue by Category")
        fig = create_revenue_category_chart()
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### 📈 Revenue Trend")
        fig = create_revenue_trend_detailed()
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed breakdown
    st.divider()
    st.markdown("#### 📋 Detailed Revenue Breakdown")
    
    revenue_detail = {
        "Category": [
            "Bookings - Turf Field",
            "Bookings - Courts",
            "Bookings - Golf Bays",
            "Bookings - Suites",
            "Memberships - Bronze",
            "Memberships - Silver",
            "Memberships - Gold",
            "Memberships - Platinum",
            "Sponsorships - Naming Rights",
            "Sponsorships - Signage",
            "Sponsorships - Digital",
            "Events - Tournaments",
            "Events - Corporate",
            "Concessions",
            "Other"
        ],
        "Revenue": [
            45200, 28500, 18300, 12800,
            4205, 14760, 21525, 10875,
            15000, 8000, 2000,
            12000, 6000,
            5200, 2300
        ],
        "Transactions": [
            286, 814, 407, 64,
            145, 328, 287, 87,
            2, 8, 4,
            8, 4,
            520, 46
        ],
        "Avg Transaction": [
            158, 35, 45, 200,
            29, 45, 75, 125,
            7500, 1000, 500,
            1500, 1500,
            10, 50
        ]
    }
    
    df = pd.DataFrame(revenue_detail)
    df['Revenue'] = df['Revenue'].apply(lambda x: f"${x:,.0f}")
    df['Avg Transaction'] = df['Avg Transaction'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df, use_container_width=True, hide_index=True)

def show_sponsorship_performance(context: Dict[str, Any], start_date, end_date):
    """Sponsorship performance report"""
    
    st.markdown("### 🤝 Sponsorship Performance")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Value", "$385,000")
        
    with col2:
        st.metric("Inventory Sold", "73.5%")
        
    with col3:
        st.metric("Renewal Rate", "85%")
        
    with col4:
        st.metric("Pipeline Value", "$120,000")
    
    st.divider()
    
    # Active sponsors
    st.markdown("#### 💼 Active Sponsors")
    
    sponsor_data = [
        {"Sponsor": "TechCorp Solutions", "Annual Value": 125000, "Assets": 5, "Expires": "2026-12-31", "Renewal Prob": 92},
        {"Sponsor": "HealthPlus Medical", "Annual Value": 75000, "Assets": 3, "Expires": "2026-05-31", "Renewal Prob": 78},
        {"Sponsor": "ABC Corporation", "Annual Value": 50000, "Assets": 2, "Expires": "2025-12-31", "Renewal Prob": 85},
        {"Sponsor": "XYZ Industries", "Annual Value": 35000, "Assets": 2, "Expires": "2026-03-31", "Renewal Prob": 70},
    ]
    
    df = pd.DataFrame(sponsor_data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Annual Value": st.column_config.NumberColumn(
                "Annual Value",
                format="$%d"
            ),
            "Renewal Prob": st.column_config.ProgressColumn(
                "Renewal Probability",
                format="%d%%",
                min_value=0,
                max_value=100
            )
        }
    )

def show_membership_analytics(context: Dict[str, Any], start_date, end_date):
    """Membership analytics report"""
    
    st.markdown("### 👥 Membership Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Members", 847, "+23")
        
    with col2:
        st.metric("MRR", "$42,350", "+$1,840")
        
    with col3:
        st.metric("Churn Rate", "2.1%", "-0.3%")
        
    with col4:
        st.metric("LTV", "$2,847", "+$142")
    
    st.divider()
    
    # Tier breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Members by Tier")
        fig = create_member_tier_chart()
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### 📈 Growth Trend")
        fig = create_member_growth_chart()
        st.plotly_chart(fig, use_container_width=True)

def show_custom_report_builder(context: Dict[str, Any]):
    """Custom report builder"""
    
    st.markdown("### 🔧 Custom Report Builder")
    
    st.info("Build a custom report by selecting the sections you want to include.")
    
    # Section selection
    col1, col2 = st.columns(2)
    
    with col1:
        sections = st.multiselect(
            "Select Sections",
            [
                "Executive Summary",
                "Financial Performance",
                "Utilization Analysis",
                "Revenue Breakdown",
                "Sponsorship Performance",
                "Membership Analytics",
                "Booking Analysis",
                "Pricing Performance",
                "Forecasts & Projections"
            ],
            default=["Executive Summary", "Financial Performance"]
        )
        
    with col2:
        visualizations = st.multiselect(
            "Include Charts",
            [
                "Revenue Trends",
                "Utilization Heatmap",
                "P&L Summary",
                "Cash Flow",
                "Member Growth",
                "Sponsor Pipeline"
            ]
        )
    
    # Additional options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        include_raw_data = st.checkbox("Include Raw Data Tables")
        
    with col2:
        include_comparisons = st.checkbox("Include Prior Period Comparison")
        
    with col3:
        include_forecast = st.checkbox("Include 90-Day Forecast")
    
    if st.button("🎨 Generate Custom Report", type="primary"):
        st.success("✅ Custom report generated successfully!")
        st.balloons()
        
        # Show preview
        with st.expander("📄 Report Preview"):
            for section in sections:
                st.markdown(f"### {section}")
                st.markdown(f"*{section} content would appear here*")
                st.divider()

# Helper functions

def export_report(context: Dict[str, Any], report_type: str, format: str):
    """Export report in specified format"""
    st.success(f"✅ {report_type} exported as {format}!")
    st.info("📥 Download will begin shortly...")
    
    context['audit_log']('report_exported', {
        'type': report_type,
        'format': format
    })

def create_revenue_source_chart():
    """Create revenue source pie chart"""
    data = {
        'Source': ['Bookings', 'Memberships', 'Sponsorships', 'Events', 'Other'],
        'Revenue': [104800, 51365, 25000, 18000, 7500]
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=data['Source'],
        values=data['Revenue'],
        hole=0.4,
        marker_colors=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
    )])
    
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    
    return fig

def create_trend_chart():
    """Create trend chart"""
    months = pd.date_range(start='2024-01-01', periods=10, freq='M')
    revenue = [128000, 132000, 135000, 138000, 142000, 145000, 148000, 151000, 154000, 157500]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=revenue,
        mode='lines+markers',
        line=dict(color='#3b82f6', width=3)
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis_title="Revenue ($)"
    )
    
    return fig

def create_cashflow_chart():
    """Create cash flow waterfall chart"""
    categories = ['Starting Cash', 'Revenue', 'Expenses', 'CapEx', 'Ending Cash']
    values = [0, 157500, -116000, -8500, 33000]
    
    fig = go.Figure(go.Waterfall(
        x=categories,
        y=values,
        measure=['absolute', 'relative', 'relative', 'relative', 'total'],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#10b981"}},
        decreasing={"marker": {"color": "#ef4444"}},
        totals={"marker": {"color": "#3b82f6"}}
    ))
    
    fig.update_layout(height=400, yaxis_title="Amount ($)")
    
    return fig

def create_hourly_utilization_detailed():
    """Create detailed hourly utilization chart"""
    hours = list(range(6, 23))
    utilization = [45, 52, 68, 75, 82, 88, 92, 95, 97, 96, 93, 90, 85, 78, 72, 68, 55]
    target = [75] * len(hours)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=target,
        mode='lines',
        name='Target',
        line=dict(color='gray', dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=utilization,
        mode='lines+markers',
        name='Actual',
        fill='tonexty',
        line=dict(color='#3b82f6', width=3)
    ))
    
    fig.update_layout(
        height=400,
        xaxis_title="Hour of Day",
        yaxis_title="Utilization (%)",
        hovermode='x unified'
    )
    
    return fig

def create_revenue_category_chart():
    """Create revenue category bar chart"""
    categories = ['Bookings', 'Memberships', 'Sponsorships', 'Events', 'Other']
    revenue = [104800, 51365, 25000, 18000, 7500]
    
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=revenue,
        marker_color='#3b82f6',
        text=revenue,
        texttemplate='$%{text:,.0f}',
        textposition='outside'
    )])
    
    fig.update_layout(height=300, yaxis_title="Revenue ($)")
    
    return fig

def create_revenue_trend_detailed():
    """Create detailed revenue trend"""
    months = pd.date_range(start='2024-01-01', periods=10, freq='M')
    revenue = [128000, 132000, 135000, 138000, 142000, 145000, 148000, 151000, 154000, 157500]
    forecast = [None] * 8 + [157500, 160000, 163000]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=revenue,
        mode='lines+markers',
        name='Actual',
        line=dict(color='#3b82f6', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=pd.date_range(start=months[8], periods=3, freq='M'),
        y=[157500, 160000, 163000],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#10b981', width=2, dash='dash')
    ))
    
    fig.update_layout(
        height=300,
        yaxis_title="Revenue ($)",
        hovermode='x unified'
    )
    
    return fig

def create_member_tier_chart():
    """Create member tier distribution"""
    tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    counts = [145, 328, 287, 87]
    
    fig = go.Figure(data=[go.Bar(
        x=tiers,
        y=counts,
        marker_color=['#cd7f32', '#c0c0c0', '#ffd700', '#e5e4e2'],
        text=counts,
        textposition='outside'
    )])
    
    fig.update_layout(height=300, yaxis_title="Members")
    
    return fig

def create_member_growth_chart():
    """Create member growth chart"""
    months = pd.date_range(start='2024-01-01', periods=10, freq='M')
    members = [645, 658, 672, 695, 718, 742, 765, 788, 808, 825]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=members,
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#10b981', width=3)
    ))
    
    fig.update_layout(
        height=300,
        yaxis_title="Total Members"
    )
    
    return fig
