"""
SportAI - Minimal Version (Streamlit Only - No Extra Dependencies)
"""

import streamlit as st
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="SportAI - Skill Shot", page_icon="⚽", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;}
    .sub-header {font-size: 1.1rem; color: #6b7280; margin-bottom: 2rem;}
    .metric-box {background: #f9fafb; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #3b82f6;}
    .success-box {background: #d1fae5; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #10b981;}
    .info-box {background: #dbeafe; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #3b82f6;}
</style>
""", unsafe_allow_html=True)

# Users
USERS = {
    "admin": {"password": "admin123", "role": "admin", "name": "System Administrator"},
    "board": {"password": "board123", "role": "board", "name": "Board Member"},
    "sponsor": {"password": "sponsor123", "role": "sponsor", "name": "Sponsor User"}
}

MODULES = {
    "admin": ["dashboard", "scheduling", "pricing", "sponsorship", "memberships", "tech", "governance", "reports"],
    "board": ["dashboard", "governance", "reports"],
    "sponsor": ["dashboard", "reports"]
}

# Session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None

# ============================================================================
# MODULES
# ============================================================================

def show_dashboard():
    st.markdown('<div class="main-header">📊 Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Real-time facility performance • {datetime.now().strftime("%B %d, %Y")}</div>', unsafe_allow_html=True)
    
    st.markdown("### Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Facility Utilization", "87.3%", "+5.2%")
    with col2:
        st.metric("Revenue (MTD)", "$142,500", "+$18,500")
    with col3:
        st.metric("Active Members", "847", "+23")
    with col4:
        st.metric("Sponsorship Sold", "73.5%", "$385,000")
    
    st.divider()
    
    # Revenue trend (using native Streamlit charts)
    st.markdown("### 📈 Revenue Trend (Last 30 Days)")
    import pandas as pd
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    revenue = [8000 + (i * 150) + (500 if i % 7 in [5,6] else 0) for i in range(30)]
    chart_data = pd.DataFrame({'Revenue': revenue}, index=dates)
    st.line_chart(chart_data, height=300)
    
    st.divider()
    
    # Utilization by asset
    st.markdown("### 🎯 Utilization by Asset Type")
    util_data = pd.DataFrame({
        'Utilization %': [92, 85, 78, 65, 71]
    }, index=['Turf Field', 'Courts', 'Golf Bays', 'Suites', 'Esports'])
    st.bar_chart(util_data, height=300)
    
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        optimization_goal = st.selectbox("Primary Goal", 
            ["Maximize Revenue", "Maximize Utilization", "Balance Both"])
        fairness = st.slider("Fairness Weight", 0.0, 1.0, 0.3)
        
    with col2:
        time_horizon = st.selectbox("Time Horizon", 
            ["Next 7 Days", "Next 14 Days", "Next 30 Days"])
        st.write("")
        st.write("")
    
    if st.button("🚀 Run AI Optimizer", type="primary"):
        with st.spinner("Optimizing schedule..."):
            st.markdown("""
            <div class="success-box">
            <strong>✅ Optimization Complete!</strong><br>
            • 12 requests scheduled<br>
            • Projected revenue increase: +$2,400<br>
            • Utilization improvement: +4.8%<br>
            • Zero conflicts detected
            </div>
            """, unsafe_allow_html=True)

def show_pricing():
    st.markdown('<div class="main-header">💰 Dynamic Pricing Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent pricing with transparency and fairness</div>', unsafe_allow_html=True)
    
    st.markdown("### 💡 Price Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        asset = st.selectbox("Asset Type", ["Turf - Full", "Turf - Half", "Court", "Golf Bay", "Suite"])
        customer = st.selectbox("Customer Type", ["Corporate", "Regular", "Youth", "Non-Profit"])
        
    with col2:
        date = st.date_input("Booking Date", datetime.now() + timedelta(days=7))
        time = st.selectbox("Time Slot", ["6am-9am", "9am-12pm", "12pm-3pm", "3pm-6pm", "6pm-9pm (Prime)", "9pm-12am"])
        
    with col3:
        duration = st.number_input("Duration (hours)", 0.5, 8.0, 2.0, 0.5)
        lead_days = (date - datetime.now().date()).days
        st.metric("Lead Time", f"{lead_days} days")
    
    if st.button("🧮 Calculate Price", type="primary"):
        base_rate = 150
        demand_mult = 1.15 if "Prime" in time else 1.0
        customer_mult = {"Youth": 0.80, "Non-Profit": 0.85, "Regular": 1.0, "Corporate": 1.15}[customer]
        lead_discount = 0.95 if lead_days >= 30 else 1.0
        
        dynamic_rate = base_rate * demand_mult * customer_mult * lead_discount
        final_price = dynamic_rate * duration
        
        st.success("✅ Price calculated successfully!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Base Rate", f"${base_rate}/hr")
        with col2:
            st.metric("Dynamic Rate", f"${dynamic_rate:.2f}/hr", f"{((dynamic_rate/base_rate-1)*100):+.1f}%")
        with col3:
            st.metric("Final Price", f"${final_price:.2f}", f"for {duration} hrs")
        
        st.divider()
        
        st.markdown("### 🔍 Pricing Breakdown")
        st.markdown(f"""
        **Base Rate:** ${base_rate}/hr  
        **Time Slot Adjustment:** {'+15%' if 'Prime' in time else 'Standard'}  
        **Customer Type:** {customer} ({int((customer_mult-1)*100):+d}%)  
        **Lead Time Discount:** {lead_days} days ({int((lead_discount-1)*100):d}%)  
        **Final Rate:** ${dynamic_rate:.2f}/hr × {duration} hrs = **${final_price:.2f}**
        """)

def show_sponsorship():
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        sponsor = st.text_input("Sponsor Name", "ABC Corporation")
        budget = st.selectbox("Budget Range", ["$10K-$25K", "$25K-$50K", "$50K-$100K", "$100K-$250K", "$250K+"])
        
    with col2:
        term = st.selectbox("Term Length", ["1 Year", "2 Years", "3 Years"])
        exclusivity = st.checkbox("Category Exclusivity Required")
    
    st.divider()
    
    st.markdown("### 🏷️ Available Assets")
    
    assets = {
        "Facility Naming Rights": 250000,
        "Center Court Naming": 75000,
        "Turf Field Naming": 100000,
        "Entry Banner (20x10ft)": 15000,
        "Dasher Boards (8 panels)": 25000,
        "Digital Package": 10000,
        "Tournament Title Sponsor": 35000,
        "Suite Package": 20000
    }
    
    selected = []
    for name, value in assets.items():
        if st.checkbox(f"**{name}** - ${value:,}/year"):
            selected.append((name, value))
    
    if selected:
        total_annual = sum(v for _, v in selected)
        term_years = int(term.split()[0])
        total_contract = total_annual * term_years
        discount = 0.15 if len(selected) >= 5 else 0.10 if len(selected) >= 3 else 0.0
        final_value = total_contract * (1 - discount)
        
        st.divider()
        
        st.markdown("### 💰 Package Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Assets", len(selected))
        with col2:
            st.metric("Annual Value", f"${total_annual:,}")
        with col3:
            st.metric("Bundle Discount", f"{discount*100:.0f}%")
        with col4:
            st.metric("Total Contract", f"${final_value:,.0f}")
        
        if st.button("📄 Generate Proposal", type="primary"):
            st.markdown(f"""
            <div class="success-box">
            <strong>✅ Proposal Generated for {sponsor}</strong><br><br>
            <strong>Package Details:</strong><br>
            • {len(selected)} assets included<br>
            • {term} contract term<br>
            • ${final_value:,} total value<br>
            • {discount*100:.0f}% bundle discount applied<br><br>
            Proposal ready for review and email delivery.
            </div>
            """, unsafe_allow_html=True)

def show_memberships():
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
    
    st.markdown("### 🎫 Membership Tiers with Elite Tech")
    
    import pandas as pd
    
    tiers = pd.DataFrame({
        "Tier": ["Bronze", "Silver", "Gold", "Platinum", "Elite Tech Add-on", "Elite Tech Standalone", "Team Elite Tech"],
        "Monthly Fee": ["$29", "$45", "$75", "$125", "+$99", "$149", "$499"],
        "Credits": [5, 10, 20, 40, 0, 15, 100],
        "Tech Access": [
            "❌ No ($25/session)",
            "✅ Basic ($15/session)",
            "✅ Advanced + AI ($10/session)",
            "✅ Full Suite ($5/session)",
            "✅ UNLIMITED ($0)",
            "✅ UNLIMITED ($0)",
            "✅ Team Analytics + UNLIMITED"
        ],
        "Members": [145, 328, 287, 87, 68, 17, 12]
    })
    
    st.dataframe(tiers, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.markdown("### 💡 Elite Tech Revenue Model")
    
    st.markdown("""
    <div class="info-box">
    <strong>Dual Revenue Streams:</strong><br><br>
    <strong>1. Membership Upgrades</strong><br>
    • Bronze → Silver: +$16/month<br>
    • Silver → Gold: +$30/month<br>
    • Gold → Elite Tech: +$99/month<br><br>
    <strong>2. Per-Session Tech Fees</strong><br>
    • Hitting/Pitching: $20/session (non-Elite Tech members)<br>
    • Basketball: $15/session<br>
    • Golf: $25/session<br>
    • Projected: 850 sessions/month = $10,200/month
    </div>
    """, unsafe_allow_html=True)

def show_tech():
    st.markdown('<div class="main-header">🎯 Elite Training Technology</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Performance tracking and analytics per pod</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Pods", "12/18", "8 available")
    with col2:
        st.metric("Athletes Training", "47")
    with col3:
        st.metric("Sessions Today", "89")
    with col4:
        st.metric("Data Points", "15.2K")
    
    st.divider()
    
    st.markdown("### 🏗️ Technology Stack by Pod")
    
    tech = [
        {"Pod": "Turf Boxes 1-3 (Hitting)", "Tech": "HitTrax + Rapsodo", "Session Fee": "$20", "Status": "🔧 Installation Pending"},
        {"Pod": "Turf Boxes 4-6 (Pitching)", "Tech": "Rapsodo Pitching", "Session Fee": "$20", "Status": "🔧 Installation Pending"},
        {"Pod": "Basketball Courts 1-4", "Tech": "Noah Basketball", "Session Fee": "$15", "Status": "🔧 Installation Pending"},
        {"Pod": "Golf Simulators 1-3", "Tech": "TrackMan (Installed)", "Session Fee": "$25", "Status": "✅ Active"},
        {"Pod": "Full Turf Field", "Tech": "GPS Tracking", "Session Fee": "$30", "Status": "📦 Equipment Ordered"},
        {"Pod": "VR Arena", "Tech": "Motion Tracking", "Session Fee": "$25", "Status": "✅ Active"}
    ]
    
    import pandas as pd
    st.dataframe(pd.DataFrame(tech), use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.markdown("### 💰 Investment & ROI Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Equipment Investment:**
        - HitTrax Systems (3): $75,000
        - Rapsodo Units (3): $11,100
        - Noah Basketball (4): $36,000
        - Veo Cameras (8): $15,000
        - GPS Tracking: $20,000
        - Infrastructure: $40,000
        
        **Total: $197,100**
        """)
        
    with col2:
        st.markdown("""
        **Projected Revenue:**
        - Month 1-3: $48,000/mo
        - Month 4-6: $60,000/mo
        - Month 7-12: $65,000/mo
        
        **Payback: 3-4 months**
        **Year 1 Revenue: $714,000**
        """)
    
    st.divider()
    
    st.markdown("### 📞 Next Steps")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 View Vendor Contacts", use_container_width=True):
            st.info("Opening vendor contact list...")
    with col2:
        if st.button("📦 Order Equipment", use_container_width=True):
            st.info("Opening equipment order forms...")
    with col3:
        if st.button("📅 Schedule Install", use_container_width=True):
            st.info("Opening installation calendar...")

def show_governance():
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
        ("Articles of Incorporation", "2023-01-15", "v1.2"),
        ("Bylaws", "2024-06-20", "v2.1"),
        ("Q3 2024 Financial Statement", "2024-10-05", "v1.0"),
        ("Sponsorship Policy", "2024-05-12", "v2.0"),
        ("Community Access Policy", "2024-03-15", "v1.0")
    ]
    
    for doc, date, version in docs:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"📄 **{doc}**")
        with col2:
            st.write(f"_{version}_")
        with col3:
            if st.button("Download", key=doc):
                st.success(f"Downloaded {doc}")
    
    st.divider()
    
    st.markdown("### 📅 Upcoming Board Meetings")
    
    st.markdown("""
    **Oct 28, 2025 - 6:00 PM**  
    Regular Board Meeting • Skill Shot Conference Room  
    Agenda: Q4 Projections, Tech Implementation Update
    
    **Nov 15, 2025 - 12:00 PM**  
    Finance Committee • Virtual - Zoom  
    Agenda: Budget Review, Capital Projects
    """)

def show_reports():
    st.markdown('<div class="main-header">📈 Reports & Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comprehensive reporting and data export</div>', unsafe_allow_html=True)
    
    report = st.selectbox("Select Report Type", [
        "Executive Summary",
        "Financial Performance",
        "Utilization Analysis",
        "Revenue Breakdown",
        "Sponsorship Performance",
        "Membership Analytics"
    ])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        start = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end = st.date_input("End Date", datetime.now())
    with col3:
        format = st.selectbox("Format", ["PDF", "Excel", "CSV"])
    
    if st.button("📊 Generate Report", type="primary"):
        st.markdown(f"""
        <div class="success-box">
        <strong>✅ {report} Generated Successfully!</strong><br><br>
        Period: {start.strftime("%B %d, %Y")} - {end.strftime("%B %d, %Y")}<br>
        Format: {format}<br><br>
        Report is ready for download.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 Download", use_container_width=True):
                st.success("Downloaded!")
        with col2:
            if st.button("📧 Email", use_container_width=True):
                st.success("Emailed!")
        with col3:
            if st.button("📤 Share", use_container_width=True):
                st.success("Shared!")

# ============================================================================
# MAIN
# ============================================================================

def login_page():
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
            st.code("Admin: admin / admin123\nBoard: board / board123\nSponsor: sponsor / sponsor123")

def main_app():
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        st.divider()
        
        st.markdown("### 📋 Navigation")
        
        labels = {
            'dashboard': '📊 Dashboard',
            'scheduling': '🤖 AI Scheduling',
            'pricing': '💰 Dynamic Pricing',
            'sponsorship': '🤝 Sponsorship',
            'memberships': '👥 Memberships',
            'tech': '🎯 Performance Tech',
            'governance': '⚖️ Governance',
            'reports': '📈 Reports'
        }
        
        selected = st.radio("Select Module", 
            MODULES.get(st.session_state.user_role, []),
            format_func=lambda x: labels.get(x, x.title()))
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Route to module
    {
        'dashboard': show_dashboard,
        'scheduling': show_scheduling,
        'pricing': show_pricing,
        'sponsorship': show_sponsorship,
        'memberships': show_memberships,
        'tech': show_tech,
        'governance': show_governance,
        'reports': show_reports
    }[selected]()

# Run
if not st.session_state.authenticated:
    login_page()
else:
    main_app()
