from typing import Any
import click, os
from simple_gdrive.auth import auth
from tqdm import tqdm
from loguru import logger
from simple_gdrive.config import Config, Scope
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build

from simple_gdrive.fs import GPath


@click.command()
@click.option("-s", "--source", help="file path", default="")
@click.option("-i", "--fileid", help="file id", default="")
@click.option("-d", "--dest", help="output file path")
@click.option(
    "-p",
    "--permission",
    help="scope of your application",
    default=Scope.readonly.name,
    type=click.Choice([scope.name for scope in Scope]),
)
def download(source: str, fileid: str, dest: str, permission: str):
    scope = Scope[permission]
    service = build("drive", "v3", credentials=auth(scope))

    if os.path.exists(source):
        pass

    if fileid.strip() != "":
        fileId = fileid
    else:
        if source.strip() == "":
            raise Exception("source or file id is required")
        fileId = GPath.from_str(source).get_id(service)

    req = service.files().get_media(fileId=fileId)
    with open(dest, "wb") as fh:
        try:
            downloader = MediaIoBaseDownload(fh, req)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%.\r" % int(status.progress() * 100), end="")
        except HttpError as error:
            logger.exception(error)


@click.command()
@click.option("-s", "--source", help="input file")
@click.option(
    "-d",
    "--dest",
    help="the destination folder, starts with `//` to set a specific shared drive, or just `/` to use the default drive of your account",
)
@click.option("--mimetype", help="mime type")
@click.option(
    "-p",
    "--permission",
    help="scope of your application",
    default=Scope.all.name,
    type=click.Choice([scope.name for scope in Scope]),
)
def upload(source: str, dest: str, mimetype: str, permission: str):
    scope = Scope[permission]
    service = build("drive", "v3", credentials=auth(scope))

    if not os.path.exists(source):
        logger.error(f"{source} not exists")
        return

    folder_id = GPath.from_str(dest).get_id(service)

    file: Any = {"name": os.path.basename(source)}
    if folder_id is not None:
        file["parents"] = [folder_id]
    media = MediaFileUpload(source, mimetype=mimetype, resumable=True)

    req = service.files().create(
        body=file, media_body=media, fields="id", supportsAllDrives=True
    )
    resp = None
    media.stream()
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print("Uploaded %d%%.\r" % int(status.progress() * 100), end="", flush=True)

    logger.info(
        "\nUpload file {} to {} successfully.\nThe file is located at is: {}",
        source,
        dest,
        f"https://drive.google.com/drive/folders/{folder_id}",
    )


@click.group()
def cli():
    pass


cli.add_command(download)
cli.add_command(upload)


if __name__ == "__main__":
    cli()
