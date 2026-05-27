-- Migration: Add refund fields to payments table
-- Phase 5: Payment Integration
-- Date: 2026-05-27

-- Add refund tracking fields
ALTER TABLE payments ADD COLUMN IF NOT EXISTS refunded_amount NUMERIC(10, 2) DEFAULT 0.0;
ALTER TABLE payments ADD COLUMN IF NOT EXISTS refund_reference VARCHAR(100);
ALTER TABLE payments ADD COLUMN IF NOT EXISTS refund_reason TEXT;
ALTER TABLE payments ADD COLUMN IF NOT EXISTS refunded_at TIMESTAMP;

-- Add index for faster refund queries
CREATE INDEX IF NOT EXISTS idx_payments_refund_reference ON payments(refund_reference);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);

-- Update existing payments to have refunded_amount = 0.0
UPDATE payments SET refunded_amount = 0.0 WHERE refunded_amount IS NULL;

-- Add check constraint to ensure refunded_amount doesn't exceed amount
ALTER TABLE payments ADD CONSTRAINT IF NOT EXISTS chk_refunded_amount 
  CHECK (refunded_amount >= 0 AND refunded_amount <= amount);

-- Add new payment status values (if using ENUM, otherwise skip)
-- ALTER TYPE payment_status ADD VALUE IF NOT EXISTS 'partially_refunded';

-- Comments for documentation
COMMENT ON COLUMN payments.refunded_amount IS 'Total amount refunded (supports partial refunds)';
COMMENT ON COLUMN payments.refund_reference IS 'M-Pesa refund transaction reference';
COMMENT ON COLUMN payments.refund_reason IS 'Reason for refund';
COMMENT ON COLUMN payments.refunded_at IS 'Timestamp when refund was processed';
