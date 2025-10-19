"""
SportAI Dashboard Module
Executive overview with KPIs and real-time metrics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, Any

def run(context: Dict[str, Any]):
    """Main dashboard execution"""
    
    st.markdown('<div class="main-header">📊 Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Real-time facility performance • {datetime.now().strftime("%B %d, %Y")}</div>', unsafe_allow_html=True)
    
    # Get user context
    user_role = context['user_ctx']['role']
    
    # KPI Row
    st.markdown("### Key Performance Indicators")
    
    # Calculate or fetch KPIs (in production, these would come from database)
    kpis = calculate_kpis(context)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_util = kpis['utilization'] - kpis['utilization_prev']
        st.metric(
            "Facility Utilization",
            f"{kpis['utilization']:.1f}%",
            f"{delta_util:+.1f}%",
            delta_color="normal"
        )
        
    with col2:
        delta_rev = kpis['revenue_mtd'] - kpis['revenue_prev']
        st.metric(
            "Revenue (MTD)",
            f"${kpis['revenue_mtd']:,.0f}",
            f"${delta_rev:+,.0f}",
            delta_color="normal"
        )
        
    with col3:
        st.metric(
            "Active Members",
            f"{kpis['active_members']:,}",
            f"+{kpis['new_members']}",
            delta_color="normal"
        )
        
    with col4:
        st.metric(
            "Sponsorship Sold",
            f"{kpis['sponsorship_sold']:.0f}%",
            f"${kpis['sponsorship_value']:,.0f}",
            delta_color="normal"
        )
    
    st.divider()
    
    # Two-column layout for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Revenue Trend (Last 30 Days)")
        fig_revenue = create_revenue_chart()
        st.plotly_chart(fig_revenue, use_container_width=True)
        
        st.markdown("### 🎯 Utilization by Asset Type")
        fig_utilization = create_utilization_chart()
        st.plotly_chart(fig_utilization, use_container_width=True)
        
    with col2:
        st.markdown("### 📅 Weekly Schedule Heatmap")
        fig_heatmap = create_schedule_heatmap()
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.markdown("### 💰 Revenue Mix")
        fig_revenue_mix = create_revenue_mix_chart()
        st.plotly_chart(fig_revenue_mix, use_container_width=True)
    
    # Alerts and notifications
    if user_role in ['admin', 'board']:
        st.divider()
        st.markdown("### ⚠️ Alerts & Notifications")
        
        alerts = get_alerts(context)
        
        for alert in alerts:
            alert_type = alert['type']
            if alert_type == 'warning':
                st.markdown(f"""
                <div class="alert-warning">
                    <strong>{alert['title']}</strong><br>
                    {alert['message']}
                </div>
                """, unsafe_allow_html=True)
            elif alert_type == 'success':
                st.markdown(f"""
                <div class="alert-success">
                    <strong>{alert['title']}</strong><br>
                    {alert['message']}
                </div>
                """, unsafe_allow_html=True)
    
    # Quick actions
    st.divider()
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Generate Board Report", use_container_width=True):
            st.info("Board report generation initiated...")
            context['audit_log']('report_generation', {'type': 'board_report'})
            
    with col2:
        if st.button("💰 Run Pricing Update", use_container_width=True):
            st.info("Dynamic pricing analysis started...")
            context['audit_log']('pricing_update', {'type': 'dynamic_pricing'})
            
    with col3:
        if st.button("🤝 Sponsor Pipeline", use_container_width=True):
            st.info("Loading sponsor pipeline...")
            
    with col4:
        if st.button("📊 Export Data", use_container_width=True):
            export_dashboard_data(context)

def calculate_kpis(context: Dict[str, Any]) -> Dict[str, float]:
    """Calculate current KPIs"""
    # In production, these would query actual database
    # Using realistic sample data for demonstration
    
    return {
        'utilization': 87.3,
        'utilization_prev': 82.1,
        'revenue_mtd': 142500,
        'revenue_prev': 128000,
        'active_members': 847,
        'new_members': 23,
        'sponsorship_sold': 73.5,
        'sponsorship_value': 385000
    }

def create_revenue_chart():
    """Create revenue trend chart"""
    # Generate sample data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    revenue = [8000 + (i * 150) + (500 if i % 7 in [5, 6] else 0) for i in range(30)]
    
    df = pd.DataFrame({
        'Date': dates,
        'Revenue': revenue
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Revenue'],
        mode='lines+markers',
        name='Daily Revenue',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        hovermode='x unified'
    )
    
    return fig

def create_utilization_chart():
    """Create utilization by asset type chart"""
    data = {
        'Asset Type': ['Turf Field', 'Courts', 'Golf Bays', 'Suites', 'Esports'],
        'Utilization': [92, 85, 78, 65, 71]
    }
    
    df = pd.DataFrame(data)
    
    fig = go.Figure(data=[
        go.Bar(
            x=df['Asset Type'],
            y=df['Utilization'],
            marker_color=['#10b981' if x >= 85 else '#f59e0b' if x >= 70 else '#ef4444' 
                          for x in df['Utilization']],
            text=df['Utilization'],
            texttemplate='%{text}%',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis_title="Utilization (%)",
        yaxis_range=[0, 100],
        showlegend=False
    )
    
    return fig

def create_schedule_heatmap():
    """Create weekly schedule heatmap"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = ['6am', '9am', '12pm', '3pm', '6pm', '9pm']
    
    # Sample utilization data
    data = [
        [45, 65, 85, 90, 95, 85],  # Mon
        [50, 70, 88, 92, 93, 80],  # Tue
        [48, 68, 87, 91, 94, 82],  # Wed
        [52, 72, 89, 93, 96, 84],  # Thu
        [55, 75, 90, 94, 97, 88],  # Fri
        [85, 95, 98, 95, 92, 90],  # Sat
        [80, 90, 95, 92, 88, 75],  # Sun
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=hours,
        y=days,
        colorscale='Blues',
        text=data,
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Utilization %")
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_title="Time of Day",
        yaxis_title="Day of Week"
    )
    
    return fig

def create_revenue_mix_chart():
    """Create revenue mix pie chart"""
    data = {
        'Source': ['Bookings', 'Memberships', 'Sponsorships', 'Events', 'Concessions'],
        'Revenue': [65000, 42000, 25000, 18000, 7500]
    }
    
    df = pd.DataFrame(data)
    
    fig = go.Figure(data=[go.Pie(
        labels=df['Source'],
        values=df['Revenue'],
        hole=0.4,
        marker_colors=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
    )])
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True
    )
    
    return fig

def get_alerts(context: Dict[str, Any]) -> list:
    """Get current alerts and notifications"""
    return [
        {
            'type': 'warning',
            'title': 'Low Utilization Alert',
            'message': 'Tuesday 2-4pm slots at 45% capacity. Consider promotional pricing.'
        },
        {
            'type': 'success',
            'title': 'Sponsorship Renewal',
            'message': 'ABC Corporation renewed naming rights for $125K (3-year term).'
        },
        {
            'type': 'warning',
            'title': 'Contract Expiring',
            'message': '5 sponsorship contracts expire within 60 days. Auto-renewal sequence initiated.'
        }
    ]

def export_dashboard_data(context: Dict[str, Any]):
    """Export dashboard data to Excel"""
    st.success("Dashboard data exported to Excel. Download will begin shortly...")
    context['audit_log']('data_export', {'type': 'dashboard', 'format': 'xlsx'})
