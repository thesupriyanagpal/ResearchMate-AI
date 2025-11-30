# Deployment Guide for ResearchMate AI

This guide explains how to deploy the ResearchMate AI application (Frontend + Backend) to **Vercel**.

## ⚠️ Important Limitations

**Persistence**: Vercel Serverless Functions are ephemeral.
- **Files**: Uploaded PDFs will **NOT** persist between requests.
- **Database**: The local ChromaDB vector index will **reset** when the function restarts.

**For Production**:
- Use a cloud storage provider (AWS S3, Google Cloud Storage) for files.
- Use a cloud vector database (Pinecone, Weaviate, or a hosted Chroma instance).
- Or deploy the backend to a stateful platform like **Render** or **Railway**.

---

## Option 1: Deploying Everything on Vercel (Quick Start)

This approach deploys both frontend and backend as a single Vercel project.

### 1. Configuration

Create a `vercel.json` file in the root directory:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/:path*"
    }
  ]
}
```

**Note**: Vercel automatically detects the `api` directory for Python functions. However, our backend is in `backend/`.
To make this work seamlessly on Vercel without restructuring, it's often easier to deploy **two separate projects** from the same repository.

### 2. Recommended Approach: Separate Projects

Since we have a `frontend` and `backend` folder, the best way is to deploy them separately on Vercel.

#### Step A: Deploy Frontend
1.  Push your code to GitHub.
2.  Go to Vercel Dashboard -> **Add New Project**.
3.  Import your repository.
4.  **Framework Preset**: Next.js
5.  **Root Directory**: Edit and select `frontend`.
6.  **Environment Variables**:
    - `NEXT_PUBLIC_API_URL`: The URL of your deployed backend (e.g., `https://researchmate-ai-backend.vercel.app/api/v1`).
    - *For now, you can leave this empty and update it after deploying the backend.*
7.  Click **Deploy**.

#### Step B: Deploy Backend
1.  Go to Vercel Dashboard -> **Add New Project**.
2.  Import the **same repository**.
3.  **Framework Preset**: Other (or Python).
4.  **Root Directory**: Edit and select `backend`.
5.  **Environment Variables**:
    - `GOOGLE_API_KEY`: Your Gemini API Key.
6.  **Build Command**: `pip install -r requirements.txt` (Vercel usually detects this).
7.  Click **Deploy**.

### 3. Connect Them
1.  Get the URL of your deployed Backend (e.g., `https://researchmate-ai-backend.vercel.app`).
2.  Go to your **Frontend Project Settings** -> **Environment Variables**.
3.  Add `NEXT_PUBLIC_API_URL` = `https://researchmate-ai-backend.vercel.app/api/v1`.
4.  **Redeploy** the Frontend (Deployment -> Redeploy).

---

## Option 2: Render (Backend) + Vercel (Frontend) [Recommended for Persistence]

If you want your uploaded files and vector index to persist (so you don't have to re-upload every time), deploy the backend to **Render**.

1.  **Backend on Render**:
    - Create a new **Web Service**.
    - Connect GitHub repo.
    - Root Directory: `backend`.
    - Build Command: `pip install -r requirements.txt`.
    - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
    - Add `GOOGLE_API_KEY` environment variable.
    - Select **Free** plan (note: spins down after inactivity) or **Starter**.

2.  **Frontend on Vercel**:
    - Follow "Step A" above.
    - Set `NEXT_PUBLIC_API_URL` to your Render URL (e.g., `https://researchmate-ai.onrender.com/api/v1`).
