# SlipSmart AI – System Architecture

## Purpose

This document describes the technical architecture of SlipSmart AI. The goal is to design a clean, scalable, and maintainable system that can start as a simple MVP and evolve into a larger sports intelligence platform.

---

# Architecture Style

SlipSmart AI will use a **modular monolith** architecture for the MVP.

This means the backend will be one FastAPI application, but the code will be separated into clear modules:

* Users
* Matches
* Predictions
* Optimizer
* Slips
* AI Assistant
* Database

This approach keeps the system simple to build and deploy while still allowing individual modules to be extracted into microservices later if needed.

---

# High-Level Architecture

```text
User
  ↓
Next.js Frontend
  ↓
FastAPI Backend
  ↓
PostgreSQL Database
```

Additional services:

```text
Sports Data API
  ↓
Match & Prediction Services

OpenAI / Gemini API
  ↓
AI Assistant Service

ML Model
  ↓
Prediction Service
```

---

# System Components

## Frontend

Technology:

* Next.js
* React
* TypeScript
* Tailwind CSS

Responsibilities:

* Display landing page
* Display upcoming matches
* Display prediction cards
* Allow users to generate slips
* Show generated slips
* Show AI explanations
* Later: user dashboard and saved slips

---

## Backend

Technology:

* FastAPI
* Python
* Pydantic
* SQLAlchemy
* Alembic

Responsibilities:

* Serve REST APIs
* Handle business logic
* Generate diversified slips
* Manage database access
* Connect to sports data APIs
* Connect to AI/LLM APIs
* Later: authentication and background jobs

---

## Database

Technology:

* PostgreSQL

Responsibilities:

* Store users
* Store teams and matches
* Store predictions
* Store generated slips
* Store slip items
* Store AI explanations
* Store model outputs and performance history later

---

## Prediction Service

Responsibilities:

* Receive match data
* Generate prediction probabilities
* Assign confidence scores
* Assign risk levels
* Store prediction results

MVP version:

* Uses sample prediction data.

Future version:

* Uses trained machine learning models such as XGBoost or LightGBM.

---

## Optimizer Service

Responsibilities:

* Generate multiple betting slip combinations
* Reduce overlap between slips
* Avoid duplicate matches inside the same slip
* Apply user strategy: Safe, Balanced, Aggressive
* Calculate total odds, potential return, average probability, and risk score

This is the core differentiating feature of SlipSmart AI.

---

## AI Assistant Service

Responsibilities:

* Explain generated slips
* Explain prediction reasoning
* Answer user questions
* Convert natural language requests into optimizer settings later

MVP version:

* Uses mock AI explanations.

Future version:

* Uses OpenAI or Gemini API.

Important:

The LLM will not be used as the main prediction engine. Prediction probabilities should come from structured data and ML/statistical models.

---

# Backend Module Structure

```text
backend/
  app/
    main.py
    core/
      config.py
      security.py
      logging.py

    db/
      session.py
      base.py

    modules/
      users/
        router.py
        service.py
        repository.py
        schemas.py
        models.py

      matches/
        router.py
        service.py
        repository.py
        schemas.py
        models.py

      predictions/
        router.py
        service.py
        repository.py
        schemas.py
        models.py

      optimizer/
        service.py
        scoring.py
        overlap.py
        schemas.py

      slips/
        router.py
        service.py
        repository.py
        schemas.py
        models.py

      ai_assistant/
        router.py
        service.py
        prompts.py
        schemas.py
```

---

# Data Flow – Generate Slips

```text
1. User opens Slip Generator page
2. Frontend sends budget, strategy, and selected matches to backend
3. Backend retrieves available predictions
4. Optimizer generates diversified slips
5. Backend calculates stake, odds, probability, and risk score
6. AI Assistant generates explanation
7. Backend returns slips and explanation
8. Frontend displays results
```

---

# MVP Data Flow

```text
Next.js Frontend
      ↓
FastAPI API
      ↓
Sample Matches + Sample Predictions
      ↓
Optimizer
      ↓
Generated Slips
      ↓
Mock AI Explanation
```

---

# Future Data Flow

```text
Sports Data API
      ↓
Scheduled Data Ingestion
      ↓
PostgreSQL
      ↓
Feature Engineering
      ↓
ML Prediction Model
      ↓
Prediction Database
      ↓
Optimizer
      ↓
AI Explanation
      ↓
Frontend
```

---

# Deployment Architecture – MVP

Initial deployment can use low-cost or free platforms:

```text
Frontend: Vercel
Backend: Render / Railway
Database: Neon / Supabase PostgreSQL
```

---

# Deployment Architecture – AWS Future Version

```text
User
  ↓
CloudFront
  ↓
S3 / Next.js Hosting
  ↓
FastAPI Backend on Elastic Beanstalk or ECS
  ↓
RDS PostgreSQL
```

Additional AWS services:

* S3 for datasets and model files
* CloudWatch for logs and monitoring
* EventBridge for scheduled data ingestion
* IAM roles for secure access
* Secrets Manager for API keys

---

# Scalability Plan

## Stage 1 – MVP

* Modular monolith
* Single backend service
* PostgreSQL
* Sample or limited sports data

## Stage 2 – Growth

* Real sports API
* User accounts
* Saved slips
* AI explanations
* Caching with Redis

## Stage 3 – Advanced

* Background workers
* Scheduled prediction jobs
* ML model retraining
* Performance tracking
* AWS deployment

## Stage 4 – Scale

Potentially split modules into separate services:

* Match Data Service
* Prediction Service
* Optimizer Service
* AI Assistant Service
* User Service

This will only be considered if traffic, team size, or scaling needs justify it.

---

# Key Technical Decisions

## Modular Monolith First

Reason:

* Faster to build
* Easier to debug
* Lower deployment complexity
* Suitable for solo development
* Can be split into microservices later

## PostgreSQL

Reason:

* Data is highly relational
* Supports complex queries
* Reliable transactions
* Good fit for users, matches, predictions, and slips

## FastAPI

Reason:

* Python-friendly
* Excellent for ML integration
* Fast API development
* Automatic OpenAPI documentation

## Next.js

Reason:

* Built on React
* Good SEO
* Better routing
* Suitable for public prediction pages

---

# Architecture Principles

* Keep business logic out of routers.
* Keep database logic inside repositories.
* Keep AI logic separate from prediction logic.
* Use environment variables for secrets.
* Avoid hardcoding provider-specific configuration.
* Design for portability before AWS migration.
* Start simple, but keep module boundaries clean.
