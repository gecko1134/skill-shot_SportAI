"""
SportAI AI Scheduling Optimizer Module
Intelligent scheduling with constraint satisfaction and optimization
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json

def run(context: Dict[str, Any]):
    """Main scheduling optimizer execution"""
    
    st.markdown('<div class="main-header">🤖 AI Scheduling Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent scheduling with constraint satisfaction</div>', unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Scheduler", 
        "🎯 Optimization", 
        "⚙️ Constraints", 
        "📊 Analysis"
    ])
    
    with tab1:
        show_scheduler_view(context)
        
    with tab2:
        show_optimization_view(context)
        
    with tab3:
        show_constraints_view(context)
        
    with tab4:
        show_analysis_view(context)

def show_scheduler_view(context: Dict[str, Any]):
    """Main scheduling interface"""
    
    st.markdown("### 📋 Schedule Overview")
    
    # Date range selector
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        start_date = st.date_input("Start Date", datetime.now())
        
    with col2:
        end_date = st.date_input("End Date", datetime.now() + timedelta(days=7))
        
    with col3:
        view_mode = st.selectbox("View", ["Week", "Day", "Month"])
    
    # Asset filter
    assets = get_available_assets()
    selected_assets = st.multiselect(
        "Filter by Asset",
        assets,
        default=assets
    )
    
    st.divider()
    
    # Current schedule visualization
    st.markdown("### 📅 Current Schedule")
    
    schedule_data = get_schedule_data(start_date, end_date, selected_assets)
    
    if not schedule_data.empty:
        fig = create_schedule_gantt(schedule_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Schedule details table
        with st.expander("📋 Schedule Details"):
            st.dataframe(
                schedule_data,
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("No bookings found for selected date range and assets.")
    
    # Quick booking form
    st.divider()
    st.markdown("### ➕ Quick Booking")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        booking_asset = st.selectbox("Asset", assets, key="new_booking_asset")
        booking_date = st.date_input("Date", key="new_booking_date")
        
    with col2:
        booking_start = st.time_input("Start Time", key="new_booking_start")
        booking_duration = st.selectbox("Duration", [1, 1.5, 2, 2.5, 3, 4], key="new_booking_duration")
        
    with col3:
        booking_customer = st.text_input("Customer", key="new_booking_customer")
        booking_type = st.selectbox("Type", ["Regular", "Youth", "Tournament", "Corporate"], key="new_booking_type")
    
    if st.button("💾 Create Booking", type="primary"):
        create_booking(context, {
            'asset': booking_asset,
            'date': booking_date,
            'start_time': booking_start,
            'duration': booking_duration,
            'customer': booking_customer,
            'type': booking_type
        })
        st.success(f"✅ Booking created for {booking_customer} on {booking_date}")
        context['audit_log']('booking_created', {
            'customer': booking_customer,
            'asset': booking_asset,
            'date': str(booking_date)
        })

def show_optimization_view(context: Dict[str, Any]):
    """AI optimization interface"""
    
    st.markdown("### 🎯 Schedule Optimization")
    
    st.info("""
    The AI optimizer automatically schedules requests to maximize:
    - **Revenue** per hour and per square foot
    - **Utilization** while preserving prime inventory
    - **Customer satisfaction** by respecting preferences and constraints
    """)
    
    # Pending requests
    st.markdown("#### 📬 Pending Booking Requests")
    
    pending_requests = get_pending_requests()
    
    if not pending_requests.empty:
        st.dataframe(pending_requests, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            optimization_goal = st.selectbox(
                "Primary Goal",
                ["Maximize Revenue", "Maximize Utilization", "Balance Both"]
            )
            
        with col2:
            fairness_weight = st.slider(
                "Fairness Weight",
                0.0, 1.0, 0.3,
                help="Higher values prioritize community/youth bookings"
            )
            
        with col3:
            time_horizon = st.selectbox(
                "Time Horizon",
                ["Next 7 Days", "Next 14 Days", "Next 30 Days"]
            )
        
        st.divider()
        
        if st.button("🚀 Run Optimizer", type="primary"):
            with st.spinner("Running AI optimization..."):
                # Simulate optimization
                result = run_optimization(
                    pending_requests,
                    optimization_goal,
                    fairness_weight,
                    time_horizon
                )
                
                st.success("✅ Optimization complete!")
                
                # Show results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Requests Scheduled", result['scheduled'])
                    
                with col2:
                    st.metric("Estimated Revenue", f"${result['revenue']:,.0f}")
                    
                with col3:
                    st.metric("Utilization Impact", f"+{result['util_increase']:.1f}%")
                
                # Detailed results
                st.markdown("#### 📊 Optimization Results")
                st.dataframe(result['schedule'], use_container_width=True)
                
                if st.button("✅ Accept & Schedule All"):
                    accept_optimized_schedule(context, result['schedule'])
                    st.success("Schedule applied successfully!")
                    
    else:
        st.info("No pending booking requests at this time.")

def show_constraints_view(context: Dict[str, Any]):
    """Constraint configuration interface"""
    
    st.markdown("### ⚙️ Scheduling Constraints")
    
    # Load current constraints
    constraints = load_constraints()
    
    st.markdown("#### 🏢 Asset Constraints")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Prime Time Hours**")
        prime_start = st.time_input("Start", constraints.get('prime_start', datetime.strptime("17:00", "%H:%M").time()))
        prime_end = st.time_input("End", constraints.get('prime_end', datetime.strptime("22:00", "%H:%M").time()))
        
        st.markdown("**Cleaning Buffers**")
        cleaning_buffer = st.number_input("Minutes between bookings", 15, 60, constraints.get('cleaning_buffer', 30))
        
    with col2:
        st.markdown("**Minimum Booking Duration**")
        min_duration = st.number_input("Hours", 0.5, 4.0, constraints.get('min_duration', 1.0), 0.5)
        
        st.markdown("**Advance Booking**")
        max_advance_days = st.number_input("Maximum days in advance", 7, 365, constraints.get('max_advance', 90))
    
    st.divider()
    
    st.markdown("#### 👥 Customer Priority Rules")
    
    priority_rules = constraints.get('priority_rules', {
        'youth': 3,
        'non_profit': 2,
        'regular': 1,
        'corporate': 0
    })
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        youth_priority = st.number_input("Youth", 0, 10, priority_rules['youth'])
        
    with col2:
        nonprofit_priority = st.number_input("Non-Profit", 0, 10, priority_rules['non_profit'])
        
    with col3:
        regular_priority = st.number_input("Regular", 0, 10, priority_rules['regular'])
        
    with col4:
        corporate_priority = st.number_input("Corporate", 0, 10, priority_rules['corporate'])
    
    st.divider()
    
    st.markdown("#### 🚫 Blackout Periods")
    
    blackouts = constraints.get('blackouts', [])
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        blackout_start = st.date_input("Blackout Start", key="blackout_start")
        
    with col2:
        blackout_end = st.date_input("Blackout End", key="blackout_end")
        
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Blackout"):
            blackouts.append({
                'start': str(blackout_start),
                'end': str(blackout_end)
            })
            st.success("Blackout period added")
    
    if blackouts:
        st.dataframe(pd.DataFrame(blackouts), use_container_width=True)
    
    st.divider()
    
    if st.button("💾 Save Constraints", type="primary"):
        save_constraints({
            'prime_start': prime_start,
            'prime_end': prime_end,
            'cleaning_buffer': cleaning_buffer,
            'min_duration': min_duration,
            'max_advance': max_advance_days,
            'priority_rules': {
                'youth': youth_priority,
                'non_profit': nonprofit_priority,
                'regular': regular_priority,
                'corporate': corporate_priority
            },
            'blackouts': blackouts
        })
        st.success("✅ Constraints saved successfully!")
        context['audit_log']('constraints_updated', {'module': 'scheduling'})

def show_analysis_view(context: Dict[str, Any]):
    """Scheduling analysis and insights"""
    
    st.markdown("### 📊 Schedule Analysis")
    
    # Utilization by hour
    st.markdown("#### ⏰ Utilization by Hour of Day")
    fig_hourly = create_hourly_utilization_chart()
    st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Conflict analysis
    st.markdown("#### ⚠️ Scheduling Conflicts & Gaps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Booking Conflicts (Last 30 Days)", 3, "-2")
        st.metric("Average Gap Time", "45 min", "+5 min")
        
    with col2:
        st.metric("Declined Requests", 12, "-4")
        st.metric("Customer Reschedules", 8, "+2")
    
    # Revenue impact
    st.markdown("#### 💰 Revenue Impact Analysis")
    
    impact_data = {
        'Scenario': ['Current Schedule', 'AI Optimized', 'Manual Override'],
        'Revenue': [142500, 168000, 135000],
        'Utilization': [87.3, 92.1, 84.5]
    }
    
    df = pd.DataFrame(impact_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Scenario'],
        y=df['Revenue'],
        name='Revenue',
        marker_color='#3b82f6'
    ))
    
    fig.update_layout(
        height=300,
        yaxis_title="Revenue ($)",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Helper functions

def get_available_assets() -> List[str]:
    """Get list of bookable assets"""
    return [
        "Turf Field - Full",
        "Turf Field - Half A",
        "Turf Field - Half B",
        "Court 1",
        "Court 2",
        "Court 3",
        "Court 4",
        "Golf Bay 1",
        "Golf Bay 2",
        "Suite A",
        "Suite B"
    ]

def get_schedule_data(start_date, end_date, assets) -> pd.DataFrame:
    """Get schedule data for date range"""
    # Sample data - in production, query database
    data = {
        'Asset': ['Turf Field - Full', 'Court 1', 'Golf Bay 1'] * 3,
        'Customer': ['Elite Soccer Club', 'Basketball League', 'Golf Lessons'] * 3,
        'Start': pd.date_range(start=start_date, periods=9, freq='3H'),
        'Duration': [2, 1.5, 1, 2, 2, 1, 1.5, 2, 1],
        'Type': ['Regular', 'Youth', 'Corporate'] * 3,
        'Status': ['Confirmed'] * 9
    }
    
    df = pd.DataFrame(data)
    df['End'] = df['Start'] + pd.to_timedelta(df['Duration'], unit='h')
    
    return df[df['Asset'].isin(assets)]

def create_schedule_gantt(df: pd.DataFrame):
    """Create Gantt chart for schedule"""
    fig = go.Figure()
    
    colors = {
        'Regular': '#3b82f6',
        'Youth': '#10b981',
        'Corporate': '#f59e0b',
        'Tournament': '#8b5cf6'
    }
    
    for _, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row['Duration']],
            y=[row['Asset']],
            base=row['Start'].hour + row['Start'].minute/60,
            orientation='h',
            name=row['Customer'],
            marker_color=colors.get(row['Type'], '#6b7280'),
            text=row['Customer'],
            textposition='inside',
            hovertemplate=f"<b>{row['Customer']}</b><br>" +
                         f"Asset: {row['Asset']}<br>" +
                         f"Time: {row['Start'].strftime('%I:%M %p')} - {row['End'].strftime('%I:%M %p')}<br>" +
                         f"Duration: {row['Duration']}h<br>" +
                         f"Type: {row['Type']}<extra></extra>"
        ))
    
    fig.update_layout(
        barmode='overlay',
        height=400,
        xaxis_title="Hour of Day",
        yaxis_title="Asset",
        showlegend=False,
        xaxis=dict(range=[6, 23])
    )
    
    return fig

def get_pending_requests() -> pd.DataFrame:
    """Get pending booking requests"""
    data = {
        'ID': ['REQ001', 'REQ002', 'REQ003', 'REQ004'],
        'Customer': ['Youth Soccer League', 'Corporate Team Building', 'Elite Basketball', 'Golf Tournament'],
        'Asset Type': ['Turf - Full', 'Court', 'Court', 'Golf Bay'],
        'Preferred Date': ['2025-10-25', '2025-10-26', '2025-10-25', '2025-10-27'],
        'Duration': [2, 3, 1.5, 4],
        'Type': ['Youth', 'Corporate', 'Regular', 'Tournament'],
        'Budget': [180, 350, 120, 450],
        'Priority': [3, 0, 1, 2]
    }
    
    return pd.DataFrame(data)

def run_optimization(requests, goal, fairness, horizon):
    """Run scheduling optimization"""
    # Simplified optimization simulation
    scheduled_count = len(requests)
    estimated_revenue = requests['Budget'].sum() * 1.15  # 15% uplift
    util_increase = 4.8
    
    # Create optimized schedule
    schedule = requests.copy()
    schedule['Assigned Date'] = schedule['Preferred Date']
    schedule['Assigned Time'] = ['17:00', '14:00', '19:00', '10:00']
    schedule['Status'] = 'Optimized'
    
    return {
        'scheduled': scheduled_count,
        'revenue': estimated_revenue,
        'util_increase': util_increase,
        'schedule': schedule
    }

def create_booking(context, booking_data):
    """Create new booking"""
    # In production, insert into database
    pass

def accept_optimized_schedule(context, schedule):
    """Accept and apply optimized schedule"""
    # In production, batch insert into database
    context['audit_log']('schedule_optimized', {
        'bookings_count': len(schedule),
        'optimization_method': 'ai'
    })

def load_constraints() -> Dict:
    """Load scheduling constraints"""
    # In production, load from database/config
    return {}

def save_constraints(constraints: Dict):
    """Save scheduling constraints"""
    # In production, save to database/config
    pass

def create_hourly_utilization_chart():
    """Create hourly utilization chart"""
    hours = list(range(6, 23))
    utilization = [45, 52, 68, 75, 82, 88, 92, 95, 97, 96, 93, 90, 85, 78, 72, 68, 55]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours,
        y=utilization,
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        height=300,
        xaxis_title="Hour of Day",
        yaxis_title="Utilization (%)",
        yaxis_range=[0, 100],
        hovermode='x unified'
    )
    
    return fig
