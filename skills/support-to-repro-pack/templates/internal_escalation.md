## Escalation Summary
{{ summary }}

## Customer Details
- Customer ID: {{ customer_id }}
- Tenant: {{ tenant_id }}
- Account tier: {{ account_tier }}

## Impact
- Environment: {{ environment }}
- Version: {{ app_version }}
- Error codes: {{ error_codes | join(', ') if error_codes else 'N/A' }}
- Affected scope: {{ affected_scope }}

## Severity: {{ severity }}
{{ severity_justification }}

## Timeline
- Issue reported: {{ reported_at }}
- First response: {{ first_response_at }}
- Current status: {{ current_status }}

## Recommended Actions
{% for action in recommended_actions %}{{ loop.index }}. {{ action }}
{% endfor %}

## Workaround
{{ workaround if workaround else 'No workaround identified yet.' }}
