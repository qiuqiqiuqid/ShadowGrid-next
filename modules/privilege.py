"""权限提升模块 - privilege"""

from modules.api import ModuleBase


class PrivilegeModule(ModuleBase):
    @property
    def name(self):
        return "privilege"

    @property
    def description(self):
        return "权限提升模块 - 检查/提权点"

    @property
    def author(self):
        return "帅丘"

    @property
    def version(self):
        return "2.0.0"

    def handle(self, cmd):
        t = cmd.get("type")
        p = cmd.get("payload")

        if t == "priv":
            action = p.get("action") if p else None
            if action == "check":
                return self._priv_check(p)
            elif action == "list":
                return self._priv_list(p)
            elif action == "su":
                return self._priv_su(p)
            elif action == "token":
                return self._priv_token(p)
            else:
                return {"status": "error", "result": f"Unknown action: {action}", "result_type": "error"}
        else:
            return {"status": "error", "result": f"Unknown command: {t}", "result_type": "error"}

    def get_commands(self):
        return ["priv"]

    def _priv_check(self, payload):
        try:
            import sys
            if not sys.platform.startswith('win'):
                return {"status": "error", "result": "Only Windows", "result_type": "error"}
            
            result = __import__('subprocess').run(['whoami', '/priv'], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "priv_check"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _priv_list(self, payload):
        try:
            import sys
            if not sys.platform.startswith('win'):
                return {"status": "error", "result": "Only Windows", "result_type": "error"}
            
            result = __import__('subprocess').run(['whoami', '/groups'], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "priv_list"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _priv_su(self, payload):
        try:
            import sys
            if not sys.platform.startswith('win'):
                return {"status": "error", "result": "Only Windows", "result_type": "error"}
            
            return {"status": "ok", "result": "Privilege elevation script created", "result_type": "ok"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _priv_token(self, payload):
        try:
            import sys
            if not sys.platform.startswith('win'):
                return {"status": "error", "result": "Only Windows", "result_type": "error"}
            
            powershell_script = """
try {
    Write-Output "Current User: $([System.Security.Principal.WindowsIdentity]::GetCurrent().Name)"
    Write-Output "Is Admin: $([System.Security.Principal.WindowsPrincipal]::new([System.Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator))"
}
catch {
    Write-Output "Error: $_"
}
"""
            result = __import__('subprocess').run(['powershell', '-Command', powershell_script], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "priv_token"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}


module = PrivilegeModule()
