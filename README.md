# Three in a Row

A static frontend with a Python serverless function for bot move processing. No third-party packages are required.

## Run locally

```sh
python3 server.py
```

Then open http://127.0.0.1:8000. Bot difficulties are processed by `/api/bot-move`; the HTML, CSS, and JavaScript are served directly from this folder.

## Deploy to Vercel

Import this repository into Vercel and deploy from the project root. Vercel serves the root HTML, CSS, and JavaScript files statically and deploys `api/bot-move.py` as the `/api/bot-move` Python Function. No always-running Python server or build command is needed.

In **Bot vs bot** mode, choose a separate difficulty for Bot 1 (X) and Bot 2 (O). Random mode picks a difficulty for each bot at the start of each round and shows both selections.
