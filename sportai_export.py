"""
SportAI Export Utilities
Handles PDF and Excel export functionality
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import io

class ExportManager:
    """Manages data export to various formats"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def export_to_excel(self, data: Dict[str, pd.DataFrame], filename: str = None) -> bytes:
        """
        Export multiple dataframes to Excel with multiple sheets
        
        Args:
            data: Dict of {sheet_name: dataframe}
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Excel file as bytes
        """
        if filename is None:
            filename = f"sportai_export_{self.timestamp}.xlsx"
        
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for sheet_name, df in data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Get workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]
                
                # Add header format
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#3b82f6',
                    'font_color': 'white',
                    'border': 1
                })
                
                # Apply header format
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # Auto-fit columns
                for i, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(str(col))
                    ) + 2
                    worksheet.set_column(i, i, max_length)
        
        output.seek(0)
        return output.getvalue()
    
    def export_board_packet(self, data: Dict[str, Any]) -> bytes:
        """
        Export comprehensive board packet to Excel
        
        Args:
            data: Dict containing all board report data
            
        Returns:
            Excel file as bytes
        """
        sheets = {}
        
        # Executive Summary
        if 'executive_summary' in data:
            sheets['Executive Summary'] = pd.DataFrame(data['executive_summary'])
        
        # Financial Summary
        if 'financials' in data:
            sheets['Financials'] = pd.DataFrame(data['financials'])
        
        # Utilization
        if 'utilization' in data:
            sheets['Utilization'] = pd.DataFrame(data['utilization'])
        
        # Sponsorships
        if 'sponsorships' in data:
            sheets['Sponsorships'] = pd.DataFrame(data['sponsorships'])
        
        # Memberships
        if 'memberships' in data:
            sheets['Memberships'] = pd.DataFrame(data['memberships'])
        
        return self.export_to_excel(sheets, f"board_packet_{self.timestamp}.xlsx")
    
    def export_sponsor_proposal(self, sponsor_data: Dict[str, Any]) -> bytes:
        """
        Export sponsor proposal to Excel
        
        Args:
            sponsor_data: Sponsor proposal information
            
        Returns:
            Excel file as bytes
        """
        sheets = {}
        
        # Proposal overview
        if 'overview' in sponsor_data:
            sheets['Proposal Overview'] = pd.DataFrame([sponsor_data['overview']])
        
        # Assets
        if 'assets' in sponsor_data:
            sheets['Assets'] = pd.DataFrame(sponsor_data['assets'])
        
        # Pricing
        if 'pricing' in sponsor_data:
            sheets['Pricing'] = pd.DataFrame(sponsor_data['pricing'])
        
        # ROI Projections
        if 'roi' in sponsor_data:
            sheets['ROI Projections'] = pd.DataFrame(sponsor_data['roi'])
        
        sponsor_name = sponsor_data.get('sponsor_name', 'sponsor')
        filename = f"proposal_{sponsor_name}_{self.timestamp}.xlsx"
        
        return self.export_to_excel(sheets, filename)
    
    def export_financial_report(self, financial_data: Dict[str, Any]) -> bytes:
        """
        Export financial report to Excel
        
        Args:
            financial_data: Financial report data
            
        Returns:
            Excel file as bytes
        """
        sheets = {
            'P&L Summary': pd.DataFrame(financial_data.get('pl_summary', [])),
            'Balance Sheet': pd.DataFrame(financial_data.get('balance_sheet', [])),
            'Cash Flow': pd.DataFrame(financial_data.get('cash_flow', [])),
            'Budget Variance': pd.DataFrame(financial_data.get('budget_variance', []))
        }
        
        return self.export_to_excel(sheets, f"financial_report_{self.timestamp}.xlsx")
    
    def export_to_csv(self, df: pd.DataFrame, filename: str = None) -> bytes:
        """
        Export dataframe to CSV
        
        Args:
            df: DataFrame to export
            filename: Optional filename
            
        Returns:
            CSV file as bytes
        """
        if filename is None:
            filename = f"sportai_export_{self.timestamp}.csv"
        
        return df.to_csv(index=False).encode('utf-8')
    
    def create_download_link(self, data: bytes, filename: str, file_type: str = "xlsx") -> str:
        """
        Create download link for Streamlit
        
        Args:
            data: File data as bytes
            filename: Filename for download
            file_type: File extension (xlsx, csv, pdf)
            
        Returns:
            HTML download link
        """
        import base64
        
        b64 = base64.b64encode(data).decode()
        
        mime_types = {
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'csv': 'text/csv',
            'pdf': 'application/pdf'
        }
        
        mime = mime_types.get(file_type, 'application/octet-stream')
        
        return f'<a href="data:{mime};base64,{b64}" download="{filename}">Download {filename}</a>'


class ReportGenerator:
    """Generate formatted reports"""
    
    def __init__(self):
        self.timestamp = datetime.now()
    
    def generate_executive_summary(self, data: Dict[str, Any]) -> str:
        """Generate executive summary text"""
        
        summary = f"""
# EXECUTIVE SUMMARY
## Skill Shot Sports Facility
### Generated: {self.timestamp.strftime("%B %d, %Y")}

---

## KEY PERFORMANCE INDICATORS

- **Total Revenue (Period):** ${data.get('revenue', 0):,.2f}
- **Facility Utilization:** {data.get('utilization', 0):.1f}%
- **Active Memberships:** {data.get('members', 0):,}
- **Net Profit Margin:** {data.get('margin', 0):.1f}%

## HIGHLIGHTS

{data.get('highlights', 'No highlights available')}

## FINANCIAL HEALTH

- **DSCR:** {data.get('dscr', 0):.2f}
- **Cash Reserves:** ${data.get('cash', 0):,.2f}
- **Operating Margin:** {data.get('operating_margin', 0):.1f}%

## STRATEGIC PRIORITIES

{data.get('priorities', 'No priorities listed')}

---

*This report was automatically generated by SportAI*
        """
        
        return summary
    
    def generate_sponsor_proposal_text(self, sponsor_data: Dict[str, Any]) -> str:
        """Generate sponsor proposal text"""
        
        sponsor_name = sponsor_data.get('sponsor_name', 'Valued Partner')
        total_value = sponsor_data.get('total_value', 0)
        
        proposal = f"""
# SPONSORSHIP PROPOSAL
## {sponsor_name}
### Presented by Skill Shot Sports Facility
### {self.timestamp.strftime("%B %d, %Y")}

---

## EXECUTIVE SUMMARY

We are pleased to present this exclusive sponsorship opportunity for {sponsor_name}.

**Total Package Value:** ${total_value:,.2f}

## PACKAGE DETAILS

{sponsor_data.get('package_description', 'Package details')}

## BRAND EXPOSURE

{sponsor_data.get('exposure_details', 'Exposure metrics')}

## INVESTMENT BREAKDOWN

{sponsor_data.get('investment_breakdown', 'Investment details')}

## NEXT STEPS

1. Review this proposal
2. Schedule a meeting to discuss details
3. Finalize agreement and execute contract

---

**Contact:** {sponsor_data.get('contact_name', 'Facility Manager')}
**Email:** {sponsor_data.get('contact_email', 'info@skillshot.com')}
**Phone:** {sponsor_data.get('contact_phone', '(555) 123-4567')}

        """
        
        return proposal


# Convenience functions for Streamlit integration

def download_excel_button(data: Dict[str, pd.DataFrame], filename: str, button_text: str = "Download Excel"):
    """
    Create Streamlit download button for Excel export
    
    Usage:
        import streamlit as st
        from utils.export import download_excel_button
        
        data = {
            'Sheet1': pd.DataFrame(...),
            'Sheet2': pd.DataFrame(...)
        }
        download_excel_button(data, 'my_report.xlsx')
    """
    import streamlit as st
    
    exporter = ExportManager()
    excel_data = exporter.export_to_excel(data, filename)
    
    st.download_button(
        label=button_text,
        data=excel_data,
        file_name=filename,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def download_csv_button(df: pd.DataFrame, filename: str, button_text: str = "Download CSV"):
    """
    Create Streamlit download button for CSV export
    
    Usage:
        import streamlit as st
        from utils.export import download_csv_button
        
        df = pd.DataFrame(...)
        download_csv_button(df, 'data.csv')
    """
    import streamlit as st
    
    exporter = ExportManager()
    csv_data = exporter.export_to_csv(df, filename)
    
    st.download_button(
        label=button_text,
        data=csv_data,
        file_name=filename,
        mime='text/csv'
    )
