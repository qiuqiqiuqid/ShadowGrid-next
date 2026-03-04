"""进程管理模块 - process"""

from modules.api import ModuleBase


class ProcessModule(ModuleBase):
    @property
    def name(self):
        return "process"

    @property
    def description(self):
        return "进程管理模块 - 查看/终止/执行"

    @property
    def author(self):
        return "帅丘"

    @property
    def version(self):
        return "2.0.0"

    def handle(self, cmd):
        t = cmd.get("type")
        p = cmd.get("payload")

        if t == "ps":
            return self._ps_list(p)
        elif t == "kill":
            return self._ps_kill(p)
        elif t == "exec":
            return self._ps_exec(p)
        elif t == "proc":
            return self._ps_info(p)
        else:
            return {"status": "error", "result": f"Unknown command: {t}", "result_type": "error"}

    def get_commands(self):
        return ["ps", "kill", "exec", "proc"]

    def _ps_list(self, payload):
        try:
            import sys
            if sys.platform.startswith('win'):
                result = __import__('subprocess').run(['tasklist'], capture_output=True, text=True, timeout=10)
            else:
                result = __import__('subprocess').run(['ps', 'aux'], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "ps_list"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _ps_kill(self, payload):
        try:
            pid = payload.get("pid") if payload else None
            if not pid:
                return {"status": "error", "result": "Need PID", "result_type": "error"}
            
            import sys
            if sys.platform.startswith('win'):
                result = __import__('subprocess').run(['taskkill', '/pid', str(pid), '/f'], capture_output=True, text=True, timeout=10)
            else:
                result = __import__('subprocess').run(['kill', '-9', str(pid)], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "ok"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _ps_exec(self, payload):
        try:
            exec_path = payload.get("path") if payload else None
            if not exec_path:
                return {"status": "error", "result": "Need path", "result_type": "error"}
            
            import sys
            if sys.platform.startswith('win'):
                __import__('subprocess').run([exec_path], creationflags=__import__('subprocess').CREATE_NO_WINDOW, timeout=5)
            else:
                __import__('subprocess').run([exec_path], timeout=5)
            
            return {"status": "ok", "result": f"Process started: {exec_path}", "result_type": "ok"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _ps_info(self, payload):
        try:
            pid = payload.get("pid") if payload else None
            if not pid:
                return {"status": "error", "result": "Need PID", "result_type": "error"}
            
            import sys
            if sys.platform.startswith('win'):
                result = __import__('subprocess').run(['tasklist', '/fi', f'pid eq {pid}'], capture_output=True, text=True, timeout=10)
            else:
                result = __import__('subprocess').run(['ps', '-p', str(pid), '-f'], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "proc_info"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}


module = ProcessModule()
