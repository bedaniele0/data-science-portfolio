"""
============================================================================
alerts.py - Multi-Channel Alerting System para Fraud Detection
============================================================================
Sistema de alertas con soporte para Slack, Teams, Email y Webhook

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Metodología: DVP-PRO
============================================================================
"""

import json
import logging
import os
import smtplib
from dataclasses import dataclass
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class AlertSeverity(Enum):
    """Severidad de la alerta."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertChannel(Enum):
    """Canales de notificación."""
    SLACK = "slack"
    TEAMS = "teams"
    EMAIL = "email"
    WEBHOOK = "webhook"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Alert:
    """Representa una alerta del sistema."""
    title: str
    message: str
    severity: AlertSeverity
    timestamp: Optional[str] = None
    metrics: Optional[Dict] = None
    metadata: Optional[Dict] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================================================
# ALERT MANAGER
# ============================================================================

class AlertManager:
    """Gestor central de alertas multi-canal."""

    def __init__(self):
        """Inicializa el Alert Manager."""
        self.slack_enabled = os.getenv("SLACK_ENABLED", "false").lower() == "true"
        self.teams_enabled = os.getenv("TEAMS_ENABLED", "false").lower() == "true"
        self.email_enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"

        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
        self.teams_webhook = os.getenv("TEAMS_WEBHOOK_URL")

    def send_alert(
        self,
        title: str,
        message: str,
        severity: AlertSeverity = AlertSeverity.INFO,
        metrics: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
    ) -> Dict[AlertChannel, bool]:
        """
        Envía alerta a todos los canales habilitados.

        Args:
            title: Título de la alerta
            message: Mensaje de la alerta
            severity: Severidad (INFO, WARNING, ERROR, CRITICAL)
            metrics: Métricas a incluir
            metadata: Metadata adicional

        Returns:
            Diccionario con resultado por canal
        """
        alert = Alert(
            title=title,
            message=message,
            severity=severity,
            metrics=metrics,
            metadata=metadata,
        )

        results = {}

        if self.slack_enabled and self.slack_webhook:
            results[AlertChannel.SLACK] = self._send_slack(alert)

        if self.teams_enabled and self.teams_webhook:
            results[AlertChannel.TEAMS] = self._send_teams(alert)

        if self.email_enabled:
            results[AlertChannel.EMAIL] = self._send_email(alert)

        return results

    def _send_slack(self, alert: Alert) -> bool:
        """Envía alerta a Slack."""
        try:
            color_map = {
                AlertSeverity.INFO: "#36a64f",
                AlertSeverity.WARNING: "#ff9800",
                AlertSeverity.ERROR: "#f44336",
                AlertSeverity.CRITICAL: "#9c27b0",
            }

            payload = {
                "channel": os.getenv("SLACK_CHANNEL", "#fraud-detection-alerts"),
                "username": "Fraud Detection Bot",
                "icon_emoji": ":shield:",
                "attachments": [{
                    "color": color_map.get(alert.severity, "#808080"),
                    "title": alert.title,
                    "text": alert.message,
                    "footer": f"Fraud Detection System | {alert.severity.value.upper()}",
                    "ts": int(datetime.now().timestamp()),
                }],
            }

            response = requests.post(self.slack_webhook, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Slack alert sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            return False

    def _send_teams(self, alert: Alert) -> bool:
        """Envía alerta a Microsoft Teams."""
        try:
            color_map = {
                AlertSeverity.INFO: "0078D4",
                AlertSeverity.WARNING: "FF8C00",
                AlertSeverity.ERROR: "D13438",
                AlertSeverity.CRITICAL: "5C2D91",
            }

            payload = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "summary": alert.title,
                "themeColor": color_map.get(alert.severity, "808080"),
                "title": f"Fraud Detection Alert: {alert.title}",
                "sections": [{
                    "activityTitle": alert.message,
                    "activitySubtitle": f"Severity: {alert.severity.value.upper()}",
                }],
            }

            response = requests.post(self.teams_webhook, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Teams alert sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send Teams alert: {e}")
            return False

    def _send_email(self, alert: Alert) -> bool:
        """Envía alerta por email."""
        try:
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", 587))
            smtp_username = os.getenv("SMTP_USERNAME")
            smtp_password = os.getenv("SMTP_PASSWORD")
            from_email = os.getenv("ALERT_EMAIL_FROM")
            to_email = os.getenv("ALERT_EMAIL_TO")

            if not all([smtp_username, smtp_password, from_email, to_email]):
                logger.error("Email configuration incomplete")
                return False

            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"[Fraud Detection Alert] {alert.title}"
            msg["From"] = from_email
            msg["To"] = to_email

            html_body = f"""
            <html>
            <body>
                <h2>{alert.title}</h2>
                <p><strong>Severity:</strong> {alert.severity.value.upper()}</p>
                <p>{alert.message}</p>
                <p><strong>Timestamp:</strong> {alert.timestamp}</p>
            </body>
            </html>
            """

            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)

            logger.info(f"Email alert sent to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False

    def send_drift_alert(
        self,
        feature_name: str,
        drift_score: float,
        threshold: float = 0.2,
    ) -> Dict[AlertChannel, bool]:
        """Envía alerta de drift detectado."""
        severity = AlertSeverity.WARNING if drift_score < 0.3 else AlertSeverity.CRITICAL

        return self.send_alert(
            title=f"Data Drift Detected: {feature_name}",
            message=f"Drift score ({drift_score:.4f}) exceeds threshold ({threshold:.4f}). "
                   f"Consider retraining the model.",
            severity=severity,
            metrics={"drift_score": drift_score, "threshold": threshold, "feature": feature_name},
            metadata={"alert_type": "data_drift", "model": "fraud-detection-model"},
        )

    def send_fraud_spike_alert(
        self,
        current_rate: float,
        expected_rate: float,
    ) -> Dict[AlertChannel, bool]:
        """Envía alerta de spike en tasa de fraude."""
        increase = abs(current_rate - expected_rate) / expected_rate * 100 if expected_rate > 0 else 0

        severity = AlertSeverity.WARNING if increase < 50 else AlertSeverity.CRITICAL

        return self.send_alert(
            title="Fraud Rate Spike Detected",
            message=f"Current fraud rate ({current_rate:.2%}) is {increase:.1f}% higher "
                   f"than expected ({expected_rate:.2%}). Investigate immediately.",
            severity=severity,
            metrics={
                "current_fraud_rate": current_rate,
                "expected_fraud_rate": expected_rate,
                "increase_pct": increase,
            },
            metadata={"alert_type": "fraud_spike"},
        )
