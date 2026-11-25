import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "linux_audit_reconstruct.py"
SPEC = importlib.util.spec_from_file_location("linux_audit_reconstruct", MODULE_PATH)
assert SPEC
assert SPEC.loader
audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


class LinuxAuditReconstructTests(unittest.TestCase):
    def parse_text(self, text: str):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audit.log"
            path.write_text(text, encoding="utf-8")
            return [event.row() for event in audit.parse_audit_log(path)]

    def test_full_event_id_prevents_serial_collision(self):
        rows = self.parse_text(
            "\n".join(
                [
                    'type=SYSCALL msg=audit(10.100:90): syscall=59 pid=1 comm="first" exe="/bin/true"',
                    'type=SYSCALL msg=audit(20.200:90): syscall=59 pid=2 comm="second" exe="/bin/false"',
                ]
            )
        )
        self.assertEqual([row["event_id"] for row in rows], ["10.100:90", "20.200:90"])

    def test_quote_aware_hex_decoding_and_sockaddr(self):
        rows = self.parse_text(
            "\n".join(
                [
                    'type=SYSCALL msg=audit(1700000000.202:802): arch=c000003e syscall=59 success=yes ppid=1200 pid=1202 auid=1000 uid=1000 comm="wget" exe=2f7573722f62696e2f77676574 key="exec"',
                    'type=CWD msg=audit(1700000000.202:802): cwd="/tmp"',
                    'type=EXECVE msg=audit(1700000000.202:802): argc=3 a0=77676574 a1="3132" a2="http://192.0.2.10/payload"',
                    'type=SYSCALL msg=audit(1700000000.303:803): arch=c000003e syscall=42 success=yes ppid=1200 pid=1203 auid=1000 uid=1000 comm="wget" exe="/usr/bin/wget" key="net"',
                    'type=SOCKADDR msg=audit(1700000000.303:803): saddr=02000050C0000210',
                ]
            )
        )
        self.assertEqual(rows[0]["exe"], "/usr/bin/wget")
        self.assertEqual(rows[0]["argv"], ["wget", "3132", "http://192.0.2.10/payload"])
        self.assertEqual(rows[0]["cwd"], "/tmp")
        self.assertEqual(rows[1]["sockaddr"], ["192.0.2.16:80"])

    def test_execve_cwd_and_proctitle_join_by_epoch_serial(self):
        rows = self.parse_text(
            "\n".join(
                [
                    'type=EXECVE msg=audit(1700000000.101:801): argc=2 a0="cat" a1="/etc/shadow"',
                    'type=SYSCALL msg=audit(1700000000.101:801): arch=c000003e syscall=59 success=yes ppid=1200 pid=1201 auid=1000 uid=0 euid=0 comm="cat" exe="/usr/bin/cat" key="exec"',
                    'type=PROCTITLE msg=audit(1700000000.101:801): proctitle=636174002F6574632F736861646F77',
                    'type=CWD msg=audit(1700000000.101:801): cwd="/home/analyst"',
                ]
            )
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["command"], "cat /etc/shadow")
        self.assertEqual(rows[0]["pid"], "1201")
        self.assertEqual(rows[0]["ppid"], "1200")
        self.assertEqual(rows[0]["uid"], "0")
        self.assertEqual(rows[0]["euid"], "0")
        self.assertEqual(rows[0]["auid"], "1000")

    def test_nested_user_cmd_hex_is_decoded(self):
        rows = self.parse_text(
            'type=USER_CMD msg=audit(1789146867.406:90): pid=975 uid=1000 auid=1000 ses=1 '
            'msg=\'cwd="/home/Tom" cmd=73687574646F776E202D68206E6F77 exe="/usr/bin/sudo" '
            'terminal=tty1 res=success\'\n'
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["command"], "shutdown -h now")
        self.assertEqual(rows[0]["exe"], "/usr/bin/sudo")
        self.assertEqual(rows[0]["cwd"], "/home/Tom")
        self.assertEqual(rows[0]["tty"], "tty1")


if __name__ == "__main__":
    unittest.main()
