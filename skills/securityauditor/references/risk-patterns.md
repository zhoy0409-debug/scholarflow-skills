# Risk Patterns

Use this reference when explaining or tuning scanner findings.

## Severity

- `info`: contextual signal.
- `low`: minor review signal.
- `medium`: risky pattern that should be reviewed before installation or publication.
- `high`: strong risk signal that should usually block trust until resolved.
- `critical`: credential or destructive behavior signal that needs immediate review.

## Categories

- `prompt_injection`: instructions that attempt to override higher-priority guidance.
- `credential_access`: reads or transmits environment variables, tokens, keys, or credential files.
- `network_exfiltration`: references network endpoints outside documentation-safe placeholders.
- `destructive_file_operation`: broad delete or overwrite behavior.
- `shell_risk`: shell execution patterns with high review risk.
- `dependency_install_risk`: runtime package installation without clear setup boundaries.
- `misleading_metadata`: skill metadata that omits risky sibling behavior.
- `permission_expansion`: attempts to weaken or bypass permission controls.
- `hidden_behavior`: concealment, obfuscation, or hidden persistence signals.
- `unsafe_hook`: install-time or lifecycle hooks that run without explicit review.

## Documentation-Safe Placeholders

Prefer placeholders such as `example.com`, `example.org`, `example.net`, `user@example.com`, `sk-EXAMPLE-DO-NOT-USE`, `192.0.2.10`, and `203.0.113.20`.

Do not include real credentials, production hostnames, customer data, or private repository content in examples.
