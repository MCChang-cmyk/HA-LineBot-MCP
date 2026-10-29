> 本專案是 [kukuxx/HA-LineBot-MCP](https://github.com/kukuxx/HA-LineBot-MCP) 的維護分支，保留 Apache-2.0 授權。
> 1.0.2 以 Home Assistant Core 2026.10.3 為相容目標，對齊官方 MCP Server 的 MCP／AnyIO 版本。仍需實機驗證。
> HACS 自訂儲存庫：`MCChang-cmyk/HA-LineBot-MCP`，類型選 Integration。

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

[contributors-shield]: https://img.shields.io/github/contributors/kukuxx/HA-LineBot-MCP.svg?style=for-the-badge
[contributors-url]: https://github.com/kukuxx/HA-LineBot-MCP/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/kukuxx/HA-LineBot-MCP.svg?style=for-the-badge
[forks-url]: https://github.com/kukuxx/HA-LineBot-MCP/network/members

[stars-shield]: https://img.shields.io/github/stars/kukuxx/HA-LineBot-MCP.svg?style=for-the-badge
[stars-url]: https://github.com/kukuxx/HA-LineBot-MCP/stargazers

[issues-shield]: https://img.shields.io/github/issues/kukuxx/HA-LineBot-MCP.svg?style=for-the-badge
[issues-url]: https://github.com/kukuxx/HA-LineBot-MCP/issues

[license-shield]: https://img.shields.io/github/license/kukuxx/HA-LineBot-MCP.svg?style=for-the-badge
[license-url]: https://github.com/kukuxx/HA-LineBot-MCP/blob/main/LICENSE


# LINE Bot MCP 整合 - Home Assistant

- [English](/README.md) | [繁體中文](/README-zh-TW.md)

將 LINE Bot 與 Model Context Protocol (MCP) 整合到 Home Assistant 的自訂整合元件。

## 🌟 主要特色

- 🤖 **完整 LINE Bot 支援** - 接收和發送各種類型的 LINE 訊息
- 🧠 **MCP 服務器** - 讓 AI 助手（Claude、ChatGPT）直接控制 LINE Bot
- 🏠 **Home Assistant 整合** - 原生整合，提供服務和感測器
- 📱 **多種訊息類型** - 文字、圖片、影片、音訊、位置、貼圖、Flex 等
- 🔄 **自動回覆** - 整合對話代理進行智慧回覆
- 📊 **即時監控** - Bot 狀態、配額使用情況監控

> [!Warning]
> 自動回覆目前為實驗性功能，有時可能會出錯

## 📋 系統需求

- Home Assistant 2025.7.0+
- LINE Developers 帳號

## 🚀 快速開始

### 1. 安裝整合

**HACS 安裝（推薦）：**
1. 在 HACS 中添加自訂儲存庫：
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=kukuxx&repository=HA-LineBot-MCP&category=Integration)
2. 搜尋並安裝 "LINE Bot MCP"
3. 重新啟動 Home Assistant

### 2. 設定 LINE Bot

1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 創建 Messaging API Channel
3. 取得 Channel Access Token 和 Channel Secret

### 3. 配置整合

1. 在 Home Assistant 中添加 "LINE Bot MCP" 整合
2. 輸入 Bot ID、Channel Access Token、Channel Secret
3. 到 **bot info sensor** 的 **attibutes** 查看 **Webhook endpoint**
4. 將 Webhook URL 填到 LINE Developers Console

## 🎯 使用方式

### Home Assistant 服務

```yaml
# 發送文字訊息
service: notify.linebot_push_message
data:
  name: "@bot123"
  to: "U1234567890abcdef1234567890abcdef"
  messages:
    - type: "text"
      text: "Hello from Home Assistant!"

# 回覆訊息
service: notify.linebot_reply_message
data:
  name: "@bot123"
  reply_token: "{{ trigger.event.data.reply_token }}"
  messages:
    - type: "text"
      text: "收到您的訊息了！"
```

### 自動化範例

```yaml
automation:
  - alias: "LINE Bot 回覆"
    trigger:
      platform: event
      event_type: linebot_@bot123_message_received
    action:
      service: notify.linebot_reply_message
      data:
        name: "@bot123"
        reply_token: "{{ trigger.event.data.reply_token }}"
        messages:
          - type: "text"
            text: "您好！我是 Home Assistant LINE Bot"
```

### MCP 工具

AI 助手可以使用以下工具：

- `push_message` - 發送訊息
- `reply_message` - 回覆訊息  
- `get_quota` - 查詢配額

**MCP 連線端點：**
- SSE: `http://your-ha-url:8123/linebotmcp/sse`

## 📱 支援的訊息類型

| 類型 | 說明 | 範例 |
|------|------|------|
| text | 純文字訊息 | `{"type": "text", "text": "Hello"}` |
| textV2 | 支援提及和表情符號 | 包含 mentions 和 emojis |
| image | 圖片訊息 | 需要圖片 URL 和預覽圖 |
| video | 影片訊息 | 需要影片 URL 和預覽圖 |
| audio | 音訊訊息 | 需要音訊 URL 和時長 |
| location | 位置訊息 | 包含座標和地址 |
| sticker | 貼圖訊息 | 需要貼圖包 ID 和貼圖 ID |
| flex | Flex 訊息 | 自訂版面設計 |
| imagemap | 圖片地圖訊息 | 包含圖片和動作 |
| template | 模板訊息 | 包含按鈕和文字 |

## 🔧 進階設定

### 選項配置

- **代理 ID**：指定對話代理（預設：`conversation.google_generative_ai`）
- **自動回覆**：啟用/停用自動回覆功能

### 事件處理

整合會觸發以下事件：

- `linebot_{bot_ID}_message_received` - 收到訊息
- `linebot_{bot_ID}_postback` - 收到 postback

事件包含用戶 ID、訊息內容、回覆 token 等資訊。

## 🐛 疑難排解

### 常見問題

**Webhook 無法接收訊息：**
- 檢查 Webhook URL 設定
- 確認 Home Assistant 可從外部存取
- 驗證 Channel Secret 正確性

**MCP 連線失敗：**
- 檢查網路連線
- 查看 Home Assistant 日誌

**訊息發送失敗：**
- 驗證 Channel Access Token
- 檢查訊息格式
- 確認目標用戶 ID

### 除錯日誌

```yaml
logger:
  default: warning
  logs:
    linebot_mcp: debug
```

## 📚 更多資源
- [LINE Messaging API 文檔](https://developers.line.biz/en/docs/messaging-api/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Home Assistant 開發指南](https://developers.home-assistant.io/)

## 🙏 致謝
MCP server 部分參考了 [homeassistant-mcp-server](https://github.com/home-assistant/core/tree/dev/homeassistant/components/mcp_server) 進行開發。