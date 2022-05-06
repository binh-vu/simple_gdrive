**simple-gdrive**: A simple command to help download and upload big files to Google Drive (using their official APIs)

### Setup

Before using the command, you must open Google Cloud Platform and create credentials for oauth: [cloud.google.com](https://cloud.google.com) > APIs & Services > Credentials. Note that if your project hasn't enabled Drive APIs, go to APIs & Services > Enabled APIs & Services and add Drive APIs.
Then, download the JSON file and put it in the AuthDir (default at `~/.simple_drive`) with the name `credentials.json`.

### Usage

Download a file:

```bash
python -m simple_gdrive download -s <path in disk> -d <path in drive>
```

Upload a file

```bash
python -m simple_gdrive upload -s <file path in disk> -d <path in drive>
```
