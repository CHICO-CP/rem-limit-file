# FILE: user_manager.py
# DESCRIPTION: User management and file tracking

import json
from datetime import datetime, timedelta
from bot_config import BotConfig

class UserManager:
    """Manage user data and file tracking"""
    
    @staticmethod
    def get_user_data(user_id, users_data):
        """Get or create user data"""
        user_id_str = str(user_id)
        if user_id_str not in users_data:
            users_data[user_id_str] = {
                'sent_files': 0,
                'block_until': None,
                'first_seen': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'total_files_sent': 0
            }
        return users_data[user_id_str]
    
    @staticmethod
    def is_user_blocked(user_data):
        """Check if user is currently blocked"""
        if user_data.get('block_until'):
            return datetime.now() < datetime.fromisoformat(user_data['block_until'])
        return False
    
    @staticmethod
    def block_user(user_data, block_duration):
        """Block user for specified duration"""
        user_data['block_until'] = (datetime.now() + block_duration).isoformat()
        return user_data
    
    @staticmethod
    def unblock_user(user_data):
        """Remove user block"""
        user_data['block_until'] = None
        return user_data
    
    @staticmethod
    def increment_file_count(user_data):
        """Increment user's file count"""
        user_data['sent_files'] += 1
        user_data['total_files_sent'] += 1
        user_data['last_activity'] = datetime.now().isoformat()
        return user_data
    
    @staticmethod
    def reset_user_files(user_data):
        """Reset user's file count and remove block"""
        user_data['sent_files'] = 0
        user_data['block_until'] = None
        return user_data
    
    @staticmethod
    def get_user_stats(user_data):
        """Get formatted user statistics"""
        remaining_files = BotConfig.FILE_LIMIT - user_data['sent_files']
        is_blocked = UserManager.is_user_blocked(user_data)
        
        stats = {
            'sent_files': user_data['sent_files'],
            'remaining_files': remaining_files,
            'total_files_sent': user_data['total_files_sent'],
            'is_blocked': is_blocked,
            'first_seen': user_data['first_seen']
        }
        
        if is_blocked:
            block_until = datetime.fromisoformat(user_data['block_until'])
            time_remaining = block_until - datetime.now()
            stats['block_remaining'] = str(time_remaining).split('.')[0]
            
        return stats