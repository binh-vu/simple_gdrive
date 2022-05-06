import click, os
from simple_gdrive.auth import auth
from tqdm import tqdm
from loguru import logger
from pathlib import Path
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build


@click.command()
@click.option("--file", help="file id or file path")
@click.option("-o", "--output", help="output file path")
def download(file: str, output: str):
    service = build("drive", "v3", credentials=auth())

    if os.path.exists(file):
        pass

    req = service.files().get_media(fileId=file)
    with open(output, "wb") as fh:
        try:
            downloader = MediaIoBaseDownload(fh, req)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
        except HttpError as error:
            logger.exception(error)


@click.command()
@click.option("--file", help="input file")
@click.option("-d", "--dest", help="the destination folder")
@click.option("--mimetype", help="mime type")
def upload(file: str, dest: str, mimetype: str):
    service = build("drive", "v3", credentials=auth())

    if not os.path.exists(file):
        logger.error(f"{file} not exists")
        return

    file_metadata = {"name": os.path.basename(file)}
    media = MediaFileUpload(file, mimetype=mimetype, resumable=True)

    resp = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print("File ID: %s" % resp.get("id"))


@click.group()
def cli():
    pass


cli.add_command(download)
cli.add_command(upload)


if __name__ == "__main__":
    cli()
