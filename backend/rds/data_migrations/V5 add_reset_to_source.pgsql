ALTER table source_label
add column "redact" BOOLEAN DEFAULT FALSE;
COMMENT ON COLUMN source_label.redact IS 'If true the user has taken back this being the source.';