# Auto YouTube Shorts (free-first starter)

This repository is a ready-to-run starter for generating a simple vertical Short using free/open-source tools, then optionally uploading it to YouTube.

## What it does
- Runs manually or on a daily GitHub Actions schedule.
- Creates a vertical 1080x1920 image video with narration.
- Uses a small set of sample facts (replace these with reviewed original scripts).
- Saves the MP4 as a downloadable GitHub Actions artifact.
- Optional YouTube upload is included, but requires YouTube API OAuth credentials.

## Important limitations
- This starter does **not** clone your voice. Free voice cloning is not reliably available as a hosted daily service. Use only a voice you own or have permission to use, and check the model licence and provider age rules.
- It does not use Claude API or another paid AI API. Sample scripts are built in. You can later add a free-tier model if its terms and limits fit.
- Automatic upload needs Google Cloud / YouTube Data API setup and a valid OAuth refresh token. The first run should be private/unlisted for testing.
- GitHub Actions free usage and artifact limits apply. Public repositories can expose code, so never commit keys, tokens, private audio, or credentials.
- Automated publishing can fail due to API quota, OAuth expiry/revocation, or YouTube project verification restrictions.

## Android setup
1. Download and unzip this project.
2. Open GitHub in Chrome and create/open your repository.
3. Upload all files and folders from this project. GitHub's web interface may require uploading files individually or using the GitHub mobile app; alternatively upload the ZIP contents from a computer.
4. In the repository, open **Actions** and enable workflows if prompted.
5. Open **Daily Shorts**, choose **Run workflow**, and start a test.
6. When complete, open the workflow run and download the `daily-short` artifact.

## Optional YouTube upload
1. In Google Cloud Console, create a project and enable YouTube Data API v3.
2. Configure OAuth consent and create OAuth client credentials.
3. Use the Google OAuth flow to obtain a refresh token with the YouTube upload scope:
   `https://www.googleapis.com/auth/youtube.upload`
4. Create a compact JSON token file with the authorized user's `client_id`, `client_secret`, `refresh_token`, and `token_uri` (`https://oauth2.googleapis.com/token`). Do not share this file.
5. In GitHub repository **Settings → Secrets and variables → Actions**, add a secret named `YOUTUBE_OAUTH_JSON` containing the entire JSON file contents.
6. Add a repository variable `YOUTUBE_UPLOAD_ENABLED` with value `true` only after private/unlisted testing.
7. Default upload privacy is `private`. To change it, edit `src/upload_youtube.py` only after testing.

YouTube may restrict public uploads for unverified API projects. Follow current Google requirements.

## Files
- `src/main.py`: creates video.
- `src/upload_youtube.py`: optional uploader.
- `.github/workflows/daily-shorts.yml`: daily schedule (09:00 IST approx).
- `requirements.txt`: Python dependencies.
