#!/usr/bin/env python3
"""
SportAI Automated Setup Script
Creates all necessary files and directories for SportAI
"""

import os
import json
from pathlib import Path

def create_directory_structure():
    """Create all required directories"""
    directories = [
        'modules',
        'utils',
        'config',
        'data',
        'tests',
        '.streamlit'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {directory}/")
    
    # Create __init__.py files
    for directory in ['modules', 'utils']:
        init_file = Path(directory) / '__init__.py'
        init_file.write_text("")
        print(f"✓ Created {directory}/__init__.py")

def create_config_files():
    """Create all configuration files"""
    
    # users.json
    users_config = {
        "admin": {
            "password": "admin123",
            "role": "admin",
            "name": "System Administrator",
            "email": "admin@skillshot.com"
        },
        "board_member": {
            "password": "board123",
            "role": "board",
            "name": "Board Member",
            "email": "board@skillshot.com"
        },
        "sponsor": {
            "password": "sponsor123",
            "role": "sponsor",
            "name": "Sponsor User",
            "email": "sponsor@skillshot.com"
        }
    }
    
    with open('config/users.json', 'w') as f:
        json.dump(users_config, f, indent=2)
    print("✓ Created config/users.json")
    
    # modules.json
    modules_config = {
        "admin": ["dashboard", "ai_scheduling", "dynamic_pricing", "sponsorship_optimizer", 
                  "membership_manager", "performance_tech", "board_governance", "reports"],
        "board": ["dashboard", "board_governance", "reports"],
        "sponsor": ["dashboard", "reports"],
        "member": ["dashboard"]
    }
    
    with open('config/modules.json', 'w') as f:
        json.dump(modules_config, f, indent=2)
    print("✓ Created config/modules.json")
    
    # pricing_rules.json
    pricing_config = {
        "base_rates": {
            "turf_full": {"prime": 275, "standard": 200, "off_peak": 150},
            "court": {"prime": 45, "standard": 35, "off_peak": 25},
            "golf_bay": {"prime": 55, "standard": 45, "off_peak": 35}
        }
    }
    
    with open('config/pricing_rules.json', 'w') as f:
        json.dump(pricing_config, f, indent=2)
    print("✓ Created config/pricing_rules.json")
    
    # guardrails.json
    guardrails_config = {
        "max_surge_factor": 1.5,
        "min_community_hours_weekly": 20,
        "youth_discount_floor": 0.70,
        "max_price_change_percent": 25
    }
    
    with open('config/guardrails.json', 'w') as f:
        json.dump(guardrails_config, f, indent=2)
    print("✓ Created config/guardrails.json")

def create_streamlit_config():
    """Create Streamlit configuration"""
    config = """[server]
headless = true
port = 8501

[theme]
primaryColor = "#3b82f6"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f9fafb"
textColor = "#1f2937"
"""
    
    with open('.streamlit/config.toml', 'w') as f:
        f.write(config)
    print("✓ Created .streamlit/config.toml")

def create_requirements():
    """Create requirements.txt"""
    requirements = """streamlit==1.28.0
pandas==2.1.1
plotly==5.17.0
python-dateutil==2.8.2
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✓ Created requirements.txt")

def create_main_app():
    """Create main_app.py"""
    main_app_code = '''"""SportAI - Main Application"""
import streamlit as st
import sys
from pathlib import Path
import json

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(page_title="SportAI - Skill Shot", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main-header { font-size: 2.5rem; font-weight: 700; color: #1f2937; }
.sub-header { font-size: 1.1rem; color: #6b7280; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

class SportAIApp:
    def __init__(self):
        self.initialize_session_state()
        self.load_configs()
        
    def initialize_session_state(self):
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
            
    def load_configs(self):
        config_path = Path(__file__).parent / 'config'
        
        for key in ['users', 'modules']:
            file_path = config_path / f'{key}.json'
            if file_path.exists():
                with open(file_path, 'r') as f:
                    st.session_state[f'config_{key}'] = json.load(f)
            else:
                st.session_state[f'config_{key}'] = {}
                
    def login_page(self):
        st.markdown('<div class="main-header">⚽ SportAI - Skill Shot</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Sports Facility Management Platform</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔐 Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", use_container_width=True):
                users = st.session_state.config_users
                if username in users and users[username]['password'] == password:
                    st.session_state.authenticated = True
                    st.session_state.user = username
                    st.session_state.user_role = users[username]['role']
                    st.session_state.user_name = users[username]['name']
                    st.rerun()
                else:
                    st.error("Invalid credentials")
                    
            with st.expander("Demo Credentials"):
                st.code("Admin: admin / admin123\\nBoard: board_member / board123")
                
    def load_module(self, module_name: str):
        try:
            # Import the module
            module_path = f"modules.{module_name}"
            import importlib
            module = importlib.import_module(module_path)
            
            # Create context
            context = {
                'session': st.session_state,
                'user_ctx': {
                    'user': st.session_state.user,
                    'role': st.session_state.user_role
                },
                'audit_log': lambda action, details: None
            }
            
            # Run module
            module.run(context)
            
        except Exception as e:
            st.error(f"Error loading module: {module_name}")
            st.code(str(e))
                
    def main_app(self):
        with st.sidebar:
            st.markdown(f"### 👤 {st.session_state.user_name}")
            st.markdown(f"**Role:** {st.session_state.user_role.title()}")
            st.divider()
            
            st.markdown("### 📋 Navigation")
            available_modules = st.session_state.config_modules.get(st.session_state.user_role, [])
            
            module_labels = {
                'dashboard': '📊 Dashboard',
                'ai_scheduling': '🤖 AI Scheduling',
                'dynamic_pricing': '💰 Dynamic Pricing',
                'sponsorship_optimizer': '🤝 Sponsorship',
                'membership_manager': '👥 Memberships',
                'performance_tech': '🎯 Performance Tech',
                'board_governance': '⚖️ Governance',
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
                
        self.load_module(selected)
        
    def run(self):
        if not st.session_state.authenticated:
            self.login_page()
        else:
            self.main_app()

if __name__ == "__main__":
    app = SportAIApp()
    app.run()
'''
    
    with open('main_app.py', 'w') as f:
        f.write(main_app_code)
    print("✓ Created main_app.py")

def create_dashboard_module():
    """Create working dashboard module"""
    dashboard_code = '''"""Dashboard Module"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def run(context):
    st.markdown('<div class="main-header">📊 Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Real-time facility performance • {datetime.now().strftime("%B %d, %Y")}</div>', unsafe_allow_html=True)
    
    # KPIs
    st.markdown("### Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Facility Utilization", "87.3%", "+5.2%")
    with col2:
        st.metric("Revenue (MTD)", "$142,500", "+12%")
    with col3:
        st.metric("Active Members", 847, "+23")
    with col4:
        st.metric("Sponsorship Sold", "73.5%", "$385K")
    
    st.divider()
    
    # Revenue chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Revenue Trend")
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        revenue = [8000 + (i * 150) for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=revenue, mode='lines+markers', 
                                 line=dict(color='#3b82f6', width=3)))
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### 🎯 Utilization by Asset")
        assets = ['Turf', 'Courts', 'Golf', 'Suites']
        util = [92, 85, 78, 65]
        
        fig = go.Figure(data=[go.Bar(x=assets, y=util, marker_color='#3b82f6')])
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    
    # Quick actions
    st.divider()
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Generate Board Report", use_container_width=True):
            st.success("Board report generated!")
    with col2:
        if st.button("💰 Run Pricing Update", use_container_width=True):
            st.success("Pricing analysis started!")
    with col3:
        if st.button("📊 Export Data", use_container_width=True):
            st.success("Data exported!")
'''
    
    with open('modules/dashboard.py', 'w') as f:
        f.write(dashboard_code)
    print("✓ Created modules/dashboard.py")

def create_placeholder_modules():
    """Create placeholder modules for other features"""
    
    modules_to_create = [
        'ai_scheduling',
        'dynamic_pricing',
        'sponsorship_optimizer',
        'membership_manager',
        'performance_tech',
        'board_governance',
        'reports'
    ]
    
    for module_name in modules_to_create:
        module_code = f'''"""
{module_name.replace('_', ' ').title()} Module
"""
import streamlit as st

def run(context):
    st.markdown(f'<div class="main-header">🎯 {module_name.replace("_", " ").title()}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Advanced features coming soon</div>', unsafe_allow_html=True)
    
    st.info("""
    This module is currently in development. The full {module_name.replace("_", " ")} features will include:
    
    - Real-time analytics and reporting
    - AI-powered optimization
    - Data visualization
    - Export capabilities
    
    Check back soon for updates!
    """)
    
    st.success("Module framework is in place and ready for enhancement!")
'''
        
        with open(f'modules/{module_name}.py', 'w') as f:
            f.write(module_code)
        print(f"✓ Created modules/{module_name}.py")

def create_readme():
    """Create README"""
    readme = """# SportAI - Skill Shot Management Platform

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run main_app.py
```

3. Login with demo credentials:
- Admin: `admin` / `admin123`
- Board: `board_member` / `board123`

## Project Structure
```
sportai/
├── main_app.py          # Main application
├── modules/             # Feature modules
├── config/              # Configuration files
└── requirements.txt     # Dependencies
```

## Next Steps
1. Change default passwords in `config/users.json`
2. Customize configurations
3. Add your facility data
4. Deploy to production

For full documentation, see DEPLOYMENT.md
"""
    
    with open('README.md', 'w') as f:
        f.write(readme)
    print("✓ Created README.md")

def main():
    print("\n" + "="*60)
    print("SportAI Setup - Creating Your Project")
    print("="*60 + "\n")
    
    create_directory_structure()
    create_config_files()
    create_streamlit_config()
    create_requirements()
    create_main_app()
    create_dashboard_module()
    create_placeholder_modules()
    create_readme()
    
    print("\n" + "="*60)
    print("✨ Setup Complete!")
    print("="*60 + "\n")
    
    print("📋 Next Steps:\n")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt\n")
    print("2. Run the application:")
    print("   streamlit run main_app.py\n")
    print("3. Login with:")
    print("   Admin: admin / admin123\n")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
