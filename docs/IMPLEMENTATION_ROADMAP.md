# Implementation Roadmap

## Phase 1: Foundation (Week 1-2)

### Backend Setup
- [x] FastAPI project structure
- [x] Database schema design
- [x] API route stubs
- [ ] PostgreSQL database creation
- [ ] Alembic migrations setup
- [ ] Supabase Auth integration
- [ ] User model + JWT

### Frontend Setup
- [x] React Native project structure
- [x] Screen component stubs
- [ ] Install and configure dependencies
- [ ] Create API client service
- [ ] Setup auth service
- [ ] Create navigation structure

### Web Setup
- [x] Next.js project structure
- [x] Basic pages
- [ ] Install and configure dependencies
- [ ] Setup Tailwind CSS
- [ ] Create API client service
- [ ] Setup auth service

### Infrastructure
- [x] Docker setup
- [x] docker-compose.yml
- [ ] Environment configuration
- [ ] Basic CI/CD pipeline (GitHub Actions)

---

## Phase 2: Authentication & User Management (Week 2-3)

### Backend
- [ ] Implement signup endpoint
- [ ] Implement login endpoint
- [ ] Implement logout endpoint
- [ ] Implement refresh token logic
- [ ] Password hashing (bcrypt)
- [ ] User model enhancements
- [ ] Database user table with RLS policies

### Frontend
- [ ] Auth service implementation
- [ ] Login screen UI
- [ ] Signup screen UI
- [ ] Password reset flow
- [ ] Token storage (Supabase)
- [ ] Auto-login on app start

### Web
- [ ] Auth pages
- [ ] Login form
- [ ] Signup form
- [ ] Protected routes
- [ ] Session management

---

## Phase 3: Deal Management (Week 3-4)

### Backend
- [ ] Implement deal CRUD endpoints
- [ ] Deal model + database
- [ ] Deal inputs model + storage
- [ ] Implement /deals/from-url endpoint (basic scraping)
- [ ] Implement /deals/from-pdf endpoint (pdfplumber)
- [ ] Implement /deals/from-image endpoint (Tesseract OCR)
- [ ] Data extraction with OpenAI

### Frontend
- [ ] Deals list screen
- [ ] New deal screen with input options
- [ ] Deal detail view
- [ ] Deal edit screen
- [ ] File upload for PDF/images
- [ ] Connect to backend API

### Web
- [ ] Deals list page
- [ ] Deal detail page
- [ ] New deal form
- [ ] File upload interface
- [ ] Deal cards/grid

---

## Phase 4: Core Underwriting Engine (Week 4-5)

### Backend - Calculations
- [ ] Implement gross scheduled income
- [ ] Implement effective gross income
- [ ] Implement operating expense calculations
- [ ] Implement NOI calculation
- [ ] Implement debt service calculations
- [ ] Implement cap rate
- [ ] Implement cash flow (monthly/annual)
- [ ] Implement cash-on-cash return
- [ ] Implement DSCR
- [ ] Implement break-even occupancy
- [ ] Implement LTV and debt yield

### Backend - Rules Engine
- [ ] Create US federal rules
- [ ] Create state-specific rules (TX, CA, FL, NY)
- [ ] Property tax estimates by county
- [ ] Insurance estimates by state
- [ ] Implement rules loader

### Backend - Projections
- [ ] 1-year projection
- [ ] 5-year projection
- [ ] 10-year projection
- [ ] Multi-year amortization
- [ ] Property appreciation modeling

### Backend - Validation & Warnings
- [ ] Validate input assumptions
- [ ] Generate risk flags
- [ ] Create deal grade (A+ to F)
- [ ] Generate AI verdict (one-sentence summary)

### API
- [ ] POST /underwriting/{deal_id}/underwrite
- [ ] GET /underwriting/{deal_id}/results
- [ ] POST /underwriting/{deal_id}/projection
- [ ] POST /underwriting/{deal_id}/scenario

---

## Phase 5: Scenarios & What-If Analysis (Week 5-6)

### Backend
- [ ] Scenario model + database
- [ ] Implement scenario creation
- [ ] Implement scenario calculations
- [ ] Scenario comparison logic
- [ ] Store scenario results

### Frontend
- [ ] Assumptions edit screen
- [ ] Scenario creation UI
- [ ] Scenario comparison view
- [ ] Side-by-side metric comparison

### Web
- [ ] Assumptions editor
- [ ] Scenario manager
- [ ] Comparison dashboard

---

## Phase 6: AI Chat Integration (Week 6-7)

### Backend
- [ ] Chat thread model + database
- [ ] Chat message model + storage
- [ ] OpenAI integration with function calling
- [ ] Define available functions for AI:
  - run_underwriting()
  - create_scenario()
  - get_projections()
  - analyze_risks()
- [ ] Function execution handler
- [ ] System prompt design

### Frontend
- [ ] Deal chat screen implementation
- [ ] Chat UI (message bubbles)
- [ ] Message input
- [ ] Chat service (API integration)
- [ ] Display calculation results from AI

### Web
- [ ] Deal chat page
- [ ] Chat interface
- [ ] Message history
- [ ] Loading states

---

## Phase 7: Document Generation (Week 7-8)

### Backend
- [ ] Document model + database
- [ ] PDF generation service
- [ ] Broker email template
- [ ] Investor memo template
- [ ] Lender summary template
- [ ] Offer letter template
- [ ] Implement all report endpoints

### Frontend
- [ ] Documents list screen
- [ ] Document generation triggers
- [ ] Document preview
- [ ] PDF sharing/export

### Web
- [ ] Documents page
- [ ] Report preview
- [ ] Email draft preview
- [ ] PDF download

---

## Phase 8: Polish & Optimization (Week 8-9)

### Backend
- [ ] Error handling improvements
- [ ] Input validation
- [ ] Rate limiting
- [ ] Caching layer (Redis)
- [ ] Performance optimization
- [ ] API documentation
- [ ] Logging and monitoring

### Frontend
- [ ] UI polish
- [ ] Error states
- [ ] Loading states
- [ ] Empty states
- [ ] Form validation
- [ ] Offline support
- [ ] Performance optimization

### Web
- [ ] Responsive design
- [ ] Dark mode support
- [ ] Accessibility audit
- [ ] Performance optimization

### Testing
- [ ] Backend unit tests
- [ ] Backend integration tests
- [ ] Frontend component tests
- [ ] End-to-end tests

---

## Phase 9: Deployment & Launch (Week 9-10)

### Backend
- [ ] Production database setup (RDS/Supabase)
- [ ] Environment variables for production
- [ ] Docker image optimization
- [ ] Deployment to Render/Railway/Fly.io
- [ ] Health checks and monitoring
- [ ] Error tracking (Sentry)

### Frontend
- [ ] EAS build configuration
- [ ] iOS build
- [ ] Android build
- [ ] TestFlight/Beta distribution

### Web
- [ ] Build optimization
- [ ] Deploy to Vercel
- [ ] Domain configuration
- [ ] HTTPS/SSL

### Launch
- [ ] Beta testing
- [ ] Feedback collection
- [ ] Bug fixes
- [ ] Public launch

---

## Phase 10: MVP Complete Features (Week 10+)

### Implemented
✅ User authentication
✅ Deal creation (URL, PDF, image, manual)
✅ Data extraction
✅ Real estate underwriting calculations
✅ Deal scoring and verdict
✅ Scenario analysis
✅ AI chat with deal
✅ Document generation
✅ Multi-platform (mobile + web)

### Not in MVP (Future)
- Neighborhood/crime/school reports
- Global country support
- Team collaboration
- Enterprise features
- Advanced asset classes (commercial, fix & flip, etc.)
- Broker dashboard
- Portfolio tracking

---

## Development Priorities

### Must Have (MVP)
1. ✅ User authentication
2. ✅ Deal CRUD
3. ✅ Data extraction
4. ✅ Underwriting calculations
5. ✅ AI chat
6. ✅ Document generation
7. ✅ Scenarios

### Should Have (MVP+)
- Deal comparison
- Multiple property types
- Risk flags

### Nice to Have (Post-MVP)
- Broker packages
- Investment memos
- Lender packages
- Neighborhood intelligence

---

## Key Implementation Notes

### Underwriting Engine
- **All calculations must be deterministic Python code**
- No AI hallucination for numbers
- Each formula must be thoroughly tested
- All assumptions must be editable and traceable

### AI Integration
- Use function calling for deterministic operations
- AI explains results, doesn't calculate
- Always show data sources and confidence scores
- Flag assumptions and estimates

### Data Extraction
- Start simple (basic regex for common patterns)
- Improve with OpenAI structured outputs
- Manual override always available
- Save source references

### Database
- Use PostgreSQL with Row-Level Security
- All queries must respect user ownership
- Regular backups
- Migration strategy for updates

### Frontend
- Mobile-first design
- Responsive web layout
- Offline capability where possible
- Native feel for mobile

---

## Testing Strategy

### Unit Tests
- Underwriting calculations
- Rules engine
- Data validation
- Formatting utilities

### Integration Tests
- API endpoints
- Database operations
- External API calls (mocked)
- OpenAI integration

### End-to-End Tests
- Deal creation flow
- Underwriting flow
- Chat interaction
- Document generation

### Manual Testing
- Mobile screens (iOS/Android)
- Web responsiveness
- Browser compatibility
- Edge cases

---

## Success Metrics (MVP Launch)

- [ ] 100+ users in first week
- [ ] 90%+ calculation accuracy verification
- [ ] <2s average API response time
- [ ] 99.9% backend uptime
- [ ] <5% daily churn
- [ ] 4.0+ app store rating
- [ ] Zero critical security issues

---

## Timeline Summary

| Phase | Duration | Target |
|-------|----------|--------|
| 1-2 | Weeks 1-2 | Foundation ready |
| 3-4 | Weeks 3-4 | Deal + Underwriting MVP |
| 5-6 | Weeks 5-6 | Scenarios + Chat |
| 7-8 | Weeks 7-8 | Reports + Polish |
| 9-10 | Weeks 9-10 | Deploy + Launch |

**Total MVP Timeline: ~10 weeks**

---

## Critical Path Items

1. Database schema finalization
2. Underwriting calculation accuracy
3. OpenAI integration for extraction + chat
4. Mobile app build & distribution
5. Production deployment infrastructure

Focus on these first to unblock other work.
