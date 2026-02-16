"""
============================================================================
alerts.py - Sistema de Alertas Multi-Canal
============================================================================
Sistema de alertas para Slack, Microsoft Teams, Email y Webhooks genéricos

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Metodología: DVP-PRO
============================================================================
"""

import os
import logging
import json
import smtplib
from typing import Dict, Any, Optional, List
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import requests

logger = logging.getLogger(__name__)


class AlertLevel:
    """Niveles de alerta."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AlertManager:
    """
    Gestor de alertas multi-canal para el sistema de forecasting.

    Soporta:
    - Slack
    - Microsoft Teams
    - Email
    - Webhooks genéricos
    """

    def __init__(self):
        """Inicializa el gestor de alertas."""
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
        self.teams_webhook = os.getenv("TEAMS_WEBHOOK_URL")
        self.generic_webhook = os.getenv("GENERIC_WEBHOOK_URL")

        # Email config
        self.email_from = os.getenv("ALERT_EMAIL_FROM")
        self.email_to = os.getenv("ALERT_EMAIL_TO")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")

        # Project info
        self.project_name = os.getenv("PROJECT_NAME", "Walmart Demand Forecasting")
        self.environment = os.getenv("ENVIRONMENT", "production")

    def send_alert(self,
                   title: str,
                   message: str,
                   level: str = AlertLevel.INFO,
                   metrics: Optional[Dict[str, Any]] = None,
                   channels: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Envía alerta a múltiples canales.

        Args:
            title: Título de la alerta
            message: Mensaje descriptivo
            level: Nivel de alerta (INFO, WARNING, ERROR, CRITICAL)
            metrics: Métricas adicionales a incluir
            channels: Canales específicos (si None, usa todos configurados)

        Returns:
            Diccionario con resultado por canal
        """
        results = {}

        # Preparar payload base
        alert_data = {
            'title': title,
            'message': message,
            'level': level,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'project': self.project_name,
            'environment': self.environment,
            'metrics': metrics or {}
        }

        # Determinar canales a usar
        if channels is None:
            channels = ['slack', 'teams', 'email', 'webhook']

        # Enviar a cada canal
        if 'slack' in channels and self.slack_webhook:
            results['slack'] = self._send_slack(alert_data)

        if 'teams' in channels and self.teams_webhook:
            results['teams'] = self._send_teams(alert_data)

        if 'email' in channels and self.email_from and self.email_to:
            results['email'] = self._send_email(alert_data)

        if 'webhook' in channels and self.generic_webhook:
            results['webhook'] = self._send_webhook(alert_data)

        return results

    def _send_slack(self, alert_data: Dict[str, Any]) -> bool:
        """
        Envía alerta a Slack.

        Args:
            alert_data: Datos de la alerta

        Returns:
            True si se envió correctamente
        """
        try:
            # Color según nivel
            color_map = {
                AlertLevel.INFO: "#36a64f",  # Verde
                AlertLevel.WARNING: "#ff9900",  # Naranja
                AlertLevel.ERROR: "#ff0000",  # Rojo
                AlertLevel.CRITICAL: "#8b0000"  # Rojo oscuro
            }

            color = color_map.get(alert_data['level'], "#808080")

            # Construir payload de Slack
            payload = {
                "username": "Walmart Forecasting Bot",
                "icon_emoji": ":chart_with_upwards_trend:",
                "attachments": [
                    {
                        "color": color,
                        "title": f"{alert_data['level']}: {alert_data['title']}",
                        "text": alert_data['message'],
                        "fields": [
                            {
                                "title": "Proyecto",
                                "value": alert_data['project'],
                                "short": True
                            },
                            {
                                "title": "Ambiente",
                                "value": alert_data['environment'],
                                "short": True
                            },
                            {
                                "title": "Timestamp",
                                "value": alert_data['timestamp'],
                                "short": False
                            }
                        ],
                        "footer": "Walmart Demand Forecasting",
                        "ts": int(datetime.now().timestamp())
                    }
                ]
            }

            # Agregar métricas si existen
            if alert_data['metrics']:
                for key, value in alert_data['metrics'].items():
                    payload["attachments"][0]["fields"].append({
                        "title": key,
                        "value": str(value),
                        "short": True
                    })

            # Enviar a Slack
            response = requests.post(
                self.slack_webhook,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                logger.info("✅ Alerta enviada a Slack")
                return True
            else:
                logger.error(f"❌ Error enviando a Slack: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"❌ Error enviando alerta a Slack: {e}")
            return False

    def _send_teams(self, alert_data: Dict[str, Any]) -> bool:
        """
        Envía alerta a Microsoft Teams.

        Args:
            alert_data: Datos de la alerta

        Returns:
            True si se envió correctamente
        """
        try:
            # Color según nivel
            color_map = {
                AlertLevel.INFO: "00FF00",  # Verde
                AlertLevel.WARNING: "FFA500",  # Naranja
                AlertLevel.ERROR: "FF0000",  # Rojo
                AlertLevel.CRITICAL: "8B0000"  # Rojo oscuro
            }

            theme_color = color_map.get(alert_data['level'], "808080")

            # Construir payload de Teams (MessageCard format)
            payload = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "summary": alert_data['title'],
                "themeColor": theme_color,
                "title": f"{alert_data['level']}: {alert_data['title']}",
                "text": alert_data['message'],
                "sections": [
                    {
                        "activityTitle": "Detalles de la Alerta",
                        "facts": [
                            {
                                "name": "Proyecto",
                                "value": alert_data['project']
                            },
                            {
                                "name": "Ambiente",
                                "value": alert_data['environment']
                            },
                            {
                                "name": "Timestamp",
                                "value": alert_data['timestamp']
                            }
                        ]
                    }
                ]
            }

            # Agregar métricas si existen
            if alert_data['metrics']:
                metrics_facts = [
                    {"name": key, "value": str(value)}
                    for key, value in alert_data['metrics'].items()
                ]
                payload["sections"].append({
                    "activityTitle": "Métricas",
                    "facts": metrics_facts
                })

            # Enviar a Teams
            response = requests.post(
                self.teams_webhook,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                logger.info("✅ Alerta enviada a Teams")
                return True
            else:
                logger.error(f"❌ Error enviando a Teams: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"❌ Error enviando alerta a Teams: {e}")
            return False

    def _send_email(self, alert_data: Dict[str, Any]) -> bool:
        """
        Envía alerta por Email.

        Args:
            alert_data: Datos de la alerta

        Returns:
            True si se envió correctamente
        """
        try:
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"[{alert_data['level']}] {alert_data['title']}"
            msg['From'] = self.email_from
            msg['To'] = self.email_to

            # Construir contenido HTML
            html_content = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; }}
                        .header {{ background-color: #f0f0f0; padding: 20px; }}
                        .content {{ padding: 20px; }}
                        .metrics {{ background-color: #f9f9f9; padding: 15px; border-left: 4px solid #4CAF50; }}
                        .footer {{ background-color: #f0f0f0; padding: 10px; font-size: 12px; color: #666; }}
                        table {{ border-collapse: collapse; width: 100%; }}
                        td, th {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h2>[{alert_data['level']}] {alert_data['title']}</h2>
                    </div>
                    <div class="content">
                        <p><strong>Mensaje:</strong> {alert_data['message']}</p>
                        <p><strong>Proyecto:</strong> {alert_data['project']}</p>
                        <p><strong>Ambiente:</strong> {alert_data['environment']}</p>
                        <p><strong>Timestamp:</strong> {alert_data['timestamp']}</p>
            """

            # Agregar métricas si existen
            if alert_data['metrics']:
                html_content += """
                        <div class="metrics">
                            <h3>Métricas</h3>
                            <table>
                """
                for key, value in alert_data['metrics'].items():
                    html_content += f"<tr><td><strong>{key}</strong></td><td>{value}</td></tr>"

                html_content += """
                            </table>
                        </div>
                """

            html_content += """
                    </div>
                    <div class="footer">
                        <p>Este es un mensaje automatizado del sistema Walmart Demand Forecasting</p>
                        <p>DVP-PRO Methodology - Ing. Daniel Varela Perez</p>
                    </div>
                </body>
            </html>
            """

            # Adjuntar HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Enviar email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info("✅ Alerta enviada por Email")
            return True

        except Exception as e:
            logger.error(f"❌ Error enviando alerta por Email: {e}")
            return False

    def _send_webhook(self, alert_data: Dict[str, Any]) -> bool:
        """
        Envía alerta a webhook genérico.

        Args:
            alert_data: Datos de la alerta

        Returns:
            True si se envió correctamente
        """
        try:
            # Enviar payload completo como JSON
            response = requests.post(
                self.generic_webhook,
                json=alert_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code in [200, 201, 202]:
                logger.info("✅ Alerta enviada a Webhook genérico")
                return True
            else:
                logger.error(f"❌ Error enviando a Webhook: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"❌ Error enviando alerta a Webhook: {e}")
            return False

    def send_model_performance_alert(self,
                                     metrics: Dict[str, float],
                                     threshold_violations: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Envía alerta de performance del modelo.

        Args:
            metrics: Métricas del modelo
            threshold_violations: Lista de umbrales violados

        Returns:
            Resultados del envío
        """
        # Determinar nivel de alerta
        if threshold_violations:
            level = AlertLevel.WARNING if len(threshold_violations) <= 2 else AlertLevel.ERROR
            title = "Degradación de Performance del Modelo"
            message = f"El modelo presenta {len(threshold_violations)} violaciones de umbral: {', '.join(threshold_violations)}"
        else:
            level = AlertLevel.INFO
            title = "Reporte de Performance del Modelo"
            message = "El modelo está operando dentro de los parámetros esperados"

        return self.send_alert(
            title=title,
            message=message,
            level=level,
            metrics=metrics
        )

    def send_drift_alert(self,
                        drift_score: float,
                        feature_drifts: Dict[str, float],
                        threshold: float = 0.1) -> Dict[str, bool]:
        """
        Envía alerta de data drift.

        Args:
            drift_score: Score global de drift
            feature_drifts: Drifts por feature
            threshold: Umbral de drift

        Returns:
            Resultados del envío
        """
        # Determinar nivel
        if drift_score > threshold * 2:
            level = AlertLevel.CRITICAL
        elif drift_score > threshold:
            level = AlertLevel.WARNING
        else:
            level = AlertLevel.INFO

        # Top features con drift
        top_drifts = sorted(feature_drifts.items(), key=lambda x: x[1], reverse=True)[:5]
        drift_list = [f"{feat}: {score:.4f}" for feat, score in top_drifts]

        title = "Detección de Data Drift"
        message = f"Drift score global: {drift_score:.4f} (umbral: {threshold:.4f}). Top features: {', '.join(drift_list)}"

        metrics = {
            'drift_score': drift_score,
            'threshold': threshold,
            'features_with_drift': len([s for s in feature_drifts.values() if s > threshold])
        }

        return self.send_alert(
            title=title,
            message=message,
            level=level,
            metrics=metrics
        )

    def send_training_complete_alert(self,
                                     metrics: Dict[str, float],
                                     model_name: str,
                                     run_id: Optional[str] = None) -> Dict[str, bool]:
        """
        Envía alerta de entrenamiento completado.

        Args:
            metrics: Métricas del modelo
            model_name: Nombre del modelo
            run_id: ID del run de MLflow

        Returns:
            Resultados del envío
        """
        title = f"Entrenamiento Completado: {model_name}"
        message = f"El modelo {model_name} ha sido entrenado exitosamente."

        if run_id:
            metrics['mlflow_run_id'] = run_id

        return self.send_alert(
            title=title,
            message=message,
            level=AlertLevel.INFO,
            metrics=metrics
        )

    def send_prediction_batch_alert(self,
                                    total_predictions: int,
                                    total_demand: float,
                                    stats: Dict[str, Any]) -> Dict[str, bool]:
        """
        Envía alerta de batch de predicciones.

        Args:
            total_predictions: Total de predicciones generadas
            total_demand: Demanda total predicha
            stats: Estadísticas adicionales

        Returns:
            Resultados del envío
        """
        title = "Batch de Predicciones Generado"
        message = f"Se generaron {total_predictions:,} predicciones con demanda total de {total_demand:,.0f} unidades"

        return self.send_alert(
            title=title,
            message=message,
            level=AlertLevel.INFO,
            metrics=stats
        )


# Singleton instance
_alert_manager = None


def get_alert_manager() -> AlertManager:
    """Obtiene instancia singleton del AlertManager."""
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager


if __name__ == "__main__":
    # Demo
    logging.basicConfig(level=logging.INFO)

    manager = get_alert_manager()

    # Test alert
    results = manager.send_alert(
        title="Test Alert",
        message="Este es un mensaje de prueba del sistema de alertas",
        level=AlertLevel.INFO,
        metrics={
            'mae': 0.85,
            'rmse': 1.23,
            'mape': 15.4
        }
    )

    print(f"Resultados: {results}")
