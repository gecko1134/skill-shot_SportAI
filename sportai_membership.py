"""
SportAI Membership Manager Module
Member management, retention, credits, and analytics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, Any, List

def run(context: Dict[str, Any]):
    """Main membership manager execution"""
    
    st.markdown('<div class="main-header">👥 Membership Manager</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Member lifecycle, retention, and credits management</div>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "👤 Members",
        "🎫 Tiers & Credits",
        "📈 Retention",
        "💳 Billing"
    ])
    
    with tab1:
        show_membership_overview(context)
        
    with tab2:
        show_member_directory(context)
        
    with tab3:
        show_tiers_and_credits(context)
        
    with tab4:
        show_retention_analytics(context)
        
    with tab5:
        show_billing_management(context)

def show_membership_overview(context: Dict[str, Any]):
    """Membership overview dashboard"""
    
    st.markdown("### 📊 Membership Metrics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Members", 847, "+23")
        
    with col2:
        st.metric("Monthly Recurring Revenue", "$42,350", "+$1,840")
        
    with col3:
        st.metric("Retention Rate", "92.5%", "+1.2%")
        
    with col4:
        st.metric("Avg Credits Used/Month", 8.4, "+0.7")
    
    st.divider()
    
    # Growth chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Membership Growth (12 Months)")
        fig_growth = create_membership_growth_chart()
        st.plotly_chart(fig_growth, use_container_width=True)
        
    with col2:
        st.markdown("#### 🥧 Members by Tier")
        fig_tiers = create_tier_distribution_chart()
        st.plotly_chart(fig_tiers, use_container_width=True)
    
    # Activity heatmap
    st.divider()
    st.markdown("#### 🔥 Member Activity Heatmap")
    fig_activity = create_activity_heatmap()
    st.plotly_chart(fig_activity, use_container_width=True)
    
    # Recent activity
    st.divider()
    st.markdown("#### 🔔 Recent Activity")
    
    recent_activity = [
        {"Time": "5 min ago", "Event": "New Member", "Details": "Sarah Johnson joined Gold tier"},
        {"Time": "12 min ago", "Event": "Credit Purchase", "Details": "Mike Chen purchased 20 credits ($180)"},
        {"Time": "25 min ago", "Event": "Tier Upgrade", "Details": "Elite FC upgraded from Silver to Platinum"},
        {"Time": "1 hour ago", "Event": "Auto-Renewal", "Details": "15 memberships auto-renewed for November"},
    ]
    
    for activity in recent_activity:
        st.markdown(f"""
        <div style="background: #f9fafb; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 3px solid #3b82f6;">
        <strong>{activity['Event']}</strong> • {activity['Time']}<br>
        {activity['Details']}
        </div>
        """, unsafe_allow_html=True)

def show_member_directory(context: Dict[str, Any]):
    """Member directory and search"""
    
    st.markdown("### 👤 Member Directory")
    
    # Search and filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_query = st.text_input("🔍 Search Members", placeholder="Name, email, or ID")
        
    with col2:
        tier_filter = st.multiselect(
            "Tier",
            ["Bronze", "Silver", "Gold", "Platinum"],
            default=["Bronze", "Silver", "Gold", "Platinum"]
        )
        
    with col3:
        status_filter = st.selectbox("Status", ["All", "Active", "Inactive", "Suspended"])
        
    with col4:
        sort_by = st.selectbox("Sort By", ["Name", "Join Date", "Credits", "Tier"])
    
    # Member list
    members = get_members_data()
    
    # Apply filters
    if search_query:
        members = members[
            members['Name'].str.contains(search_query, case=False, na=False) |
            members['Email'].str.contains(search_query, case=False, na=False)
        ]
    
    members = members[members['Tier'].isin(tier_filter)]
    
    if status_filter != "All":
        members = members[members['Status'] == status_filter]
    
    st.dataframe(
        members,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Credits": st.column_config.ProgressColumn(
                "Credits",
                format="%d",
                min_value=0,
                max_value=50
            )
        }
    )
    
    # Quick actions
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add New Member", use_container_width=True):
            show_add_member_form(context)
            
    with col2:
        if st.button("📧 Send Newsletter", use_container_width=True):
            st.success("Newsletter sent to all active members")
            context['audit_log']('newsletter_sent', {'count': len(members)})
            
    with col3:
        if st.button("📊 Export List", use_container_width=True):
            st.success("Member list exported to Excel")
            
    with col4:
        if st.button("💳 Billing Run", use_container_width=True):
            st.info("Starting monthly billing cycle...")

def show_add_member_form(context: Dict[str, Any]):
    """Add new member form"""
    
    with st.form("add_member_form"):
        st.markdown("### ➕ Add New Member")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            phone = st.text_input("Phone")
            
        with col2:
            tier = st.selectbox("Membership Tier", ["Bronze", "Silver", "Gold", "Platinum"])
            initial_credits = st.number_input("Initial Credits", min_value=0, value=10)
            household = st.text_input("Household ID (optional)")
        
        notes = st.text_area("Notes")
        
        submitted = st.form_submit_button("💾 Create Member", type="primary")
        
        if submitted:
            if name and email:
                st.success(f"✅ Member '{name}' created successfully!")
                context['audit_log']('member_created', {'name': name, 'tier': tier})
            else:
                st.error("Name and email are required")

def show_tiers_and_credits(context: Dict[str, Any]):
    """Tier management and credit pricing"""
    
    st.markdown("### 🎫 Membership Tiers")
    
    tiers = get_membership_tiers()
    
    # Tier comparison table
    tier_comparison = []
    
    for tier_name, tier_data in tiers.items():
        tier_comparison.append({
            'Tier': tier_name,
            'Monthly Fee': f"${tier_data['monthly_fee']}",
            'Credits Included': tier_data['credits_included'],
            'Discount': f"{tier_data['booking_discount']*100:.0f}%",
            'Priority Booking': '✓' if tier_data['priority_booking'] else '—',
            'Suite Access': '✓' if tier_data['suite_access'] else '—',
            'Active Members': tier_data['member_count']
        })
    
    st.dataframe(pd.DataFrame(tier_comparison), use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Edit tier configuration
    st.markdown("#### ⚙️ Configure Tiers")
    
    selected_tier = st.selectbox("Select Tier to Edit", list(tiers.keys()))
    
    tier_config = tiers[selected_tier]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        monthly_fee = st.number_input(
            "Monthly Fee ($)",
            min_value=0,
            value=tier_config['monthly_fee']
        )
        
        credits_included = st.number_input(
            "Credits Included",
            min_value=0,
            value=tier_config['credits_included']
        )
        
    with col2:
        booking_discount = st.slider(
            "Booking Discount (%)",
            0, 30,
            int(tier_config['booking_discount'] * 100)
        )
        
        credit_rollover = st.number_input(
            "Max Credit Rollover",
            min_value=0,
            value=tier_config.get('max_rollover', 10)
        )
        
    with col3:
        priority_booking = st.checkbox(
            "Priority Booking",
            value=tier_config['priority_booking']
        )
        
        suite_access = st.checkbox(
            "Suite Access",
            value=tier_config['suite_access']
        )
        
        guest_passes = st.number_input(
            "Monthly Guest Passes",
            min_value=0,
            value=tier_config.get('guest_passes', 0)
        )
    
    if st.button("💾 Save Tier Configuration"):
        st.success(f"✅ {selected_tier} tier updated successfully!")
        context['audit_log']('tier_updated', {'tier': selected_tier})
    
    # Credit pricing
    st.divider()
    st.markdown("#### 💰 Credit Pricing (À La Carte)")
    
    credit_packages = [
        {"Credits": 5, "Price": 55, "Per Credit": 11.00, "Discount": "0%"},
        {"Credits": 10, "Price": 100, "Per Credit": 10.00, "Discount": "9%"},
        {"Credits": 20, "Price": 180, "Per Credit": 9.00, "Discount": "18%"},
        {"Credits": 50, "Price": 400, "Per Credit": 8.00, "Discount": "27%"},
    ]
    
    st.dataframe(pd.DataFrame(credit_packages), use_container_width=True, hide_index=True)

def show_retention_analytics(context: Dict[str, Any]):
    """Retention analytics and insights"""
    
    st.markdown("### 📈 Retention Analytics")
    
    # Retention metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("30-Day Retention", "94.2%", "+1.5%")
        
    with col2:
        st.metric("90-Day Retention", "88.7%", "+2.1%")
        
    with col3:
        st.metric("12-Month Retention", "76.3%", "+0.8%")
        
    with col4:
        st.metric("Avg Member LTV", "$2,847", "+$142")
    
    st.divider()
    
    # Cohort analysis
    st.markdown("#### 📊 Cohort Retention Analysis")
    
    fig_cohort = create_cohort_retention_chart()
    st.plotly_chart(fig_cohort, use_container_width=True)
    
    # Churn risk analysis
    st.divider()
    st.markdown("#### ⚠️ Churn Risk Analysis")
    
    churn_risks = [
        {"Member": "John Smith", "Tier": "Gold", "Risk Score": 85, "Reason": "Low usage (2 bookings in 90 days)", "Last Visit": "45 days ago"},
        {"Member": "Elite FC", "Tier": "Platinum", "Risk Score": 72, "Reason": "Credits unused (18 remaining)", "Last Visit": "12 days ago"},
        {"Member": "Sarah Lee", "Tier": "Silver", "Risk Score": 68, "Reason": "Payment failed", "Last Visit": "3 days ago"},
    ]
    
    df_risk = pd.DataFrame(churn_risks)
    
    st.dataframe(
        df_risk,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Risk Score": st.column_config.ProgressColumn(
                "Risk Score",
                format="%d",
                min_value=0,
                max_value=100
            )
        }
    )
    
    # Win-back campaigns
    st.divider()
    st.markdown("#### 🎯 Win-Back Campaigns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Inactive Members (60+ days)**")
        st.metric("Count", 24)
        if st.button("📧 Send Win-Back Offer", key="winback1"):
            st.success("Win-back email sent with 20% discount")
            
    with col2:
        st.markdown("**Downgraded Members**")
        st.metric("Count", 8)
        if st.button("📧 Send Upgrade Incentive", key="winback2"):
            st.success("Upgrade offer sent with bonus credits")

def show_billing_management(context: Dict[str, Any]):
    """Billing and payment management"""
    
    st.markdown("### 💳 Billing Management")
    
    # Billing summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Revenue", "$42,350")
        
    with col2:
        st.metric("Outstanding", "$1,250", "3 accounts")
        
    with col3:
        st.metric("Failed Payments", 5)
        
    with col4:
        st.metric("Next Billing Cycle", "Nov 1")
    
    st.divider()
    
    # Upcoming charges
    st.markdown("#### 📅 Upcoming Charges (Next 7 Days)")
    
    upcoming_charges = [
        {"Date": "2025-10-20", "Member": "Sarah Johnson", "Tier": "Gold", "Amount": 75, "Status": "Scheduled"},
        {"Date": "2025-10-22", "Member": "Elite FC", "Tier": "Platinum", "Amount": 125, "Status": "Scheduled"},
        {"Date": "2025-10-23", "Member": "Mike Chen", "Tier": "Silver", "Amount": 45, "Status": "Scheduled"},
        {"Date": "2025-10-25", "Member": "Basketball Club", "Tier": "Gold", "Amount": 75, "Status": "Retry"},
    ]
    
    st.dataframe(pd.DataFrame(upcoming_charges), use_container_width=True, hide_index=True)
    
    # Failed payments
    st.divider()
    st.markdown("#### ⚠️ Failed Payments - Action Required")
    
    failed_payments = [
        {"Member": "John Doe", "Amount": 45, "Attempts": 2, "Last Try": "2025-10-15", "Action": "Update card"},
        {"Member": "XYZ Corp", "Amount": 125, "Attempts": 1, "Last Try": "2025-10-17", "Action": "Contact"},
    ]
    
    df_failed = pd.DataFrame(failed_payments)
    st.dataframe(df_failed, use_container_width=True, hide_index=True)
    
    if st.button("📧 Send Payment Reminder to All"):
        st.success("Payment reminders sent to 5 members")
        context['audit_log']('payment_reminders_sent', {'count': 5})
    
    # Billing actions
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Run Billing Cycle", type="primary", use_container_width=True):
            st.info("Processing billing for all active members...")
            
    with col2:
        if st.button("📊 Generate Revenue Report", use_container_width=True):
            st.success("Revenue report generated")
            
    with col3:
        if st.button("💾 Export Transactions", use_container_width=True):
            st.success("Transaction export complete")

# Helper functions

def get_members_data() -> pd.DataFrame:
    """Get member directory data"""
    return pd.DataFrame([
        {"ID": "M001", "Name": "Sarah Johnson", "Email": "sarah.j@email.com", 
         "Tier": "Gold", "Credits": 12, "Join Date": "2024-03-15", "Status": "Active"},
        {"ID": "M002", "Name": "Elite Soccer FC", "Email": "contact@elitefc.com", 
         "Tier": "Platinum", "Credits": 25, "Join Date": "2023-09-01", "Status": "Active"},
        {"ID": "M003", "Name": "Mike Chen", "Email": "mike.c@email.com", 
         "Tier": "Silver", "Credits": 8, "Join Date": "2024-06-20", "Status": "Active"},
        {"ID": "M004", "Name": "Basketball League", "Email": "info@bball.org", 
         "Tier": "Gold", "Credits": 15, "Join Date": "2024-01-10", "Status": "Active"},
        {"ID": "M005", "Name": "Corporate Team", "Email": "team@corp.com", 
         "Tier": "Bronze", "Credits": 5, "Join Date": "2024-08-05", "Status": "Active"},
    ])

def get_membership_tiers() -> Dict:
    """Get membership tier configurations"""
    return {
        'Bronze': {
            'monthly_fee': 29,
            'credits_included': 5,
            'booking_discount': 0.05,
            'priority_booking': False,
            'suite_access': False,
            'max_rollover': 5,
            'guest_passes': 0,
            'member_count': 145
        },
        'Silver': {
            'monthly_fee': 45,
            'credits_included': 10,
            'booking_discount': 0.10,
            'priority_booking': False,
            'suite_access': False,
            'max_rollover': 10,
            'guest_passes': 2,
            'member_count': 328
        },
        'Gold': {
            'monthly_fee': 75,
            'credits_included': 20,
            'booking_discount': 0.15,
            'priority_booking': True,
            'suite_access': True,
            'max_rollover': 20,
            'guest_passes': 4,
            'member_count': 287
        },
        'Platinum': {
            'monthly_fee': 125,
            'credits_included': 40,
            'booking_discount': 0.20,
            'priority_booking': True,
            'suite_access': True,
            'max_rollover': 40,
            'guest_passes': 8,
            'member_count': 87
        }
    }

def create_membership_growth_chart():
    """Create membership growth chart"""
    months = pd.date_range(start='2024-01-01', periods=12, freq='M')
    members = [645, 658, 672, 695, 718, 742, 765, 788, 808, 825, 837, 847]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=members,
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_title="Month",
        yaxis_title="Total Members",
        hovermode='x unified'
    )
    
    return fig

def create_tier_distribution_chart():
    """Create tier distribution pie chart"""
    tiers = get_membership_tiers()
    
    data = {
        'Tier': list(tiers.keys()),
        'Count': [t['member_count'] for t in tiers.values()]
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=data['Tier'],
        values=data['Count'],
        hole=0.4,
        marker_colors=['#cd7f32', '#c0c0c0', '#ffd700', '#e5e4e2']
    )])
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True
    )
    
    return fig

def create_activity_heatmap():
    """Create member activity heatmap"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = ['6am', '9am', '12pm', '3pm', '6pm', '9pm']
    
    # Sample activity data
    data = [
        [12, 18, 24, 28, 35, 22],  # Mon
        [15, 22, 26, 32, 38, 25],  # Tue
        [14, 20, 25, 30, 36, 24],  # Wed
        [16, 24, 28, 34, 40, 28],  # Thu
        [18, 26, 30, 36, 42, 32],  # Fri
        [35, 45, 52, 48, 55, 38],  # Sat
        [32, 42, 48, 45, 50, 35],  # Sun
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=hours,
        y=days,
        colorscale='Blues',
        text=data,
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Visits")
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_title="Time of Day",
        yaxis_title="Day of Week"
    )
    
    return fig

def create_cohort_retention_chart():
    """Create cohort retention chart"""
    cohorts = ['Jan 24', 'Feb 24', 'Mar 24', 'Apr 24', 'May 24', 'Jun 24']
    months = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5']
    
    # Sample retention data (percentages)
    data = [
        [100, 95, 92, 88, 85, 82],
        [100, 96, 93, 90, 87, None],
        [100, 97, 94, 91, None, None],
        [100, 96, 93, None, None, None],
        [100, 98, None, None, None, None],
        [100, None, None, None, None, None],
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=months,
        y=cohorts,
        colorscale='RdYlGn',
        text=data,
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Retention %")
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis_title="Months Since Join",
        yaxis_title="Join Cohort"
    )
    
    return fig
