"""
SportAI Database Utilities
Handles database connections, queries, and data persistence
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path: str = "data/sportai.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                name TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        
        # Assets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_id TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                name TEXT NOT NULL,
                capacity INTEGER,
                square_footage INTEGER,
                hourly_rate_prime REAL,
                hourly_rate_standard REAL,
                hourly_rate_offpeak REAL,
                active BOOLEAN DEFAULT 1
            )
        """)
        
        # Bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER,
                customer_name TEXT NOT NULL,
                customer_email TEXT,
                customer_type TEXT,
                booking_date DATE NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                duration_hours REAL,
                rate_per_hour REAL,
                total_amount REAL,
                status TEXT DEFAULT 'confirmed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                notes TEXT,
                FOREIGN KEY (asset_id) REFERENCES assets(id)
            )
        """)
        
        # Members table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                tier TEXT,
                credits_balance REAL DEFAULT 0,
                join_date DATE,
                status TEXT DEFAULT 'active',
                household_id TEXT,
                notes TEXT
            )
        """)
        
        # Sponsors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sponsors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                industry TEXT,
                contact_name TEXT,
                contact_email TEXT,
                contact_phone TEXT,
                status TEXT DEFAULT 'active',
                tier TEXT,
                annual_value REAL,
                contract_start DATE,
                contract_end DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Sponsorship assets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sponsorship_assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sponsor_id INTEGER,
                asset_name TEXT NOT NULL,
                asset_category TEXT,
                annual_value REAL,
                start_date DATE,
                end_date DATE,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (sponsor_id) REFERENCES sponsors(id)
            )
        """)
        
        # Contracts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                party_id INTEGER,
                party_type TEXT,
                contract_type TEXT,
                start_date DATE,
                end_date DATE,
                annual_value REAL,
                total_value REAL,
                status TEXT DEFAULT 'active',
                document_url TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_date DATE NOT NULL,
                transaction_type TEXT,
                category TEXT,
                amount REAL NOT NULL,
                description TEXT,
                reference_id TEXT,
                reference_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Audit log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                user_role TEXT,
                action TEXT,
                details TEXT,
                ip_address TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def insert_booking(self, booking_data: Dict) -> int:
        """Insert new booking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO bookings (
                asset_id, customer_name, customer_email, customer_type,
                booking_date, start_time, end_time, duration_hours,
                rate_per_hour, total_amount, status, created_by, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            booking_data.get('asset_id'),
            booking_data.get('customer_name'),
            booking_data.get('customer_email'),
            booking_data.get('customer_type'),
            booking_data.get('booking_date'),
            booking_data.get('start_time'),
            booking_data.get('end_time'),
            booking_data.get('duration_hours'),
            booking_data.get('rate_per_hour'),
            booking_data.get('total_amount'),
            booking_data.get('status', 'confirmed'),
            booking_data.get('created_by'),
            booking_data.get('notes')
        ))
        
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return booking_id
    
    def get_bookings(self, start_date: str = None, end_date: str = None, 
                     asset_id: int = None) -> pd.DataFrame:
        """Get bookings with optional filters"""
        conn = self.get_connection()
        
        query = "SELECT * FROM bookings WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND booking_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND booking_date <= ?"
            params.append(end_date)
        
        if asset_id:
            query += " AND asset_id = ?"
            params.append(asset_id)
        
        query += " ORDER BY booking_date, start_time"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def insert_member(self, member_data: Dict) -> int:
        """Insert new member"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO members (
                member_id, name, email, phone, tier, credits_balance,
                join_date, status, household_id, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            member_data.get('member_id'),
            member_data.get('name'),
            member_data.get('email'),
            member_data.get('phone'),
            member_data.get('tier'),
            member_data.get('credits_balance', 0),
            member_data.get('join_date'),
            member_data.get('status', 'active'),
            member_data.get('household_id'),
            member_data.get('notes')
        ))
        
        member_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return member_id
    
    def get_members(self, status: str = None) -> pd.DataFrame:
        """Get members with optional status filter"""
        conn = self.get_connection()
        
        query = "SELECT * FROM members"
        params = []
        
        if status:
            query += " WHERE status = ?"
            params.append(status)
        
        query += " ORDER BY name"
        
        df = pd.read_sql_query(query, conn, params=params if params else None)
        conn.close()
        
        return df
    
    def insert_sponsor(self, sponsor_data: Dict) -> int:
        """Insert new sponsor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sponsors (
                name, industry, contact_name, contact_email, contact_phone,
                status, tier, annual_value, contract_start, contract_end
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sponsor_data.get('name'),
            sponsor_data.get('industry'),
            sponsor_data.get('contact_name'),
            sponsor_data.get('contact_email'),
            sponsor_data.get('contact_phone'),
            sponsor_data.get('status', 'active'),
            sponsor_data.get('tier'),
            sponsor_data.get('annual_value'),
            sponsor_data.get('contract_start'),
            sponsor_data.get('contract_end')
        ))
        
        sponsor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return sponsor_id
    
    def log_audit(self, user_id: str, user_role: str, action: str, 
                  details: Dict, ip_address: str = None):
        """Log audit trail"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO audit_log (user_id, user_role, action, details, ip_address)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            user_role,
            action,
            json.dumps(details),
            ip_address
        ))
        
        conn.commit()
        conn.close()
    
    def get_revenue_summary(self, start_date: str, end_date: str) -> Dict:
        """Get revenue summary for date range"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as booking_count,
                SUM(total_amount) as total_revenue,
                AVG(total_amount) as avg_booking_value,
                SUM(duration_hours) as total_hours
            FROM bookings
            WHERE booking_date BETWEEN ? AND ?
            AND status = 'confirmed'
        """, (start_date, end_date))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'booking_count': result[0] or 0,
            'total_revenue': result[1] or 0,
            'avg_booking_value': result[2] or 0,
            'total_hours': result[3] or 0
        }
    
    def get_utilization_stats(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Get utilization statistics by asset"""
        conn = self.get_connection()
        
        query = """
            SELECT 
                a.name as asset_name,
                a.asset_type,
                COUNT(b.id) as booking_count,
                SUM(b.duration_hours) as booked_hours,
                SUM(b.total_amount) as revenue
            FROM assets a
            LEFT JOIN bookings b ON a.id = b.asset_id
                AND b.booking_date BETWEEN ? AND ?
                AND b.status = 'confirmed'
            WHERE a.active = 1
            GROUP BY a.id, a.name, a.asset_type
            ORDER BY revenue DESC
        """
        
        df = pd.read_sql_query(query, conn, params=[start_date, end_date])
        conn.close()
        
        return df
    
    def seed_sample_data(self):
        """Seed database with sample data for testing"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Sample assets
        assets = [
            ('skill_shot_main', 'turf_full', 'Turf Field - Full', 22, 7200, 275, 200, 150),
            ('skill_shot_main', 'court', 'Court 1', 12, 900, 45, 35, 25),
            ('skill_shot_main', 'court', 'Court 2', 12, 900, 45, 35, 25),
            ('skill_shot_main', 'golf_bay', 'Golf Bay 1', 6, 400, 55, 45, 35),
            ('skill_shot_main', 'suite', 'Suite A', 20, 1200, 200, 150, 100),
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO assets (
                site_id, asset_type, name, capacity, square_footage,
                hourly_rate_prime, hourly_rate_standard, hourly_rate_offpeak
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, assets)
        
        conn.commit()
        conn.close()

# Global database instance
db = DatabaseManager()
