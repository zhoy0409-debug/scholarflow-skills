## Problem Summary
{{ summary }}

## Environment
| Field | Value |
|-------|-------|
{% if environment %}| Environment | {{ environment }} |
{% endif %}{% if app_version %}| Version | {{ app_version }} |
{% endif %}{% if build_number %}| Build | {{ build_number }} |
{% endif %}{% if browser %}| Browser | {{ browser }}{% if browser_version %} {{ browser_version }}{% endif %} |
{% endif %}{% if os %}| OS | {{ os }} |
{% endif %}{% if region %}| Region | {{ region }} |
{% endif %}{% if user_role %}| User Role | {{ user_role }} |
{% endif %}{% for key, val in feature_flags.items() %}| Feature Flag: {{ key }} | {{ val }} |
{% endfor %}

{% if error_codes %}
## Error Codes
{{ error_codes | join(', ') }}
{% endif %}

{% if stack_trace %}
## Stack Trace
```
{{ stack_trace }}
```
{% endif %}

{% if timeline %}
## Event Timeline
| Timestamp | Level | Event |
|-----------|-------|-------|
{% for ev in timeline %}| {{ ev.timestamp }} | {{ ev.level or '-' }} | {{ ev.event }} |
{% endfor %}
{% endif %}

## Reproduction Steps
{% for step in repro_steps %}{{ loop.index }}. {{ step }}
{% endfor %}

## Root Cause Hypothesis
{{ root_cause }}

## Missing Information
{% if missing_info %}{% for item in missing_info %}- {{ item }}
{% endfor %}{% else %}All critical information is present.{% endif %}
