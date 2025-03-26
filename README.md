# Azure Queue Storage 管理系統

這是一個基於 Flask 的網頁應用程式，用於管理 Azure Queue Storage 中的訊息。系統提供直觀的使用者介面，可以輕鬆地新增、讀取、刪除訊息，並支援多個 Queue 的管理。

## 功能特點

- 訊息管理
  - 新增訊息
  - 讀取訊息（自動刪除已讀訊息）
  - 刪除特定訊息
  - 即時更新訊息列表（每 5 秒自動重新整理）

- Queue 管理
  - 支援多個 Queue 的切換
  - 自動檢查並創建不存在的 Queue
  - 顯示所有可用的 Queue

## 系統需求

- Python 3.6 或更高版本
- Azure Storage Account 和連接字串
- 必要的 Python 套件（見 requirements.txt）

## 安裝步驟

1. 克隆專案到本地：
```bash
git clone [專案網址]
cd [專案目錄]
```

2. 安裝必要的套件：
```bash
pip install -r requirements.txt
```

3. 設定環境變數：
   - 複製 `.env.example` 檔案為 `.env`
   - 在 `.env` 檔案中設定您的 Azure Storage 連接字串：
```
AZURE_STORAGE_CONNECTION_STRING=您的連接字串
QUEUE_NAME=預設佇列名稱
```

## 執行應用程式

1. 啟動應用程式：
```bash
python app.py
```

2. 開啟瀏覽器，訪問：
```
http://localhost:5000
```

## 使用說明

### 首頁功能

1. Queue 選擇
   - 使用下拉選單選擇要操作的 Queue
   - 點選「切換 Queue」按鈕或直接選擇即可切換

2. 新增訊息
   - 在文字區域輸入訊息內容
   - 點選「新增訊息」按鈕發送

3. 訊息列表
   - 顯示當前 Queue 中的所有訊息
   - 可以點選「刪除」按鈕刪除特定訊息
   - 列表每 5 秒自動更新

### 讀取訊息頁面

1. 點選「讀取訊息」按鈕進入讀取頁面
2. 點選「讀取下一筆訊息」按鈕讀取訊息
3. 訊息會以提示框形式顯示
4. 讀取後訊息會自動從佇列中刪除

## 注意事項

- 確保 Azure Storage Account 有足夠的權限
- 訊息讀取後會自動刪除，請謹慎操作
- 建議定期備份重要訊息

## 技術細節

- 使用 Flask 框架開發
- 整合 Azure Queue Storage SDK
- 使用 Bootstrap 5 建立響應式介面
- 使用 JavaScript 實現即時更新功能

## 授權

[授權類型]

## 貢獻指南

歡迎提交 Issue 和 Pull Request 來改進這個專案。 