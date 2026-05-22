# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints (except auth) require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## Auth Endpoints

### POST /api/auth/signup
Register a new user

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Investor"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user_id": "uuid",
  "email": "user@example.com"
}
```

### POST /api/auth/login
User login

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200):**
Same as signup response

### POST /api/auth/logout
Logout current user

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

### GET /api/auth/me
Get current authenticated user

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Investor",
  "subscription_plan": "pro",
  "monthly_deal_limit": 50,
  "deals_used_this_month": 12
}
```

---

## Deals Endpoints

### POST /api/deals
Create a new deal

**Request:**
```json
{
  "title": "Downtown Duplex",
  "address": "123 Main St",
  "city": "Austin",
  "state": "TX",
  "zip_code": "78701",
  "property_type": "duplex",
  "unit_count": 2,
  "asking_price": 500000,
  "source_type": "manual",
  "source_url": null
}
```

**Response (201):**
```json
{
  "id": "deal-uuid",
  "title": "Downtown Duplex",
  "address": "123 Main St",
  "city": "Austin",
  "state": "TX",
  "zip_code": "78701",
  "property_type": "duplex",
  "unit_count": 2,
  "asking_price": 500000,
  "deal_grade": null,
  "ai_verdict": null,
  "status": "draft",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### GET /api/deals
List all deals for current user

**Query Params:**
- `status`: draft, active, archived
- `limit`: default 20
- `offset`: default 0
- `sort_by`: created_at, updated_at, deal_grade (default: created_at)

**Response (200):**
```json
{
  "data": [
    { ... deal objects ... }
  ],
  "total": 45,
  "limit": 20,
  "offset": 0
}
```

### GET /api/deals/{deal_id}
Get specific deal details

**Response (200):**
Deal object with full details

### PATCH /api/deals/{deal_id}
Update a deal

**Request:**
```json
{
  "title": "Updated Title",
  "asking_price": 525000
}
```

**Response (200):**
Updated deal object

### DELETE /api/deals/{deal_id}
Delete a deal

**Response (200):**
```json
{
  "message": "Deal deleted successfully"
}
```

### POST /api/deals/{deal_id}/from-url
Extract deal data from property URL

**Request:**
```json
{
  "url": "https://www.zillow.com/homedetails/..."
}
```

**Response (200):**
```json
{
  "extracted_data": {
    "asking_price": 500000,
    "property_taxes": 3000,
    ...
  },
  "confidence": 0.87
}
```

### POST /api/deals/{deal_id}/from-pdf
Extract deal data from PDF file

**Request:** Multipart form with file upload

**Response (200):**
Extracted data with confidence scores

---

## Underwriting Endpoints

### POST /api/underwriting/{deal_id}/underwrite
Run underwriting calculations

**Request:**
```json
{
  "purchase_price": 500000,
  "monthly_rent": 2500,
  "vacancy_rate": 0.05,
  "property_taxes_annual": 3000,
  "insurance_annual": 1200,
  "repairs_maintenance_annual": 2000,
  "management_rate": 0.08,
  "capex_reserve_annual": 2000,
  "down_payment_percent": 0.25,
  "interest_rate": 0.065,
  "loan_term_years": 30,
  "property_type": "single_family"
}
```

**Response (200):**
```json
{
  "noi": 52000,
  "cap_rate": 0.104,
  "cash_flow_monthly": 450,
  "cash_flow_annual": 5400,
  "cash_on_cash_return": 0.085,
  "dscr": 1.28,
  "total_cash_invested": 127500,
  "break_even_occupancy": 0.65,
  "deal_grade": "A",
  "ai_verdict": "Strong cash-flow deal at asking price. Verify CapEx and tax assumptions.",
  "risk_flags": [
    "CapEx reserve relatively low",
    "Tax reassessment risk"
  ]
}
```

### GET /api/underwriting/{deal_id}/results
Get latest underwriting results

**Response (200):**
Underwriting result object

### POST /api/underwriting/{deal_id}/projection
Run multi-year projection

**Query Params:**
- `years`: 1, 5, 10, 30 (default: 5)
- `rent_growth_rate`: 0.03 (default)
- `expense_growth_rate`: 0.025 (default)
- `appreciation_rate`: 0.03 (default)

**Response (200):**
```json
{
  "projections": [
    {
      "year": 1,
      "property_value": 515000,
      "gross_income": 30000,
      "operating_expenses": 8000,
      "noi": 22000,
      "debt_service": 18000,
      "cash_flow": 4000,
      "loan_balance": 360000,
      "equity": 155000,
      "cash_on_cash": 0.032
    },
    ...
  ],
  "total_return": 150000,
  "irr": 0.156,
  "equity_multiple": 2.2
}
```

### POST /api/underwriting/{deal_id}/scenario
Create what-if scenario

**Request:**
```json
{
  "scenario_name": "Offer at $475k",
  "changed_inputs": {
    "purchase_price": 475000
  }
}
```

**Response (201):**
```json
{
  "scenario_id": "scenario-uuid",
  "scenario_name": "Offer at $475k",
  "results": { ... underwriting results ... },
  "created_at": "2024-01-15T10:30:00Z"
}
```

### GET /api/underwriting/{deal_id}/scenarios
List all scenarios for a deal

**Response (200):**
```json
[
  { ... scenario objects ... }
]
```

---

## Chat Endpoints

### POST /api/chat/{deal_id}/message
Send message to deal AI

**Request:**
```json
{
  "message": "What if I offer $475,000?",
  "context": {
    "scenario_name": "Offer at $475k"
  }
}
```

**Response (200):**
```json
{
  "id": "msg-uuid",
  "role": "assistant",
  "content": "If you offer $475,000 instead of the asking price...",
  "created_at": "2024-01-15T10:30:00Z",
  "tool_calls": [
    {
      "name": "run_underwriting",
      "args": { ... }
    }
  ]
}
```

### GET /api/chat/{deal_id}/thread
Get full chat thread for a deal

**Response (200):**
```json
{
  "thread_id": "thread-uuid",
  "deal_id": "deal-uuid",
  "title": "Downtown Duplex Chat",
  "message_count": 5,
  "created_at": "2024-01-15T10:30:00Z",
  "messages": [
    { ... message objects ... }
  ]
}
```

### GET /api/chat/{deal_id}/messages
List chat messages with pagination

**Query Params:**
- `limit`: default 50
- `offset`: default 0

**Response (200):**
List of message objects

---

## Reports Endpoints

### POST /api/reports/{deal_id}/generate-report
Generate deal summary report

**Request:**
```json
{
  "report_type": "pdf",
  "include_sections": ["metrics", "assumptions", "risks", "projections"]
}
```

**Response (200):**
```json
{
  "document_id": "doc-uuid",
  "deal_id": "deal-uuid",
  "document_type": "summary",
  "title": "Downtown Duplex - Deal Summary",
  "content": "...",
  "pdf_url": "https://...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### POST /api/reports/{deal_id}/generate-broker-email
Generate broker inquiry email

**Response (200):**
Document object

### POST /api/reports/{deal_id}/generate-investor-memo
Generate investor memo

**Response (200):**
Document object

### POST /api/reports/{deal_id}/generate-lender-summary
Generate lender summary

**Response (200):**
Document object

### POST /api/reports/{deal_id}/export-pdf
Export deal as PDF

**Response:** PDF file download

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to access this resource"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

- Free plan: 100 requests/minute
- Pro plan: 1000 requests/minute
- Elite plan: 10000 requests/minute

Rate limit info in response headers:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`
