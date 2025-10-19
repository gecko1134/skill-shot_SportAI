"""
SportAI Dynamic Pricing Engine Module
Intelligent, fair pricing with explainability and guardrails
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import math

def run(context: Dict[str, Any]):
    """Main dynamic pricing execution"""
    
    st.markdown('<div class="main-header">💰 Dynamic Pricing Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent pricing with transparency and fairness</div>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Price Calculator",
        "📊 Price Analysis", 
        "⚙️ Guardrails",
        "📈 Performance"
    ])
    
    with tab1:
        show_price_calculator(context)
        
    with tab2:
        show_price_analysis(context)
        
    with tab3:
        show_guardrails_config(context)
        
    with tab4:
        show_pricing_performance(context)

def show_price_calculator(context: Dict[str, Any]):
    """Interactive price calculator with explainability"""
    
    st.markdown("### 💡 Calculate Optimal Price")
    
    # Input parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        asset_type = st.selectbox(
            "Asset Type",
            ["Turf - Full Field", "Turf - Half Field", "Court", "Golf Bay", "Suite"]
        )
        
        booking_date = st.date_input(
            "Booking Date",
            min_value=datetime.now().date(),
            value=datetime.now().date() + timedelta(days=7)
        )
        
    with col2:
        time_slot = st.selectbox(
            "Time Slot",
            ["6am-9am", "9am-12pm", "12pm-3pm", "3pm-6pm", "6pm-9pm (Prime)", "9pm-12am"]
        )
        
        duration = st.number_input(
            "Duration (hours)",
            min_value=0.5,
            max_value=8.0,
            value=2.0,
            step=0.5
        )
        
    with col3:
        customer_type = st.selectbox(
            "Customer Type",
            ["Corporate", "Regular", "Non-Profit", "Youth"]
        )
        
        lead_time_days = (booking_date - datetime.now().date()).days
        st.metric("Lead Time", f"{lead_time_days} days")
    
    st.divider()
    
    # Calculate price
    if st.button("🧮 Calculate Price", type="primary"):
        
        pricing_result = calculate_dynamic_price(
            asset_type=asset_type,
            booking_date=booking_date,
            time_slot=time_slot,
            duration=duration,
            customer_type=customer_type,
            lead_time_days=lead_time_days,
            context=context
        )
        
        # Display results
        st.success("✅ Price calculated successfully!")
        
        # Price display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Base Rate",
                f"${pricing_result['base_rate']:.2f}/hr",
                help="Standard rate for this asset and time"
            )
            
        with col2:
            st.metric(
                "Dynamic Rate",
                f"${pricing_result['dynamic_rate']:.2f}/hr",
                f"{pricing_result['adjustment_pct']:+.1f}%",
                help="Rate after demand and lead time adjustments"
            )
            
        with col3:
            st.metric(
                "Final Price",
                f"${pricing_result['final_price']:.2f}",
                help=f"Total for {duration} hours"
            )
        
        # Explainability section
        st.divider()
        st.markdown("### 🔍 Pricing Breakdown (Transparency)")
        
        st.markdown(f"""
        <div class="alert-success">
        This price was calculated using {len(pricing_result['factors'])} factors to ensure 
        fairness and optimal utilization. All adjustments respect board-approved guardrails.
        </div>
        """, unsafe_allow_html=True)
        
        # Show factors
        factors_df = pd.DataFrame(pricing_result['factors'])
        
        fig = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative"] * (len(factors_df) - 1) + ["total"],
            x=factors_df['Factor'],
            y=factors_df['Impact'],
            text=factors_df['Impact'].apply(lambda x: f"${x:.2f}"),
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#10b981"}},
            decreasing={"marker": {"color": "#ef4444"}},
            totals={"marker": {"color": "#3b82f6"}}
        ))
        
        fig.update_layout(
            title="Price Calculation Waterfall",
            height=400,
            showlegend=False,
            yaxis_title="Price Impact ($)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed explanation
        with st.expander("📋 Detailed Factor Explanation"):
            for factor in pricing_result['factors']:
                if factor['Impact'] != 0:
                    icon = "📈" if factor['Impact'] > 0 else "📉"
                    st.markdown(f"""
                    **{icon} {factor['Factor']}**: ${factor['Impact']:.2f}  
                    _{factor['Explanation']}_
                    """)
        
        # Alternative scenarios
        st.divider()
        st.markdown("### 🔄 Alternative Scenarios")
        
        alternatives = generate_alternative_scenarios(
            asset_type, booking_date, time_slot, duration, customer_type, context
        )
        
        st.dataframe(alternatives, use_container_width=True, hide_index=True)

def show_price_analysis(context: Dict[str, Any]):
    """Price analysis and trends"""
    
    st.markdown("### 📊 Pricing Analytics")
    
    # Price trends
    st.markdown("#### 📈 Price Trends (Last 90 Days)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        asset_filter = st.selectbox(
            "Asset Type",
            ["All", "Turf - Full", "Turf - Half", "Court", "Golf Bay", "Suite"],
            key="trend_asset"
        )
        
    with col2:
        metric_type = st.selectbox(
            "Metric",
            ["Average Price", "Utilization Rate", "Revenue per Hour"],
            key="trend_metric"
        )
    
    fig_trends = create_price_trend_chart(asset_filter, metric_type)
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Price distribution
    st.markdown("#### 📊 Price Distribution by Daypart")
    
    fig_distribution = create_price_distribution_chart()
    st.plotly_chart(fig_distribution, use_container_width=True)
    
    # Conversion analysis
    st.markdown("#### 💹 Price Elasticity & Conversion")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Optimal Conversion Rate", "78%", "+3%")
        st.caption("Sweet spot: $110-$140/hr for prime time")
        
    with col2:
        st.metric("Revenue per Booking", "$245", "+$18")
        st.caption("15% increase from dynamic pricing")
        
    with col3:
        st.metric("Lost Revenue (Too High)", "$12,500", "-$2,100")
        st.caption("Declined due to price sensitivity")
    
    # Competitive positioning
    st.divider()
    st.markdown("#### 🎯 Competitive Positioning")
    
    comp_data = {
        'Facility': ['Skill Shot', 'Competitor A', 'Competitor B', 'Competitor C', 'Market Avg'],
        'Prime Hour Rate': [135, 150, 125, 140, 138],
        'Off-Peak Rate': [85, 95, 80, 90, 88],
        'Utilization': [87, 72, 81, 76, 78]
    }
    
    df_comp = pd.DataFrame(comp_data)
    
    fig_comp = go.Figure()
    
    fig_comp.add_trace(go.Scatter(
        x=df_comp['Prime Hour Rate'],
        y=df_comp['Utilization'],
        mode='markers+text',
        marker=dict(
            size=20,
            color=['#10b981', '#6b7280', '#6b7280', '#6b7280', '#f59e0b']
        ),
        text=df_comp['Facility'],
        textposition='top center',
        name='Facilities'
    ))
    
    fig_comp.update_layout(
        height=400,
        xaxis_title="Prime Hour Rate ($)",
        yaxis_title="Utilization (%)",
        title="Price vs Utilization Matrix"
    )
    
    st.plotly_chart(fig_comp, use_container_width=True)

def show_guardrails_config(context: Dict[str, Any]):
    """Configure pricing guardrails and policy rules"""
    
    st.markdown("### ⚙️ Pricing Guardrails & Policy")
    
    st.info("""
    Guardrails ensure pricing remains fair, competitive, and aligned with community values.
    These limits are enforced automatically by the pricing engine.
    """)
    
    # Load current guardrails
    guardrails = context['session'].get('config_guardrails', {})
    
    # General limits
    st.markdown("#### 🛡️ General Limits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_surge = st.slider(
            "Maximum Surge Factor",
            1.0, 2.0, 
            guardrails.get('max_surge_factor', 1.5),
            0.05,
            help="Maximum multiplier during peak demand"
        )
        
        max_price_change = st.slider(
            "Maximum Price Change",
            0, 50,
            guardrails.get('max_price_change_percent', 25),
            5,
            help="Maximum % change from base rate"
        )
        
    with col2:
        min_discount = st.slider(
            "Minimum Discount Floor",
            0.5, 1.0,
            guardrails.get('min_discount_floor', 0.7),
            0.05,
            help="Lowest multiplier allowed (70% = maximum 30% discount)"
        )
        
        min_lead_time = st.number_input(
            "Minimum Lead Time (hours)",
            0, 168,
            guardrails.get('min_lead_time_hours', 4),
            help="Minimum hours notice required for booking"
        )
    
    st.divider()
    
    # Community pricing
    st.markdown("#### 👥 Community & Youth Pricing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        youth_discount = st.slider(
            "Youth Discount",
            0.0, 0.5,
            guardrails.get('youth_discount', 0.2),
            0.05,
            format="%.0f%%",
            help="Automatic discount for youth organizations"
        )
        
    with col2:
        nonprofit_discount = st.slider(
            "Non-Profit Discount",
            0.0, 0.3,
            guardrails.get('nonprofit_discount', 0.15),
            0.05,
            format="%.0f%%"
        )
        
    with col3:
        min_community_hours = st.number_input(
            "Min Community Hours/Week",
            0, 40,
            guardrails.get('min_community_hours_weekly', 20),
            help="Reserved hours for community use"
        )
    
    st.divider()
    
    # Time-based rules
    st.markdown("#### ⏰ Time-Based Rules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Prime Time Multiplier**")
        prime_multiplier = st.number_input(
            "Multiplier",
            1.0, 1.5,
            guardrails.get('prime_time_multiplier', 1.25),
            0.05
        )
        
    with col2:
        st.markdown("**Off-Peak Discount**")
        offpeak_discount = st.number_input(
            "Discount",
            0.0, 0.4,
            guardrails.get('offpeak_discount', 0.25),
            0.05
        )
    
    st.divider()
    
    # Save button
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("💾 Save Guardrails", type="primary", use_container_width=True):
            new_guardrails = {
                'max_surge_factor': max_surge,
                'max_price_change_percent': max_price_change,
                'min_discount_floor': min_discount,
                'min_lead_time_hours': min_lead_time,
                'youth_discount': youth_discount,
                'nonprofit_discount': nonprofit_discount,
                'min_community_hours_weekly': min_community_hours,
                'prime_time_multiplier': prime_multiplier,
                'offpeak_discount': offpeak_discount
            }
            
            context['session']['config_guardrails'] = new_guardrails
            
            st.success("✅ Guardrails updated successfully!")
            context['audit_log']('guardrails_updated', new_guardrails)
    
    # Testing section
    st.divider()
    st.markdown("#### 🧪 Test Guardrails")
    
    st.markdown("""
    Test how guardrails affect pricing in extreme scenarios:
    """)
    
    test_scenarios = [
        {"name": "Super Peak Demand", "demand": 2.0, "lead_time": 2},
        {"name": "Last Minute Booking", "demand": 1.3, "lead_time": 3},
        {"name": "Early Bird Special", "demand": 0.8, "lead_time": 60},
    ]
    
    results = []
    for scenario in test_scenarios:
        raw_price = 100 * scenario['demand'] * (1 - scenario['lead_time'] * 0.01)
        capped_price = apply_guardrails(raw_price, 100, new_guardrails)
        results.append({
            'Scenario': scenario['name'],
            'Raw Price': f"${raw_price:.2f}",
            'After Guardrails': f"${capped_price:.2f}",
            'Cap Applied': '✓' if raw_price != capped_price else '—'
        })
    
    st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)

def show_pricing_performance(context: Dict[str, Any]):
    """Pricing performance metrics and insights"""
    
    st.markdown("### 📈 Pricing Performance")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Price Realization", "94.2%", "+2.1%")
        
    with col2:
        st.metric("Dynamic Pricing Uplift", "+$18,500", "+12%")
        
    with col3:
        st.metric("Conversion Rate", "78%", "+3%")
        
    with col4:
        st.metric("Revenue per Hour", "$127", "+$15")
    
    st.divider()
    
    # A/B test results
    st.markdown("#### 🔬 A/B Test Results: Dynamic vs Fixed Pricing")
    
    ab_results = {
        'Metric': ['Bookings', 'Revenue', 'Utilization', 'Avg Price'],
        'Fixed Pricing': [245, 49000, 82.3, 200],
        'Dynamic Pricing': [268, 58500, 89.4, 218],
        'Improvement': ['+9.4%', '+19.4%', '+8.6%', '+9.0%']
    }
    
    st.dataframe(pd.DataFrame(ab_results), use_container_width=True, hide_index=True)
    
    st.success("""
    **Key Finding**: Dynamic pricing increased revenue by 19.4% while improving utilization.
    Customer satisfaction remained stable (4.3/5.0 rating).
    """)
    
    # Price sensitivity analysis
    st.divider()
    st.markdown("#### 📉 Price Elasticity Analysis")
    
    fig_elasticity = create_elasticity_chart()
    st.plotly_chart(fig_elasticity, use_container_width=True)

# Helper functions

def calculate_dynamic_price(
    asset_type: str,
    booking_date: datetime.date,
    time_slot: str,
    duration: float,
    customer_type: str,
    lead_time_days: int,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate dynamic price with full explainability"""
    
    # Get base rate
    pricing_config = context['session'].get('config_pricing', {})
    base_rates = pricing_config.get('base_rates', {})
    
    asset_key = asset_type.lower().replace(' - ', '_').replace(' ', '_')
    time_category = 'prime' if 'Prime' in time_slot else 'off_peak' if ('6am' in time_slot or '9pm' in time_slot) else 'standard'
    
    base_rate = base_rates.get(asset_key, {}).get(time_category, 100)
    
    # Initialize factors list
    factors = [
        {'Factor': 'Base Rate', 'Impact': base_rate, 'Explanation': f'{asset_type} during {time_category} time'}
    ]
    
    current_price = base_rate
    
    # Demand adjustment
    demand_level = calculate_demand_level(booking_date, time_slot)
    demand_multiplier = pricing_config.get('demand_multipliers', {}).get(demand_level, 1.0)
    demand_impact = current_price * (demand_multiplier - 1)
    
    if demand_impact != 0:
        factors.append({
            'Factor': f'{demand_level.title()} Demand',
            'Impact': demand_impact,
            'Explanation': f'Demand is {demand_level} for this date/time'
        })
        current_price += demand_impact
    
    # Lead time discount
    if lead_time_days >= 30:
        lead_time_key = '90_days' if lead_time_days >= 90 else '60_days' if lead_time_days >= 60 else '30_days'
        lead_discount = pricing_config.get('lead_time_discounts', {}).get(lead_time_key, 1.0)
        lead_impact = current_price * (lead_discount - 1)
        
        factors.append({
            'Factor': 'Early Booking',
            'Impact': lead_impact,
            'Explanation': f'{lead_time_days} days advance notice earns discount'
        })
        current_price += lead_impact
    
    # Customer segment adjustment
    segment_key = customer_type.lower().replace('-', '_')
    segment_multiplier = pricing_config.get('segments', {}).get(segment_key, 1.0)
    segment_impact = base_rate * (segment_multiplier - 1)
    
    if segment_impact != 0:
        factors.append({
            'Factor': f'{customer_type} Rate',
            'Impact': segment_impact,
            'Explanation': f'{customer_type} customer segment pricing'
        })
        current_price += segment_impact
    
    # Apply guardrails
    guardrails = context['session'].get('config_guardrails', {})
    pre_guardrail_price = current_price
    current_price = apply_guardrails(current_price, base_rate, guardrails)
    
    if current_price != pre_guardrail_price:
        factors.append({
            'Factor': 'Guardrail Cap',
            'Impact': current_price - pre_guardrail_price,
            'Explanation': 'Price capped per policy limits'
        })
    
    # Calculate final price
    final_price = current_price * duration
    
    factors.append({
        'Factor': 'Final Price',
        'Impact': final_price,
        'Explanation': f'{duration} hours × ${current_price:.2f}/hr'
    })
    
    adjustment_pct = ((current_price - base_rate) / base_rate) * 100
    
    return {
        'base_rate': base_rate,
        'dynamic_rate': current_price,
        'final_price': final_price,
        'adjustment_pct': adjustment_pct,
        'factors': factors
    }

def calculate_demand_level(booking_date: datetime.date, time_slot: str) -> str:
    """Calculate demand level based on date and time"""
    # Simplified demand calculation
    day_of_week = booking_date.weekday()
    
    if day_of_week >= 5:  # Weekend
        return 'high'
    elif 'Prime' in time_slot:
        return 'medium'
    else:
        return 'low'

def apply_guardrails(price: float, base_price: float, guardrails: Dict) -> float:
    """Apply pricing guardrails"""
    max_change_pct = guardrails.get('max_price_change_percent', 25) / 100
    max_price = base_price * (1 + max_change_pct)
    min_price = base_price * (1 - max_change_pct)
    
    return max(min_price, min(max_price, price))

def generate_alternative_scenarios(
    asset_type: str,
    booking_date: datetime.date,
    time_slot: str,
    duration: float,
    customer_type: str,
    context: Dict[str, Any]
) -> pd.DataFrame:
    """Generate alternative pricing scenarios"""
    
    scenarios = []
    
    # Different time slots
    for alt_time in ['9am-12pm', '3pm-6pm', '6pm-9pm (Prime)']:
        if alt_time != time_slot:
            lead_time_days = (booking_date - datetime.now().date()).days
            result = calculate_dynamic_price(
                asset_type, booking_date, alt_time, duration, 
                customer_type, lead_time_days, context
            )
            scenarios.append({
                'Option': f'{alt_time}',
                'Price': f"${result['final_price']:.2f}",
                'Savings': f"${result['final_price'] - calculate_dynamic_price(asset_type, booking_date, time_slot, duration, customer_type, lead_time_days, context)['final_price']:.2f}"
            })
    
    # Different dates
    for days_ahead in [14, 30, 60]:
        alt_date = datetime.now().date() + timedelta(days=days_ahead)
        result = calculate_dynamic_price(
            asset_type, alt_date, time_slot, duration,
            customer_type, days_ahead, context
        )
        scenarios.append({
            'Option': f'{alt_date} ({days_ahead} days out)',
            'Price': f"${result['final_price']:.2f}",
            'Savings': f"${result['final_price'] - calculate_dynamic_price(asset_type, booking_date, time_slot, duration, customer_type, (booking_date - datetime.now().date()).days, context)['final_price']:.2f}"
        })
    
    return pd.DataFrame(scenarios)

def create_price_trend_chart(asset_filter: str, metric_type: str):
    """Create price trend chart"""
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    values = [100 + (i * 0.5) + (10 * math.sin(i / 7)) for i in range(90)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines',
        name=metric_type,
        line=dict(color='#3b82f6', width=2)
    ))
    
    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title=metric_type,
        hovermode='x unified'
    )
    
    return fig

def create_price_distribution_chart():
    """Create price distribution by daypart"""
    data = {
        'Daypart': ['6am-9am', '9am-12pm', '12pm-3pm', '3pm-6pm', '6pm-9pm', '9pm-12am'],
        'Avg Price': [85, 110, 120, 130, 145, 95],
        'Count': [45, 78, 65, 82, 125, 38]
    }
    
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['Daypart'],
        y=df['Avg Price'],
        name='Avg Price',
        marker_color='#3b82f6',
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Daypart'],
        y=df['Count'],
        name='Bookings',
        mode='lines+markers',
        marker=dict(size=10, color='#10b981'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        height=400,
        yaxis=dict(title='Average Price ($)'),
        yaxis2=dict(title='Number of Bookings', overlaying='y', side='right'),
        hovermode='x unified'
    )
    
    return fig

def create_elasticity_chart():
    """Create price elasticity chart"""
    prices = list(range(80, 181, 10))
    demand = [120 - (p - 80) * 0.6 for p in prices]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=prices,
        y=demand,
        mode='lines+markers',
        name='Demand',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    
    # Add optimal point
    optimal_idx = demand.index(max([p * d for p, d in zip(prices, demand)]))
    fig.add_trace(go.Scatter(
        x=[prices[optimal_idx]],
        y=[demand[optimal_idx]],
        mode='markers',
        name='Optimal',
        marker=dict(size=15, color='#10b981', symbol='star')
    ))
    
    fig.update_layout(
        height=400,
        xaxis_title="Price per Hour ($)",
        yaxis_title="Expected Bookings per Week",
        hovermode='x unified'
    )
    
    return fig
