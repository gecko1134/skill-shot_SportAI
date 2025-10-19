"""
SportAI Sponsorship Optimizer Module
Intelligent sponsorship bundling, pricing, and contract management
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json

def run(context: Dict[str, Any]):
    """Main sponsorship optimizer execution"""
    
    st.markdown('<div class="main-header">🤝 Sponsorship Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Maximize sponsorship revenue with intelligent bundling</div>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📦 Bundle Builder",
        "📊 Inventory",
        "💼 Active Sponsors",
        "📄 Contracts",
        "📈 Analytics"
    ])
    
    with tab1:
        show_bundle_builder(context)
        
    with tab2:
        show_inventory_view(context)
        
    with tab3:
        show_active_sponsors(context)
        
    with tab4:
        show_contract_manager(context)
        
    with tab5:
        show_sponsorship_analytics(context)

def show_bundle_builder(context: Dict[str, Any]):
    """Interactive bundle builder with presentation mode"""
    
    st.markdown("### 📦 Create Sponsorship Package")
    
    # Sponsor profile
    st.markdown("#### 🎯 Sponsor Profile")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sponsor_name = st.text_input("Sponsor Name", "ABC Corporation")
        sponsor_industry = st.selectbox(
            "Industry",
            ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "Food & Beverage"]
        )
        
    with col2:
        budget_range = st.selectbox(
            "Budget Range",
            ["$10K-$25K", "$25K-$50K", "$50K-$100K", "$100K-$250K", "$250K+"]
        )
        objectives = st.multiselect(
            "Objectives",
            ["Brand Awareness", "Lead Generation", "Community Engagement", "Employee Engagement"],
            default=["Brand Awareness"]
        )
        
    with col3:
        term_length = st.selectbox("Term Length", ["1 Year", "2 Years", "3 Years"])
        exclusivity = st.checkbox("Category Exclusivity Required")
    
    st.divider()
    
    # Available assets
    st.markdown("#### 🏷️ Available Assets")
    
    assets = get_available_assets()
    
    # Display assets in categories
    col1, col2 = st.columns(2)
    
    selected_assets = []
    
    with col1:
        st.markdown("**Naming Rights & Premium**")
        for asset in assets:
            if asset['category'] in ['Naming Rights', 'Premium']:
                if st.checkbox(
                    f"{asset['name']} - ${asset['annual_value']:,}/yr",
                    key=f"asset_{asset['id']}"
                ):
                    selected_assets.append(asset)
        
        st.markdown("**Digital & Media**")
        for asset in assets:
            if asset['category'] == 'Digital':
                if st.checkbox(
                    f"{asset['name']} - ${asset['annual_value']:,}/yr",
                    key=f"asset_{asset['id']}"
                ):
                    selected_assets.append(asset)
    
    with col2:
        st.markdown("**Physical Signage**")
        for asset in assets:
            if asset['category'] == 'Signage':
                if st.checkbox(
                    f"{asset['name']} - ${asset['annual_value']:,}/yr",
                    key=f"asset_{asset['id']}"
                ):
                    selected_assets.append(asset)
        
        st.markdown("**Activation & Events**")
        for asset in assets:
            if asset['category'] == 'Activation':
                if st.checkbox(
                    f"{asset['name']} - ${asset['annual_value']:,}/yr",
                    key=f"asset_{asset['id']}"
                ):
                    selected_assets.append(asset)
    
    st.divider()
    
    # Bundle summary
    if selected_assets:
        st.markdown("### 💰 Package Summary")
        
        # Calculate totals
        annual_total = sum(asset['annual_value'] for asset in selected_assets)
        term_years = int(term_length.split()[0])
        total_value = annual_total * term_years
        
        # Volume discount
        discount_pct = calculate_bundle_discount(len(selected_assets), total_value)
        discounted_total = total_value * (1 - discount_pct)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Assets Included", len(selected_assets))
            
        with col2:
            st.metric("Annual Value", f"${annual_total:,}")
            
        with col3:
            st.metric("Bundle Discount", f"{discount_pct*100:.0f}%")
            
        with col4:
            st.metric("Total Contract Value", f"${discounted_total:,.0f}")
        
        # Assets table
        st.markdown("#### 📋 Selected Assets")
        
        assets_df = pd.DataFrame([{
            'Asset': a['name'],
            'Category': a['category'],
            'Annual Value': f"${a['annual_value']:,}",
            'Est. Impressions': f"{a['impressions']:,}",
            'CPM': f"${(a['annual_value'] / a['impressions'] * 1000):.2f}"
        } for a in selected_assets])
        
        st.dataframe(assets_df, use_container_width=True, hide_index=True)
        
        # ROI projection
        st.markdown("#### 📊 Projected ROI")
        
        total_impressions = sum(a['impressions'] for a in selected_assets)
        cpm = (discounted_total / total_impressions * 1000) if total_impressions > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Impressions/Year",
                f"{total_impressions:,}",
                help="Estimated annual impressions across all assets"
            )
            
        with col2:
            st.metric(
                "Blended CPM",
                f"${cpm:.2f}",
                help="Cost per thousand impressions"
            )
            
        with col3:
            market_cpm = 25.00
            savings = (market_cpm - cpm) / market_cpm * 100
            st.metric(
                "vs Market CPM",
                f"{savings:.0f}% better",
                help=f"Market average CPM: ${market_cpm}"
            )
        
        # Actions
        st.divider()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📄 Generate Proposal", type="primary", use_container_width=True):
                generate_proposal(context, sponsor_name, selected_assets, discounted_total, term_years)
                
        with col2:
            if st.button("📧 Email to Prospect", use_container_width=True):
                st.success(f"Proposal sent to {sponsor_name}")
                context['audit_log']('proposal_sent', {'sponsor': sponsor_name, 'value': discounted_total})
                
        with col3:
            if st.button("💾 Save as Template", use_container_width=True):
                st.success("Package saved as template")
                
        with col4:
            if st.button("🎯 Optimize Bundle", use_container_width=True):
                optimized = optimize_bundle(selected_assets, budget_range, objectives)
                st.info(f"Optimization complete! Suggested {len(optimized)} changes.")
    
    else:
        st.info("👆 Select assets above to build a sponsorship package")

def show_inventory_view(context: Dict[str, Any]):
    """Sponsorship inventory management"""
    
    st.markdown("### 📊 Sponsorship Inventory")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    inventory_stats = calculate_inventory_stats()
    
    with col1:
        st.metric("Total Inventory Value", f"${inventory_stats['total_value']:,}")
        
    with col2:
        st.metric("Sold", f"{inventory_stats['sold_pct']:.0f}%", f"${inventory_stats['sold_value']:,}")
        
    with col3:
        st.metric("Available", f"{inventory_stats['available_pct']:.0f}%", f"${inventory_stats['available_value']:,}")
        
    with col4:
        st.metric("Expiring (90 days)", inventory_stats['expiring_count'])
    
    st.divider()
    
    # Inventory by category
    st.markdown("#### 📦 Inventory by Category")
    
    assets = get_available_assets()
    
    # Group by category
    categories = {}
    for asset in assets:
        cat = asset['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(asset)
    
    # Display each category
    for category, cat_assets in categories.items():
        with st.expander(f"{category} ({len(cat_assets)} assets)"):
            df = pd.DataFrame([{
                'Asset': a['name'],
                'Annual Value': f"${a['annual_value']:,}",
                'Status': a['status'],
                'Impressions': f"{a['impressions']:,}",
                'Available From': a.get('available_from', 'Now')
            } for a in cat_assets])
            
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Add new asset
    st.divider()
    st.markdown("#### ➕ Add New Asset")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        new_asset_name = st.text_input("Asset Name")
        new_asset_category = st.selectbox("Category", list(categories.keys()))
        
    with col2:
        new_asset_value = st.number_input("Annual Value ($)", min_value=0, value=5000)
        new_asset_impressions = st.number_input("Annual Impressions", min_value=0, value=50000)
        
    with col3:
        new_asset_type = st.selectbox("Type", ["Physical", "Digital", "Event", "Mixed"])
        new_asset_exclusivity = st.checkbox("Exclusivity Available")
        
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Add Asset"):
            st.success(f"Asset '{new_asset_name}' added to inventory")
            context['audit_log']('asset_added', {'name': new_asset_name, 'value': new_asset_value})

def show_active_sponsors(context: Dict[str, Any]):
    """Active sponsor management"""
    
    st.markdown("### 💼 Active Sponsors")
    
    sponsors = get_active_sponsors()
    
    # Sponsor cards
    for sponsor in sponsors:
        with st.expander(f"🏢 {sponsor['name']} - ${sponsor['annual_value']:,}/yr"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Contract Details**")
                st.write(f"Term: {sponsor['term_start']} to {sponsor['term_end']}")
                st.write(f"Annual Value: ${sponsor['annual_value']:,}")
                st.write(f"Total Value: ${sponsor['total_value']:,}")
                st.write(f"Assets: {sponsor['asset_count']}")
                
            with col2:
                st.markdown("**Performance**")
                st.write(f"Impressions YTD: {sponsor['impressions_ytd']:,}")
                st.write(f"Events Activated: {sponsor['events_activated']}")
                st.write(f"Satisfaction: {'⭐' * sponsor['satisfaction_rating']}")
                st.write(f"Renewal Likelihood: {sponsor['renewal_probability']}%")
                
            with col3:
                st.markdown("**Quick Actions**")
                if st.button("📊 View Performance", key=f"perf_{sponsor['id']}"):
                    st.info("Loading performance dashboard...")
                if st.button("📧 Send Update", key=f"email_{sponsor['id']}"):
                    st.success("Update email sent")
                if st.button("🔄 Renewal Proposal", key=f"renew_{sponsor['id']}"):
                    st.info("Generating renewal proposal...")
            
            # Performance chart
            st.markdown("**Impressions Tracking**")
            fig = create_sponsor_performance_chart(sponsor)
            st.plotly_chart(fig, use_container_width=True)

def show_contract_manager(context: Dict[str, Any]):
    """Contract management interface"""
    
    st.markdown("### 📄 Contract Management")
    
    # Contract status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Contracts", 12)
        
    with col2:
        st.metric("Pending Signature", 3)
        
    with col3:
        st.metric("Expiring (60 days)", 5)
        
    with col4:
        st.metric("Renewal Rate", "85%", "+5%")
    
    st.divider()
    
    # Contract list
    st.markdown("#### 📋 All Contracts")
    
    contracts = get_contracts()
    
    df = pd.DataFrame(contracts)
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Status",
            ["Active", "Pending", "Expiring", "Expired"],
            default=["Active", "Pending", "Expiring"]
        )
        
    with col2:
        value_filter = st.selectbox(
            "Value Range",
            ["All", "$0-$25K", "$25K-$50K", "$50K-$100K", "$100K+"]
        )
        
    with col3:
        sort_by = st.selectbox(
            "Sort By",
            ["End Date", "Value", "Sponsor Name"]
        )
    
    # Display filtered contracts
    filtered_df = df[df['Status'].isin(status_filter)]
    
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Actions": st.column_config.TextColumn("Actions", width="medium")
        }
    )
    
    # Auto-renewal engine
    st.divider()
    st.markdown("#### 🔄 Auto-Renewal Engine")
    
    st.info("""
    The auto-renewal engine automatically:
    - Identifies contracts expiring in 90 days
    - Prepares renewal proposals with performance data
    - Suggests upsell opportunities based on sponsor objectives
    - Schedules outreach and follow-ups
    """)
    
    if st.button("🚀 Run Auto-Renewal Scan"):
        with st.spinner("Analyzing renewal opportunities..."):
            renewal_opps = [
                {"Sponsor": "ABC Corp", "Expires": "2025-12-31", "Value": 125000, "Upsell": 15000, "Confidence": 92},
                {"Sponsor": "XYZ Inc", "Expires": "2026-01-15", "Value": 75000, "Upsell": 10000, "Confidence": 78},
                {"Sponsor": "123 LLC", "Expires": "2025-11-30", "Value": 50000, "Upsell": 5000, "Confidence": 85},
            ]
            
            st.success(f"✅ Found {len(renewal_opps)} renewal opportunities")
            
            st.dataframe(pd.DataFrame(renewal_opps), use_container_width=True, hide_index=True)

def show_sponsorship_analytics(context: Dict[str, Any]):
    """Sponsorship analytics and insights"""
    
    st.markdown("### 📈 Sponsorship Analytics")
    
    # Revenue trends
    st.markdown("#### 💰 Revenue Trends")
    
    fig_revenue = create_sponsorship_revenue_chart()
    st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Pipeline analysis
    st.markdown("#### 🎯 Sales Pipeline")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pipeline_data = {
            'Stage': ['Prospect', 'Proposal', 'Negotiation', 'Contract', 'Closed'],
            'Count': [15, 8, 5, 3, 12],
            'Value': [500000, 400000, 280000, 180000, 1200000]
        }
        
        df_pipeline = pd.DataFrame(pipeline_data)
        
        fig = go.Figure(go.Funnel(
            y=df_pipeline['Stage'],
            x=df_pipeline['Count'],
            textinfo="value+percent initial",
            marker=dict(color=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'])
        ))
        
        fig.update_layout(height=400, title="Pipeline by Count")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        fig2 = go.Figure(go.Funnel(
            y=df_pipeline['Stage'],
            x=df_pipeline['Value'],
            textinfo="value",
            marker=dict(color=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'])
        ))
        
        fig2.update_layout(height=400, title="Pipeline by Value ($)")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Industry breakdown
    st.markdown("#### 🏭 Sponsors by Industry")
    
    industry_data = {
        'Industry': ['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing'],
        'Sponsors': [4, 3, 2, 2, 1],
        'Total Value': [450000, 280000, 200000, 150000, 120000]
    }
    
    fig_industry = go.Figure(data=[go.Pie(
        labels=industry_data['Industry'],
        values=industry_data['Total Value'],
        hole=0.4,
        marker_colors=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
    )])
    
    fig_industry.update_layout(height=400)
    st.plotly_chart(fig_industry, use_container_width=True)

# Helper functions

def get_available_assets() -> List[Dict]:
    """Get available sponsorship assets"""
    return [
        # Naming Rights
        {'id': 1, 'name': 'Facility Naming Rights', 'category': 'Naming Rights', 
         'annual_value': 250000, 'status': 'Available', 'impressions': 2000000},
        {'id': 2, 'name': 'Dome Naming Rights', 'category': 'Naming Rights', 
         'annual_value': 150000, 'status': 'Sold', 'impressions': 1500000},
        
        # Premium
        {'id': 3, 'name': 'Center Court Naming', 'category': 'Premium', 
         'annual_value': 75000, 'status': 'Available', 'impressions': 800000},
        {'id': 4, 'name': 'Turf Field Naming', 'category': 'Premium', 
         'annual_value': 100000, 'status': 'Available', 'impressions': 1000000},
        
        # Signage
        {'id': 5, 'name': 'Entry Banner (20x10ft)', 'category': 'Signage', 
         'annual_value': 15000, 'status': 'Available', 'impressions': 500000},
        {'id': 6, 'name': 'Dasher Boards (8 panels)', 'category': 'Signage', 
         'annual_value': 25000, 'status': 'Available', 'impressions': 600000},
        {'id': 7, 'name': 'Lobby Wall Graphics', 'category': 'Signage', 
         'annual_value': 12000, 'status': 'Sold', 'impressions': 400000},
        
        # Digital
        {'id': 8, 'name': 'Website Homepage Banner', 'category': 'Digital', 
         'annual_value': 8000, 'status': 'Available', 'impressions': 250000},
        {'id': 9, 'name': 'Social Media Package', 'category': 'Digital', 
         'annual_value': 10000, 'status': 'Available', 'impressions': 500000},
        {'id': 10, 'name': 'Email Newsletter Sponsor', 'category': 'Digital', 
         'annual_value': 5000, 'status': 'Available', 'impressions': 120000},
        
        # Activation
        {'id': 11, 'name': 'Tournament Title Sponsor', 'category': 'Activation', 
         'annual_value': 35000, 'status': 'Available', 'impressions': 750000},
        {'id': 12, 'name': 'Suite Package (10 events)', 'category': 'Activation', 
         'annual_value': 20000, 'status': 'Available', 'impressions': 50000},
        {'id': 13, 'name': 'Community Day Presenting', 'category': 'Activation', 
         'annual_value': 15000, 'status': 'Available', 'impressions': 300000},
    ]

def calculate_bundle_discount(asset_count: int, total_value: float) -> float:
    """Calculate volume discount for bundle"""
    if asset_count >= 5:
        return 0.15
    elif asset_count >= 3:
        return 0.10
    elif total_value >= 100000:
        return 0.08
    return 0.0

def calculate_inventory_stats() -> Dict:
    """Calculate inventory statistics"""
    assets = get_available_assets()
    
    total_value = sum(a['annual_value'] for a in assets)
    sold_value = sum(a['annual_value'] for a in assets if a['status'] == 'Sold')
    available_value = total_value - sold_value
    
    sold_count = sum(1 for a in assets if a['status'] == 'Sold')
    
    return {
        'total_value': total_value,
        'sold_value': sold_value,
        'available_value': available_value,
        'sold_pct': (sold_value / total_value * 100) if total_value > 0 else 0,
        'available_pct': (available_value / total_value * 100) if total_value > 0 else 0,
        'expiring_count': 5
    }

def get_active_sponsors() -> List[Dict]:
    """Get active sponsors"""
    return [
        {
            'id': 1,
            'name': 'TechCorp Solutions',
            'annual_value': 125000,
            'total_value': 375000,
            'term_start': '2024-01-01',
            'term_end': '2026-12-31',
            'asset_count': 5,
            'impressions_ytd': 1850000,
            'events_activated': 8,
            'satisfaction_rating': 5,
            'renewal_probability': 92
        },
        {
            'id': 2,
            'name': 'HealthPlus Medical',
            'annual_value': 75000,
            'total_value': 150000,
            'term_start': '2024-06-01',
            'term_end': '2026-05-31',
            'asset_count': 3,
            'impressions_ytd': 950000,
            'events_activated': 4,
            'satisfaction_rating': 4,
            'renewal_probability': 78
        }
    ]

def get_contracts() -> List[Dict]:
    """Get all contracts"""
    return [
        {'Sponsor': 'TechCorp Solutions', 'Value': '$375,000', 'Start': '2024-01-01', 
         'End': '2026-12-31', 'Status': 'Active', 'Assets': 5},
        {'Sponsor': 'HealthPlus Medical', 'Value': '$150,000', 'Start': '2024-06-01', 
         'End': '2026-05-31', 'Status': 'Active', 'Assets': 3},
        {'Sponsor': 'ABC Corporation', 'Value': '$50,000', 'Start': '2025-01-01', 
         'End': '2025-12-31', 'Status': 'Pending', 'Assets': 2},
        {'Sponsor': 'XYZ Industries', 'Value': '$125,000', 'Start': '2023-01-01', 
         'End': '2025-12-31', 'Status': 'Expiring', 'Assets': 4},
    ]

def generate_proposal(context: Dict, sponsor_name: str, assets: List, total_value: float, term_years: int):
    """Generate sponsorship proposal"""
    st.success(f"""
    ✅ Proposal generated for {sponsor_name}
    
    **Package Summary:**
    - {len(assets)} assets included
    - ${total_value:,.0f} total contract value
    - {term_years}-year term
    
    The proposal has been saved and is ready for review.
    """)
    
    context['audit_log']('proposal_generated', {
        'sponsor': sponsor_name,
        'assets': len(assets),
        'value': total_value
    })

def optimize_bundle(assets: List, budget: str, objectives: List) -> List:
    """Optimize asset bundle based on criteria"""
    # Simplified optimization
    return []

def create_sponsor_performance_chart(sponsor: Dict):
    """Create sponsor performance chart"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    impressions = [150000 + (i * 15000) for i in range(10)]
    target = [185000] * 10
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=impressions,
        mode='lines+markers',
        name='Actual',
        line=dict(color='#3b82f6', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=target,
        mode='lines',
        name='Target',
        line=dict(color='#10b981', dash='dash', width=2)
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis_title="Impressions",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_sponsorship_revenue_chart():
    """Create sponsorship revenue trend chart"""
    months = pd.date_range(start='2024-01-01', periods=12, freq='M')
    revenue = [75000, 82000, 78000, 95000, 110000, 125000, 
               135000, 142000, 138000, 155000, 168000, 185000]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=months,
        y=revenue,
        marker_color='#3b82f6',
        name='Monthly Revenue'
    ))
    
    fig.update_layout(
        height=400,
        yaxis_title="Revenue ($)",
        xaxis_title="Month",
        showlegend=False
    )
    
    return fig
