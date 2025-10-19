"""
SportAI Setup Script
Automated setup and initialization for SportAI system
"""

import os
import json
from pathlib import Path
import sys

def create_directory_structure():
    """Create required directory structure"""
    
    directories = [
        'config',
        'modules',
        'utils',
        'data',
        'tests',
        'logs',
        '.streamlit'
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {directory}/")
    
    # Create __init__.py files
    for directory in ['modules', 'utils']:
        init_file = Path(directory) / '__init__.py'
        init_file.touch(exist_ok=True)
    
    print("  ✓ Created __init__.py files")

def create_config_files():
    """Create default configuration files"""
    
    print("\nCreating configuration files...")
    
    config_path = Path('config')
    
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
        },
        "member": {
            "password": "member123",
            "role": "member",
            "name": "Member User",
            "email": "member@skillshot.com"
        }
    }
    
    with open(config_path / 'users.json', 'w') as f:
        json.dump(users_config, f, indent=2)
    print("  ✓ Created users.json")
    
    # modules.json
    modules_config = {
        "admin": [
            "dashboard",
            "ai_scheduling",
            "dynamic_pricing",
            "sponsorship_optimizer",
            "membership_manager",
            "facility_ops",
            "grant_builder",
            "board_governance",
            "event_manager",
            "reports"
        ],
        "board": [
            "dashboard",
            "board_governance",
            "reports"
        ],
        "sponsor": [
            "sponsor_portal",
            "reports"
        ],
        "member": [
            "member_portal",
            "bookings"
        ],
        "staff": [
            "facility_ops",
            "event_manager"
        ]
    }
    
    with open(config_path / 'modules.json', 'w') as f:
        json.dump(modules_config, f, indent=2)
    print("  ✓ Created modules.json")
    
    # pricing_rules.json
    pricing_config = {
        "base_rates": {
            "turf_full": {
                "prime": 275,
                "standard": 200,
                "off_peak": 150
            },
            "turf_half": {
                "prime": 150,
                "standard": 110,
                "off_peak": 85
            },
            "court": {
                "prime": 45,
                "standard": 35,
                "off_peak": 25
            },
            "golf_bay": {
                "prime": 55,
                "standard": 45,
                "off_peak": 35
            }
        },
        "demand_multipliers": {
            "high": 1.25,
            "medium": 1.0,
            "low": 0.85
        },
        "lead_time_discounts": {
            "90_days": 0.85,
            "60_days": 0.90,
            "30_days": 0.95
        },
        "segments": {
            "youth": 0.80,
            "non_profit": 0.85,
            "regular": 1.0,
            "corporate": 1.15,
            "tournament": 1.20
        }
    }
    
    with open(config_path / 'pricing_rules.json', 'w') as f:
        json.dump(pricing_config, f, indent=2)
    print("  ✓ Created pricing_rules.json")
    
    # guardrails.json
    guardrails_config = {
        "max_surge_factor": 1.5,
        "min_community_hours_weekly": 20,
        "youth_discount_floor": 0.70,
        "max_price_change_percent": 25,
        "min_lead_time_hours": 4
    }
    
    with open(config_path / 'guardrails.json', 'w') as f:
        json.dump(guardrails_config, f, indent=2)
    print("  ✓ Created guardrails.json")

def create_env_file():
    """Create .env template file"""
    
    print("\nCreating .env template...")
    
    env_template = """# SportAI Environment Variables
# Copy this file to .env and fill in your actual values

# Database (optional - defaults to SQLite)
# DATABASE_URL=postgresql://user:password@localhost/sportai

# Email (SendGrid)
# SENDGRID_API_KEY=your_sendgrid_api_key
# SENDGRID_FROM_EMAIL=noreply@skillshot.com

# Google APIs (optional)
# GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json

# Stripe (optional)
# STRIPE_API_KEY=your_stripe_api_key
# STRIPE_WEBHOOK_SECRET=your_webhook_secret

# SportsKey (optional)
# SPORTSKEY_API_KEY=your_sportskey_api_key
# SPORTSKEY_API_URL=https://api.sportskey.com

# Application Settings
DEBUG=true
LOG_LEVEL=INFO
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_template)
    print("  ✓ Created .env.template")
    print("    📝 Copy .env.template to .env and configure your secrets")

def create_streamlit_config():
    """Create Streamlit configuration"""
    
    print("\nCreating Streamlit configuration...")
    
    streamlit_dir = Path('.streamlit')
    streamlit_dir.mkdir(exist_ok=True)
    
    config_content = """[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#3b82f6"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f9fafb"
textColor = "#1f2937"
"""
    
    with open(streamlit_dir / 'config.toml', 'w') as f:
        f.write(config_content)
    print("  ✓ Created .streamlit/config.toml")

def initialize_database():
    """Initialize the database with sample data"""
    
    print("\nInitializing database...")
    
    try:
        from utils.database import db
        db.init_database()
        db.seed_sample_data()
        print("  ✓ Database initialized with sample data")
    except Exception as e:
        print(f"  ⚠ Database initialization skipped: {e}")
        print("    Database will be initialized on first run")

def create_readme():
    """Create quick start README"""
    
    print("\nCreating README...")
    
    readme_content = """# SportAI - Skill Shot Management Platform

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.template .env
# Edit .env with your configuration
```

### 3. Run the Application
```bash
streamlit run main_app.py
```

### 4. Login
Default credentials:
- **Admin:** `admin` / `admin123`
- **Board:** `board_member` / `board123`
- **Sponsor:** `sponsor` / `sponsor123`

⚠️ **IMPORTANT:** Change default passwords before deploying to production!

## Project Structure
```
sportai/
├── main_app.py          # Main application
├── config/              # Configuration files
├── modules/             # Application modules
├── utils/               # Utility functions
├── data/                # Database files
└── tests/               # Unit tests
```

## Documentation
See README.md for full documentation.

## Support
Contact: support@skillshot.com
"""
    
    with open('QUICKSTART.md', 'w') as f:
        f.write(readme_content)
    print("  ✓ Created QUICKSTART.md")

def print_next_steps():
    """Print next steps for user"""
    
    print("\n" + "="*60)
    print("✨ SportAI Setup Complete! ✨")
    print("="*60)
    
    print("\n📋 Next Steps:\n")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt\n")
    
    print("2. (Optional) Configure environment:")
    print("   cp .env.template .env")
    print("   # Edit .env with your API keys\n")
    
    print("3. Run the application:")
    print("   streamlit run main_app.py\n")
    
    print("4. Access the application:")
    print("   Open your browser to http://localhost:8501\n")
    
    print("5. Login with default credentials:")
    print("   Admin: admin / admin123\n")
    
    print("⚠️  SECURITY NOTICE:")
    print("   Change default passwords in config/users.json")
    print("   before deploying to production!\n")
    
    print("📚 Documentation:")
    print("   See README.md for detailed documentation")
    print("   See QUICKSTART.md for quick reference\n")
    
    print("="*60)

def main():
    """Main setup function"""
    
    print("\n" + "="*60)
    print("SportAI Setup - Skill Shot Sports Facility")
    print("="*60 + "\n")
    
    try:
        create_directory_structure()
        create_config_files()
        create_env_file()
        create_streamlit_config()
        create_readme()
        initialize_database()
        print_next_steps()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
