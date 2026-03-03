"""Shell 命令执行模块"""

from modules.api import ModuleBase


class ShellModule(ModuleBase):
    @property
    def name(self):
        return "shell"

    @property
    def description(self):
        return "Shell 命令执行模块"

    @property
    def author(self):
        return "帅丘"

    @property
    def version(self):
        return "2.0.0"

    def handle(self, cmd):
        t = cmd.get("type")
        p = cmd.get("payload")

        if t == "shell":
            return self._shell(p)
        else:
            return {"status": "error", "result": f"Unknown command: {t}", "result_type": "error"}

    def get_commands(self):
        return ["shell"]

    def _shell(self, payload):
        try:
            import subprocess
            result = subprocess.run(
                payload, shell=True, capture_output=True, text=True, timeout=30
            )
            output = result.stdout + result.stderr
            return {"status": "ok", "result": output, "result_type": "shell"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}


module = ShellModule()
