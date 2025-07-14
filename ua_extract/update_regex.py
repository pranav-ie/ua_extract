import os
import shutil
import subprocess
import tempfile

class Regexes:
    def __init__(
        self,
        upstream_path: str = "ua_extract/regexes/upstream",
        repo_url: str = "https://github.com/matomo-org/device-detector.git",
        branch: str = "master",
        sparse_dir: str = "regexes",
        cleanup: bool = True
    ):
        self.upstream_path = upstream_path
        self.repo_url = repo_url
        self.branch = branch
        self.sparse_dir = sparse_dir
        self.cleanup = cleanup

    def update_user_agents(self):
        if self.cleanup and os.path.exists(self.upstream_path):
            shutil.rmtree(self.upstream_path)

        with tempfile.TemporaryDirectory() as temp:
            subprocess.run([
                "git", "clone",
                "--depth", "1",
                "--filter=blob:none",
                "--sparse",
                "--branch", self.branch,
                self.repo_url,
                temp
            ], check=True)

            subprocess.run([
                "git", "-C", temp,
                "sparse-checkout", "set", self.sparse_dir
            ], check=True)

            os.makedirs(os.path.dirname(self.upstream_path), exist_ok=True)
            shutil.move(os.path.join(temp, self.sparse_dir), self.upstream_path)
