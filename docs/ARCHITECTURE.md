# DealMind Architecture

## System Overview

DealMind is a full-stack real estate underwriting platform with:
- **Mobile**: React Native + Expo (iOS/Android)
- **Web**: Next.js 14 (responsive web app)
- **Backend**: FastAPI + Python (REST API)
- **Database**: PostgreSQL (relational data)
- **Storage**: Supabase (files, auth)
- **AI**: OpenAI (extraction, chat, document generation)
- **Payments**: Stripe (subscription billing)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Clients                              │
├─────────────────────────────────────────────────────────────┤
│  React Native (Expo)  │  Next.js Web  │  Mobile Browser    │
└──────────┬────────────┴──────┬────────┴─────────────────────┘
           │                   │
           └─────────┬─────────┘
                     │
            ┌────────▼────────┐
            │   API Gateway   │
            │  CORS / Auth    │
            └────────┬────────┘
                     │
        ┌────────────▼────────────┐
        │    FastAPI Backend      │
        │   (Uvicorn Server)      │
        ├────────────────────────┤
        │  API Routes:           │
        │  - /api/auth           │
        │  - /api/deals          │
        │  - /api/underwriting   │
        │  - /api/chat           │
        │  - /api/reports        │
        └────────┬───────────────┘
                 │
    ┌────────────┼────────────┬─────────────┐
    │            │            │             │
┌───▼──┐  ┌─────▼────┐  ┌────▼─────┐  ┌───▼────────┐
│ Auth │  │ Business │  │ External │  │  Storage   │
│Logic │  │  Logic   │  │  APIs    │  │ & Files    │
└──────┘  └──────────┘  └──────────┘  └────────────┘
    │            │            │             │
    │            │    ┌────────┼─────────────┼──────────────┐
    │            │    │        │             │              │
    │       ┌────▼────▼─────┐  │        ┌────▼─────┐   ┌───▼────┐
    │       │ Underwriting  │  │        │ Supabase │   │ OpenAI │
    │       │ Calculations  │  │        │ Storage  │   │  API   │
    │       │ (Core Logic)  │  │        └──────────┘   └────────┘
    │       └────┬──────────┘  │
    │            │             │
    │       ┌────▼────┐   ┌────▼──────┐
    │       │  Rules  │   │ Google    │
    │       │ Engine  │   │ Maps API  │
    │       └─────────┘   └───────────┘
    │
    └────────────┬────────────────┐
                 │                │
            ┌────▼──────┐    ┌────▼──────┐
            │PostgreSQL │    │   Redis   │
            │ (Main DB) │    │ (Cache)   │
            └───────────┘    └───────────┘
```

## Layer Architecture

### 1. Frontend Layer

**React Native (Mobile)**
```
App.tsx
├── Screens
│   ├── HomeScreen (deal list)
│   ├── NewDealScreen (input methods)
│   ├── DealSummaryScreen (metrics)
│   ├── DealChatScreen (AI interaction)
│   └── AssumptionsScreen (edit parameters)
├── Components (reusable UI)
├── Services (API calls, Supabase)
└── Utils (helpers, storage)
```

**Next.js (Web)**
```
app/
├── layout.tsx (root)
├── page.tsx (home)
├── deals/ (deal pages)
├── components/ (React components)
└── lib/ (utilities, API clients)
```

### 2. API Layer (FastAPI)

**Router Structure:**
```
app/api/
├── auth.py (auth endpoints)
├── deals.py (CRUD operations)
├── underwriting.py (calculations)
├── chat.py (AI interaction)
└── reports.py (document generation)
```

**Key Features:**
- OpenAPI/Swagger documentation
- CORS middleware
- JWT authentication
- Request/response validation with Pydantic

### 3. Business Logic Layer

```
app/services/
├── auth_service.py (user management)
├── deal_service.py (deal operations)
├── underwriting_service.py (calculations)
├── extraction_service.py (data extraction)
├── chat_service.py (AI interaction)
└── report_service.py (document generation)
```

### 4. Data Access Layer

```
app/models/
├── user.py (SQLAlchemy)
├── deal.py
├── deal_input.py
├── underwriting_result.py
├── scenario.py
├── chat_thread.py
└── document.py
```

### 5. Database Layer

**PostgreSQL:**
- Relational tables for all data
- Row-level security (RLS) for multi-tenancy
- Indexes for performance
- Migrations with Alembic

**Redis Cache:**
- User session storage
- Rate limiting
- Calculation caching

## Data Flow

### 1. Deal Creation Flow
```
Client (URL/PDF/Manual)
    ↓
API: POST /deals
    ↓
DealService.create_deal()
    ↓
DataExtractionService.extract_from_source()
    ↓
OpenAI (extract structured data)
    ↓
ValidationService.validate_assumptions()
    ↓
Database: Save deal + inputs
    ↓
Response: Deal object + confidence scores
```

### 2. Underwriting Flow
```
Client: POST /underwrite
    ↓
UnderwritingService.calculate()
    ↓
Core Formulas (deterministic):
  - NOI = EGI - Operating Expenses
  - Cap Rate = NOI / Purchase Price
  - Cash Flow = NOI - Debt Service
  - DSCR = NOI / Annual Debt Service
  - CoC = Annual Cash Flow / Total Cash Invested
    ↓
RulesEngine.apply_country_rules()
    ↓
AIService.generate_verdict()
    ↓
Database: Save results
    ↓
Response: All metrics + grade + verdict
```

### 3. Chat Flow
```
Client: POST /chat with message
    ↓
ChatService.add_user_message()
    ↓
OpenAI (with function calling):
  - System prompt with deal context
  - Available functions for calculations
  - Current assumptions and scenarios
    ↓
OpenAI may call functions (backend calculations)
    ↓
Function execution (deterministic):
  - run_underwriting()
  - create_scenario()
  - get_projections()
    ↓
OpenAI generates response with results
    ↓
Database: Save assistant message
    ↓
Response: Assistant message + tool calls + results
```

## Key Components

### Underwriting Engine
```
app/services/underwriting_service.py
```
Core real estate calculations:
- Gross Scheduled Income (GSI)
- Effective Gross Income (EGI)
- Operating Expense calculations
- Net Operating Income (NOI)
- Debt Service calculations
- Cash Flow projections
- DSCR, CoC, Cap Rate, IRR
- 5/10-year projections

**Critical:** All math is deterministic Python code, NOT AI.

### Rules Engine
```
app/rules/
├── us/
│   ├── federal.py
│   ├── texas.py
│   ├── california.py
│   └── florida.py
└── [other countries]
```

Rules for:
- Property tax rates by county
- Insurance estimates by state
- Depreciation assumptions
- Closing cost percentages
- Loan amortization standards

### Extraction Service
```
app/services/extraction_service.py
```

Input processing:
- **URL extraction:** Fetch + parse listing pages
- **PDF extraction:** pdfplumber + PyMuPDF + OCR
- **Image extraction:** Tesseract OCR
- **LLM extraction:** OpenAI with JSON schema
- **Validation:** Compare against county records

### Chat Service
```
app/services/chat_service.py
```

Features:
- Message history (per deal)
- Function calling integration
- Context management
- Tool result formatting

### Report Generator
```
app/services/report_service.py
```

Generates:
- Deal summary PDF
- Broker inquiry email
- Investor memo
- Lender summary
- Offer letter

## External Integrations

### OpenAI
```
- GPT-4 for extraction and chat
- Text embeddings for semantic search (later)
- Function calling for tool integration
```

### Supabase
```
- Authentication (email, Google, Apple)
- File storage (PDFs, images)
- Realtime (optional for live updates)
- Row-level security (RLS policies)
```

### Google Maps/Places
```
- Geocoding (address → coordinates)
- Places search (nearby amenities)
- Distance matrix (drive time)
```

### Stripe
```
- Subscription management
- Payment processing
- Webhook handling
```

## Security Architecture

### Authentication
- JWT tokens (issued by Supabase)
- Token validation on every request
- Automatic token refresh

### Authorization
- Row-level security (RLS) at database level
- User can only access their own deals
- Subscription limits enforced in service layer

### Data Protection
- HTTPS only
- Password hashing (bcrypt)
- Encrypted file storage
- Rate limiting (Stripe-style)
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy)

### Audit Trail
- Created/updated timestamps
- User tracking on sensitive operations
- Webhook logs (Stripe, etc.)

## Performance Optimizations

### Database
- Indexing on user_id, created_at, deal_id
- Connection pooling (20 connections)
- Query optimization with SQLAlchemy

### Caching
- Redis for session storage
- User subscription data cached
- Calculation results cached per scenario

### Async Operations
- Celery for long-running tasks:
  - PDF processing
  - Image OCR
  - Email sending
  - OpenAI API calls

### Frontend
- Expo caching for assets
- Next.js static generation where possible
- Code splitting and lazy loading

## Deployment Architecture

### MVP Deployment
```
Frontend:
  - Vercel (Next.js automatic)
  - Expo for mobile builds

Backend:
  - Railway / Render / Fly.io
  - Docker container
  - PostgreSQL managed service

Storage:
  - Supabase managed database
  - Supabase object storage
```

### Production Scaling
```
Load Balancing:
  - CloudFlare
  - AWS Application Load Balancer

Compute:
  - AWS ECS / Kubernetes
  - Auto-scaling groups

Database:
  - RDS PostgreSQL (with Read Replicas)
  - Aurora for high-availability

Cache:
  - ElastiCache Redis

CDN:
  - CloudFront
  - Bunny CDN

Monitoring:
  - DataDog / New Relic
  - Sentry for error tracking
  - CloudWatch logs
```

## Error Handling

### API Layer
- Exception classes for each error type
- Standardized error response format
- HTTP status codes
- Error logging

### Service Layer
- Try/catch with proper cleanup
- Validation before operations
- Transaction rollback on failure

### Client Layer
- Toast notifications
- Error boundary (React)
- Offline detection
- Retry logic

## Testing Strategy

### Backend
```
pytest/
├── unit/ (services, models)
├── integration/ (API endpoints)
├── e2e/ (full workflows)
└── conftest.py
```

### Frontend
```
jest/
├── components/ (UI tests)
├── services/ (API mock tests)
└── screens/ (navigation)
```

## Monitoring & Logging

### Backend Logging
```
- Request/response logging
- Exception logging with stack traces
- Performance metrics
- OpenAI API call logging
- Database query logging
```

### Metrics
```
- API latency
- Error rates
- Database performance
- OpenAI API costs
- File upload bandwidth
```
