# Bug Severity Rubric

This document defines how the Bug Report Classifier AI determines the severity of a reported bug. The model matches keywords and context from the bug description against the rules below.

---

## Critical (P0)

**Definition:** System is down, data is lost or corrupted, security is breached, or a core feature is completely broken for ALL users. No workaround exists.

**Response Time:** Immediate — within 1 hour

**Examples:**
- App crashes on launch for all users
- Production database is not responding
- User passwords or personal data exposed
- Payment system charging users incorrectly
- Entire site/service is unreachable

**Trigger Keywords:**
crash, down, outage, data loss, security breach, vulnerability, production down, server down, not working at all, all users affected, payment failed, money lost, cannot login, database down, emergency, urgent, broken completely, total failure, hacked, unauthorized access, data leak, corruption, unresponsive, exploit

**Assign To:** The primary contact of the matched area + immediately escalate to Engineering Manager and CTO.

---

## High (P1)

**Definition:** A major feature is broken or severely degraded. Many users are affected. A workaround may exist but is not practical for regular use.

**Response Time:** Within 4 hours

**Examples:**
- Search returns no results for any query
- User registration/signup flow is broken
- Push notifications not delivering to any device
- API response time exceeds 10 seconds
- File upload fails consistently

**Trigger Keywords:**
broken, not working, fails, error, cannot, unable to, blocked, major, significant, many users, regression, performance degradation, slow response, timeout, 500 error, internal server error, api failure, registration broken, login issue, notification failure, data not saving, sync failure, import failed, export broken

**Assign To:** The primary contact of the matched area + notify the team lead.

---

## Medium (P2)

**Definition:** A feature is partially broken or behaves incorrectly in certain conditions. Some users are affected. A reasonable workaround exists.

**Response Time:** Within 24 hours

**Examples:**
- Dark mode text color wrong on one specific page
- Sorting doesn't work on a particular column
- Form validation shows a misleading error message
- Pagination skips a page
- Promo code applies wrong discount amount

**Trigger Keywords:**
incorrect, wrong, misaligned, display issue, sometimes, intermittent, workaround, partial, specific page, one user, some users, minor bug, visual, formatting, alignment, not showing correctly, inconsistent, edge case, pagination, sorting issue, filter not working, wrong data, wrong color, wrong text, truncated, overlapping, responsive issue, delayed

**Assign To:** The primary contact of the matched area.

---

## Low (P3)

**Definition:** Cosmetic issue, typo, minor visual glitch, or a "nice to have" improvement. Does not affect functionality.

**Response Time:** Within 1 week (or next sprint)

**Examples:**
- Typo on a page
- Button hover color slightly off from design spec
- Console deprecation warning
- Tooltip appears in wrong position
- 1px border visible on app icon

**Trigger Keywords:**
typo, spelling, cosmetic, minor, nice to have, enhancement, suggestion, improvement, polish, hover, tooltip, placeholder, deprecation, warning, console log, pixel, spacing, padding, margin, font size, color shade, icon, animation, transition, scroll behavior, copy change, text update, label wrong

**Assign To:** The primary contact of the matched area (add to backlog).

---

## Decision Flow

```
Bug Report Received
       │
       ▼
┌──────────────────┐
│ Does it match any │
│ CRITICAL keywords │──── Yes ──→ Severity = Critical (P0)
│ or patterns?      │
└───────┬──────────┘
        │ No
        ▼
┌──────────────────┐
│ Does it match any │
│ HIGH keywords or  │──── Yes ──→ Severity = High (P1)
│ patterns?         │
└───────┬──────────┘
        │ No
        ▼
┌──────────────────┐
│ Does it match any │
│ MEDIUM keywords   │──── Yes ──→ Severity = Medium (P2)
│ or patterns?      │
└───────┬──────────┘
        │ No
        ▼
Severity = Low (P3)
```

---

## Area Detection Flow

```
Bug Description Text
       │
       ▼
┌────────────────────────┐
│ TF-IDF Vectorize the   │
│ description + all area  │
│ keywords                │
└───────┬────────────────┘
        │
        ▼
┌────────────────────────┐
│ Cosine Similarity:      │
│ Compare description     │
│ vector against each     │
│ area's keyword vector   │
└───────┬────────────────┘
        │
        ▼
  Highest scoring area
  = Affected Area
        │
        ▼
  Look up primary_contact
  from team.json
  = Suggested Assignee
```

---

## Notes

- If multiple areas have similar scores (within 10% of each other), the classifier should list all matching areas.
- Critical and High bugs should always trigger a Slack notification to the assigned person.
- The classifier uses TF-IDF + cosine similarity — no cloud LLM APIs are used.
- To improve accuracy, add more keywords to `team.json` for each area.
