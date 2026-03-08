"""Notification tool for sending async notifications to Home Assistant."""

from typing import Any, Awaitable, Callable

from nanobot.agent.tools.base import Tool


class NotificationTool(Tool):
    """Tool to send persistent notifications to Home Assistant."""

    def __init__(
        self,
        send_callback: Callable[[str, str, str | None], Awaitable[None]] | None = None,
    ):
        """Initialize the notification tool.

        Args:
            send_callback: Async callback to send notification (title, message, notification_id)
        """
        self._send_callback = send_callback

    def set_send_callback(
        self, callback: Callable[[str, str, str | None], Awaitable[None]]
    ) -> None:
        """Set the callback for sending notifications."""
        self._send_callback = callback

    @property
    def name(self) -> str:
        return "ha_notify"

    @property
    def description(self) -> str:
        return (
            "Send a persistent notification to Home Assistant. "
            "Use this for important alerts, task completion notifications, "
            "or async updates that should be visible in the HA UI."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Notification title"
                },
                "message": {
                    "type": "string",
                    "description": "Notification message body"
                },
                "notification_id": {
                    "type": "string",
                    "description": "Optional: unique ID for the notification (allows updates/dismissal)"
                }
            },
            "required": ["title", "message"]
        }

    async def execute(
        self,
        title: str,
        message: str,
        notification_id: str | None = None,
        **kwargs: Any
    ) -> str:
        if not self._send_callback:
            return "Error: Home Assistant notification not available (not connected)"

        try:
            await self._send_callback(title, message, notification_id)
            return f"Notification sent to Home Assistant: {title}"
        except Exception as e:
            return f"Error sending notification: {str(e)}"
