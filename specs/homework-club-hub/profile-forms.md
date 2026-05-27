---
doc_kind: form-specification
status: draft
visibility: public_sample
last_updated: 2026-05-25
team: team-2
---

# Profile Form Specifications: Homework Club Hub

This document defines the data fields required for the Tutor and Parent/Student onboarding flows. These fields are designed to support both manual filtering and the AI-driven pairing engine.

## 1. Tutor Profile Form
**Goal**: Capture academic expertise, cultural identity, and professional background.

| Field Name | Type | Requirement | Purpose |
| :--- | :--- | :--- | :--- |
| Full Name | Text | Required | Identification |
| Email | Email | Required | Communication |
| Location | Text | Required | Proximity/Timezone |
| Primary Subject | Dropdown | Required | Core matching |
| Secondary Subjects | Multi-select | Optional | Broaden matching |
| Education Level | Dropdown | Required | Quality assurance |
| Native Language(s) | Multi-select | Required | Linguistic pairing |
| Cultural Background | Text/Tags | Required | Cultural resonance matching |
| Bio | Text Area | Required | **AI Pairing Source**: Used to analyze teaching style and values |
| Background Check | File/Checkbox | Required | Safety verification |
| Availability | Calendar/Grid | Required | Scheduling |

---

## 2. Parent/Student Profile Form
**Goal**: Capture specific academic gaps and preferred support environments.

| Field Name | Type | Requirement | Purpose |
| :--- | :--- | :--- | :--- |
| Parent Name | Text | Required | Primary contact |
| Contact Phone | Phone | Required | Coordination |
| Student Grade | Dropdown | Required | Level-appropriate matching |
| Target Subject(s) | Multi-select | Required | Core matching |
| Specific Topics | Text Area | Optional | Granular need (e.g., "Calculus limits") |
| Preferred Language | Dropdown | Required | Linguistic pairing |
| Cultural Preference | Text/Tags | Optional | Cultural resonance matching |
| Student Bio | Text Area | Required | **AI Pairing Source**: Used to analyze learning style and barriers |
| Availability | Calendar/Grid | Required | Scheduling |
