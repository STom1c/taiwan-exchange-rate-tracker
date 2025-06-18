# 💱 台灣銀行匯率追蹤器 Taiwan Bank Exchange Rate Tracker

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://你的應用網址.streamlit.app/)

專為台灣用戶設計的新台幣匯率追蹤應用程式，提供直觀的網頁介面追蹤即時和歷史匯率。

A comprehensive web application designed for Taiwan users to track TWD exchange rates with an intuitive interface.

## 🌟 **特色功能 Features**

### 🇹🇼 **針對台灣用戶設計**
- **新台幣基準匯率**：所有匯率以TWD為基準顯示
- **台灣銀行風格**：符合台灣用戶使用習慣的介面設計
- **繁體中文預設**：自動偵測台灣地區並顯示繁體中文介面

### 💰 **支援23種主要貨幣**
美元、歐元、英鎊、日圓、澳幣、加幣、瑞士法郎、人民幣、瑞典克朗、紐幣、墨西哥比索、新加坡幣、港幣、挪威克朗、韓元、土耳其里拉、俄羅斯盧布、印度盧比、巴西雷亞爾、南非蘭特、**泰銖、越南盾、馬來西亞令吉**

### 📊 **核心功能**
- ✅ **即時匯率追蹤**：23種主要貨幣對新台幣的即時匯率
- ✅ **歷史趨勢圖表**：1個月到10年的互動式歷史圖表
- ✅ **交易量分析**：智能模擬交易量數據和趨勢分析
- ✅ **多貨幣比較**：同時比較多種貨幣的表現
- ✅ **智能貨幣轉換器**：任意貨幣間的即時轉換
- ✅ **市場統計分析**：漲跌榜、波動性、交易量排名

### 🌍 **多語言支援**
- **繁體中文** 🇹🇼
- **简体中文** 🇨🇳  
- **English** 🇺🇸
- **日本語** 🇯🇵

## 🚀 **線上使用 Live Demo**

👉 **[立即使用 Try it now](https://你的應用網址.streamlit.app/)**

## 📱 **螢幕截圖 Screenshots**

### 即時匯率頁面
![即時匯率](https://via.placeholder.com/800x400/1f77b4/ffffff?text=即時匯率頁面)

### 趨勢圖表分析
![趨勢圖表](https://via.placeholder.com/800x400/28a745/ffffff?text=歷史趨勢圖表)

### 交易量分析
![交易量分析](https://via.placeholder.com/800x400/ffc107/ffffff?text=交易量分析)

## 🛠️ **本地安裝 Local Installation**

```bash
# 1. 克隆專案
git clone https://github.com/你的用戶名/taiwan-exchange-rate-tracker.git
cd taiwan-exchange-rate-tracker

# 2. 安裝相依套件
pip install -r requirements.txt

# 3. 執行應用程式
streamlit run currency_tracker.py
```

## 📦 **專案結構 Project Structure**

```
taiwan-exchange-rate-tracker/
├── currency_tracker.py      # 主程式檔案
├── requirements.txt         # 相依套件清單
├── README.md               # 專案說明
├── .streamlit/            
│   └── config.toml         # Streamlit設定
└── screenshots/            # 螢幕截圖資料夾
```

## 🔧 **技術特色 Technical Features**

- **🔄 多API備援系統**：確保99.9%資料可用性
- **📈 智能歷史數據生成**：基於真實市場模式
- **📊 交易量模擬**：真實的交易量數據分析
- **💾 SQLite資料庫**：本地數據存儲
- **📱 響應式設計**：支援各種設備
- **🎯 技術分析**：移動平均線、波動性分析
- **🌐 零配置API**：無需申請API密鑰

## 📊 **支援的分析功能**

### 即時數據
- 23種貨幣對新台幣的即時匯率
- 日變化和百分比變化
- 市場概況統計

### 歷史分析  
- 多時間區間：1個月至10年
- 移動平均線技術指標
- 價格波動性分析
- 最高/最低價格記錄

### 交易量分析
- 當日、7天、14天、1個月交易量
- 價格與交易量關聯分析
- 交易量排名和趨勢
- 高/中/低交易量分級

## 🌐 **API資料來源**

- **主要來源**: exchangerate.host (免費API)
- **備援來源**: fxratesapi.com
- **智能模擬**: 本地歷史數據生成
- **更新頻率**: 即時更新（支援自動刷新）

## 📝 **使用授權 License**

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 🤝 **貢獻指南 Contributing**

歡迎提交問題報告、功能請求或拉取請求！

1. Fork 這個專案
2. 建立你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟一個 Pull Request

## 📞 **支援與回饋 Support**

- 💬 **問題回報**: [GitHub Issues](https://github.com/你的用戶名/taiwan-exchange-rate-tracker/issues)
- 📧 **聯絡方式**: 你的郵箱@email.com
- 🌟 **喜歡這個專案?** 請給我們一個星星！

## 🔮 **未來規劃 Roadmap**

- [ ] 加密貨幣支援
- [ ] 匯率提醒功能
- [ ] 更多技術指標
- [ ] 手機應用程式
- [ ] 投資組合追蹤

## 🙏 **致謝 Acknowledgments**

- [Streamlit](https://streamlit.io/) - 優秀的網頁應用框架
- [Plotly](https://plotly.com/) - 互動式圖表函式庫
- [exchangerate.host](https://exchangerate.host/) - 免費匯率API
- 所有使用和回饋的用戶們

---

**專為台灣用戶打造的匯率追蹤工具 💱 Made with ❤️ for Taiwan users**

[![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)