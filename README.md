# DealMind - AI Real Estate Underwriting Platform

> Paste a deal. Get the numbers. Talk to the deal. Decide faster.

A mobile-first AI real estate underwriting platform that automates property analysis, generates instant financial insights, and enables conversational deal analysis through an integrated AI chat interface.

## 📋 Quick Links

- [Full Specification](./SPECIFICATION.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Development Setup](./docs/SETUP.md)
- [API Documentation](./docs/API.md)

## 🏗️ Project Structure

```
DealMind/
├── frontend/           # React Native Expo app (iOS/Android)
├── web/               # Next.js web app
├── backend/           # FastAPI Python backend
├── docs/              # Documentation
├── SPECIFICATION.md   # Full technical requirements
└── README.md         # This file
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL 14+
- Docker & Docker Compose (optional)

### Frontend (React Native)

```bash
cd frontend
npm install
npx expo start
```

### Web (Next.js)

```bash
cd web
npm install
npm run dev
```

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## 📱 Main Features (MVP)

### User Input
- ✅ Paste property URL (Zillow, Redfin, LoopNet)
- ✅ Upload PDF (offering memos, broker packages)
- ✅ Upload images (flyers, rent rolls)
- ✅ Manual data entry

### Underwriting
- ✅ Automatic property data extraction
- ✅ Instant real estate calculations:
  - NOI, Cap Rate, Cash Flow
  - DSCR, Cash-on-Cash Return
  - Break-even Occupancy
  - 5/10-year projections

### AI Chat
- ✅ Deal-specific chat thread
- ✅ Scenario questions:
  - "What if I offer $850,000?"
  - "What if rent increases 5%?"
  - "What if CapEx is $50,000?"
- ✅ Document generation:
  - Broker emails
  - Investor memos
  - Lender summaries

### Documents
- ✅ Deal summary PDF
- ✅ Professional reports
- ✅ Email drafts

## 🔧 Technology Stack

| Layer | Technology |
|-------|-----------|
| Mobile | React Native + Expo |
| Web | Next.js 14 + TypeScript |
| Backend | FastAPI + Python |
| Database | PostgreSQL |
| Auth | Supabase Auth |
| Storage | Supabase Storage |
| AI | OpenAI API |
| Billing | Stripe |

## 📊 Database Schema

Key tables:
- `users` - User accounts and subscriptions
- `deals` - Real estate deals
- `deal_inputs` - Raw input data and extracted fields
- `underwriting_results` - Calculated metrics
- `scenarios` - Deal scenarios and what-ifs
- `chat_threads` - Chat conversations per deal
- `documents` - Generated reports and documents

See [Database Schema](./docs/DATABASE.md) for details.

## 🔐 Security

- Supabase Auth with email/password, Google, Apple login
- Row-level security (RLS) - users access only their deals
- HTTPS-only API
- Rate limiting and input validation
- Encrypted file storage

## 💰 Subscription Plans

| Plan | Deals/Month | Features |
|------|------------|----------|
| Free | 3 | Basic underwriting, limited chat |
| Pro | 50 | Full underwriting, deal chat, scenarios |
| Elite | Unlimited | All features + reports + neighborhood tools |
| Enterprise | Unlimited | Team accounts, broker dashboard, API access |

## 📚 API Endpoints

### Authentication
```
POST   /auth/signup
POST   /auth/login
POST   /auth/logout
GET    /auth/me
```

### Deals
```
POST   /deals
GET    /deals
GET    /deals/{deal_id}
PATCH  /deals/{deal_id}
DELETE /deals/{deal_id}
```

### Underwriting
```
POST   /deals/{deal_id}/underwrite
GET    /deals/{deal_id}/results
POST   /deals/{deal_id}/scenario
GET    /deals/{deal_id}/scenarios
```

### Chat
```
POST   /deals/{deal_id}/chat
GET    /deals/{deal_id}/chat
```

### Documents
```
POST   /deals/{deal_id}/generate-report
POST   /deals/{deal_id}/generate-broker-email
POST   /deals/{deal_id}/generate-investor-memo
```

See [Full API Documentation](./docs/API.md) for complete endpoints.

## 🎯 Roadmap

### Phase 1: MVP (Current)
- ✅ U.S. only
- ✅ Residential investment
- ✅ Mobile + Web
- ✅ AI underwriting & chat
- ✅ Basic documents

### Phase 2: Data Expansion
- Rent estimates API integration
- Neighborhood & crime reports
- School quality data
- Market trend analysis

### Phase 3: Professional Tools
- Broker packages
- Team collaboration
- Portfolio tracking
- Deal comparison

### Phase 4: Advanced Assets
- Commercial multifamily
- Fix & flip
- BRRRR investing
- Development projects

### Phase 5: Global Expansion
- Germany, UK, Canada support
- Multi-currency
- Localized tax rules
- Multilingual interface

## 🤝 Contributing

See [Contributing Guidelines](./docs/CONTRIBUTING.md)

## 📄 License

[TBD]

## 📞 Support

Email: support@dealmind.io
