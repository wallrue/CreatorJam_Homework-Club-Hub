---
doc_kind: vision-spec
status: draft
visibility: public_sample
last_updated: 2026-05-26
team: team-2
---

# Vision Spec: Homework Club Hub

## 1. Context and Problem Statement
Access to quality academic support is currently gated by a significant financial barrier. Many parents cannot afford private tutoring, leaving students to struggle in critical subjects—particularly the sciences—without the necessary guidance to succeed. 

Beyond financial constraints, language and cultural barriers often complicate the learning process. Students may struggle to connect with tutors who do not share their linguistic background or cultural context, which can hinder trust and academic progress.

Simultaneously, there is a latent pool of skilled volunteers who are eager to support students but lack a structured way to find those in need or coordinate their help. The Homework Club Hub exists to bridge this gap, removing the financial and linguistic obstacles for families and providing a way to pair students with volunteers of the same culture and language. By adding professional and social incentives, the Hub turns volunteering from a simple "favor" into a career-building opportunity, creating a sustainable, community-driven learning environment.

## 2. North Star Vision
A digital platform connecting volunteer tutors with students who need academic support, with scheduling, progress tracking, and subject matching.

## 3. Design Principles
- **Cultural and Linguistic Resonance**: Learning is most effective when students feel seen and understood. The platform prioritizes pairing students with tutors who share their language and cultural background to foster trust and psychological safety.
- **Radical Accessibility**: Financial status should never be a barrier to academic success. The platform must remain free for students and easy to access regardless of the device they use.
- **Community-Driven Empowerment**: The hub is not just a tool, but a bridge. It empowers volunteers by providing a clear, structured way to give back to their own community.
- **Trust and Safety**: To ensure a safe environment for students and volunteers, the platform prioritizes safety through simple vetting and clear boundaries.

## 4. Current-State Assumptions and Unknowns

### Assumptions
- **Volunteer Availability**: There is a sufficient number of qualified volunteers skilled in sciences who are willing to volunteer their time.
- **Student Demand**: The primary barriers for students are financial and coordination-based, and they are eager to use a digital hub.
- **Cultural Pairing Value**: Pairing by culture/language significantly increases the student's learning outcome and comfort level.
- **Incentive Value**: Professional visibility (profile links, publicity on Indigenomics platforms) and community rewards (workshops, retreats) are strong enough drivers to sustain long-term volunteer commitment.

### Unknowns
- **Vetting Process**: How to verify academic expertise and ensure student safety without creating a prohibitive barrier for volunteers.
- **Scheduling Conflict**: Whether a simple scheduling tool is sufficient or if complex school-schedule overlaps require more advanced logic.
- **Engagement Strategy**: How to best structure the incentive system (e.g., LinkedIn-ready profile links, Indigenomics social features) to ensure tutor retention.
- **Technology Access**: Whether the students most in need have the necessary devices and internet access to use a digital hub.
- **Partnership Logistics**: How to coordinate and fund the workshops and retreats mentioned as incentives.

## 5. Research Notes or Evidence
- **First-Hand Field Observation**: Through experience as a science volunteer at a neighborhood house, it has been directly observed that the demand for academic support far outweighs the available supply of tutors.
- **Publicity Gap**: There is a noted lack of visibility and outreach regarding the need for volunteers, meaning many potentially qualified helpers are unaware that students in their own neighborhoods are struggling.
- **Financial Gap Observation**: The widespread inability of low-income families to afford private tutoring, creating a "learning gap" in high-stakes subjects like science.
- **Cultural/Linguistic Friction**: The observation that students struggle more when there is a cultural or linguistic mismatch with their educator, hindering trust and communication.
- **Professional Incentive Trend**: The growing value of "social proof" and "portfolio building" (e.g., LinkedIn profiles, community recognition) as a driver for high-skill volunteering.

## 6. Proposed Architecture or Operating Model

### User Roles
- **Students/Parents**: Parents sign up their children, specifying the subjects needed and cultural/linguistic preferences.
- **Volunteer Tutors**: Professionals or students who create a profile, list their expertise, and undergo a mandatory criminal background check for safety.
- **Admin/Facilitator**: Oversees the vetting process and manages high-level platform health.

### Data Schema (Foundation Layer)
- **Users Table**: `user_id (PK)`, `full_name`, `email`, `password_hash`, `role (student_parent/volunteer/admin)`, `subject`, `language`, `created_at`.

### Key Flows & State Map (Logic Layer)
- **User Onboarding**: Signup $\rightarrow$ Enter Full Name, Email, Password, Role, Subject, and Language $\rightarrow$ Account Created.
- **Tutor Search**: Enter Subject/Language Filter $\rightarrow$ API returns matching volunteers from Users table.
- **AI Pairing**: Logged-in user requests match $\rightarrow$ System calculates score based on `subject` (weight 2) and `language` (weight 1) $\rightarrow$ Returns best-scoring volunteer with reasoning.
- **Profile Viewing**: User enters a name $\rightarrow$ System fetches public profile details for that user.

### API Endpoint Map (Bridge Layer)
- `GET /`: Home page.
- `GET /login`: Login page.
- `GET /join`: Signup page.
- `GET /profile`: Profile view page (supports `?name=...` for public viewing).
- `GET /search`: Tutor search page.
- `POST /api/join`: Creates a new user in the `users` table.
- `POST /api/login`: Authenticates user via email/password; sets session.
- `GET /api/me`: Retrieves current logged-in user's details.
- `GET /api/profile`: Retrieves profile details by name.
- `GET /api/tutors`: Returns filtered list of volunteers based on `subject` and `language` query params.
- `GET /api/ai-match`: Returns the best-matching tutor for the current user based on subject/language overlap.

### Core Features
- **Role-Based Access**: Support for `student_parent` and `volunteer` roles.
- **Subject & Language Matching**: Tutors are searchable and matchable via specific academic subjects and linguistic backgrounds.
- **Simplified AI Match**: A scoring-based recommendation engine that suggests tutors based on a priority of (Subject + Language) > (Subject) > (Language).
- **Public Profile Discovery**: Ability to view other members' basic profiles by name.

## 7. Multi-Phase Roadmap

### Phase 1: The Jam Prototype (Core Value)
- **Basic Profiles**: Simple signup for Tutors (expertise, culture, profile picture) and Parents (student needs). Functional profile update capabilities for volunteers.
- **Manual Matching**: Filterable search by subject and cultural background.
- **AI Pairing Mock-up**: A demonstration of how the AI analyzes bios to suggest compatible pairings.
- **Basic Booking**: A request system to initiate a session.
- **Initial Feedback**: Simple star ratings or "Thank You" notes from students.

### Phase 2: MVP (Functional Tool)
- **Automated Vetting**: Integration with a background check service and "Verified" badges.
- **Full AI Engine**: A working LLM-based matching system that pairs based on bio sentiment and shared values.
- **Career Portfolio**: Generation of shareable public links showcasing a tutor's verified hours, impact analytics (e.g., student progress metrics), and student reviews.
- **Detailed Reviews**: Written testimonials from parents and students to build tutor credibility.
- **Progress Tracking**: Simple logging for session outcomes and academic growth.

### Phase 3: Long-term Scale (Community Ecosystem)
- **Community Events**: Coordination of physical workshops and retreats for tutors and students.
- **Institutional Partnerships**: Direct referral pipelines with local schools and neighborhood houses.
- **Indigenomics Integration**: Full publicity integration with Indigenomics websites and socials to attract a wider pool of volunteers.

## 8. Acceptance Criteria
To consider the Jam prototype successful, the following must be demonstrated:
- **Profile Creation**: A user can successfully create a profile, selecting their role (Student/Parent, Volunteer, or Admin) and specifying academic expertise, cultural/linguistic tags (expanded language options), and a profile picture during signup.
- **Profile Management**: A volunteer can successfully update their availability, expertise, and profile information without needing to recreate their account.
- **Student Request**: A parent can submit a request specifying the subject needed and preferred cultural background.
- **Matching Logic**: The system can successfully filter and return a list of tutors that match the specified subject and culture.
- **AI Pairing Demo**: The system provides a "Suggested Match" based on an analysis of the bios provided by both parties (demonstrating the potential for bio-based pairing).
- **Feedback Loop**: A student or parent can leave a basic rating or a "Thank You" note after a session.

## 9. Risks, Constraints, and Mitigations
- **Risk: Safety and Trust** — Connecting volunteers with students carries inherent risks.
    - *Mitigation*: Mandatory criminal background checks, a "Verified" badge system, and clear community guidelines.
- **Risk: Volunteer Burnout** — High demand for tutors may lead to burnout.
    - *Mitigation*: Implementation of professional incentives (career portfolios) and community-focused rewards (retreats, workshops) to maintain motivation.
- **Risk: Digital Divide** — The students most in need may lack reliable internet or devices.
    - *Mitigation*: Designing a lightweight, mobile-first interface and exploring partnerships with neighborhood houses for physical access points.

## 10. Dependencies and Open Questions
- **Dependencies**: 
    - A reliable third-party service or API for criminal background checks.
    - Collaboration with the Indigenomics team for publicity and website integration.
- **Open Questions**:
    - How do we effectively handle disputes or poor-quality tutoring experiences?
    - What is the optimal balance between a strict vetting process and a low barrier to entry for volunteers?

## 11. First 3-5 Next Actions
1. **Form Design**: Draft the specific fields for Tutor and Parent profiles (including bio and cultural tags).
2. **AI Logic Mapping**: Define the prompt and criteria for the AI pairing feature to analyze bios effectively.
3. **Prototype Mock-ups**: Create wireframes for the Tutor Search and "Suggested Match" screens.
4. **Validation**: Run the `validate-frontmatter.py` script to ensure the spec is technically ready for the kit.
