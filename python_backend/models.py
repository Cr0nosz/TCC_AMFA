from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
import pytz

db = SQLAlchemy()

# Fuso horário de São Paulo

SP_TZ = pytz.timezone('America/Sao_Paulo')

def generate_uuid():
    return str(uuid.uuid4())

def get_sp_now():
    """Retorna a data/hora atual no fuso horário de São Paulo (naive datetime)"""
    # Retorna datetime sem timezone info, mas no horário de São Paulo
    return datetime.now(SP_TZ).replace(tzinfo=None)

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    role = Column(Text, nullable=False, default='user')
    is_email_confirmed = Column(Boolean, default=False, nullable=False)
    email_verification_code_hash = Column(Text, nullable=True)
    email_verification_expires_at = Column(DateTime, nullable=True)
    email_verification_attempts = Column(Integer, default=0, nullable=False)
    last_email_verification_sent_at = Column(DateTime, nullable=True)
    last_verification_attempt_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=get_sp_now, nullable=False)
    updated_at = Column(DateTime, default=get_sp_now, onupdate=get_sp_now, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'emailVerified': self.is_email_confirmed,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

class AccessLog(db.Model):
    __tablename__ = 'access_logs'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, db.ForeignKey('users.id'), nullable=True)
    action = Column(Text, nullable=False)  # login, logout, register
    success = Column(Boolean, nullable=False)
    ip_address = Column(Text, nullable=True)
    user_agent = Column(Text, nullable=True)
    location = Column(JSON, nullable=True)
    device_info = Column(JSON, nullable=True)
    login_time = Column(DateTime, default=get_sp_now, nullable=False)
    blocked_reason = Column(Text, nullable=True)
    session_blocked = Column(Boolean, default=False, nullable=False)

    def to_dict(self):
        # Formata a localização como string, se existir
        location_str = None
        if self.location:
            parts = []
            if self.location.get('city'):
                parts.append(self.location['city'])
            if self.location.get('region'):
                parts.append(self.location['region'])
            if self.location.get('country'):
                parts.append(self.location['country'])
            location_str = ', '.join(parts) if parts else None
        
        # Formata as informações do dispositivo como string, se existir
        device_str = None
        if self.device_info:
            parts = []
            if self.device_info.get('browser'):
                parts.append(self.device_info['browser'])
            if self.device_info.get('os'):
                parts.append(self.device_info['os'])
            device_str = ' on '.join(parts) if parts else None
        
        return {
            'id': self.id,
            'userId': self.user_id,
            'action': self.action,
            'success': self.success,
            'ipAddress': self.ip_address,
            'userAgent': self.user_agent,
            'location': location_str,
            'deviceInfo': device_str,
            'timestamp': self.login_time.isoformat() if self.login_time else None,
            'blockedReason': self.blocked_reason,
            'sessionBlocked': self.session_blocked
        }

class SecuritySession(db.Model):
    __tablename__ = 'security_sessions'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, db.ForeignKey('users.id'), nullable=False)
    ip_address = Column(Text, nullable=False)
    user_agent = Column(Text, nullable=True)
    location = Column(JSON, nullable=True)
    device_info = Column(JSON, nullable=True)
    security_code_hash = Column(Text, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    verification_attempts = Column(Integer, default=0, nullable=False)
    max_attempts = Column(Integer, default=5, nullable=False)
    is_confirmed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=get_sp_now, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'location': self.location,
            'device_info': self.device_info,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'verification_attempts': self.verification_attempts,
            'max_attempts': self.max_attempts,
            'is_confirmed': self.is_confirmed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LoginAttempt(db.Model):
    __tablename__ = 'login_attempts'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(Text, nullable=False)
    ip_address = Column(Text, nullable=False)
    success = Column(Boolean, nullable=False)
    attempted_at = Column(DateTime, default=get_sp_now, nullable=False)
    blocked_until = Column(DateTime, nullable=True)

class SecurityBlock(db.Model):
    __tablename__ = 'security_blocks'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(Text, nullable=False)
    ip_address = Column(Text, nullable=False)
    block_reason = Column(Text, nullable=False)  # Brute_force, "Viagem impossível"
    blocked_at = Column(DateTime, default=get_sp_now, nullable=False)
    blocked_until = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=get_sp_now, nullable=False)
