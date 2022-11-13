**simple-gdrive**: A simple command to help download and upload big files to Google Drive (using their official APIs)

### Setup

Before using the command, you must open Google Cloud Platform and create credentials for oauth: [cloud.google.com](https://cloud.google.com) > APIs & Services > Credentials. Note that if your project hasn't enabled Drive APIs, go to APIs & Services > Enabled APIs & Services and add Drive APIs.
Then, download the JSON file and put it in the AuthDir (default at `~/.simple_gdrive`) with the name `credentials.json`. When you run the script for the first time, it will redirect to your browser so you can authenicate and give permission to YOUR application (created in the previous step) to access to your drive. Then, you will obtain an access token saving to the same drive with name `tokens.json`. Keeping the two files safe (or delete `tokens.json` after usage) and nobody else will have access to your data.

### Installation

```bash
pip install simple-gdrive
```

### Usage

Invoke the command by running `gdrive` or `python -m simple_gdrive`.

Download a file:

```bash
gdrive download -s <path in disk> -d <path in drive>
```

Upload a file

```bash
gdrive upload -s <file path in disk> -d <path in drive>
```

For example:

```bash
gdrive download -s //KGData/Wikipedia/20220420/enwiki-NS0-20220420-ENTERPRISE-HTML.json.tar.gz -d enwiki.json.tar.gz
```

```bash
gdrive upload -s ./enwiki-NS0-20220420-ENTERPRISE-HTML.json.tar.gz -d //KGData/Wikipedia/20220420/enwiki-NS0-20220420-ENTERPRISE-HTML.json.tar.gz
```

If the path in Google drive startswith `/`, the top folder/file will be in your drive (e.g., `/abc` points to the folder `abc` in your drive). If it starts with `//`, the first level will be the name of the shared drive and the second level will be the folder/file in the shared drive (e.g., `//KGData/abc` points to the folder `abc` in KGData shared drive).
