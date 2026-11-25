"""Guarded process execution must fail before launching unsafe commands."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import process_guard


class ProcessGuardTests(unittest.TestCase):
    def test_rejects_mutations_unknown_tools_and_control_bytes(self):
        for args in (["gh", "pr", "merge", "178"], ["git", "push", "origin"],
                     ["git", "remote", "add", "evil", "https://evil.invalid"],
                     ["git", "branch", "-D", "main"],
                     ["git", "reset", "--hard", "HEAD"],
                     ["git", "log", "--exec=evil"],
                     ["python", "-c", "print(1)"], ["gh", "api", "repos/a/b/pulls/1"],
                     ["gh", "pr", "view", "178\n--web"], ["git", "log", "bad\x00argument"]):
            with self.subTest(args=args), patch.object(process_guard.subprocess, "run") as call:
                with self.assertRaises(ValueError):
                    process_guard.invoke(args)
                call.assert_not_called()

    def test_git_allowlist_accepts_only_exact_read_operations(self):
        fake = Path(__file__).resolve()
        with patch.object(process_guard.shutil, "which", return_value=str(fake)), \
             patch.object(process_guard.subprocess, "run") as run:
            for args in process_guard.GIT_READ_OPERATIONS:
                with self.subTest(args=args):
                    process_guard.invoke(["git", *args])
            self.assertEqual(len(process_guard.GIT_READ_OPERATIONS), run.call_count)

    def test_diff_target_pattern_accepts_sha_and_rejects_arbitrary_ref(self):
        fake = Path(__file__).resolve()
        sha = "a" * 40
        with patch.object(process_guard.shutil, "which", return_value=str(fake)), \
             patch.object(process_guard.subprocess, "run") as run:
            process_guard.invoke(["git", "diff", "-z", "--name-only", "--no-renames", f"origin/main...{sha}"])
            self.assertEqual(1, run.call_count)

        for bad in ("main", "HEAD~1", "origin/main...main;rm", f"origin/main...{sha};evil"):
            with self.subTest(bad=bad), patch.object(process_guard.subprocess, "run") as call:
                with self.assertRaises(ValueError):
                    process_guard.invoke(["git", "diff", "-z", "--name-only", "--no-renames", bad])
                call.assert_not_called()

    def test_allowed_gh_uses_absolute_binary_and_no_shell(self):
        fake = Path(__file__).resolve()
        with patch.object(process_guard.shutil, "which", return_value=str(fake)), \
             patch.object(process_guard.subprocess, "run") as run:
            process_guard.invoke(["gh", "pr", "checks", "178"])
            self.assertEqual(str(fake), run.call_args.args[0][0])
            self.assertIs(False, run.call_args.kwargs["shell"])
            self.assertIs(False, run.call_args.kwargs["check"])


    def test_graphql_accepts_only_known_fields_and_operations(self):
        fake = Path(__file__).resolve()
        good = (["gh", "api", "graphql", "-f", "query=query($owner:String!){x}", "-f", "owner=o",
                 "-f", "name=n", "-F", "number=1", "-f", "after=abc"],
                ["gh", "api", "graphql", "-f",
                 "query=mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{id}}}",
                 "-f", "id=PRRT_x"])
        bad = (["gh", "api", "graphql"],
               ["gh", "api", "graphql", "-f", "query=mutation{deleteRepository(x)}"],
               ["gh", "api", "graphql", "-f", "query=query{x}", "--hostname", "evil.invalid"],
               ["gh", "api", "graphql", "-f", "query=query{x}", "-H", "X: y"],
               ["gh", "api", "graphql", "-f", "query=query{x}", "--input", "file"],
               ["gh", "api", "graphql", "-f", "owner=o"],
               ["gh", "api", "graphql", "-F", "query=@file"])
        with patch.object(process_guard.shutil, "which", return_value=str(fake)), \
             patch.object(process_guard.subprocess, "run") as run:
            for args in good:
                with self.subTest(args=args):
                    process_guard.invoke(args)
            for args in bad:
                with self.subTest(args=args), self.assertRaises(ValueError):
                    process_guard.invoke(args)
        self.assertEqual(len(good), run.call_count)

    def test_ls_remote_accepts_only_origin_or_github_and_branch_refs(self):
        fake = Path(__file__).resolve()
        good = (["git", "ls-remote", "origin", "refs/heads/feat/pr-tool"],
                ["git", "ls-remote", "https://github.com/someone/fork.git", "refs/heads/main"])
        bad = (["git", "ls-remote", "--upload-pack=evil", "refs/heads/main"],
               ["git", "ls-remote", "https://evil.invalid/a/b.git", "refs/heads/main"],
               ["git", "ls-remote", "origin", "refs/heads/../x"],
               ["git", "ls-remote", "origin", "refs/tags/v1"])
        with patch.object(process_guard.shutil, "which", return_value=str(fake)), \
             patch.object(process_guard.subprocess, "run") as run:
            for args in good:
                process_guard.invoke(args)
            for args in bad:
                with self.subTest(args=args), self.assertRaises(ValueError):
                    process_guard.invoke(args)
        self.assertEqual(len(good), run.call_count)


if __name__ == "__main__":
    unittest.main()
