"""
SportAI - Complete Sports Facility Management Platform
Main Application Entry Point
"""

import streamlit as st
import importlib
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import json
from datetime import datetime

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

# Page config
st.set_page_config(
    page_title="SportAI - Skill Shot Management",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
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
        border-left: 4px solid #3b82f6;
    }
    .alert-warning {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .alert-success {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .stButton>button {
        background: #3b82f6;
        color: white;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

class SportAIApp:
    """Main application controller"""
    
    def __init__(self):
        self.initialize_session_state()
        self.load_configs()
        self.load_user_context()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'site_id' not in st.session_state:
            st.session_state.site_id = 'skill_shot_main'
        if 'audit_log' not in st.session_state:
            st.session_state.audit_log = []
            
    def load_configs(self):
        """Load all configuration files"""
        config_path = Path(__file__).parent / 'config'
        
        # Create default configs if they don't exist
        config_path.mkdir(exist_ok=True)
        
        configs = {
            'users': 'users.json',
            'pricing': 'pricing_rules.json',
            'sponsorship_inventory': 'sponsorship_inventory.json',
            'sponsorship_assets': 'sponsorship_assets.json',
            'guardrails': 'guardrails.json',
            'modules': 'modules.json'
        }
        
        for key, filename in configs.items():
            file_path = config_path / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    st.session_state[f'config_{key}'] = json.load(f)
            else:
                st.session_state[f'config_{key}'] = self.get_default_config(key)
                
    def get_default_config(self, config_type: str) -> Dict:
        """Return default configuration for each type"""
        defaults = {
            'users': {
                'admin': {
                    'password': 'admin123',  # Change in production!
                    'role': 'admin',
                    'name': 'System Administrator',
                    'email': 'admin@skillshot.com'
                },
                'board_member': {
                    'password': 'board123',
                    'role': 'board',
                    'name': 'Board Member',
                    'email': 'board@skillshot.com'
                },
                'sponsor': {
                    'password': 'sponsor123',
                    'role': 'sponsor',
                    'name': 'Sponsor User',
                    'email': 'sponsor@skillshot.com'
                }
            },
            'modules': {
                'admin': [
                    'dashboard',
                    'ai_scheduling',
                    'dynamic_pricing',
                    'sponsorship_optimizer',
                    'membership_manager',
                    'facility_ops',
                    'grant_builder',
                    'board_governance',
                    'event_manager',
                    'reports'
                ],
                'board': [
                    'dashboard',
                    'board_governance',
                    'reports'
                ],
                'sponsor': [
                    'sponsor_portal',
                    'reports'
                ],
                'member': [
                    'member_portal',
                    'bookings'
                ],
                'staff': [
                    'facility_ops',
                    'event_manager'
                ]
            },
            'pricing': {
                'base_rates': {
                    'turf_full': {'prime': 275, 'standard': 200, 'off_peak': 150},
                    'turf_half': {'prime': 150, 'standard': 110, 'off_peak': 85},
                    'court': {'prime': 45, 'standard': 35, 'off_peak': 25},
                    'golf_bay': {'prime': 55, 'standard': 45, 'off_peak': 35}
                },
                'demand_multipliers': {
                    'high': 1.25,
                    'medium': 1.0,
                    'low': 0.85
                },
                'lead_time_discounts': {
                    '30_days': 0.95,
                    '60_days': 0.90,
                    '90_days': 0.85
                },
                'segments': {
                    'youth': 0.80,
                    'non_profit': 0.85,
                    'corporate': 1.15,
                    'tournament': 1.20
                }
            },
            'sponsorship_inventory': {},
            'sponsorship_assets': {},
            'guardrails': {
                'max_surge_factor': 1.5,
                'min_community_hours_weekly': 20,
                'youth_discount_floor': 0.70,
                'max_price_change_percent': 25
            }
        }
        return defaults.get(config_type, {})
        
    def load_user_context(self):
        """Load current user context and permissions"""
        if st.session_state.authenticated and st.session_state.user:
            user_data = st.session_state.config_users.get(st.session_state.user, {})
            st.session_state.user_role = user_data.get('role', 'guest')
            st.session_state.user_email = user_data.get('email', '')
            st.session_state.user_name = user_data.get('name', st.session_state.user)
        else:
            st.session_state.user_role = 'guest'
            
    def get_available_modules(self) -> list:
        """Get list of modules available to current user"""
        role = st.session_state.user_role
        return st.session_state.config_modules.get(role, [])
        
    def audit_log(self, action: str, details: Dict[str, Any]):
        """Add entry to audit log"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'user': st.session_state.user,
            'role': st.session_state.user_role,
            'action': action,
            'details': details
        }
        st.session_state.audit_log.append(entry)
        
    def login_page(self):
        """Display login page"""
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
                    self.load_user_context()
                    self.audit_log('login', {'username': username})
                    st.rerun()
                else:
                    st.error("Invalid credentials")
                    
            with st.expander("Demo Credentials"):
                st.markdown("""
                **Admin:** `admin` / `admin123`  
                **Board:** `board_member` / `board123`  
                **Sponsor:** `sponsor` / `sponsor123`
                """)
                
    def load_module(self, module_name: str):
        """Dynamically load and run a module"""
        try:
            module_path = f"modules.{module_name}"
            module = importlib.import_module(module_path)
            
            # Create module context
            context = {
                'session': st.session_state,
                'user_ctx': {
                    'user': st.session_state.user,
                    'role': st.session_state.user_role,
                    'email': st.session_state.user_email,
                    'name': st.session_state.user_name,
                    'site_id': st.session_state.site_id
                },
                'audit_log': self.audit_log
            }
            
            # Run module
            module.run(context)
            
        except ModuleNotFoundError:
            st.warning(f"Module '{module_name}' not yet implemented. Coming soon!")
        except Exception as e:
            st.error(f"Error loading module: {str(e)}")
            with st.expander("Error Details"):
                st.exception(e)
                
    def main_app(self):
        """Main application interface"""
        # Sidebar
        with st.sidebar:
            st.markdown(f"### 👤 {st.session_state.user_name}")
            st.markdown(f"**Role:** {st.session_state.user_role.title()}")
            st.markdown(f"**Site:** Skill Shot")
            st.divider()
            
            # Navigation
            st.markdown("### 📋 Navigation")
            available_modules = self.get_available_modules()
            
            module_labels = {
                'dashboard': '📊 Dashboard',
                'ai_scheduling': '🤖 AI Scheduling',
                'dynamic_pricing': '💰 Dynamic Pricing',
                'sponsorship_optimizer': '🤝 Sponsorship',
                'membership_manager': '👥 Memberships',
                'facility_ops': '🏢 Facility Ops',
                'grant_builder': '📄 Grants',
                'board_governance': '⚖️ Governance',
                'event_manager': '📅 Events',
                'sponsor_portal': '🎯 Sponsor Portal',
                'member_portal': '🎫 Member Portal',
                'reports': '📈 Reports',
                'bookings': '📅 Bookings'
            }
            
            selected = st.radio(
                "Select Module",
                available_modules,
                format_func=lambda x: module_labels.get(x, x.title())
            )
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True):
                self.audit_log('logout', {'username': st.session_state.user})
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()
                
        # Main content area
        self.load_module(selected)
        
    def run(self):
        """Main application runner"""
        if not st.session_state.authenticated:
            self.login_page()
        else:
            self.main_app()

# Run application
if __name__ == "__main__":
    app = SportAIApp()
    app.run()
