Streamlit app deployment

This repository contains a Streamlit app `app .py`.

Deploy to Streamlit Cloud:

1. Create a GitHub repository and push this project (include `app .py` and `requirements.txt`).
2. Go to https://streamlit.io/cloud and sign in with GitHub.
3. Click "New app", select your repo and branch, then set the main file to `app .py` and deploy.

Notes:
- `requirements.txt` must list all Python dependencies.
- If your file name contains spaces (`app .py`), Streamlit Cloud can still run it; if issues arise, rename to `app.py` and update repository.

Secrets / API keys:
- Do NOT keep API keys in source. Use Streamlit Cloud secrets: on the app page go to "Settings → Secrets" and add `GOOGLE_API_KEY` with your key.
- The app reads the key from `st.secrets["GOOGLE_API_KEY"]` and will disable AI insights if it's missing.

Local test:

```bash
python -m streamlit run "app .py"
```
