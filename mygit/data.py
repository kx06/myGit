import hashlib
from pathlib import Path
from pathlib import PurePath


class MyGitFuncs:

    GIT_DIR = ".mygit"

    def __init__(self):
        self.cwd = Path.cwd()
        self.git_dir = self.cwd

        def find_root(cwd):
            root = PurePath(cwd).anchor
            while cwd != root:
                for i in Path.iterdir(cwd):
                    if i.is_dir():
                        if i.name == self.GIT_DIR:
                            self.git_dir = cwd / self.GIT_DIR
                            return True
                    cwd = cwd.parent
            return False

        find_root(self.cwd)

    def init(self):
        if Path(self.GIT_DIR).exists():
            raise Exception(f"repository already exists")
        Path(self.GIT_DIR).mkdir()
        Path(PurePath(self.GIT_DIR, "objects").joinpath()).mkdir()

    def hash_object(self, data, type_="blob"):
        obj = type_.encode() + b"\x00" + data
        oid = hashlib.sha256(obj).hexdigest()
        path = self.git_dir / "objects" / oid
        with path.open(mode="wb") as f:
            f.write(obj)
        return oid

    def get_object(self, oid, expected="blob"):
        path = self.git_dir / "objects" / oid
        if not path.exists():
            raise Exception(f"object {oid} not found")
        with path.open(mode="rb") as f:
            obj = f.read()
        type_, _, content = obj.partition(b"\x00")
        type_ = type_.decode()
        if expected is not None and type_ != expected:
            raise ValueError(f"Expected{expected}, got {type_}")
        return content
