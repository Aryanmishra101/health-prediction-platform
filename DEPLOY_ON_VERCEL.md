# Deploying to Vercel

This guide explains how to deploy your Django Health Prediction Platform to Vercel.

## Prerequisites

1.  **Vercel Account**: Sign up at [vercel.com](https://vercel.com).
2.  **Vercel CLI** (Optional but recommended): Install via `npm i -g vercel`.
3.  **Git Repository**: Your project should be pushed to a Git repository (GitHub/GitLab/Bitbucket).

## Configuration Files Created

I have already created the necessary configuration files for you:

*   `vercel.json`: Vercel configuration file.
*   `vercel_app.py`: Entry point for the application.
*   `build_files.sh`: Script to install dependencies and collect static files.

## Deployment Steps

### Option 1: Using Vercel Dashboard (Recommended)

1.  Push your code to your Git repository.
2.  Go to the [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New..."** -> **"Project"**.
3.  Import your Git repository.
4.  In the **Configure Project** step:
    *   **Framework Preset**: Select **Other**.
    *   **Build Command**: Enter `sh build_files.sh`.
    *   **Output Directory**: Leave it empty (default).
    *   **Install Command**: Leave it empty (handled by build script).
5.  **Environment Variables**: Add the following environment variables (same as your `.env` or Render/Railway config):
    *   `SECRET_KEY`: Your Django secret key.
    *   `DEBUG`: `False`
    *   `DATABASE_URL`: Your database connection string (e.g., from Supabase, Railway, or Neon). **Note**: Vercel does not provide a database, you must use an external one.
    *   `ALLOWED_HOSTS`: `*` (or your vercel domain).
6.  Click **Deploy**.

### Option 2: Using Vercel CLI

1.  Open your terminal in the project root.
2.  Run `vercel login` if you haven't already.
3.  Run `vercel`.
4.  Follow the prompts:
    *   Set up and deploy? **Yes**
    *   Which scope? (Select your account)
    *   Link to existing project? **No**
    *   Project name? (Press Enter)
    *   In which directory is your code located? **./**
    *   Want to modify these settings? **Yes**
    *   **Build Command**: `sh build_files.sh`
    *   **Output Directory**: (Press Enter to skip)
    *   **Development Command**: (Press Enter to skip)
    *   **Install Command**: (Press Enter to skip)
5.  Wait for deployment.

## Important Notes

*   **Database**: Vercel is serverless and ephemeral. You **must** use an external database (like Supabase, Neon, or Railway Postgres). SQLite will **not** work effectively because the data will be lost on every deployment/restart. Ensure `DATABASE_URL` is set.
*   **Size Limit**: Vercel Serverless Functions have a size limit (usually 250MB uncompressed). Your project uses `pandas` and `scikit-learn`, which are heavy. If deployment fails due to size, consider removing unused dependencies or using a lighter alternative.
*   **Static Files**: We are using `whitenoise` to serve static files. The `build_files.sh` script handles `collectstatic`.

## Troubleshooting

*   **"Module not found"**: Ensure all dependencies are in `requirements.txt`.
*   **"Size exceeded"**: Check the build logs. You might need to exclude large files or dependencies.
