# Database Schema

## Overview

DealMind uses PostgreSQL for data persistence with the following key tables:

## Tables

### `users`
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  subscription_plan TEXT DEFAULT 'free',
  monthly_deal_limit INTEGER DEFAULT 3,
  deals_used_this_month INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### `deals`
```sql
CREATE TABLE deals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  source_type TEXT, -- url, pdf, image, manual
  source_url TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  zip_code TEXT,
  country TEXT DEFAULT 'US',
  latitude NUMERIC,
  longitude NUMERIC,
  property_type TEXT,
  unit_count INTEGER,
  asking_price NUMERIC,
  status TEXT DEFAULT 'draft', -- draft, active, archived
  deal_grade TEXT,
  ai_verdict TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### `deal_inputs`
```sql
CREATE TABLE deal_inputs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  deal_id UUID NOT NULL REFERENCES deals(id) ON DELETE CASCADE,
  input_data JSONB, -- Raw input data
  assumptions JSONB, -- User assumptions
  extracted_fields JSONB, -- Extracted property/financial data
  confidence_scores JSONB, -- Confidence scores per field
  created_at TIMESTAMP DEFAULT NOW()
);
```

### `underwriting_results`
```sql
CREATE TABLE underwriting_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  deal_id UUID NOT NULL REFERENCES deals(id) ON DELETE CASCADE,
  scenario_id UUID,
  noi NUMERIC,
  cap_rate NUMERIC,
  cash_flow_monthly NUMERIC,
  cash_flow_annual NUMERIC,
  cash_on_cash NUMERIC,
  dscr NUMERIC,
  irr NUMERIC,
  equity_multiple NUMERIC,
  break_even_occupancy NUMERIC,
  results_json JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### `scenarios`
```sql
CREATE TABLE scenarios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  deal_id UUID NOT NULL REFERENCES deals(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  changed_inputs JSONB,
  results_json JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_deal FOREIGN KEY (deal_id) REFERENCES deals(id)
);
```

### `chat_threads`
```sql
CREATE TABLE chat_threads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  deal_id UUID NOT NULL REFERENCES deals(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_deal FOREIGN KEY (deal_id) REFERENCES deals(id),
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### `chat_messages`
```sql
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id UUID NOT NULL REFERENCES chat_threads(id) ON DELETE CASCADE,
  role TEXT NOT NULL, -- user, assistant
  content TEXT NOT NULL,
  tool_calls JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_thread FOREIGN KEY (thread_id) REFERENCES chat_threads(id)
);
```

### `documents`
```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  deal_id UUID NOT NULL REFERENCES deals(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  document_type TEXT, -- summary, broker_email, investor_memo, etc
  title TEXT NOT NULL,
  content TEXT,
  pdf_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_deal FOREIGN KEY (deal_id) REFERENCES deals(id),
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Indices

```sql
CREATE INDEX idx_deals_user_id ON deals(user_id);
CREATE INDEX idx_deals_created_at ON deals(created_at DESC);
CREATE INDEX idx_deal_inputs_deal_id ON deal_inputs(deal_id);
CREATE INDEX idx_underwriting_results_deal_id ON underwriting_results(deal_id);
CREATE INDEX idx_scenarios_deal_id ON scenarios(deal_id);
CREATE INDEX idx_chat_threads_deal_id ON chat_threads(deal_id);
CREATE INDEX idx_chat_messages_thread_id ON chat_messages(thread_id);
CREATE INDEX idx_documents_deal_id ON documents(deal_id);
```

## Row-Level Security (RLS)

Enable RLS on all user-facing tables to ensure users can only access their own data:

```sql
ALTER TABLE deals ENABLE ROW LEVEL SECURITY;
ALTER TABLE deal_inputs ENABLE ROW LEVEL SECURITY;
ALTER TABLE underwriting_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE scenarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_threads ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Example RLS policy for deals
CREATE POLICY "Users can view their own deals" ON deals
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own deals" ON deals
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

## Migration Strategy

Use Alembic for Python/SQLAlchemy migrations:

```bash
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```
