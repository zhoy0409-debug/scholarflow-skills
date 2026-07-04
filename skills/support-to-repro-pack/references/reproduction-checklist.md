# Reproduction Checklist

When analyzing a support ticket, verify that the following information is present. Mark missing items and generate follow-up questions.

## Critical (must have to reproduce)

- [ ] **Environment**: production / staging / development / sandbox
- [ ] **Application version**: version number or build ID
- [ ] **Error message or symptom**: exact error text, HTTP status code, or visible behavior
- [ ] **Steps to trigger**: what the user did before the error occurred

## Important (significantly helps reproduction)

- [ ] **Browser / Client**: browser name + version, or client app version
- [ ] **Operating System**: OS name + version
- [ ] **User role / permissions**: admin, member, viewer, etc.
- [ ] **Account type**: free, pro, enterprise, trial
- [ ] **Timestamp**: when the issue first occurred
- [ ] **Frequency**: always reproducible, intermittent, one-time
- [ ] **Affected scope**: single user, single tenant, all users, specific region

## Nice to Have (accelerates debugging)

- [ ] **Network conditions**: VPN, proxy, corporate firewall
- [ ] **Feature flags**: any experimental features enabled
- [ ] **Region / data center**: which region the request was routed to
- [ ] **Related recent changes**: recent deployments, config changes, migrations
- [ ] **Workaround**: has the user found any way to work around the issue
- [ ] **Screenshots / screen recording**: visual evidence of the issue
- [ ] **Console logs / network tab**: browser developer tools output
- [ ] **Server logs**: application logs around the time of the incident

## Follow-up Question Templates

For each missing critical/important item, use these templates:

- Environment: "Could you confirm which environment this occurred in? (production, staging, etc.)"
- Version: "What version of the application are you using? You can find this in Settings > About."
- Steps: "Could you walk us through the exact steps you took before seeing this error?"
- Browser: "Which browser and version are you using? (e.g., Chrome 122, Firefox 124)"
- Frequency: "Does this happen every time you try, or only sometimes?"
- Scope: "Are other users in your organization experiencing the same issue?"
