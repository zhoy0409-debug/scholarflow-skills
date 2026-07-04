# PII Redaction Rules

## Regex-Handled (by Python backend)

The following PII types are detected and replaced by the `repro_pack redact` command:

| Type | Pattern | Placeholder |
|------|---------|-------------|
| Email | `user@domain.com` | `[EMAIL_N]` |
| Phone (US/CN) | `+1-xxx`, `138xxxx` | `[PHONE_N]` |
| IPv4/IPv6 | `192.168.x.x` | `[IP_ADDRESS_N]` |
| AWS Key | `AKIA...` | `[AWS_KEY_N]` |
| JWT | `eyJ...` | `[JWT_N]` |
| Bearer Token | `Bearer xxx` | `[AUTH_TOKEN_N]` |
| API Key | `api_key=xxx` | `[API_KEY_N]` |
| Credit Card | Visa/MC/Amex patterns | `[CREDIT_CARD_N]` |
| SSN (US) | `xxx-xx-xxxx` | `[SSN_N]` |
| China ID Card | 18-digit ID | `[ID_CARD_N]` |
| UUID | `xxxxxxxx-xxxx-...` | `[UUID_N]` |
| Password | `password=xxx` | `[PASSWORD_N]` |
| Cookie | `Cookie: xxx` | `[COOKIE_N]` |
| URL with creds | `http://user:pass@host` | `[URL_WITH_CREDENTIALS_N]` |
| Private Key | `-----BEGIN PRIVATE KEY-----` | `[PRIVATE_KEY_N]` |

## AI Semantic Redaction (your responsibility)

The regex engine cannot catch these — you must find and replace them manually:

1. **Names in natural language**: "张三说他的账号登不上" → "[CUSTOMER_NAME] 说他的账号登不上"
2. **Internal project codenames**: "Project Phoenix 的 API 挂了" → "[PROJECT_NAME] 的 API 挂了"
3. **Customer company names**: "Acme Corp 的租户" → "[CUSTOMER_ORG] 的租户"
4. **Internal employee names**: "找 @david 看一下" → "找 [INTERNAL_STAFF] 看一下"
5. **Tenant/org identifiers in sentences**: "他们的 tenant 是 acme-prod-01" → "他们的 tenant 是 [TENANT_ID]"
6. **Addresses and locations**: Physical addresses, office locations
7. **Custom domain names**: Customer-specific subdomains that reveal identity

## Redaction Principles

- When in doubt, redact. False positives are acceptable; false negatives are not.
- Maintain referential consistency: the same entity should get the same placeholder throughout.
- Preserve structure: `[EMAIL_1]` in the ticket should map to the same person as `[EMAIL_1]` in the logs.
