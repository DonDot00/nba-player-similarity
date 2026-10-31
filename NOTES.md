# Notes: Windows commands (Git Bash)

Run everything below in **Git Bash**. Commands that differ in cmd or PowerShell are marked.

---

## One-time installs

1. **Python 3.11+** from python.org. Tick "Add python.exe to PATH".
   - Then turn off the Store shortcut: Settings > Apps > Advanced app settings > App execution aliases > switch off the two `python` entries.
2. **Git** (includes Git Bash).
3. **GitHub CLI** (optional): `winget install GitHub.cli`, then `gh auth login`.
4. **VS Code** + the Python extension.

Check them (open a new Git Bash window first):

```bash
python --version      # should say 3.11 or higher
git --version
gh --version          # optional
```

---

## Project setup

```bash
git clone <repo-url>
cd nba-player-similarity
py -m venv .venv                  # use "py" if "python" opens the Microsoft Store
source .venv/Scripts/activate     # Windows path: Scripts, not bin
pip install -r requirements.txt
pytest
```

Your prompt should show `(.venv)` after activating. Activate again every time you open a new terminal:

```bash
source .venv/Scripts/activate
```

| Shell | Activate command |
|---|---|
| Git Bash | `source .venv/Scripts/activate` |
| PowerShell | `.venv\Scripts\Activate.ps1` |
| cmd | `.venv\Scripts\activate.bat` |

If PowerShell blocks the script: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

---

## Daily git workflow

```bash
git checkout main
git pull                                  # get everyone's latest work
git checkout -b feature/<short-name>      # one branch per task

# ...write code, then:
pytest                                    # make sure tests pass
git status
git add <files>                           # add specific files, not everything
git commit -m "Your message here"
git push -u origin feature/<short-name>   # first push of the branch

gh pr create                              # open the pull request
```

After a teammate approves and CI passes, merge on GitHub, then:

```bash
git checkout main
git pull
git branch -d feature/<short-name>
```

Never push directly to `main`.

---

## Running things

```bash
pytest                          # all tests
pytest tests/test_features.py   # one file
pytest -k "rate_limited"        # tests whose name matches
pytest -x                       # stop at the first failure
pytest -v                       # verbose

python -m nba_similarity.pipeline                    # run the pipeline (once implemented)
uvicorn nba_similarity.api.main:app --reload         # start the API at http://127.0.0.1:8000
```

The API's auto-generated docs live at http://127.0.0.1:8000/docs.

---

## Packages

```bash
pip install pyarrow             # needed for Parquet files in data/raw/
pip install httpx pytest-asyncio  # for testing async / FastAPI code
pip freeze | grep -i <name>     # check what version is installed
pip install -r requirements.txt # re-run after a teammate adds packages
```

If you add a package, add it to `requirements.txt` in the same PR.

---

## Data

```bash
ls -lh data/raw/                # check file sizes (keep each under ~50 MB)
```

- `data/raw/` (Parquet or CSV) **is committed**.
- `data/*.db` (SQLite) is **never committed**. Build it locally from the raw files.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Python was not found; run without arguments to install from the Microsoft Store` | Install Python from python.org and turn off the App execution aliases (see above). |
| `python` works but `pip` doesn't | Use `python -m pip install ...`. |
| `source: .venv/bin/activate: No such file` | On Windows it's `.venv/Scripts/activate`. |
| `ModuleNotFoundError: nba_similarity` | Activate the venv, and run commands from the repo root. Check `pytest.ini` for the `pythonpath` setting. |
| `ModuleNotFoundError: pyarrow` | `pip install pyarrow` |
| NBA.com times out or blocks you | Increase the delay between requests. Don't loop on retries. |
| Tests hit the network | Mock the API. Tests must never call NBA.com. |
