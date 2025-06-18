import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Optional
import sqlite3
import os
import locale
import streamlit.components.v1 as components
import random
import math

# Page configuration
st.set_page_config(
    page_title="台灣銀行匯率追蹤器",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to hide cursor on selectbox and improve styling
st.markdown("""
<style>
    /* Hide cursor on selectbox */
    .stSelectbox > div > div > div > div {
        cursor: default !important;
    }
    
    /* Hide cursor on multiselect */
    .stMultiSelect > div > div > div > div {
        cursor: default !important;
    }
    
    /* Improve selectbox appearance */
    .stSelectbox > div > div > div {
        cursor: default !important;
        user-select: none;
    }
    
    /* Custom styling for volume cards */
    .volume-card {
        background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    /* Trading volume indicators */
    .volume-high { color: #28a745; font-weight: bold; }
    .volume-medium { color: #ffc107; font-weight: bold; }
    .volume-low { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Multi-language support
class LanguageManager:
    def __init__(self):
        self.translations = {
            'en': {
                'title': '💱 Taiwan Bank Exchange Rate Tracker',
                'subtitle': 'Track real-time and historical exchange rates for 23 currencies (TWD base)',
                'settings': 'Settings',
                'language': 'Language',
                'auto_refresh': 'Auto-refresh data',
                'refresh_interval': 'Refresh interval (minutes)',
                'time_period': 'Select time period for charts',
                'current_rates': '📊 Current Rates',
                'trend_charts': '📈 Trend Charts',
                'currency_comparison': '🔍 Currency Comparison',
                'currency_converter': '🧮 Currency Converter',
                'trading_volume': '📊 Trading Volume',
                'statistics': '📋 Statistics',
                'fetching_rates': 'Fetching latest exchange rates...',
                'current_rates_title': 'Current Exchange Rates (TWD Base)',
                'currency': 'Currency',
                'rate': 'Rate (TWD)',
                'change': 'Change',
                'change_percent': 'Change %',
                'trend': 'Trend',
                'gainers': 'Stronger vs TWD',
                'losers': 'Weaker vs TWD',
                'total_currencies': 'Total Currencies',
                'avg_change': 'Avg Change %',
                'trend_title': 'Exchange Rate Trends vs TWD',
                'select_currency': 'Select currency to view trend',
                'current_rate': 'Current Rate',
                'min_rate': 'Min Rate',
                'max_rate': 'Max Rate',
                'volatility': 'Volatility',
                'no_data': 'No historical data available for',
                'comparison_title': 'Currency Comparison vs TWD',
                'select_currencies': 'Select currencies to compare',
                'performance_summary': 'Performance Summary',
                'converter_title': 'Currency Converter',
                'from_currency': 'From Currency',
                'to_currency': 'To Currency',
                'amount': 'Amount',
                'exchange_rate': 'Exchange Rate',
                'market_stats': 'Market Statistics',
                'market_overview': 'Market Overview',
                'top_gainers': '🔝 Strongest vs TWD',
                'top_losers': '📉 Weakest vs TWD',
                'volatility_ranking': '📊 Volatility Ranking',
                'trading_volume_title': 'Trading Volume Analysis',
                'volume_period': 'Select volume period',
                'daily_volume': 'Daily Volume',
                'total_volume': 'Total Volume',
                'avg_volume': 'Average Volume',
                'volume_trend': 'Volume Trend',
                'high_volume': 'High Volume',
                'medium_volume': 'Medium Volume',
                'low_volume': 'Low Volume',
                'volume_chart_title': 'Trading Volume Chart',
                'volume_summary': 'Volume Summary',
                'today': 'Today',
                '7_days': '7 Days',
                '14_days': '14 Days',
                '1_month': '1 Month',
                'data_source': 'Data Source',
                'last_updated': 'Last Updated',
                'network_error': 'Network error',
                'api_error': 'API Error',
                'database_error': 'Database error for',
                'unable_fetch': 'Unable to fetch exchange rate data. Using simulated data.',
                'simulated_note': '* Using simulated historical data based on real market patterns',
                'periods': {
                    '1 Month': '1 Month',
                    '3 Months': '3 Months', 
                    '6 Months': '6 Months',
                    '1 Year': '1 Year',
                    '3 Years': '3 Years',
                    '5 Years': '5 Years',
                    '10 Years': '10 Years'
                }
            },
            'zh-TW': {
                'title': '💱 台灣銀行匯率追蹤器',
                'subtitle': '追蹤新台幣兌換23種世界貨幣的即時和歷史匯率',
                'settings': '設定',
                'language': '語言',
                'auto_refresh': '自動刷新數據',
                'refresh_interval': '刷新間隔（分鐘）',
                'time_period': '選擇圖表時間區間',
                'current_rates': '📊 即時匯率',
                'trend_charts': '📈 趨勢圖表',
                'currency_comparison': '🔍 貨幣比較',
                'currency_converter': '🧮 貨幣轉換器',
                'trading_volume': '📊 交易量分析',
                'statistics': '📋 統計數據',
                'fetching_rates': '正在獲取最新匯率...',
                'current_rates_title': '即時匯率（以新台幣為基準）',
                'currency': '貨幣',
                'rate': '匯率 (TWD)',
                'change': '變化',
                'change_percent': '變化%',
                'trend': '趨勢',
                'gainers': '對台幣升值',
                'losers': '對台幣貶值',
                'total_currencies': '總貨幣數',
                'avg_change': '平均變化%',
                'trend_title': '對新台幣匯率趨勢',
                'select_currency': '選擇要查看趨勢的貨幣',
                'current_rate': '目前匯率',
                'min_rate': '最低匯率',
                'max_rate': '最高匯率',
                'volatility': '波動性',
                'no_data': '沒有歷史數據可用於',
                'comparison_title': '對新台幣貨幣比較',
                'select_currencies': '選擇要比較的貨幣',
                'performance_summary': '表現摘要',
                'converter_title': '貨幣轉換器',
                'from_currency': '來源貨幣',
                'to_currency': '目標貨幣',
                'amount': '金額',
                'exchange_rate': '匯率',
                'market_stats': '市場統計',
                'market_overview': '市場概況',
                'top_gainers': '🔝 對台幣最強勢',
                'top_losers': '📉 對台幣最弱勢',
                'volatility_ranking': '📊 波動性排名',
                'trading_volume_title': '交易量分析',
                'volume_period': '選擇交易量期間',
                'daily_volume': '每日交易量',
                'total_volume': '總交易量',
                'avg_volume': '平均交易量',
                'volume_trend': '交易量趨勢',
                'high_volume': '高交易量',
                'medium_volume': '中等交易量',
                'low_volume': '低交易量',
                'volume_chart_title': '交易量圖表',
                'volume_summary': '交易量摘要',
                'today': '今日',
                '7_days': '7天',
                '14_days': '14天',
                '1_month': '1個月',
                'data_source': '數據來源',
                'last_updated': '最後更新',
                'network_error': '網路錯誤',
                'api_error': 'API錯誤',
                'database_error': '資料庫錯誤',
                'unable_fetch': '無法獲取匯率數據，使用模擬數據。',
                'simulated_note': '* 使用基於真實市場模式的模擬歷史數據',
                'periods': {
                    '1 Month': '1個月',
                    '3 Months': '3個月',
                    '6 Months': '6個月', 
                    '1 Year': '1年',
                    '3 Years': '3年',
                    '5 Years': '5年',
                    '10 Years': '10年'
                }
            },
            'zh-CN': {
                'title': '💱 台湾银行汇率跟踪器',
                'subtitle': '跟踪新台币兑换23种世界货币的实时和历史汇率',
                'settings': '设置',
                'language': '语言',
                'auto_refresh': '自动刷新数据',
                'refresh_interval': '刷新间隔（分钟）',
                'time_period': '选择图表时间区间',
                'current_rates': '📊 实时汇率',
                'trend_charts': '📈 趋势图表',
                'currency_comparison': '🔍 货币比较',
                'currency_converter': '🧮 货币转换器',
                'trading_volume': '📊 交易量分析',
                'statistics': '📋 统计数据',
                'fetching_rates': '正在获取最新汇率...',
                'current_rates_title': '实时汇率（以新台币为基准）',
                'currency': '货币',
                'rate': '汇率 (TWD)',
                'change': '变化',
                'change_percent': '变化%',
                'trend': '趋势',
                'gainers': '对台币升值',
                'losers': '对台币贬值',
                'total_currencies': '总货币数',
                'avg_change': '平均变化%',
                'trend_title': '对新台币汇率趋势',
                'select_currency': '选择要查看趋势的货币',
                'current_rate': '当前汇率',
                'min_rate': '最低汇率',
                'max_rate': '最高汇率',
                'volatility': '波动性',
                'no_data': '没有历史数据可用于',
                'comparison_title': '对新台币货币比较',
                'select_currencies': '选择要比较的货币',
                'performance_summary': '表现摘要',
                'converter_title': '货币转换器',
                'from_currency': '源货币',
                'to_currency': '目标货币',
                'amount': '金额',
                'exchange_rate': '汇率',
                'market_stats': '市场统计',
                'market_overview': '市场概况',
                'top_gainers': '🔝 对台币最强势',
                'top_losers': '📉 对台币最弱势',
                'volatility_ranking': '📊 波动性排名',
                'trading_volume_title': '交易量分析',
                'volume_period': '选择交易量期间',
                'daily_volume': '每日交易量',
                'total_volume': '总交易量',
                'avg_volume': '平均交易量',
                'volume_trend': '交易量趋势',
                'high_volume': '高交易量',
                'medium_volume': '中等交易量',
                'low_volume': '低交易量',
                'volume_chart_title': '交易量图表',
                'volume_summary': '交易量摘要',
                'today': '今日',
                '7_days': '7天',
                '14_days': '14天',
                '1_month': '1个月',
                'data_source': '数据来源',
                'last_updated': '最后更新',
                'network_error': '网络错误',
                'api_error': 'API错误',
                'database_error': '数据库错误',
                'unable_fetch': '无法获取汇率数据，使用模拟数据。',
                'simulated_note': '* 使用基于真实市场模式的模拟历史数据',
                'periods': {
                    '1 Month': '1个月',
                    '3 Months': '3个月',
                    '6 Months': '6个月',
                    '1 Year': '1年',
                    '3 Years': '3年',
                    '5 Years': '5年',
                    '10 Years': '10年'
                }
            },
            'ja': {
                'title': '💱 台湾銀行為替レート追跡ツール',
                'subtitle': '台湾ドル対23種類の世界通貨のリアルタイムおよび過去の為替レートを追跡',
                'settings': '設定',
                'language': '言語',
                'auto_refresh': 'データの自動更新',
                'refresh_interval': '更新間隔（分）',
                'time_period': 'チャートの期間を選択',
                'current_rates': '📊 現在のレート',
                'trend_charts': '📈 トレンドチャート',
                'currency_comparison': '🔍 通貨比較',
                'currency_converter': '🧮 通貨コンバーター',
                'trading_volume': '📊 取引量分析',
                'statistics': '📋 統計',
                'fetching_rates': '最新の為替レートを取得中...',
                'current_rates_title': '現在の為替レート（台湾ドル基準）',
                'currency': '通貨',
                'rate': 'レート (TWD)',
                'change': '変化',
                'change_percent': '変化%',
                'trend': 'トレンド',
                'gainers': '台湾ドルに対し上昇',
                'losers': '台湾ドルに対し下落',
                'total_currencies': '総通貨数',
                'avg_change': '平均変化%',
                'trend_title': '台湾ドル対為替レートトレンド',
                'select_currency': 'トレンドを表示する通貨を選択',
                'current_rate': '現在のレート',
                'min_rate': '最低レート',
                'max_rate': '最高レート',
                'volatility': 'ボラティリティ',
                'no_data': '利用可能な過去データがありません',
                'comparison_title': '台湾ドル対通貨比較',
                'select_currencies': '比較する通貨を選択',
                'performance_summary': 'パフォーマンス概要',
                'converter_title': '通貨コンバーター',
                'from_currency': '元の通貨',
                'to_currency': '変換先通貨',
                'amount': '金額',
                'exchange_rate': '為替レート',
                'market_stats': '市場統計',
                'market_overview': '市場概況',
                'top_gainers': '🔝 台湾ドルに対し最強',
                'top_losers': '📉 台湾ドルに対し最弱',
                'volatility_ranking': '📊 ボラティリティランキング',
                'trading_volume_title': '取引量分析',
                'volume_period': '取引量期間を選択',
                'daily_volume': '日次取引量',
                'total_volume': '総取引量',
                'avg_volume': '平均取引量',
                'volume_trend': '取引量トレンド',
                'high_volume': '高取引量',
                'medium_volume': '中取引量',
                'low_volume': '低取引量',
                'volume_chart_title': '取引量チャート',
                'volume_summary': '取引量概要',
                'today': '今日',
                '7_days': '7日',
                '14_days': '14日',
                '1_month': '1か月',
                'data_source': 'データソース',
                'last_updated': '最終更新',
                'network_error': 'ネットワークエラー',
                'api_error': 'APIエラー',
                'database_error': 'データベースエラー',
                'unable_fetch': '為替レートデータを取得できません。シミュレーションデータを使用します。',
                'simulated_note': '* 実際の市場パターンに基づくシミュレーション歴史データを使用',
                'periods': {
                    '1 Month': '1か月',
                    '3 Months': '3か月',
                    '6 Months': '6か月',
                    '1 Year': '1年',
                    '3 Years': '3年',
                    '5 Years': '5年',
                    '10 Years': '10年'
                }
            }
        }
        
        self.languages = {
            'en': 'English',
            'zh-TW': '繁體中文',
            'zh-CN': '简体中文',
            'ja': '日本語'
        }
    
    def detect_language(self):
        """Detect user's language based on browser locale"""
        try:
            # JavaScript to get browser language
            browser_lang_js = """
            <script>
                const lang = navigator.language || navigator.userLanguage || 'zh-TW';
                parent.window.browserLanguage = lang;
            </script>
            """
            components.html(browser_lang_js, height=0)
            
            # Map browser locales to our supported languages
            if hasattr(st.session_state, 'browser_language'):
                browser_lang = st.session_state.browser_language.lower()
            else:
                browser_lang = 'zh-tw'  # Default to Traditional Chinese
            
            if browser_lang.startswith('zh-tw') or browser_lang.startswith('zh-hant'):
                return 'zh-TW'
            elif browser_lang.startswith('zh-cn') or browser_lang.startswith('zh-hans') or browser_lang.startswith('zh'):
                return 'zh-CN'
            elif browser_lang.startswith('ja'):
                return 'ja'
            elif browser_lang.startswith('en'):
                return 'en'
            else:
                return 'zh-TW'  # Default to Traditional Chinese for Taiwan
        except:
            return 'zh-TW'
    
    def get_text(self, key, lang='zh-TW'):
        """Get translated text"""
        try:
            keys = key.split('.')
            text = self.translations[lang]
            for k in keys:
                text = text[k]
            return text
        except (KeyError, TypeError):
            # Fallback to Traditional Chinese
            try:
                keys = key.split('.')
                text = self.translations['zh-TW']
                for k in keys:
                    text = text[k]
                return text
            except:
                return key

class TWDCurrencyTracker:
    def __init__(self):
        self.base_currency = "TWD"
        self.db_file = "twd_currency_data.db"
        self.init_database()
        
        # Top 23 popular currencies to convert to TWD (including Southeast Asian currencies)
        self.popular_currencies = [
            "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD", 
            "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", "RUB", "INR", "BRL", "ZAR",
            "THB", "VND", "MYR"
        ]
        
        # Currency names for better display
        self.currency_names = {
            "TWD": "新台幣 Taiwan Dollar", "USD": "美元 US Dollar", "EUR": "歐元 Euro", 
            "GBP": "英鎊 British Pound", "JPY": "日圓 Japanese Yen",
            "AUD": "澳幣 Australian Dollar", "CAD": "加幣 Canadian Dollar", 
            "CHF": "瑞士法郎 Swiss Franc", "CNY": "人民幣 Chinese Yuan", 
            "SEK": "瑞典克朗 Swedish Krona", "NZD": "紐幣 New Zealand Dollar",
            "MXN": "墨西哥比索 Mexican Peso", "SGD": "新加坡幣 Singapore Dollar", 
            "HKD": "港幣 Hong Kong Dollar", "NOK": "挪威克朗 Norwegian Krone", 
            "KRW": "韓元 South Korean Won", "TRY": "土耳其里拉 Turkish Lira",
            "RUB": "俄羅斯盧布 Russian Ruble", "INR": "印度盧比 Indian Rupee", 
            "BRL": "巴西雷亞爾 Brazilian Real", "ZAR": "南非蘭特 South African Rand",
            "THB": "泰銖 Thai Baht", "VND": "越南盾 Vietnamese Dong", "MYR": "馬來西亞令吉 Malaysian Ringgit"
        }
        
        # Current approximate TWD rates (how much TWD you get for 1 unit of foreign currency)
        self.base_rates = {
            "USD": 30.8, "EUR": 33.5, "GBP": 39.2, "JPY": 0.206, "AUD": 20.4, 
            "CAD": 22.8, "CHF": 34.6, "CNY": 4.25, "SEK": 2.91, "NZD": 18.9,
            "MXN": 1.79, "SGD": 22.9, "HKD": 3.95, "NOK": 2.85, "KRW": 0.0233,
            "TRY": 0.90, "RUB": 0.33, "INR": 0.369, "BRL": 6.18, "ZAR": 1.68,
            "THB": 0.87, "VND": 0.00125, "MYR": 6.95
        }

    def init_database(self):
        """Initialize SQLite database for storing historical data"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create table with new structure
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS twd_exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency TEXT,
                rate REAL,
                volume REAL DEFAULT 0,
                timestamp DATETIME,
                UNIQUE(currency, timestamp)
            )
        ''')
        
        # Check if volume column exists, if not add it
        cursor.execute("PRAGMA table_info(twd_exchange_rates)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'volume' not in columns:
            try:
                cursor.execute('ALTER TABLE twd_exchange_rates ADD COLUMN volume REAL DEFAULT 0')
                st.info("資料庫已升級，新增交易量欄位 / Database upgraded with volume column")
            except sqlite3.Error as e:
                # If ALTER TABLE fails, create a backup and recreate table
                try:
                    # Backup existing data
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS twd_exchange_rates_backup AS 
                        SELECT * FROM twd_exchange_rates
                    ''')
                    
                    # Drop old table
                    cursor.execute('DROP TABLE IF EXISTS twd_exchange_rates')
                    
                    # Create new table with volume column
                    cursor.execute('''
                        CREATE TABLE twd_exchange_rates (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            currency TEXT,
                            rate REAL,
                            volume REAL DEFAULT 0,
                            timestamp DATETIME,
                            UNIQUE(currency, timestamp)
                        )
                    ''')
                    
                    # Restore data with default volume
                    cursor.execute('''
                        INSERT INTO twd_exchange_rates (currency, rate, volume, timestamp)
                        SELECT currency, rate, 0, timestamp FROM twd_exchange_rates_backup
                    ''')
                    
                    # Drop backup table
                    cursor.execute('DROP TABLE IF EXISTS twd_exchange_rates_backup')
                    
                    st.success("資料庫結構已重建並保留歷史數據 / Database structure rebuilt with historical data preserved")
                    
                except sqlite3.Error as backup_error:
                    st.warning(f"資料庫升級失敗，使用新結構 / Database upgrade failed, using new structure: {backup_error}")
        
        conn.commit()
        conn.close()

    def get_current_rates(self) -> Optional[Dict]:
        """Fetch current exchange rates with TWD as base currency"""
        try:
            # Try to get USD to other currencies first, then convert to TWD base
            apis = [
                'https://api.exchangerate.host/latest?base=USD',
                'https://api.fxratesapi.com/latest?base=USD'
            ]
            
            for api_url in apis:
                try:
                    response = requests.get(api_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        usd_rates = data.get('rates', {})
                        
                        if 'TWD' in usd_rates:
                            # Convert to TWD base
                            twd_usd_rate = usd_rates['TWD']  # How much TWD for 1 USD
                            twd_rates = {}
                            
                            # Add USD
                            twd_rates['USD'] = twd_usd_rate
                            
                            # Convert other currencies to TWD base
                            for currency, usd_rate in usd_rates.items():
                                if currency in self.popular_currencies and currency != 'USD':
                                    # TWD per unit of foreign currency = (TWD per USD) / (foreign currency per USD)
                                    twd_rates[currency] = twd_usd_rate / usd_rate
                            
                            return twd_rates
                            
                except requests.exceptions.RequestException:
                    continue
                except Exception:
                    continue
        except Exception:
            pass
        
        # If all APIs fail, return rates based on base_rates with some variation
        st.warning("API 連接失敗，使用模擬數據 / API connection failed, using simulated data")
        return self._get_simulated_rates()

    def _get_simulated_rates(self) -> Dict:
        """Generate simulated rates based on realistic TWD exchange rates"""
        simulated_rates = {}
        for currency, base_rate in self.base_rates.items():
            # Add small random variation (-3% to +3%)
            variation = random.uniform(-0.03, 0.03)
            simulated_rates[currency] = base_rate * (1 + variation)
        
        return simulated_rates

    def save_rates_to_db(self, rates: Dict, volumes: Dict = None):
        """Save current rates and volumes to database"""
        if not rates:
            return
            
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Check if volume column exists
        cursor.execute("PRAGMA table_info(twd_exchange_rates)")
        columns = [column[1] for column in cursor.fetchall()]
        has_volume = 'volume' in columns
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for currency, rate in rates.items():
            if currency in self.popular_currencies:
                try:
                    if has_volume:
                        volume = volumes.get(currency, 0) if volumes else self._generate_volume(currency)
                        cursor.execute(
                            "INSERT OR REPLACE INTO twd_exchange_rates (currency, rate, volume, timestamp) VALUES (?, ?, ?, ?)",
                            (currency, rate, volume, timestamp)
                        )
                    else:
                        # Fallback for old database structure
                        cursor.execute(
                            "INSERT OR REPLACE INTO twd_exchange_rates (currency, rate, timestamp) VALUES (?, ?, ?)",
                            (currency, rate, timestamp)
                        )
                except sqlite3.Error:
                    continue
        
        conn.commit()
        conn.close()

    def _generate_volume(self, currency: str) -> float:
        """Generate realistic trading volume for a currency"""
        # Base volumes in millions TWD equivalent
        base_volumes = {
            'USD': 15000, 'EUR': 8000, 'GBP': 5000, 'JPY': 12000, 'AUD': 3000,
            'CAD': 2000, 'CHF': 1500, 'CNY': 6000, 'SEK': 800, 'NZD': 600,
            'MXN': 400, 'SGD': 2500, 'HKD': 4000, 'NOK': 700, 'KRW': 3500,
            'TRY': 300, 'RUB': 200, 'INR': 1200, 'BRL': 500, 'ZAR': 300,
            'THB': 1800, 'VND': 900, 'MYR': 1100
        }
        
        base_volume = base_volumes.get(currency, 1000)
        
        # Add random variation (±30%)
        variation = random.uniform(0.7, 1.3)
        
        # Add time-based variation (higher volume during business hours)
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:  # Business hours
            time_factor = 1.2
        elif 19 <= current_hour <= 22:  # Evening trading
            time_factor = 0.8
        else:  # Night/early morning
            time_factor = 0.4
        
        return base_volume * variation * time_factor

    def generate_historical_data(self, currency: str, days: int) -> pd.DataFrame:
        """Generate realistic historical data with rates and volumes based on current rates and market patterns"""
        if currency not in self.base_rates:
            return pd.DataFrame()
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Generate date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Base rate and volume for this currency
        base_rate = self.base_rates[currency]
        base_volume = self._get_base_volume(currency)
        
        # Generate realistic price and volume movements
        rates = []
        volumes = []
        current_rate = base_rate
        
        # Different volatility for different currencies
        volatility_map = {
            'USD': 0.008, 'EUR': 0.010, 'GBP': 0.012, 'JPY': 0.008, 'AUD': 0.015,
            'CAD': 0.012, 'CHF': 0.009, 'CNY': 0.006, 'SEK': 0.013, 'NZD': 0.016,
            'MXN': 0.020, 'SGD': 0.008, 'HKD': 0.003, 'NOK': 0.014, 'KRW': 0.012,
            'TRY': 0.030, 'RUB': 0.025, 'INR': 0.010, 'BRL': 0.018, 'ZAR': 0.020,
            'THB': 0.012, 'VND': 0.008, 'MYR': 0.015
        }
        
        volatility = volatility_map.get(currency, 0.012)
        
        # Generate realistic price and volume walk
        for i, date in enumerate(date_range):
            # Price movement
            random_change = np.random.normal(0, volatility)
            trend = math.sin(i * 2 * math.pi / 365) * 0.001  # Annual cycle
            mean_reversion = (base_rate - current_rate) * 0.001  # Mean reversion
            
            change = random_change + trend + mean_reversion
            current_rate = current_rate * (1 + change)
            
            # Ensure rate doesn't go negative or too extreme
            current_rate = max(current_rate, base_rate * 0.5)
            current_rate = min(current_rate, base_rate * 2.0)
            
            # Volume movement (inversely correlated with price stability)
            price_volatility = abs(change)
            volume_multiplier = 1 + (price_volatility * 10)  # Higher volatility = higher volume
            
            # Add random volume variation
            volume_variation = random.uniform(0.6, 1.4)
            
            # Day of week effect (lower volume on weekends)
            weekday = date.weekday()
            if weekday >= 5:  # Weekend
                weekday_factor = 0.3
            else:  # Weekday
                weekday_factor = 1.0
            
            daily_volume = base_volume * volume_multiplier * volume_variation * weekday_factor
            
            rates.append(current_rate)
            volumes.append(daily_volume)
        
        # Create DataFrame
        df = pd.DataFrame({
            'timestamp': date_range,
            'rate': rates,
            'volume': volumes
        })
        
        df.set_index('timestamp', inplace=True)
        return df

    def _get_base_volume(self, currency: str) -> float:
        """Get base trading volume for a currency"""
        base_volumes = {
            'USD': 15000, 'EUR': 8000, 'GBP': 5000, 'JPY': 12000, 'AUD': 3000,
            'CAD': 2000, 'CHF': 1500, 'CNY': 6000, 'SEK': 800, 'NZD': 600,
            'MXN': 400, 'SGD': 2500, 'HKD': 4000, 'NOK': 700, 'KRW': 3500,
            'TRY': 300, 'RUB': 200, 'INR': 1200, 'BRL': 500, 'ZAR': 300,
            'THB': 1800, 'VND': 900, 'MYR': 1100
        }
        return base_volumes.get(currency, 1000)

    def get_historical_data(self, currency: str, days: int) -> pd.DataFrame:
        """Get historical data with rates and volumes (generated if not in database)"""
        conn = sqlite3.connect(self.db_file)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # First check if volume column exists
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(twd_exchange_rates)")
        columns = [column[1] for column in cursor.fetchall()]
        has_volume = 'volume' in columns
        
        if has_volume:
            query = """
                SELECT timestamp, rate, volume 
                FROM twd_exchange_rates 
                WHERE currency = ? 
                AND timestamp >= ? 
                AND timestamp <= ?
                ORDER BY timestamp
            """
        else:
            query = """
                SELECT timestamp, rate 
                FROM twd_exchange_rates 
                WHERE currency = ? 
                AND timestamp >= ? 
                AND timestamp <= ?
                ORDER BY timestamp
            """
        
        try:
            df = pd.read_sql_query(
                query, 
                conn, 
                params=(currency, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            )
        except Exception as e:
            conn.close()
            # If query fails, generate historical data
            return self.generate_historical_data(currency, days)
        
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.set_index('timestamp')
            
            # Add volume column if it doesn't exist
            if 'volume' not in df.columns:
                df['volume'] = df['rate'].apply(lambda x: self._generate_volume(currency))
            # Fill missing volume data if it exists but has null values
            elif df['volume'].isnull().any():
                df['volume'] = df['volume'].fillna(df['rate'].apply(lambda x: self._generate_volume(currency)))
        else:
            # Generate historical data if not in database
            df = self.generate_historical_data(currency, days)
        
        return df

    def get_volume_data(self, currency: str, period: str) -> pd.DataFrame:
        """Get volume data for specific periods"""
        period_days = {
            'today': 1,
            '7_days': 7,
            '14_days': 14,
            '1_month': 30
        }
        
        days = period_days.get(period, 7)
        return self.get_historical_data(currency, days)

    def calculate_statistics(self, df: pd.DataFrame) -> Dict:
        """Calculate statistical metrics for the currency including volume"""
        if df.empty:
            return {}
        
        current_rate = df['rate'].iloc[-1]
        previous_rate = df['rate'].iloc[0] if len(df) > 1 else current_rate
        
        stats = {
            'current': current_rate,
            'change': current_rate - previous_rate,
            'change_percent': ((current_rate - previous_rate) / previous_rate * 100) if previous_rate != 0 else 0,
            'min': df['rate'].min(),
            'max': df['rate'].max(),
            'mean': df['rate'].mean(),
            'volatility': df['rate'].std(),
            'trend': 'up' if current_rate > previous_rate else 'down' if current_rate < previous_rate else 'stable'
        }
        
        # Add volume statistics if volume data exists
        if 'volume' in df.columns and not df['volume'].isnull().all():
            current_volume = df['volume'].iloc[-1] if len(df) > 0 else 0
            previous_volume = df['volume'].iloc[0] if len(df) > 1 else current_volume
            
            stats.update({
                'current_volume': current_volume,
                'total_volume': df['volume'].sum(),
                'avg_volume': df['volume'].mean(),
                'max_volume': df['volume'].max(),
                'min_volume': df['volume'].min(),
                'volume_change': current_volume - previous_volume,
                'volume_change_percent': ((current_volume - previous_volume) / previous_volume * 100) if previous_volume != 0 else 0,
                'volume_trend': 'up' if current_volume > previous_volume else 'down' if current_volume < previous_volume else 'stable'
            })
        
        return stats

def create_trend_chart(df: pd.DataFrame, currency: str, period: str, lang_manager, current_lang):
    """Create interactive trend chart"""
    if df.empty:
        return None
    
    fig = go.Figure()
    
    # Add main trend line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['rate'],
        mode='lines',
        name=f'{currency}/TWD',
        line=dict(color='#1f77b4', width=2),
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Date: %{x}<br>' +
                      'Rate: %{y:.4f} TWD<br>' +
                      '<extra></extra>'
    ))
    
    # Add moving average if enough data points
    if len(df) >= 7:
        df['ma7'] = df['rate'].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['ma7'],
            mode='lines',
            name='7-day MA',
            line=dict(color='orange', width=1, dash='dash'),
            hovertemplate='7-day MA: %{y:.4f} TWD<extra></extra>'
        ))
    
    # Customize layout
    fig.update_layout(
        title=f'{currency}/TWD {lang_manager.get_text("trend_title", current_lang)} - {period}',
        xaxis_title='Date',
        yaxis_title='Exchange Rate (TWD)',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        showlegend=True
    )
    
    # Add range selector
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="7d", step="day", stepmode="backward"),
                    dict(count=30, label="30d", step="day", stepmode="backward"),
                    dict(count=90, label="3m", step="day", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    return fig

def create_volume_chart(df: pd.DataFrame, currency: str, period: str, lang_manager, current_lang):
    """Create trading volume chart"""
    if df.empty or 'volume' not in df.columns:
        return None
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=[
            f'{currency}/TWD {lang_manager.get_text("trend_title", current_lang)}',
            f'{lang_manager.get_text("volume_chart_title", current_lang)}'
        ],
        row_heights=[0.7, 0.3]
    )
    
    # Add price chart
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['rate'],
            mode='lines',
            name=f'{currency}/TWD Rate',
            line=dict(color='#1f77b4', width=2),
            hovertemplate='Date: %{x}<br>Rate: %{y:.4f} TWD<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add volume chart
    colors = ['red' if df['volume'].iloc[i] < df['volume'].iloc[i-1] else 'green' 
              for i in range(1, len(df))]
    colors.insert(0, 'blue')  # First bar color
    
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['volume'],
            name='Trading Volume',
            marker_color=colors,
            hovertemplate='Date: %{x}<br>Volume: %{y:,.0f} M TWD<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f'{currency} {lang_manager.get_text("trading_volume_title", current_lang)} - {period}',
        hovermode='x unified',
        template='plotly_white',
        height=600,
        showlegend=True
    )
    
    # Update axes
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Exchange Rate (TWD)", row=1, col=1)
    fig.update_yaxes(title_text="Volume (M TWD)", row=2, col=1)
    
    return fig

def create_comparison_chart(tracker: TWDCurrencyTracker, currencies: List[str], days: int, lang_manager, current_lang):
    """Create comparison chart for multiple currencies vs TWD"""
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set1
    
    for i, currency in enumerate(currencies):
        df = tracker.get_historical_data(currency, days)
        if not df.empty:
            # Normalize to show percentage change from start
            normalized = (df['rate'] / df['rate'].iloc[0] - 1) * 100
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=normalized,
                mode='lines',
                name=currency,
                line=dict(color=colors[i % len(colors)], width=2),
                hovertemplate=f'<b>{currency}</b><br>' +
                              'Date: %{x}<br>' +
                              'Change: %{y:.2f}%<br>' +
                              '<extra></extra>'
            ))
    
    fig.update_layout(
        title=f'{lang_manager.get_text("comparison_title", current_lang)} (% Change)',
        xaxis_title='Date',
        yaxis_title='Change (%)',
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig

def main():
    # Initialize language manager
    lang_manager = LanguageManager()
    
    # Initialize session state for language
    if 'language' not in st.session_state:
        st.session_state.language = lang_manager.detect_language()
    
    # Get current language
    current_lang = st.session_state.language
    
    # Helper function to get translated text
    def t(key):
        return lang_manager.get_text(key, current_lang)
    
    st.title(t('title'))
    st.markdown(t('subtitle'))
    
    # Initialize tracker
    tracker = TWDCurrencyTracker()
    
    # Sidebar
    st.sidebar.header(t('settings'))
    
    # Language selection
    selected_language = st.sidebar.selectbox(
        t('language'),
        options=list(lang_manager.languages.keys()),
        format_func=lambda x: lang_manager.languages[x],
        index=list(lang_manager.languages.keys()).index(current_lang)
    )
    
    # Update language if changed
    if selected_language != current_lang:
        st.session_state.language = selected_language
        st.rerun()
    
    # Database management
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔧 " + t('settings').replace('Settings', 'Database'))
    
    if st.sidebar.button("🔄 重置資料庫 / Reset Database"):
        try:
            # Remove old database file
            if os.path.exists(tracker.db_file):
                os.remove(tracker.db_file)
            
            # Reinitialize database
            tracker.init_database()
            st.sidebar.success("資料庫已重置 / Database reset successfully!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"重置失敗 / Reset failed: {e}")
    
    st.sidebar.markdown("---")
    
    # Auto-refresh option
    auto_refresh = st.sidebar.checkbox(t('auto_refresh'), value=False)
    if auto_refresh:
        refresh_interval = st.sidebar.slider(t('refresh_interval'), 1, 60, 5)
    
    # Time period selection
    time_periods = {
        t('periods.1 Month'): 30,
        t('periods.3 Months'): 90,
        t('periods.6 Months'): 180,
        t('periods.1 Year'): 365,
        t('periods.3 Years'): 1095,
        t('periods.5 Years'): 1825,
        t('periods.10 Years'): 3650
    }
    
    selected_period = st.sidebar.selectbox(
        t('time_period'),
        options=list(time_periods.keys()),
        index=1
    )
    
    days = time_periods[selected_period]
    
    # Fetch current rates
    with st.spinner(t('fetching_rates')):
        current_rates = tracker.get_current_rates()
    
    if current_rates:
        # Save to database with generated volumes
        tracker.save_rates_to_db(current_rates)
        
        # Main tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            t('current_rates'), 
            t('trend_charts'), 
            t('currency_comparison'),
            t('currency_converter'),
            t('trading_volume'),
            t('statistics')
        ])
        
        with tab1:
            st.header(t('current_rates_title'))
            
            # Create current rates dataframe
            rates_data = []
            for currency in tracker.popular_currencies:
                if currency in current_rates:
                    rate = current_rates[currency]
                    name = tracker.currency_names.get(currency, currency)
                    
                    # Get historical data for change calculation
                    df_1d = tracker.get_historical_data(currency, 2)
                    change = 0
                    change_percent = 0
                    
                    if not df_1d.empty and len(df_1d) > 1:
                        prev_rate = df_1d['rate'].iloc[-2]
                        change = rate - prev_rate
                        change_percent = (change / prev_rate * 100) if prev_rate != 0 else 0
                    
                    rates_data.append({
                        t('currency'): f"{currency} ({name})",
                        t('rate'): f"{rate:.4f}",
                        t('change'): f"{change:+.4f}",
                        t('change_percent'): f"{change_percent:+.2f}%",
                        t('trend'): '📈' if change > 0 else '📉' if change < 0 else '➡️'
                    })
            
            df_rates = pd.DataFrame(rates_data)
            
            # Display as interactive table
            st.dataframe(
                df_rates,
                use_container_width=True,
                hide_index=True
            )
            
            # Quick stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                gainers = sum(1 for item in rates_data if '+' in item[t('change_percent')])
                st.metric(t('gainers'), gainers, delta=None)
            
            with col2:
                losers = sum(1 for item in rates_data if '-' in item[t('change_percent')])
                st.metric(t('losers'), losers, delta=None)
            
            with col3:
                st.metric(t('total_currencies'), len(rates_data), delta=None)
            
            with col4:
                try:
                    avg_change = np.mean([float(item[t('change_percent')].replace('%', '').replace('+', '')) for item in rates_data])
                    st.metric(t('avg_change'), f"{avg_change:.2f}%", delta=None)
                except:
                    st.metric(t('avg_change'), "0.00%", delta=None)
            
            # Note about data source
            st.info(t('simulated_note'))
        
        with tab2:
            st.header(f"{t('trend_title')} - {selected_period}")
            
            # Currency selection for individual charts
            selected_currency = st.selectbox(
                t('select_currency'),
                options=tracker.popular_currencies,
                format_func=lambda x: f"{x} ({tracker.currency_names.get(x, x)})"
            )
            
            # Get historical data
            df_historical = tracker.get_historical_data(selected_currency, days)
            
            if not df_historical.empty:
                # Create and display trend chart
                fig = create_trend_chart(df_historical, selected_currency, selected_period, lang_manager, current_lang)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Statistics for selected currency
                stats = tracker.calculate_statistics(df_historical)
                if stats:
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.metric(t('current_rate'), f"{stats['current']:.4f} TWD")
                    
                    with col2:
                        st.metric(
                            t('change'), 
                            f"{stats['change']:+.4f}",
                            delta=f"{stats['change_percent']:+.2f}%"
                        )
                    
                    with col3:
                        st.metric(t('min_rate'), f"{stats['min']:.4f}")
                    
                    with col4:
                        st.metric(t('max_rate'), f"{stats['max']:.4f}")
                    
                    with col5:
                        st.metric(t('volatility'), f"{stats['volatility']:.4f}")
            else:
                st.warning(f"{t('no_data')} {selected_currency}")
        
        with tab3:
            st.header(t('comparison_title'))
            
            # Multi-select for currencies to compare
            compare_currencies = st.multiselect(
                t('select_currencies'),
                options=tracker.popular_currencies,
                default=["USD", "EUR", "JPY", "THB"],
                format_func=lambda x: f"{x} ({tracker.currency_names.get(x, x)})"
            )
            
            if compare_currencies:
                fig_comparison = create_comparison_chart(tracker, compare_currencies, days, lang_manager, current_lang)
                st.plotly_chart(fig_comparison, use_container_width=True)
                
                # Comparison table
                st.subheader(t('performance_summary'))
                comparison_data = []
                
                for currency in compare_currencies:
                    df = tracker.get_historical_data(currency, days)
                    if not df.empty:
                        stats = tracker.calculate_statistics(df)
                        comparison_data.append({
                            t('currency'): currency,
                            t('current_rate'): f"{stats['current']:.4f}",
                            t('change_percent'): f"{stats['change_percent']:+.2f}%",
                            t('volatility'): f"{stats['volatility']:.4f}",
                            'Min': f"{stats['min']:.4f}",
                            'Max': f"{stats['max']:.4f}"
                        })
                
                if comparison_data:
                    st.dataframe(pd.DataFrame(comparison_data), hide_index=True)
        
        with tab4:
            st.header(t('converter_title'))
            
            col1, col2 = st.columns(2)
            
            with col1:
                from_currency = st.selectbox(
                    t('from_currency'),
                    options=["TWD"] + tracker.popular_currencies,
                    format_func=lambda x: f"{x} ({tracker.currency_names.get(x, x)})"
                )
                
                amount = st.number_input(t('amount'), min_value=0.0, value=1.0, step=0.01)
            
            with col2:
                to_currency = st.selectbox(
                    t('to_currency'),
                    options=tracker.popular_currencies + ["TWD"],
                    format_func=lambda x: f"{x} ({tracker.currency_names.get(x, x)})"
                )
            
            if from_currency != to_currency:
                if from_currency == "TWD":
                    # TWD to foreign currency
                    rate = current_rates.get(to_currency, 0)
                    if rate > 0:
                        converted = amount / rate  # Divide because rate is foreign currency per TWD
                    else:
                        converted = 0
                elif to_currency == "TWD":
                    # Foreign currency to TWD
                    rate = current_rates.get(from_currency, 0)
                    converted = amount * rate
                else:
                    # Cross currency calculation via TWD
                    from_rate = current_rates.get(from_currency, 0)
                    to_rate = current_rates.get(to_currency, 0)
                    if from_rate != 0 and to_rate != 0:
                        # Convert from_currency to TWD, then TWD to to_currency
                        twd_amount = amount * from_rate
                        converted = twd_amount / to_rate
                    else:
                        converted = 0
                
                st.success(f"{amount:,.2f} {from_currency} = {converted:,.4f} {to_currency}")
                
                if from_currency == "TWD":
                    rate_display = 1 / rate if rate != 0 else 0
                    st.info(f"{t('exchange_rate')}: 1 {from_currency} = {rate_display:.4f} {to_currency}")
                elif to_currency == "TWD":
                    rate_display = rate
                    st.info(f"{t('exchange_rate')}: 1 {from_currency} = {rate_display:.4f} {to_currency}")
                else:
                    rate_display = from_rate / to_rate if to_rate != 0 else 0
                    st.info(f"{t('exchange_rate')}: 1 {from_currency} = {rate_display:.4f} {to_currency}")
        
        with tab5:
            st.header(t('trading_volume_title'))
            
            # Volume period selection
            volume_periods = {
                t('today'): 'today',
                t('7_days'): '7_days',
                t('14_days'): '14_days',
                t('1_month'): '1_month'
            }
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_volume_period = st.selectbox(
                    t('volume_period'),
                    options=list(volume_periods.keys()),
                    index=1
                )
                volume_period_key = volume_periods[selected_volume_period]
            
            with col2:
                volume_currency = st.selectbox(
                    t('select_currency'),
                    options=tracker.popular_currencies,
                    format_func=lambda x: f"{x} ({tracker.currency_names.get(x, x)})",
                    key="volume_currency"
                )
            
            # Get volume data
            volume_df = tracker.get_volume_data(volume_currency, volume_period_key)
            
            if not volume_df.empty and 'volume' in volume_df.columns:
                # Create volume chart
                volume_fig = create_volume_chart(volume_df, volume_currency, selected_volume_period, lang_manager, current_lang)
                if volume_fig:
                    st.plotly_chart(volume_fig, use_container_width=True)
                
                # Volume statistics
                vol_stats = tracker.calculate_statistics(volume_df)
                if vol_stats and 'current_volume' in vol_stats:
                    st.subheader(t('volume_summary'))
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        current_vol = vol_stats['current_volume']
                        vol_level = 'high_volume' if current_vol > vol_stats['avg_volume'] * 1.2 else 'low_volume' if current_vol < vol_stats['avg_volume'] * 0.8 else 'medium_volume'
                        st.metric(
                            t('daily_volume'), 
                            f"{current_vol:,.0f}M",
                            delta=t(vol_level)
                        )
                    
                    with col2:
                        st.metric(
                            t('total_volume'),
                            f"{vol_stats['total_volume']:,.0f}M"
                        )
                    
                    with col3:
                        st.metric(
                            t('avg_volume'),
                            f"{vol_stats['avg_volume']:,.0f}M"
                        )
                    
                    with col4:
                        vol_change = vol_stats.get('volume_change_percent', 0)
                        st.metric(
                            t('volume_trend'),
                            f"{vol_change:+.1f}%",
                            delta=f"vs previous period"
                        )
                
                # Volume ranking for all currencies
                st.subheader(f"{t('trading_volume_title')} - {selected_volume_period}")
                
                volume_ranking = []
                for curr in tracker.popular_currencies:
                    curr_vol_df = tracker.get_volume_data(curr, volume_period_key)
                    if not curr_vol_df.empty and 'volume' in curr_vol_df.columns:
                        curr_stats = tracker.calculate_statistics(curr_vol_df)
                        if curr_stats and 'total_volume' in curr_stats:
                            volume_ranking.append({
                                t('currency'): curr,
                                t('total_volume'): f"{curr_stats['total_volume']:,.0f}M",
                                t('avg_volume'): f"{curr_stats['avg_volume']:,.0f}M",
                                t('volume_trend'): f"{curr_stats.get('volume_change_percent', 0):+.1f}%"
                            })
                
                if volume_ranking:
                    # Sort by total volume
                    volume_ranking.sort(key=lambda x: float(x[t('total_volume')].replace('M', '').replace(',', '')), reverse=True)
                    st.dataframe(pd.DataFrame(volume_ranking), hide_index=True)
            else:
                st.warning(f"{t('no_data')} {volume_currency} volume data")
        
        with tab6:
            st.header(t('market_stats'))
            
            # Overall market statistics
            st.subheader(t('market_overview'))
            
            all_stats = []
            for currency in tracker.popular_currencies:
                df = tracker.get_historical_data(currency, days)
                if not df.empty:
                    stats = tracker.calculate_statistics(df)
                    stats['currency'] = currency
                    all_stats.append(stats)
            
            if all_stats:
                # Top gainers and losers
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(t('top_gainers'))
                    gainers = sorted(all_stats, key=lambda x: x['change_percent'], reverse=True)[:5]
                    for stat in gainers:
                        st.write(f"**{stat['currency']}**: {stat['change_percent']:+.2f}%")
                
                with col2:
                    st.subheader(t('top_losers'))
                    losers = sorted(all_stats, key=lambda x: x['change_percent'])[:5]
                    for stat in losers:
                        st.write(f"**{stat['currency']}**: {stat['change_percent']:+.2f}%")
                
                # Volatility ranking
                st.subheader(t('volatility_ranking'))
                volatility_ranking = sorted(all_stats, key=lambda x: x['volatility'], reverse=True)
                
                volatility_data = []
                for stat in volatility_ranking:
                    volatility_data.append({
                        t('currency'): stat['currency'],
                        t('volatility'): f"{stat['volatility']:.4f}",
                        t('current_rate'): f"{stat['current']:.4f}",
                        t('change_percent'): f"{stat['change_percent']:+.2f}%"
                    })
                
                st.dataframe(pd.DataFrame(volatility_data), hide_index=True)
    
    else:
        st.error(t('unable_fetch'))
    
    # Auto-refresh functionality
    if auto_refresh:
        time.sleep(refresh_interval * 60)
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(f"**{t('data_source')}**: 台灣銀行 Bank of Taiwan | **{t('last_updated')}**: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()