"""Celery Beat schedule configuration."""
from celery.schedules import crontab
from app.config import settings

# Celery Beat schedule
CELERY_BEAT_SCHEDULE = {
    # Monitor all prices every 30 minutes
    'monitor-all-prices': {
        'task': 'app.tasks.monitor_prices.monitor_all_prices',
        'schedule': settings.price_check_interval * 60.0,  # Convert minutes to seconds
        'options': {'queue': 'monitoring'}
    },
    
    # Monitor price sources every hour
    'monitor-sources-round': {
        'task': 'app.tasks.monitor_prices.monitor_sources_round',
        'schedule': 3600.0,  # Every hour
        'options': {'queue': 'monitoring'}
    },
    
    # Parse competitors every hour
    'parse-competitors': {
        'task': 'app.tasks.parse_competitors.parse_competitors',
        'schedule': settings.parse_interval * 60.0,
        'args': ('petrov',),
        'options': {'queue': 'parsing'}
    },
    
    # Calculate prices every hour
    'update-prices': {
        'task': 'app.tasks.update_prices.update_all_prices',
        'schedule': settings.price_calculate_interval * 60.0,
        'options': {'queue': 'pricing'}
    },
    
    # Cleanup old alerts daily at 3 AM
    'cleanup-old-alerts': {
        'task': 'app.tasks.maintenance.cleanup_old_alerts',
        'schedule': crontab(hour=3, minute=0),
        'options': {'queue': 'maintenance'}
    },
}
