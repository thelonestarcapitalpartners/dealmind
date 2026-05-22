# Real Estate AI Underwriting Platform — Full Technical Requirements

## 1. Product Vision

Build a mobile-first AI real estate underwriting platform where users can paste a property link, upload a PDF, upload images, or manually enter data, and the system automatically extracts property information, runs real estate investment calculations, generates deal insights, allows users to chat with the deal, and creates professional documents for brokers, investors, lenders, and partners.

The platform should feel like **ChatGPT for real estate deals**.

Core promise:

> Paste a deal. Get the numbers. Talk to the deal. Decide faster.

---

# 2. Primary User Types

## 2.1 Real Estate Investors

They want to analyze properties quickly without spreadsheets.

Needs:

* Instant underwriting
* Cash flow analysis
* Cap rate
* Cash-on-cash return
* DSCR
* ROI
* IRR
* Appreciation projections
* Refinance scenarios
* Offer price scenarios
* Deal comparison
* Investor reports

## 2.2 Brokers / Agents

They want to present deals better.

Needs:

* Auto-generated offering summaries
* Seller pricing strategy
* Buyer-facing financial reports
* Broker email drafts
* Deal PDFs
* Neighborhood reports
* Market comps

## 2.3 Sellers

They want to price strategically.

Needs:

* Suggested listing price
* Buyer-return simulation
* "Leave meat on the bone" pricing
* Seller net proceeds
* Deal attractiveness score

## 2.4 Lenders

They want clean numbers.

Needs:

* DSCR
* LTV
* Debt yield
* NOI
* Loan assumptions
* Stabilized projections
* PDF loan package

## 2.5 International Investors

They want to analyze deals in different countries.

Needs:

* Country detection
* Currency handling
* Local tax assumptions
* Local purchase cost rules
* Local investment formulas

---

# 3. Core Platform Experience

## 3.1 Main User Flow

1. User opens mobile app or web app.
2. User taps **New Deal**.
3. User chooses input method:

   * Paste property URL
   * Upload PDF
   * Upload images
   * Paste raw text
   * Manual entry
4. System extracts property data.
5. System detects:

   * Address
   * Country
   * State/province
   * City
   * ZIP/postal code
   * Property type
   * Unit count
   * Investment type
6. System runs underwriting.
7. User sees:

   * Deal summary
   * Key metrics
   * Risk score
   * AI verdict
   * Missing data warnings
8. User can chat with the deal:

   * "What if I offer $850,000 instead?"
   * "Run 10-year cash flow."
   * "Add $50,000 CapEx."
   * "What if rent increases 3% per year?"
9. User can generate documents:

   * Broker email
   * Investor memo
   * Lender summary
   * Offer letter
   * PDF report
   * Pitch deck later

---

# 4. Platform Architecture

## 4.1 Recommended Tech Stack

### Frontend

Use:

* **React Native with Expo** for mobile app
* **Next.js** for web app
* **TypeScript** everywhere
* **TailwindCSS** for styling
* **Shadcn UI** for web components
* **React Native Paper** or **NativeWind** for mobile UI

Reason:

* Mobile-first
* Cross-platform iOS/Android
* Web app possible with shared logic
* Fast MVP development

---

### Backend

Use:

* **Python FastAPI** for API backend
* **PostgreSQL** for relational database
* **Supabase** or **Neon** for managed Postgres
* **Redis** for caching
* **Celery** or **RQ** for background jobs
* **Docker** for deployment

Reason:

* Python is best for calculations, AI workflows, data extraction, and underwriting models.

---

### AI Layer

Use:

* OpenAI API / GPT models for:

  * Data extraction
  * Chat with deal
  * Document generation
  * Explanation layer
  * Scenario interpretation
* Structured output using JSON schemas
* Function calling/tool calling for calculations

Important principle:

> The LLM should explain and reason, but the math must be done by deterministic backend functions.

Do **not** let the LLM invent financial calculations.

---

### Database

Use:

* PostgreSQL
* pgvector if semantic memory/search is needed
* Prisma or SQLAlchemy ORM

---

### File Storage

Use:

* Supabase Storage, AWS S3, or Cloudflare R2

Store:

* Uploaded PDFs
* Property images
* Generated reports
* Parsed documents
* Export files

---

### Deployment

MVP:

* Vercel for web frontend
* Railway / Render / Fly.io for backend
* Supabase for database/storage/auth

Scale:

* AWS ECS / Kubernetes
* RDS Postgres
* S3
* CloudFront
* ElastiCache Redis

---

# 5. Main Modules

## 5.1 Authentication Module

Features:

* Email/password login
* Google login
* Apple login for iOS
* Forgot password
* User profile
* Subscription status
* Deal usage limits

Recommended:

* Supabase Auth
* Clerk
* Firebase Auth

User fields:

```json
{
  "id": "uuid",
  "email": "string",
  "name": "string",
  "subscription_plan": "free | pro | elite | enterprise",
  "monthly_deal_limit": "integer",
  "deals_used_this_month": "integer",
  "created_at": "timestamp"
}
```

---

## 5.2 Deal Input Module

Input types:

### URL Input

User can paste:

* Zillow link
* Redfin link
* Realtor.com link
* LoopNet link
* Crexi link
* MLS public page
* Broker website listing
* Custom property website

System should:

* Fetch page content where legally allowed
* Extract visible listing data
* Save raw HTML/text
* Detect missing fields

Important:

Scraping must respect terms of service. Long term, use APIs/licensed data providers.

---

### PDF Upload

User uploads:

* Offering memorandum
* Broker package
* Rent roll
* T12
* Flyer
* Appraisal
* Inspection report

System should:

* Extract text
* Extract tables
* Identify document type
* Pull key data
* Preserve source references

Use:

* PyMuPDF
* pdfplumber
* Unstructured.io
* Tesseract OCR if scanned
* LLM extraction with schema validation

---

### Image Upload

User uploads:

* Flyer photo
* Property photo
* Rent roll screenshot
* Broker screenshot

System should:

* Use OCR
* Extract relevant text
* Detect property data

---

### Manual Entry

Allow user to enter:

* Purchase price
* Rent
* Units
* Taxes
* Insurance
* Repairs
* Vacancy
* Management
* Utilities
* Financing
* Closing costs
* Exit assumptions

---

# 6. Data Extraction Engine

## 6.1 Required Extracted Fields

Property identity:

```json
{
  "property_name": "string",
  "address": "string",
  "city": "string",
  "state": "string",
  "zip_code": "string",
  "country": "string",
  "latitude": "number",
  "longitude": "number"
}
```

Property details:

```json
{
  "property_type": "single_family | condo | duplex | triplex | fourplex | small_multifamily | commercial_multifamily | retail | office | industrial | land | mixed_use",
  "unit_count": "integer",
  "bedrooms": "number",
  "bathrooms": "number",
  "square_feet": "number",
  "lot_size": "number",
  "year_built": "integer",
  "occupancy_status": "vacant | occupied | partially_occupied | unknown"
}
```

Financial data:

```json
{
  "asking_price": "number",
  "current_rent_monthly": "number",
  "market_rent_monthly": "number",
  "gross_scheduled_income": "number",
  "vacancy_rate": "number",
  "property_taxes_annual": "number",
  "insurance_annual": "number",
  "hoa_monthly": "number",
  "utilities_annual": "number",
  "repairs_maintenance_annual": "number",
  "property_management_rate": "number",
  "capex_reserve_annual": "number",
  "other_expenses_annual": "number"
}
```

Financing data:

```json
{
  "down_payment_percent": "number",
  "loan_amount": "number",
  "interest_rate": "number",
  "loan_term_years": "integer",
  "amortization_years": "integer",
  "points": "number",
  "closing_costs": "number"
}
```

Source confidence:

```json
{
  "field_name": "asking_price",
  "value": 1000000,
  "source": "PDF page 3",
  "confidence": 0.95,
  "needs_user_confirmation": false
}
```

---

# 7. Validation Engine

The system must validate all extracted data.

Examples:

* If property tax is missing, estimate it by county average.
* If rent is missing, use rent estimate APIs.
* If insurance is missing, use default assumption by property type/state.
* If unit count conflicts between PDF and listing, flag it.
* If expenses are unrealistically low, warn user.
* If cap rate looks too high, ask whether income is current or projected.

Each field should have:

* Value
* Source
* Confidence score
* Manual override option

Never hide weak assumptions.

---

# 8. Underwriting Calculation Engine

This must be deterministic code, not AI hallucination.

## 8.1 Core Formulas

### Gross Scheduled Income

```text
GSI = monthly_rent * 12
```

### Effective Gross Income

```text
EGI = GSI - vacancy_loss + other_income
```

### Operating Expenses

```text
Operating Expenses = taxes + insurance + repairs + maintenance + management + utilities + capex_reserve + HOA + other_expenses
```

### Net Operating Income

```text
NOI = EGI - Operating Expenses
```

### Cap Rate

```text
Cap Rate = NOI / Purchase Price
```

### Monthly Debt Service

Use amortization formula.

### Annual Debt Service

```text
Annual Debt Service = Monthly Debt Service * 12
```

### Cash Flow

```text
Annual Cash Flow = NOI - Annual Debt Service
Monthly Cash Flow = Annual Cash Flow / 12
```

### Cash-on-Cash Return

```text
CoC = Annual Cash Flow / Total Cash Invested
```

### DSCR

```text
DSCR = NOI / Annual Debt Service
```

### Total Cash Invested

```text
Total Cash Invested = Down Payment + Closing Costs + Rehab + Initial Reserves
```

### Break-even Occupancy

```text
Break-even Occupancy = (Operating Expenses + Debt Service) / Gross Scheduled Income
```

### Loan-to-Value

```text
LTV = Loan Amount / Property Value
```

### Debt Yield

```text
Debt Yield = NOI / Loan Amount
```

---

## 8.2 Projection Engine

Support:

* 1-year projection
* 2-year projection
* 5-year projection
* 10-year projection
* 30-year projection

Inputs:

```json
{
  "rent_growth_rate": 0.03,
  "expense_growth_rate": 0.025,
  "appreciation_rate": 0.03,
  "vacancy_rate": 0.05,
  "selling_cost_percent": 0.06,
  "refinance_year": 5,
  "exit_year": 10
}
```

Outputs by year:

```json
{
  "year": 1,
  "property_value": 1030000,
  "gross_income": 96000,
  "operating_expenses": 38000,
  "NOI": 58000,
  "debt_service": 42000,
  "cash_flow": 16000,
  "loan_balance": 760000,
  "equity": 270000,
  "cash_on_cash": 0.08
}
```

---

## 8.3 Scenario Engine

Users should be able to ask:

* What if price drops to $800,000?
* What if interest rate becomes 5.75%?
* What if rent increases by 10%?
* What if CapEx is $100,000?
* What if vacancy is 10%?
* What if I refinance in year 5?
* What if I sell in year 10?
* What if I use seller financing?
* What if I house hack?
* What if one unit is vacant?
* What if taxes reassess after purchase?

Each scenario should create a saved version.

Scenario table:

```json
{
  "scenario_id": "uuid",
  "deal_id": "uuid",
  "name": "Offer at $850k",
  "inputs_changed": {},
  "results": {},
  "created_at": "timestamp"
}
```

---

# 9. Property Type Logic

The platform must adapt based on property type.

## 9.1 Single-Family Rental

Metrics:

* Rent-to-price ratio
* Cash flow
* Cap rate
* CoC
* Appreciation
* Debt service
* Maintenance estimate
* Vacancy estimate

## 9.2 Duplex / Triplex / Fourplex

Metrics:

* Unit-level rent
* Owner-occupied scenario
* FHA / conventional house hack assumptions
* Per-unit expenses
* DSCR
* Cash flow if living in one unit

## 9.3 5+ Unit Multifamily

Metrics:

* NOI
* Cap rate
* DSCR
* Debt yield
* Stabilized NOI
* Value-add rent upside
* Exit cap
* IRR
* Equity multiple

## 9.4 Large Commercial Multifamily

Additional:

* T12 analysis
* Rent roll analysis
* Loss-to-lease
* Bad debt
* Payroll
* Replacement reserves
* Preferred return
* Waterfall model later

## 9.5 Fix and Flip

Metrics:

* Purchase price
* Rehab cost
* ARV
* Holding costs
* Selling costs
* Profit
* ROI
* Timeline
* LTV
* LTC

Formula:

```text
Profit = ARV - Purchase Price - Rehab - Holding Costs - Selling Costs - Financing Costs
```

## 9.6 BRRRR

Metrics:

* Buy
* Rehab
* Rent
* Refinance
* Repeat
* Cash left in deal
* Refinance proceeds
* DSCR after refinance

## 9.7 Land / Development

Later version:

* Lot count
* Entitlement risk
* Road/utilities cost
* Soft costs
* Hard costs
* Absorption timeline
* Exit price
* Profit margin

---

# 10. AI Chat With Deal

Each deal should have its own chat thread.

## 10.1 Chat Behavior

The AI must know:

* Deal data
* Extracted sources
* Current assumptions
* Saved scenarios
* User preferences
* Property type
* Location
* Country rules

User can ask:

* "Explain this deal simply."
* "Why is cash flow negative?"
* "What price makes this deal good?"
* "What rent do I need to break even?"
* "What should I offer?"
* "Write a message to the broker."
* "Create an investor summary."
* "Compare this with Deal B."
* "What are the biggest risks?"

## 10.2 Important AI Rule

AI must not make up numbers.

If data is missing, it should say:

> "This number is estimated because the source did not provide insurance. I used a default assumption of $X/year. You can edit it."

---

# 11. AI Output Style

Each deal should get:

## 11.1 One-Sentence Verdict

Examples:

* "This deal is weak at asking price because cash flow is negative and DSCR is below 1.0."
* "This deal becomes attractive if purchased below $850,000 or if rents increase by 12%."
* "Strong cash-flow deal, but taxes and CapEx assumptions need verification."

## 11.2 Deal Grade

Use:

* A+
* A
* B
* C
* D
* F

Grade factors:

* Cash flow
* DSCR
* Cap rate
* CoC return
* Market risk
* Debt risk
* Expense risk
* Data confidence
* Upside potential

## 11.3 Risk Flags

Examples:

* Missing rent roll
* Tax reassessment risk
* Insurance not verified
* Expense ratio too low
* Occupancy unclear
* Market rent assumption aggressive
* CapEx not included
* DSCR below lender standard

---

# 12. Document Generator

Users can generate:

## 12.1 Broker Email

Prompt:

> Write a professional email to the broker asking for rent roll, T12, utility bills, tax history, insurance quote, and seller motivation.

## 12.2 Offer Letter

Includes:

* Property
* Offer price
* Terms
* Due diligence period
* Financing
* Closing timeline
* Reason based on numbers

## 12.3 Investor Memo

Includes:

* Executive summary
* Property overview
* Deal metrics
* Purchase assumptions
* Financing assumptions
* Risk factors
* Return projections
* Exit strategy

## 12.4 Lender Summary

Includes:

* Borrower summary
* Property overview
* NOI
* DSCR
* LTV
* Loan request
* Rent roll
* Stabilized scenario

## 12.5 Seller Pricing Report

Includes:

* Recommended asking price
* Buyer return at different prices
* Seller net proceeds
* Market positioning
* Suggested pricing strategy

## 12.6 PDF Export

Use:

* HTML-to-PDF renderer
* WeasyPrint, Playwright PDF, or React PDF

---

# 13. Neighborhood Intelligence Features

## 13.1 Neighborhood Report

Based on property address, generate:

* Nearby grocery stores
* Pharmacies
* Hospitals
* Schools
* Universities
* Parks
* Gyms
* Restaurants
* Public transportation
* Major employers
* Highways
* Airports
* Shopping centers

For each:

```json
{
  "name": "Walmart Supercenter",
  "category": "grocery",
  "distance_miles": 1.2,
  "drive_time_minutes": 5,
  "rating": 4.1
}
```

Use:

* Google Places API
* Google Maps API
* OpenStreetMap
* Yelp Fusion API later

---

## 13.2 Crime Report

Sources:

* Local police department APIs where available
* City open data portals
* FBI Crime Data API
* NeighborhoodScout-style licensed data later

Output:

* Crime score
* Violent crime
* Property crime
* Trend over time
* Comparison to city average
* Investor-friendly explanation

Important:

Crime data must include disclaimers because sources vary by city.

---

## 13.3 School Report

Sources:

* GreatSchools API if available
* Niche-like licensed data later
* Government school district data
* Google Places for nearby schools

Output:

* Nearby schools
* Ratings
* Distance
* District
* Rent/resale impact explanation

---

## 13.4 Market Report

Sources:

* Zillow/Redfin data where licensed
* ATTOM
* RentCast
* Census
* FRED
* Local MLS integration later

Output:

* Median home price
* Median rent
* Rent growth
* Price growth
* Days on market
* Inventory trend
* Population growth
* Income trend
* Employment drivers

---

# 14. Data Provider Integrations

## 14.1 MVP Possible APIs

Use cheaper/easier APIs first:

* RentCast API for rent estimates and property data
* ATTOM API for property records
* Google Maps / Places API
* Census API
* FBI Crime Data API
* FRED API
* OpenStreetMap
* Mapbox

## 14.2 Later APIs

* MLS partnerships
* CoStar / LoopNet data licensing
* Crexi partnership
* CoreLogic
* Black Knight
* Reonomy
* GreatSchools
* HouseCanary
* AirDNA for STR analysis

---

# 15. Global Country Logic

The system should detect country from address.

## 15.1 Country Detection

Use:

* Google Geocoding API
* Mapbox Geocoding
* OpenStreetMap Nominatim

Store:

```json
{
  "country": "United States",
  "country_code": "US",
  "currency": "USD",
  "region": "Texas",
  "local_tax_ruleset": "US_TX"
}
```

## 15.2 Rules Engine

Create modular rules per country/state.

Example folder:

```text
rules/
  us/
    federal.py
    texas.py
    florida.py
    california.py
  germany/
    federal.py
    hamburg.py
    bavaria.py
  uk/
  canada/
```

## 15.3 U.S. Rules

Must support:

* Property tax by county
* Insurance estimate by state
* Depreciation assumptions
* Closing cost assumptions
* Loan amortization
* DSCR lending assumptions
* 1031 exchange estimator later

## 15.4 Germany Rules

Later support:

* Grunderwerbsteuer
* Notarkosten
* Grundbuchkosten
* Maklerprovision
* Hausgeld
* Instandhaltungsrücklage
* AfA depreciation
* Einkommensteuer assumptions
* Warmmiete/Kaltmiete distinction

---

# 16. Database Schema

## 16.1 Users

```sql
users (
  id uuid primary key,
  email text unique,
  full_name text,
  subscription_plan text,
  monthly_deal_limit int,
  deals_used_this_month int,
  created_at timestamp
)
```

## 16.2 Deals

```sql
deals (
  id uuid primary key,
  user_id uuid references users(id),
  title text,
  source_type text,
  source_url text,
  address text,
  city text,
  state text,
  zip_code text,
  country text,
  latitude numeric,
  longitude numeric,
  property_type text,
  unit_count int,
  asking_price numeric,
  status text,
  deal_grade text,
  ai_verdict text,
  created_at timestamp,
  updated_at timestamp
)
```

## 16.3 Deal Inputs

```sql
deal_inputs (
  id uuid primary key,
  deal_id uuid references deals(id),
  input_data jsonb,
  assumptions jsonb,
  extracted_fields jsonb,
  confidence_scores jsonb,
  created_at timestamp
)
```

## 16.4 Underwriting Results

```sql
underwriting_results (
  id uuid primary key,
  deal_id uuid references deals(id),
  scenario_id uuid,
  noi numeric,
  cap_rate numeric,
  cash_flow_monthly numeric,
  cash_flow_annual numeric,
  cash_on_cash numeric,
  dscr numeric,
  irr numeric,
  equity_multiple numeric,
  break_even_occupancy numeric,
  results_json jsonb,
  created_at timestamp
)
```

## 16.5 Scenarios

```sql
scenarios (
  id uuid primary key,
  deal_id uuid references deals(id),
  name text,
  changed_inputs jsonb,
  results_json jsonb,
  created_at timestamp
)
```

## 16.6 Chat Threads

```sql
chat_threads (
  id uuid primary key,
  deal_id uuid references deals(id),
  user_id uuid references users(id),
  title text,
  created_at timestamp
)
```

## 16.7 Chat Messages

```sql
chat_messages (
  id uuid primary key,
  thread_id uuid references chat_threads(id),
  role text,
  content text,
  tool_calls jsonb,
  created_at timestamp
)
```

## 16.8 Documents

```sql
documents (
  id uuid primary key,
  deal_id uuid references deals(id),
  user_id uuid references users(id),
  document_type text,
  title text,
  content text,
  pdf_url text,
  created_at timestamp
)
```

---

# 17. API Endpoints

## Auth

```text
POST /auth/signup
POST /auth/login
POST /auth/logout
GET /auth/me
```

## Deals

```text
POST /deals
GET /deals
GET /deals/{deal_id}
DELETE /deals/{deal_id}
PATCH /deals/{deal_id}
```

## Deal Input

```text
POST /deals/from-url
POST /deals/from-pdf
POST /deals/from-image
POST /deals/manual
```

## Underwriting

```text
POST /deals/{deal_id}/underwrite
GET /deals/{deal_id}/results
POST /deals/{deal_id}/scenario
GET /deals/{deal_id}/scenarios
```

## Chat

```text
POST /deals/{deal_id}/chat
GET /deals/{deal_id}/chat
```

## Reports

```text
POST /deals/{deal_id}/generate-report
POST /deals/{deal_id}/generate-broker-email
POST /deals/{deal_id}/generate-investor-memo
POST /deals/{deal_id}/generate-lender-summary
POST /deals/{deal_id}/export-pdf
```

## Neighborhood

```text
GET /deals/{deal_id}/neighborhood
GET /deals/{deal_id}/crime
GET /deals/{deal_id}/schools
GET /deals/{deal_id}/market
```

## Subscription

```text
GET /billing/plans
POST /billing/checkout
POST /billing/webhook
GET /billing/status
```

---

# 18. UI Requirements

## 18.1 Mobile App Main Screens

### Home Screen

Shows:

* New Deal button
* Recent deals
* Deal search
* Usage limit
* Subscription status

### New Deal Screen

Options:

* Paste Link
* Upload PDF
* Upload Image
* Manual Entry

### Deal Summary Screen

Shows:

* Property photo
* Address
* Price
* Unit count
* Deal grade
* AI verdict
* Key metrics:

  * Cap rate
  * Cash flow
  * CoC
  * DSCR
  * NOI

### Deal Chat Screen

Chat interface like ChatGPT.

Each deal has its own thread.

Plus button opens tools:

* Neighborhood Report
* Crime Report
* School Report
* Market Trends
* Offer Letter
* Investor Memo
* Lender Summary
* Scenario Builder
* PDF Export

### Assumptions Screen

Editable inputs:

* Price
* Rent
* Vacancy
* Expenses
* Loan terms
* CapEx
* Appreciation
* Exit cap
* Rent growth

### Scenario Screen

Shows different scenarios side by side.

Example:

* Asking price
* Offer at $900k
* Offer at $850k
* Stabilized rents
* Refinance year 5

### Documents Screen

Generated documents:

* Broker emails
* Investor memos
* Lender packages
* PDF reports

---

# 19. Subscription Model

## Free

* 3 deals/month
* Basic underwriting
* Limited chat
* No PDF export

## Pro

* 50 deals/month
* Full underwriting
* Deal chat
* Scenario analysis
* Basic PDF export

## Elite

* Unlimited deals
* Full reports
* Neighborhood/crime/school tools
* Advanced projections
* Investor/lender documents

## Enterprise

* Team accounts
* Broker dashboard
* API access
* White-label reports
* Shared deal rooms

Use Stripe for billing.

---

# 20. Security Requirements

Must include:

* Secure authentication
* Row-level security by user
* Encrypted file storage
* HTTPS only
* Rate limiting
* Input sanitization
* File upload virus scanning later
* API key protection
* Audit logs for enterprise

Important:

Users should never access another user's deals.

---

# 21. AI Safety and Reliability Requirements

The AI must:

* Show assumptions
* Distinguish actual numbers from estimates
* Avoid legal/tax guarantees
* Recommend professional review for legal/tax decisions
* Never fabricate data sources
* Flag uncertainty
* Let users edit numbers
* Save calculation history

Every report should include:

> This analysis is based on available data and assumptions. It is not legal, tax, or financial advice. Verify all numbers before making investment decisions.

---

# 22. MVP Scope

Do **not** build everything first.

## MVP Version 1 Should Include

Must-have:

1. User login
2. Paste property link
3. Upload PDF
4. Manual input fallback
5. Data extraction
6. Basic U.S. underwriting
7. Single-family and 2–4 unit support
8. Multifamily basic support
9. Deal summary
10. Chat with deal
11. Scenario changes
12. PDF summary export
13. Broker email generator
14. Investor memo generator
15. Subscription limits

Do not include at first:

* Global countries
* Full crime reports
* Full school reports
* Enterprise teams
* MLS integrations
* Development underwriting
* Waterfall modeling

Build the wedge first:

> Paste a link or PDF → get instant numbers → chat with the deal.

That is the killer MVP.

---

# 23. Future Roadmap

## Phase 1 — MVP

* U.S. only
* Residential investment
* Mobile-first
* AI underwriting
* Chat with deal

## Phase 2 — Data Expansion

* Rent estimates
* Neighborhood reports
* Crime reports
* School reports
* Market trends
* Better comp engine

## Phase 3 — Professional Tools

* Broker packages
* Lender packages
* Team collaboration
* Deal comparison
* Portfolio tracking

## Phase 4 — Advanced Asset Classes

* Commercial multifamily
* Retail
* Office
* Industrial
* Development
* Land
* BRRRR
* Fix and flip
* Short-term rentals

## Phase 5 — Global Expansion

* Germany
* UK
* Canada
* France
* UAE
* Country-specific taxes
* Currency conversion
* Multilingual interface
