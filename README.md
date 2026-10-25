# Three in a Row

A small static frontend with a Python standard-library server for bot move processing. No dependencies are required.

## Run locally

```sh
python3 server.py
```

Then open http://127.0.0.1:8000. Bot difficulties are processed by `/api/bot-move`; the HTML, CSS, and JavaScript are served directly from this folder.

In **Bot vs bot** mode, choose a separate difficulty for Bot 1 (X) and Bot 2 (O). Random mode picks a difficulty for each bot at the start of each round and shows both selections.
