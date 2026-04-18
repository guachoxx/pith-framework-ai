#!/usr/bin/env bash
# Pith Framework — Notify on Stop Hook
# Sends a desktop notification when Claude Code completes a task.

TITLE="Pith Framework"
MESSAGE="Task completed — ready for your input"

case "$(uname -s)" in
    Darwin)
        osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\"" 2>/dev/null
        ;;
    Linux)
        if command -v notify-send &>/dev/null; then
            notify-send "$TITLE" "$MESSAGE" 2>/dev/null
        elif grep -qi microsoft /proc/version 2>/dev/null; then
            # WSL — use PowerShell toast via script block to avoid escape issues
            powershell.exe -NoProfile -Command '
                [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
                $template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02
                $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template)
                $text = $xml.GetElementsByTagName("text")
                $text[0].AppendChild($xml.CreateTextNode("Pith Framework")) | Out-Null
                $text[1].AppendChild($xml.CreateTextNode("Task completed -- ready for your input")) | Out-Null
                $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Pith Framework")
                $notifier.Show([Windows.UI.Notifications.ToastNotification]::new($xml))
            ' 2>/dev/null
        fi
        ;;
    MINGW*|MSYS*|CYGWIN*)
        # Native Windows (Git Bash / MSYS2) — use PowerShell toast
        powershell.exe -NoProfile -Command '
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            $template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02
            $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template)
            $text = $xml.GetElementsByTagName("text")
            $text[0].AppendChild($xml.CreateTextNode("Pith Framework")) | Out-Null
            $text[1].AppendChild($xml.CreateTextNode("Task completed -- ready for your input")) | Out-Null
            $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Pith Framework")
            $notifier.Show([Windows.UI.Notifications.ToastNotification]::new($xml))
        ' 2>/dev/null
        ;;
esac

exit 0
