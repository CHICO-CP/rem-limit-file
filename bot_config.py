# FILE: bot_config.py
# DESCRIPTION: Configuration and constants management

import os
import json
from datetime import timedelta

class BotConfig:
    """Bot configuration and constants"""
    
    # File management settings
    FILE_LIMIT = 3
    BLOCK_DURATION = timedelta(hours=12)
    ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.jpg', '.png', '.zip', '.py', '.json']
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    # Bot settings
    BOT_NAME = "FileGuard Pro"
    BOT_VERSION = "2.0.0"
    ADMIN_ID = None  # Will be set from config
    
    # Paths
    CONFIG_FILE = 'config/bot_config.json'
    USERS_FILE = 'data/users.json'
    STATS_FILE = 'data/statistics.json'
    LOG_FILE = 'logs/bot_activity.log'

class ConfigManager:
    """Manage bot configuration files"""
    
    @staticmethod
    def initialize_config():
        """Create configuration directory and files if they don't exist"""
        os.makedirs('config', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # Create config file if it doesn't exist
        if not os.path.exists(BotConfig.CONFIG_FILE):
            config_data = {
                'token': input("🤖 Enter the bot token: "),
                'allowed_group_id': input("👥 Enter the allowed group ID (leave blank for all groups): ") or None,
                'admin_id': input("👑 Enter the admin user ID (for special commands): ") or None,
                'welcome_message': "Welcome to FileGuard Pro! 🛡️",
                'auto_cleanup_days': 30
            }
            ConfigManager.save_config(config_data)
            
        # Create users file if it doesn't exist
        if not os.path.exists(BotConfig.USERS_FILE):
            ConfigManager.save_users_data({})
            
        # Create statistics file if it doesn't exist
        if not os.path.exists(BotConfig.STATS_FILE):
            ConfigManager.save_stats_data({
                'total_files_processed': 0,
                'total_blocks_issued': 0,
                'active_users': 0,
                'bot_start_time': None
            })
    
    @staticmethod
    def load_config():
        """Load configuration from file"""
        with open(BotConfig.CONFIG_FILE, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_config(config_data):
        """Save configuration to file"""
        with open(BotConfig.CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
    
    @staticmethod
    def load_users_data():
        """Load users data from file"""
        with open(BotConfig.USERS_FILE, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_users_data(users_data):
        """Save users data to file"""
        with open(BotConfig.USERS_FILE, 'w') as f:
            json.dump(users_data, f, indent=4)
    
    @staticmethod
    def load_stats_data():
        """Load statistics data from file"""
        with open(BotConfig.STATS_FILE, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_stats_data(stats_data):
        """Save statistics data to file"""
        with open(BotConfig.STATS_FILE, 'w') as f:
            json.dump(stats_data, f, indent=4)