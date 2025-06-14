from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, JSON
from infrastructure.database import db

class EmailNotificationStatus(str, Enum):
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'

class EmailNotification(db.Model):
    __tablename__ = 'email_notifications'

    id = Column(Integer, primary_key=True)
    subject = Column(String(255), nullable=False)
    content = Column(String(10000), nullable=False)
    recipients = Column(JSON, nullable=False)
    template_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default=EmailNotificationStatus.PENDING.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
