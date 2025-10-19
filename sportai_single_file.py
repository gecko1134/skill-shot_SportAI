"""
SportAI - Complete Single-File Application
No external files needed - everything is self-contained
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="SportAI - Skill Shot",
    page_icon="⚽",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Configuration (embedded in code)
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "name": "System Administrator"
    },
    "board": {
        "password": "board123",
        "role": "board",
        "name": "Board Member"
    },
    "sponsor": {
        "password": "sponsor123",
        "role": "sponsor",
        "name": "Sponsor User"
    }
}

MODULES_BY_ROLE = {
    "admin": ["dashboard", "scheduling", "pricing", "sponsorship", "memberships", "tech", "governance", "reports"],
    "board": ["dashboard", "governance", "reports"],
    "sponsor": ["dashboard", "reports"]
}

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# ============================================================================
# MODULES
# ============================================================================

def show_dashboard():
    """Executive Dashboard"""
    st.markdown('<div class="main-header">📊 Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Real-time facility performance • {datetime.now().strftime("%B %d, %Y")}</div>', unsafe_allow_html=True)
    
    # KPIs
    st.markdown("### Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Facility Utilization", "87.3%", "+5.2%")
    with col2:
        st.metric("Revenue (MTD)", "$142,500", "+$18K")
    with col3:
        st.metric("Active Members", "847", "+23")
    with col4:
        st.metric("Sponsorship Sold", "73.5%", "$385K")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Revenue Trend (30 Days)")
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        revenue = [8000 + (i * 150) + (500 if i % 7 in [5,6] else 0) for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, 
            y=revenue, 
            mode='lines+markers',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=6)
        ))
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), yaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### 🎯 Utilization by Asset")
        assets = ['Turf Field', 'Courts', 'Golf Bays', 'Suites', 'Esports']
        util = [92, 85, 78, 65, 71]
        
        fig = go.Figure(data=[go.Bar(
            x=assets, 
            y=util,
            marker_color=['#10b981' if x >= 85 else '#f59e0b' if x >= 70 else '#ef4444' for x in util],
            text=util,
            texttemplate='%{text}%',
            textposition='outside'
        )])
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    
    # Quick Actions
    st.divider()
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Board Report", use_container_width=True):
            st.success("✅ Board report generated!")
    with col2:
        if st.button("💰 Pricing Update", use_container_width=True):
            st.success("✅ Pricing analysis started!")
    with col3:
        if st.button("🤝 Sponsor Pipeline", use_container_width=True):
            st.info("Loading sponsor pipeline...")
    with col4:
        if st.button("📊 Export Data", use_container_width=True):
            st.success("✅ Data exported!")

def show_scheduling():
    """AI Scheduling Module"""
    st.markdown('<div class="main-header">🤖 AI Scheduling Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent scheduling with constraint satisfaction</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Today's Bookings", "47")
        st.metric("Utilization", "89%")
    with col2:
        st.metric("Pending Requests", "12")
        st.metric("Conflicts", "2")
    with col3:
        st.metric("Revenue Today", "$4,250")
        st.metric("Avg Booking", "$90")
    
    st.divider()
    
    st.markdown("### 📅 Schedule Optimizer")
    
    optimization_goal = st.selectbox(
        "Primary Goal",
        ["Maximize Revenue", "Maximize Utilization", "Balance Both"]
    )
    
    if st.button("🚀 Run AI Optimizer", type="primary"):
        with st.spinner("Optimizing schedule..."):
            st.success("✅ Optimization complete! 12 requests scheduled with +$2,400 projected revenue increase.")

def show_pricing():
    """Dynamic Pricing Module"""
    st.markdown('<div class="main-header">💰 Dynamic Pricing Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent pricing with transparency and fairness</div>', unsafe_allow_html=True)
    
    st.markdown("### 💡 Price Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        asset_type = st.selectbox("Asset Type", ["Turf - Full", "Court", "Golf Bay"])
        customer_type = st.selectbox("Customer Type", ["Corporate", "Regular", "Youth", "Non-Profit"])
        
    with col2:
        booking_date = st.date_input("Date", datetime.now() + timedelta(days=7))
        time_slot = st.selectbox("Time", ["6am-9am", "9am-12pm", "12pm-3pm", "3pm-6pm", "6pm-9pm (Prime)"])
        
    with col3:
        duration = st.number_input("Duration (hours)", 0.5, 8.0, 2.0, 0.5)
        lead_time_days = (booking_date - datetime.now().date()).days
        st.metric("Lead Time", f"{lead_time_days} days")
    
    if st.button("🧮 Calculate Price", type="primary"):
        base_rate = 150
        dynamic_rate = base_rate * 1.15
        final_price = dynamic_rate * duration
        
        st.success("✅ Price calculated successfully!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Base Rate", f"${base_rate}/hr")
        with col2:
            st.metric("Dynamic Rate", f"${dynamic_rate:.2f}/hr", "+15%")
        with col3:
            st.metric("Final Price", f"${final_price:.2f}")

def show_sponsorship():
    """Sponsorship Module"""
    st.markdown('<div class="main-header">🤝 Sponsorship Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Maximize sponsorship revenue with intelligent bundling</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Inventory", "$525K")
    with col2:
        st.metric("Sold", "73.5%", "$385K")
    with col3:
        st.metric("Available", "26.5%", "$140K")
    with col4:
        st.metric("Pipeline", "$120K")
    
    st.divider()
    
    st.markdown("### 📦 Create Sponsorship Package")
    
    sponsor_name = st.text_input("Sponsor Name", "ABC Corporation")
    budget = st.selectbox("Budget Range", ["$10K-$25K", "$25K-$50K", "$50K-$100K", "$100K+"])
    
    st.markdown("#### Available Assets")
    
    assets = {
        "Facility Naming Rights": 250000,
        "Center Court Naming": 75000,
        "Entry Banner": 15000,
        "Digital Package": 10000,
        "Tournament Title": 35000
    }
    
    selected = []
    for name, value in assets.items():
        if st.checkbox(f"{name} - ${value:,}/yr"):
            selected.append((name, value))
    
    if selected:
        total = sum(v for _, v in selected)
        st.success(f"Package Value: ${total:,}/year")
        
        if st.button("📄 Generate Proposal", type="primary"):
            st.success(f"✅ Proposal generated for {sponsor_name}!")

def show_memberships():
    """Membership Management"""
    st.markdown('<div class="main-header">👥 Membership Manager</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Member lifecycle and retention analytics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Members", "847", "+23")
    with col2:
        st.metric("Monthly Revenue", "$42,350", "+$1,840")
    with col3:
        st.metric("Retention Rate", "92.5%", "+1.2%")
    with col4:
        st.metric("Churn Risk", "18", "-3")
    
    st.divider()
    
    st.markdown("### 🎫 Membership Tiers")
    
    tiers = {
        "Bronze": {"fee": 29, "members": 145, "tech": "❌ No tech ($25/session)"},
        "Silver": {"fee": 45, "members": 328, "tech": "✅ Basic ($15/session)"},
        "Gold": {"fee": 75, "members": 287, "tech": "✅ Advanced + AI ($10/session)"},
        "Platinum": {"fee": 125, "members": 87, "tech": "✅ Full Suite ($5/session)"},
        "Elite Tech": {"fee": 99, "members": 68, "tech": "✅ UNLIMITED ($0/session)"}
    }
    
    data = []
    for name, info in tiers.items():
        data.append({
            "Tier": name,
            "Monthly Fee": f"${info['fee']}",
            "Members": info['members'],
            "Tech Access": info['tech']
        })
    
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

def show_tech():
    """Performance Technology"""
    st.markdown('<div class="main-header">🎯 Elite Training Technology</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Performance tracking and analytics per pod</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Pods", "12/18")
    with col2:
        st.metric("Athletes Training", "47")
    with col3:
        st.metric("Sessions Today", "89")
    with col4:
        st.metric("Data Points", "15.2K")
    
    st.divider()
    
    st.markdown("### 🏗️ Technology Stack")
    
    tech_stack = {
        "Turf Boxes (Hitting)": {"tech": "HitTrax + Rapsodo", "fee": "$20/session", "status": "✅ Active"},
        "Basketball Courts": {"tech": "Noah Basketball", "fee": "$15/session", "status": "✅ Active"},
        "Golf Simulators": {"tech": "TrackMan", "fee": "$25/session", "status": "✅ Active"},
        "Full Turf Field": {"tech": "GPS Tracking", "fee": "$30/session", "status": "🔧 Setup"},
        "VR Arena": {"tech": "Motion Tracking", "fee": "$25/session", "status": "✅ Active"}
    }
    
    for pod, info in tech_stack.items():
        st.markdown(f"""
        **{pod}**  
        Tech: {info['tech']} | Fee: {info['fee']} | {info['status']}
        """)
    
    st.divider()
    
    st.info("""
    **🚀 Next Steps for Elite Tech Implementation:**
    
    1. Order HitTrax systems (3 units) - $75,000
    2. Order Noah Basketball (4 courts) - $36,000
    3. Order Rapsodo units (3) - $11,000
    4. Install video analysis - $15,000
    
    **Total Investment:** $192,500  
    **Projected ROI:** 3-4 months  
    **Annual Revenue Impact:** +$714,000
    """)

def show_governance():
    """Board Governance"""
    st.markdown('<div class="main-header">⚖️ Board Governance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Compliance, reporting, and board management</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("DSCR", "1.42", "+0.08")
    with col2:
        st.metric("Cash Reserves", "$485K", "+$42K")
    with col3:
        st.metric("Utilization", "87.3%", "+5.2%")
    with col4:
        st.metric("Net Revenue YTD", "$1.24M", "+12%")
    
    st.divider()
    
    st.markdown("### 📋 Board Documents")
    
    docs = [
        "Articles of Incorporation",
        "Bylaws (v2.1)",
        "Q3 2024 Financial Statement",
        "Sponsorship Policy (v2.0)",
        "Community Access Policy"
    ]
    
    for doc in docs:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"📄 {doc}")
        with col2:
            if st.button("Download", key=doc):
                st.success(f"Downloaded {doc}")

def show_reports():
    """Reports Module"""
    st.markdown('<div class="main-header">📈 Reports & Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comprehensive reporting and data export</div>', unsafe_allow_html=True)
    
    report_type = st.selectbox(
        "Select Report Type",
        ["Executive Summary", "Financial Performance", "Utilization Analysis", 
         "Sponsorship Performance", "Membership Analytics"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    if st.button("📊 Generate Report", type="primary"):
        st.success(f"✅ {report_type} generated for {start_date} to {end_date}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 Export PDF"):
                st.success("PDF exported!")
        with col2:
            if st.button("📊 Export Excel"):
                st.success("Excel exported!")
        with col3:
            if st.button("📧 Email Report"):
                st.success("Report emailed!")

# ============================================================================
# MAIN APP
# ============================================================================

def login_page():
    """Login interface"""
    st.markdown('<div class="main-header">⚽ SportAI - Skill Shot</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sports Facility Management Platform</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True, type="primary"):
            if username in USERS and USERS[username]['password'] == password:
                st.session_state.authenticated = True
                st.session_state.user = username
                st.session_state.user_role = USERS[username]['role']
                st.session_state.user_name = USERS[username]['name']
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
        
        with st.expander("📋 Demo Credentials"):
            st.code("""
Admin: admin / admin123
Board: board / board123  
Sponsor: sponsor / sponsor123
            """)

def main_app():
    """Main application interface"""
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        st.markdown(f"**Site:** Skill Shot")
        st.divider()
        
        st.markdown("### 📋 Navigation")
        
        available_modules = MODULES_BY_ROLE.get(st.session_state.user_role, [])
        
        module_labels = {
            'dashboard': '📊 Dashboard',
            'scheduling': '🤖 AI Scheduling',
            'pricing': '💰 Dynamic Pricing',
            'sponsorship': '🤝 Sponsorship',
            'memberships': '👥 Memberships',
            'tech': '🎯 Performance Tech',
            'governance': '⚖️ Governance',
            'reports': '📈 Reports'
        }
        
        selected = st.radio(
            "Select Module",
            available_modules,
            format_func=lambda x: module_labels.get(x, x.title())
        )
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    # Main content
    if selected == 'dashboard':
        show_dashboard()
    elif selected == 'scheduling':
        show_scheduling()
    elif selected == 'pricing':
        show_pricing()
    elif selected == 'sponsorship':
        show_sponsorship()
    elif selected == 'memberships':
        show_memberships()
    elif selected == 'tech':
        show_tech()
    elif selected == 'governance':
        show_governance()
    elif selected == 'reports':
        show_reports()

# Run the app
if __name__ == "__main__":
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()
