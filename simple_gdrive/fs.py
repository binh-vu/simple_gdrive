from optparse import Option
from re import I
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class GFileId:
    id: str
    name: str


@dataclass
class GPath:
    """Path of an item (file or folder) in Google Drive"""

    paths: List[str]
    drive_name: Optional[str]

    @staticmethod
    def from_str(path: str) -> "GPath":
        if path.endswith("/"):
            path = path[:-1]

        assert path.startswith(
            "/"
        ), f"Invalid path: {path}. Should starts with `/` (your drive) or `//<shared_drive_name>` (a shared drive)"

        if path.startswith("//"):
            path = path[2:]
            if path.find("/") == -1:
                drive_name = path
                paths = []
            else:
                drive_name, path = path.split("/", 1)
                paths = path.split("/")
        else:
            drive_name = None
            paths = path[1:].split("/")
        return GPath(paths, drive_name)

    def get_id(self, service) -> Optional[GFileId]:
        """Get id of the folder or file in a drive.

        Args:
            service: Google Drive service instance.
            path: Path to the file or folder.
            drive_name: Name of the shared drive.
        """
        files = service.files()
        if self.drive_name is not None:
            drive_id = self.get_drive_id(service)
            args = {
                "corpora": "drive",
                "driveId": drive_id,
                "includeItemsFromAllDrives": True,
                "supportsAllDrives": True,
            }
            parent = drive_id
            filename = self.drive_name
        else:
            args = {
                "corpora": "user",
            }
            parent = "root"
            filename = "user"

        if len(self.paths) == 0:
            if self.drive_name is None:
                return None
            else:
                return GFileId(id=parent, name=filename)

        for name in self.paths:
            resp = files.list(
                q=f"name = '{name}' and '{parent}' in parents",
                fields="files(kind, id, name, mimeType, driveId, parents)",
                pageSize=1,
                **args,
            ).execute()

            file = resp.get("files")[0]
            parent = file["id"]
            filename = file["name"]

        return GFileId(id=parent, name=filename)

    def get_drive_id(self, service):
        resp = service.drives().list().execute()
        for drive in resp.get("drives"):
            if drive["name"] == self.drive_name:
                return drive["id"]

        raise Exception(f"Drive {self.drive_name} not found")
