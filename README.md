# 🤖 Rem - Advanced Telegram File Management Bot

![Rem Banner](img/rem_banner.png)
![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot_API-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-purple.svg)

**Rem** is a sophisticated Telegram bot designed to manage file uploads in groups with advanced user tracking, limits, and administrative controls. Perfect for communities that need controlled file sharing environments.

## 🚀 Features

### 🔒 Smart File Management
- **User-specific file limits** - Configurable upload limits per user
- **Automatic blocking system** - Temporary blocks when limits are exceeded
- **Real-time tracking** - Live monitoring of user activity
- **Multi-format support** - All common file types supported

### 👑 Administrative Controls
- **Admin panel** - Comprehensive management interface
- **User reset capabilities** - Reset user limits instantly
- **Broadcast system** - Send messages to all users
- **Activity statistics** - Detailed usage analytics

### 📊 Advanced Analytics
- **User statistics** - Individual user activity tracking
- **System metrics** - Bot performance and usage data
- **Logging system** - Comprehensive activity logs
- **Real-time monitoring** - Live status updates

### ⚙️ Professional Architecture
- **Modular design** - Clean, maintainable code structure
- **Configuration management** - Easy setup and customization
- **Error handling** - Robust exception management
- **Auto-setup** - Automatic file and directory creation

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Required Python packages

### Quick Setup

1. **Clone the repository**
```bash
git clone https://github.com/CHICO-CP/rem-limit-file.git
cd rem-limit-file
```

1. **Install dependencies**

```bash
pip install pyTelegramBotAPI
```

1. **Run the bot**

```bash
python main.py
```

1. **Follow the setup wizard to configure your bot token and settings**

### Manual Configuration

**Create the configuration structure manually if needed:**

```bash
# Create directory structure
mkdir -p config data logs

# Create configuration file
echo '{
  "token": "YOUR_BOT_TOKEN_HERE",
  "allowed_group_id": null,
  "admin_id": "YOUR_ADMIN_ID",
  "welcome_message": "Welcome to Rem! 🛡️",
  "auto_cleanup_days": 30
}' > config/bot_config.json
```

# 🛠️ Configuration

### Bot Settings

- **Token: Your Telegram Bot API token**
- **Allowed Group ID: Restrict bot to specific group (null for all groups)**
- **Admin ID: User ID with administrative privileges**
- **File Limit: Maximum files per user (default: 3)**
- **Block Duration: Temporary block duration (default: 12 hours)**

### File Structure

```
rem-limit-file/
├── main.py                 # Main bot executable
├── bot_config.py          # Configuration management
├── user_manager.py        # User data handling
├── bot_commands.py        # Command handlers
├── config/
│   └── bot_config.json    # Bot configuration
├── data/
│   ├── users.json         # User data storage
│   └── statistics.json    # Usage statistics
└── logs/
    └── bot_activity.log   # Activity logs
```

# 💻 Usage

### User Commands

- **/start - Welcome message and bot information**
- **/help - Comprehensive help guide**
- **/stats - View your upload statistics**
- **/myinfo - Check your current status and limits**

### Admin Commands

- **/admin - Access administration panel**
- **/reset - Reset all user file counts**
- **/broadcast - Send message to all users**

### File Upload System

1. Users can upload files up to the configured limit
2. Bot tracks each user's file count in real-time
3. Users receive notifications about remaining uploads
4. Temporary block applied when limits are exceeded
5. Automatic unblock after configured duration

# 📊 Commands Overview

| Command | Description | Access |
|---------|-------------|---------|
| `/start` | Welcome message and bot info | All users |
| `/help` | Detailed usage instructions | All users |
| `/stats` | Personal upload statistics | All users |
| `/myinfo` | Current status and limits | All users |
| `/admin` | Administration panel | Admin only |
| `/reset` | Reset user file counts | Admin only |
| `/broadcast` | Message all users | Admin only |

# 🔧 Customization

### Modify File Limits

Edit bot_config.py:

```python
FILE_LIMIT = 5  # Change from default 3
BLOCK_DURATION = timedelta(hours=24)  # Change block duration
```

Custom Welcome Message

Update bot_config.json:

```json
{
  "welcome_message": "Your custom welcome message here!",
  // ... other settings
}
```

### Add New File Types

Modify allowed extensions in bot_config.py:

```python
ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.jpg', '.png', '.zip', '.docx', '.xlsx']
```

# 🐛 Troubleshooting

## Common Issues

**Bot not starting:**
- Verify bot token is correct
- Check Python version (3.7+ required)
- Ensure pyTelegramBotAPI is installed

**File uploads not tracked:**
- Check bot has message permissions in group
- Verify configuration files are properly created
- Check logs for specific error messages

**Admin commands not working:**
- Verify admin ID is correctly set in configuration
- Ensure user ID matches exactly

## Logs and Debugging
Check `logs/bot_activity.log` for detailed error information and bot activity.

# 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Include docstrings for all functions
- Add comments for complex logic
- Maintain modular architecture

# 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# 🔒 Security & Privacy

- User data is stored locally in JSON format
- No personal information is shared with third parties
- All file processing happens locally
- Configuration files contain only essential bot settings

# 📞 Support & Contact

- **Developer**: Ghost Developer
- **GitHub**: [github.com/CHICO-CP](https://github.com/CHICO-CP)
- **Telegram**: [@Gh0stDeveloper](https://t.me/Gh0stDeveloper)
- **Issues**: [GitHub Issues](https://github.com/CHICO-CP/rem-limit-file/issues)

# 🙏 Acknowledgments

- Thanks to the pyTelegramBotAPI team for the excellent library
- Telegram for their robust Bot API
- The open-source community for continuous inspiration

---

**⭐ If you find this project useful, please give it a star on GitHub!**

**🛡️ Secure File Management • 🔧 Professional Tools • 🚀 Easy Deployment**