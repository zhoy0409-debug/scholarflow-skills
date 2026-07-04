# Severity Matrix

Use this matrix to assess the severity of a reported issue.

## Severity Levels

### P0 — Service Down
- **Criteria**: Entire service or critical path is unavailable for all/most users
- **Examples**: Login broken for everyone, data loss, security breach, payment processing down
- **Expected response**: Immediate, all-hands
- **Customer communication**: Proactive status page update, direct outreach within 1 hour

### P1 — Critical Feature Broken (No Workaround)
- **Criteria**: Core feature is broken for a significant user segment, no workaround exists
- **Examples**: Cannot create/save data, export completely broken, API returning 500 for all requests
- **Expected response**: Within 4 hours
- **Customer communication**: Acknowledge within 2 hours, updates every 4 hours

### P2 — Core Feature Broken (Workaround Exists)
- **Criteria**: Important feature is broken but users can work around it
- **Examples**: Export fails but data is accessible via API, UI broken but mobile app works
- **Expected response**: Within 1 business day
- **Customer communication**: Acknowledge within 4 hours, provide workaround

### P3 — Minor Issue
- **Criteria**: Non-critical feature affected, minor inconvenience
- **Examples**: Sorting doesn't work on one column, tooltip shows wrong text, slow but functional
- **Expected response**: Within 1 week
- **Customer communication**: Acknowledge, add to backlog

### P4 — Cosmetic / Enhancement
- **Criteria**: Visual issue or feature request
- **Examples**: Alignment off by a few pixels, color inconsistency, "nice to have" feature
- **Expected response**: Backlog
- **Customer communication**: Thank and log

## Assessment Factors

When determining severity, consider:
1. **Blast radius**: How many users/tenants are affected?
2. **Business impact**: Does it block revenue-generating activities?
3. **Data integrity**: Is data at risk of loss or corruption?
4. **Security**: Is there a security or privacy implication?
5. **Workaround availability**: Can users achieve their goal another way?
6. **Trend**: Is the issue getting worse over time?
