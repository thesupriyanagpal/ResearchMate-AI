---
description: Step-by-step guide to deploy SN-Insight to Vercel
---

# Deploying SN-Insight to Vercel

This comprehensive guide walks you through deploying the SN-Insight (ResearchMate AI) application to Vercel. The project consists of a Next.js frontend and a FastAPI backend.

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ A [Vercel account](https://vercel.com/signup) (free tier works)
- ✅ Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
- ✅ Google Gemini API key (for the backend)
- ✅ [Vercel CLI](https://vercel.com/docs/cli) installed (optional, but recommended)

### Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

## ⚠️ Important Considerations

### Persistence Limitations

Vercel Serverless Functions are **ephemeral**, which means:

- 🚫 **Uploaded PDFs will NOT persist** between requests
- 🚫 **ChromaDB vector index will reset** when functions restart
- 🚫 **No permanent file storage** on the serverless platform

### Recommended Solutions for Production

For a production-ready deployment with persistence:

1. **File Storage**: Use AWS S3, Google Cloud Storage, or Cloudflare R2
2. **Vector Database**: Use Pinecone, Weaviate, or hosted Chroma instance
3. **Alternative Backend Hosting**: Deploy backend to Render, Railway, or Fly.io (see Option 3)

---

## 🚀 Deployment Options

Choose the option that best fits your needs:

- **Option 1**: Both frontend and backend on Vercel (Quick, but limited persistence)
- **Option 2**: Separate Vercel projects for frontend and backend (Recommended for Vercel)
- **Option 3**: Frontend on Vercel + Backend on Render (Best for persistence)

---

## Option 1: Single Vercel Project (Monorepo)

Deploy both frontend and backend as a single Vercel project.

### Step 1: Prepare Your Repository

Ensure your project structure looks like this:

```
SN-Insight/
├── frontend/          # Next.js app
├── backend/           # FastAPI app
├── .gitignore
└── README.md
```

### Step 2: Create Root vercel.json

Create a `vercel.json` file in the **root directory**:

```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/.next",
  "framework": "nextjs",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/backend/app/main.py"
    }
  ]
}
```

### Step 3: Deploy via Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import your Git repository
4. Configure the project:
   - **Framework Preset**: Next.js
   - **Root Directory**: Leave as root (`.`)
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/.next`

### Step 4: Add Environment Variables

Add the following environment variables:

**For Backend:**
- `GOOGLE_API_KEY`: Your Gemini API key

**For Frontend:**
- `NEXT_PUBLIC_API_URL`: `/api/v1` (relative path)

### Step 5: Deploy

Click **"Deploy"** and wait for the build to complete.

### Limitations of This Approach

- Backend routing can be complex
- Harder to debug issues
- Not ideal for separate scaling

---

## Option 2: Separate Vercel Projects (Recommended)

Deploy frontend and backend as **two separate Vercel projects** from the same repository.

### Part A: Deploy the Frontend

#### Step 1: Create New Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import your repository

#### Step 2: Configure Frontend Project

- **Project Name**: `sn-insight-frontend` (or your choice)
- **Framework Preset**: Next.js
- **Root Directory**: Click **"Edit"** → Select `frontend`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

#### Step 3: Add Frontend Environment Variables

For now, leave `NEXT_PUBLIC_API_URL` empty. We'll update it after deploying the backend.

Alternatively, set a placeholder:
- **Key**: `NEXT_PUBLIC_API_URL`
- **Value**: `https://placeholder.com/api/v1` (temporary)

#### Step 4: Deploy Frontend

Click **"Deploy"** and wait for completion.

Your frontend will be available at: `https://sn-insight-frontend.vercel.app`

---

### Part B: Deploy the Backend

#### Step 1: Create New Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import the **same repository**

#### Step 2: Configure Backend Project

- **Project Name**: `sn-insight-backend` (or your choice)
- **Framework Preset**: Other (or Python)
- **Root Directory**: Click **"Edit"** → Select `backend`
- **Build Command**: Leave empty (Vercel auto-detects `requirements.txt`)
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt` (auto-detected)

#### Step 3: Verify vercel.json in Backend

Ensure `/backend/vercel.json` exists with:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/app/main.py" }
  ]
}
```

✅ This file already exists in your project.

#### Step 4: Add Backend Environment Variables

Add the following environment variable:

- **Key**: `GOOGLE_API_KEY`
- **Value**: Your Google Gemini API key

#### Step 5: Deploy Backend

Click **"Deploy"** and wait for completion.

Your backend will be available at: `https://sn-insight-backend.vercel.app`

---

### Part C: Connect Frontend to Backend

#### Step 1: Get Backend URL

Copy your deployed backend URL (e.g., `https://sn-insight-backend.vercel.app`)

#### Step 2: Update Frontend Environment Variable

1. Go to your **Frontend Project** in Vercel Dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Update or add:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://sn-insight-backend.vercel.app/api/v1`
4. Click **"Save"**

#### Step 3: Redeploy Frontend

1. Go to **Deployments** tab
2. Click the **three dots** (⋯) on the latest deployment
3. Select **"Redeploy"**
4. Check **"Use existing Build Cache"** (optional, for faster builds)
5. Click **"Redeploy"**

#### Step 4: Test Your Application

Visit your frontend URL and test:
- Upload a PDF
- Generate summaries
- Extract insights
- Verify API connectivity

---

## Option 3: Frontend on Vercel + Backend on Render

For **persistent storage** and better backend performance, deploy the backend to Render.

### Part A: Deploy Backend to Render

#### Step 1: Create Render Account

Sign up at [Render.com](https://render.com)

#### Step 2: Create New Web Service

1. Click **"New"** → **"Web Service"**
2. Connect your Git repository
3. Configure the service:
   - **Name**: `sn-insight-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Step 3: Add Environment Variables

Add in the **Environment** section:
- **Key**: `GOOGLE_API_KEY`
- **Value**: Your Google Gemini API key

#### Step 4: Choose Plan

- **Free**: Spins down after 15 minutes of inactivity (slower cold starts)
- **Starter ($7/month)**: Always on, better performance

#### Step 5: Deploy

Click **"Create Web Service"** and wait for deployment.

Your backend will be available at: `https://sn-insight-backend.onrender.com`

---

### Part B: Deploy Frontend to Vercel

Follow **Option 2 - Part A** above, but set:

- **Key**: `NEXT_PUBLIC_API_URL`
- **Value**: `https://sn-insight-backend.onrender.com/api/v1`

---

## 🔧 Using Vercel CLI

For faster deployments and better control, use the Vercel CLI.

### Deploy Frontend

```bash
cd /Users/niteshnagpal/Developer/Personal/projects/SN-Insight/frontend

# Login to Vercel (first time only)
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Deploy Backend

```bash
cd /Users/niteshnagpal/Developer/Personal/projects/SN-Insight/backend

# Login to Vercel (first time only)
vercel login

# Set environment variable
vercel env add GOOGLE_API_KEY

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

---

## 🔍 Post-Deployment Checklist

After deployment, verify the following:

### ✅ Frontend Checks

- [ ] Frontend loads without errors
- [ ] UI is responsive and styled correctly
- [ ] All pages are accessible
- [ ] Environment variables are set correctly

### ✅ Backend Checks

- [ ] API endpoints are accessible
- [ ] Health check endpoint works: `GET /api/v1/health`
- [ ] CORS is configured correctly
- [ ] Environment variables are loaded

### ✅ Integration Checks

- [ ] Frontend can communicate with backend
- [ ] File upload works (note: files won't persist on Vercel)
- [ ] PDF processing works
- [ ] Insights generation works
- [ ] Error handling works properly

### ✅ Performance Checks

- [ ] Page load times are acceptable
- [ ] API response times are reasonable
- [ ] No console errors in browser
- [ ] No server errors in Vercel logs

---

## 🐛 Troubleshooting

### Frontend Issues

#### Build Fails

**Error**: `Module not found` or `Cannot find module`

**Solution**:
```bash
# Ensure all dependencies are in package.json
cd frontend
npm install
npm run build  # Test locally first
```

#### Environment Variables Not Working

**Error**: `NEXT_PUBLIC_API_URL is undefined`

**Solution**:
- Ensure variable starts with `NEXT_PUBLIC_`
- Redeploy after adding/changing environment variables
- Check browser console for the actual value

#### CORS Errors

**Error**: `Access-Control-Allow-Origin` error

**Solution**: Ensure backend CORS is configured to allow your frontend domain.

---

### Backend Issues

#### Import Errors

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Ensure `vercel.json` points to correct path:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/app/main.py" }
  ]
}
```

#### Function Timeout

**Error**: `Function execution timed out`

**Solution**:
- Vercel has a 10-second timeout on Hobby plan
- Optimize your code or upgrade to Pro plan (60 seconds)
- Consider deploying backend to Render for longer timeouts

#### Environment Variables Not Loading

**Error**: API key is `None` or undefined

**Solution**:
1. Go to Project Settings → Environment Variables
2. Ensure `GOOGLE_API_KEY` is set
3. Redeploy the project

#### ChromaDB Errors

**Error**: `ChromaDB initialization failed`

**Solution**:
- ChromaDB may not work well on Vercel serverless
- Consider using Pinecone or hosted Chroma for production
- Or deploy backend to Render/Railway

---

### General Issues

#### Deployment Stuck

**Solution**:
1. Check Vercel status page: https://www.vercel-status.com
2. Cancel and retry deployment
3. Check build logs for errors

#### Domain Not Working

**Solution**:
1. Wait a few minutes for DNS propagation
2. Check domain settings in Vercel
3. Ensure domain is properly configured

---

## 🔄 Updating Your Deployment

### Automatic Deployments

Vercel automatically deploys when you push to your Git repository:

```bash
# Make changes
git add .
git commit -m "Update feature X"
git push origin main

# Vercel will automatically deploy
```

### Manual Deployments

Using Vercel CLI:

```bash
# Deploy specific directory
cd frontend  # or backend
vercel --prod
```

Using Vercel Dashboard:
1. Go to **Deployments** tab
2. Click **"Redeploy"** on any previous deployment

---

## 🎯 Best Practices

### 1. Use Environment Variables

Never hardcode API keys or secrets:

```typescript
// ✅ Good
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// ❌ Bad
const apiUrl = "https://my-backend.vercel.app";
```

### 2. Enable Preview Deployments

- Every pull request gets a preview URL
- Test changes before merging to production
- Share preview links with team members

### 3. Monitor Your Application

- Check Vercel Analytics for performance metrics
- Review deployment logs regularly
- Set up error tracking (Sentry, LogRocket)

### 4. Optimize Build Times

```json
// package.json
{
  "scripts": {
    "build": "next build",
    "postbuild": "next-sitemap"  // Optional optimizations
  }
}
```

### 5. Use Custom Domains

1. Go to Project Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed
4. Enable HTTPS (automatic)

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Vercel Logs**: Project → Deployments → Click deployment → View logs
2. **Vercel Community**: https://github.com/vercel/vercel/discussions
3. **Vercel Support**: https://vercel.com/support
4. **Stack Overflow**: Tag questions with `vercel` and `nextjs`

---

## 🎉 Success!

Your SN-Insight application should now be live on Vercel! 

**Frontend**: `https://your-frontend.vercel.app`  
**Backend**: `https://your-backend.vercel.app` or Render

Share your deployed application and start analyzing research papers! 🚀
