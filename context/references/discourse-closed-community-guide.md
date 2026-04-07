# Discourse for Closed/Private Research Communities: Technical Reference

**Status**: Research reference document  
**Date**: April 2026  
**Audience**: Product Owner, Developers (anyone unfamiliar with Discourse)  
**Purpose**: Detailed guide to Discourse capabilities for CLEAgora (closed research communities, invitation-only enrollment, structured discussion phases, participant engagement)

---

## 1. Closed Registration & Invitation-Only Access

### 1.1 Core Settings: Three Modes of Access Control

Discourse provides three independent site settings that control how users can register and access your instance. These can be combined in different ways:

#### **login_required**
- **What it does**: Requires all visitors to be logged in to view any content (topics, categories). Without login, users see only the login page.
- **When to use**: When you want zero public visibility — not even anonymous browsing is allowed.
- **Note**: This is a hard barrier; even search engines cannot index your content.

#### **invite_only**
- **What it does**: Disables the public signup form entirely. New users cannot self-register; they must be invited via email or invited directly by someone with invitation privileges.
- **When to use**: Standard choice for research studies. Allows fine-grained control over recruitment and enrollment.
- **Admin panel**: Settings → Login

#### **must_approve_users**
- **What it does**: Any user who signs up (or redeems an invite) must be manually approved by an admin before they gain full access to the community.
- **When to use**: When you want additional vetting beyond email validation. Allows admins to review and approve each participant.
- **Interaction**: Can be combined with `invite_only`. Users who redeem invites will still need approval if this setting is enabled.
- **Staff bypass**: Invites created by staff (admins/moderators) typically bypass the approval requirement.
- **Admin panel**: Settings → Login

### 1.2 Recommended Configurations for Research

**Scenario 1: Fully Invitation-Only (No Self-Signup)**
```
invite_only: ON
login_required: ON (optional, recommended for extra privacy)
must_approve_users: OFF
```
Result: Only invited users can register. Staff sends invites, users redeem and immediately gain access. Minimal friction.

**Scenario 2: Invitation + Manual Approval (Strict Enrollment)**
```
invite_only: ON
login_required: ON
must_approve_users: ON
```
Result: Even invited users must be approved. Good for pre-screening or screening out dropouts before they can see study materials. Adds friction; use if necessary.

**Scenario 3: Open Signup + Approval (Hybrid)**
```
invite_only: OFF
login_required: ON (optional)
must_approve_users: ON
allow_signup: ON
```
Result: Anyone can attempt signup, but admins must approve. Useful if you're using external recruitment or have a public signup link but want to review everyone.

### 1.3 Email-Based Invitation System

#### **How Email Invitations Work**

1. **Admin/Staff sends invite**: Go to Admin → Users → Send Invite (or bulk upload CSV).
2. **Email is sent** to the invitee's address with a unique invite link. The email is customizable (see Customization).
3. **Invitee clicks link** in their email, is taken to a signup form pre-populated with the email address.
4. **Invitee creates account** (sets password, chooses username) and immediately gains access (unless `must_approve_users` is ON).
5. **Invite is redeemed** and marked as used in the admin panel.

#### **Key Details**

- **Trust Level for Invitations**: By default, users at Trust Level 2 (Members) and above can invite new users. This is configurable.
- **Customization**: The invitation email text and the welcome message can be customized via:
  - Admin → Customize → Email Templates (edit invitation email)
  - Admin → Customize → Text (search "invite" to customize all invite-related text)
  - The email can include redirects to specific topics or categories when the user first joins.

#### **API Endpoint for Invites**

- **Create invite via API**: `POST /invites` (requires API key and appropriate permissions)
- **Bulk create via API**: There is no dedicated bulk endpoint, but you can automate by looping `POST /invites` for each user, or use the CSV bulk import.
- **CSV bulk import**: Go to Admin → Users → Send Invite, upload a CSV with email addresses and optional group assignments. If a user already exists, they are added to the specified groups instead of being invited.

**Example CSV format**:
```
email,groups
participant1@example.com,study-cohort-a,respondents
participant2@example.com,study-cohort-a,respondents
participant3@example.com,study-cohort-b,respondents
```

#### **Invite Expiry & Tokens**

- Invitations have an expiry (default: 30 days, configurable in settings).
- Each invite generates a unique token (e.g., `inviteid12345abcde`).
- If an invite expires, admins can resend it or create a new one.

### 1.4 Email Domain Whitelisting (Optional)

If you want to restrict registration to specific email domains (e.g., corporate or institutional email only):

- **Setting**: `allowed_email_domains` (list of domains, pipe-delimited)
- **How it works**: Only users with email addresses matching the whitelisted domains can sign up or be invited.
- **Example**: Set to `company.com|university.edu` to allow only those domains.
- **Admin panel**: Settings → Email

---

## 2. Groups and Permissions

### 2.1 What are Discourse Groups?

Groups in Discourse are collections of users that can be assigned permissions, be mentioned (@group-name), receive bulk invitations, and be auto-assigned to categories or topics.

#### **Types of Groups**

- **Automatic groups**: Built-in groups (e.g., "trust_level_1", "staff", "moderators") that update automatically based on user properties.
- **Manual groups**: Created by admins, managed by adding/removing users.
- **Group owners**: Can invite users to the group (if allowed), message the group, and see group activity.

### 2.2 Creating and Managing Study-Specific Groups

**Use case**: CLEAgora may run multiple studies in parallel or sequentially. Each study needs:
- A roster of enrolled participants
- Different permission levels (e.g., full access vs. view-only)
- Potential sub-groups (e.g., Study A Cohort 1, Study A Cohort 2)

**How to set up**:

1. **Create a parent group per study**:
   - Go to Admin → Groups → Create New Group
   - Name: `study-a-respondents` (or similar)
   - Set privacy: "Closed" (members can only join by invite/admin action)
   - Configure visibility: "Private" (only members and staff see the group)

2. **Create sub-groups for cohorts or phases** (optional):
   - Name: `study-a-cohort-1`, `study-a-cohort-2`, etc.
   - Make these sub-groups members of the parent group (if you want to manage permissions at the parent level)

3. **Assign users to groups**:
   - Manually: Admin → Groups → [Group] → Add Members
   - Via invite: When you send an invite (CSV bulk import or individual), specify the group(s) to auto-add the user to
   - Via API: `PUT /groups/{group_id}/members` (batch add users)

### 2.3 Group Permissions vs. Category Permissions

**Groups** control:
- Who can be mentioned and messaged
- Who can be bulk-invited to categories/topics
- Access to category discussions (in combination with category settings)
- Admin panel access (e.g., "moderators_group")

**Categories** control:
- Who can see a category
- Who can create, reply to, or edit topics
- Visibility of category contents

**Pattern**: You typically create a group, then assign that group permissions to one or more categories. For example:
- Group `study-a-respondents` has "See + Reply" permission on category `Study A Discussion`
- Group `study-a-respondents` has no access to category `Admin Notes` (only staff can see it)

### 2.4 Group Membership APIs

Discourse provides API endpoints for group management:

- **Add users to group**: `PUT /groups/{group_id}/members.json` with array of user IDs
- **Remove users from group**: `DELETE /groups/{group_id}/members/{user_id}.json`
- **List group members**: `GET /groups/{group_id}/members.json`
- **Create group**: `POST /groups.json`

Example (Python):
```python
import requests

API_KEY = "your_api_key"
API_URL = "https://discourse.example.com"

# Add users to a group
group_id = 123
user_ids = [456, 789, 1011]

response = requests.put(
    f"{API_URL}/groups/{group_id}/members.json",
    headers={"Api-Key": API_KEY},
    json={"user_ids": user_ids}
)
```

---

## 3. Categories, Subcategories, and Discussion Structure

### 3.1 Category Hierarchy

Discourse organizes topics into categories. You can have:
- **Top-level categories**: Main areas (e.g., "Study A Discussion", "Study B Discussion", "General")
- **Subcategories**: Nested under a parent (e.g., "Study A Discussion" > "Phase 1: Awareness", "Phase 2: Evaluation")

**Nesting depth**: Discourse allows subcategories of subcategories, but best practice is to keep it shallow (2–3 levels) for usability.

### 3.2 Recommended Structure for Research

**Example for multi-phase study**:
```
Study A Discussion (parent category)
├── Phase 1: Problem Discovery (subcategory)
├── Phase 2: Solution Exploration (subcategory)
├── Phase 3: Evaluation (subcategory)
└── General Discussion (subcategory, for off-topic within the study)

Study B Discussion (parent category)
├── Phase 1: Background (subcategory)
├── Phase 2: Experience Sharing (subcategory)
└── Housekeeping (subcategory, for admin notes, rescheduling, etc.)
```

**Permissions pattern**:
- All participants in Study A have "See + Reply" on Study A Discussion and all its subcategories
- Only admins/moderators have "See + Reply" on any "Housekeeping" or "Admin Notes" categories

### 3.3 Tags vs. Categories

**Categories** are hierarchical; topics belong to exactly one category.  
**Tags** are flat and cross-cutting; a topic can have multiple tags.

**When to use tags in addition to categories**:
- Tags are useful for cross-study labeling (e.g., all posts about "pricing" across multiple studies tagged `pricing`)
- Stimulus-based discussions: if you show different stimuli (images, articles) to different groups, you can tag topics with the stimulus name
- Metadata: tag posts with complexity level, sentiment, or research code without changing category structure

**Example**:
- Category: `Study A Discussion > Phase 2: Solution Exploration`
- Tags: `stimulus-a`, `high-priority`, `consensus-emerging`

### 3.4 Topic Templates

Topic templates pre-fill the text box when users create a new topic in a category. Useful for research studies:

**How to set up**:
1. Go to Admin → Categories → [Category] → Edit Category
2. Find the "Topic Template" field
3. Enter markdown/text that should appear in every new topic created in that category

**Example for stimulus-based discussion**:
```markdown
## Your Response

Please share your thoughts on the stimulus shown above.

### What stands out to you?
[Your response here]

### Would you use this?
- [ ] Definitely
- [ ] Probably
- [ ] Unsure
- [ ] Probably not
- [ ] Definitely not

### Any additional comments?
[Your response here]
```

**Result**: When a new topic is created, this template appears in the compose box, guiding respondents to answer in a structured way.

### 3.5 Topic Details for Structured Discussion

Beyond the template, topics can have:
- **Title**: Searchable, shown in topic lists
- **Body**: Supports markdown, code blocks, embedded media
- **Tags**: Searchable, cross-cutting metadata
- **Solved plugin** (optional): Mark a reply as "solution" for Q&A-style discussions
- **Pinned topics**: "Pin" a topic in a category to keep it at the top (e.g., study instructions, schedule)

---

## 4. User Onboarding & Welcome Experience

### 4.1 Discobot: Automated New User Tutorial

Discobot is Discourse's built-in bot that automatically sends a welcome private message to every new user. It guides them through basic forum mechanics interactively.

**What Discobot teaches**:
- How to reply to a message
- How to mention someone
- How to quote a post
- Forum navigation basics
- How to edit a post
- How to flag/report content

**Default behavior**: Enabled by default. Every new user gets a PM from `@discobot` with an interactive tutorial.

**Customization**:
- **Edit Discobot's messages**: Admin → Customize → Text → Search for "discobot" to find customizable strings
- **Disable Discobot**: Admin → Plugins → Discobot → Uncheck "Enable"
- **Edit Discobot's name/avatar**: Go to Discobot's user profile (https://discourse.example.com/u/discobot), click Edit, modify username, avatar, etc.

### 4.2 Custom Welcome Message

In addition to (or instead of) Discobot, you can set a custom welcome message that admins send manually or that appears in a pinned welcome topic.

**Option 1: Pinned Welcome Topic**
1. Create a topic in a visible category (e.g., "General")
2. Write your welcome message in markdown
3. Go to topic settings (⋯ menu) → Admin → Pin Topic
4. Choose "Pin in category" and select the category
5. Optionally pin globally ("Pin site-wide") for maximum visibility

**Example welcome topic content**:
```markdown
# Welcome to Study A Research Community

This is a private research community for participants in Study A.

## How This Works

1. **Your role**: Share your genuine thoughts, experiences, and reactions
2. **Discussion format**: We'll explore topics in phases. See the categories on the left.
3. **Timeline**: The study runs for 4 weeks. Check the pinned schedule topic.
4. **Questions**: DM a moderator or post in #questions.

## Guidelines

- Be respectful and curious
- No spam or commercial content
- Confidentiality: what's shared here stays here
- Opt-out anytime: reply to the enrollment email

## Getting Started

1. Introduce yourself in #introductions
2. Read the stimulus in Phase 1
3. Share your initial thoughts in the Phase 1 discussion

Let's begin!
```

### 4.3 Onboarding Banner Plugin

For more sophisticated onboarding, Discourse has an "Onboarding Banner" plugin that displays a custom banner at the top of the site until users dismiss it.

**How to use**:
1. Admin → Plugins → Onboarding Banner
2. Create a topic to act as the banner content (can include links, instructions, etc.)
3. Configure the plugin to display that topic
4. Users see it on first visit, can dismiss, and it doesn't re-appear

### 4.4 Custom Onboarding Sequence (Advanced)

For CLEAgora, you may want a more custom flow:
1. New user joins → assigned to group → automatically added to a "welcome" category with structured onboarding topics
2. Onboarding topics use topic templates and pinned responses that explain the study flow
3. Use the automation of group/category assignment (via invite CSV) to route users appropriately

---

## 5. Notifications & Engagement

### 5.1 Email Notification Types

Discourse sends email notifications for:
- **Direct replies**: Someone replies to a post you made
- **Quotes**: Someone quotes you
- **Mentions**: Someone @mentions you
- **Invitations**: You're invited to join or to a private message
- **Messages**: Someone sends you a private message
- **Category updates**: (If subscribed) New topics in a watched category
- **Activity summaries / Digests**: Periodic summaries of popular topics (for inactive users)
- **Topic notifications**: (If watching a topic) Activity in that topic

### 5.2 User-Level Notification Settings

Each user can configure their email notification preferences:
1. User profile → Preferences → Email
2. Options include:
   - "Email me when someone replies to my post" → Always / Only when away / Never
   - "Email me when someone quotes me" → Always / Only when away / Never
   - "Email me when someone mentions me" → Always / Only when away / Never
   - "Email me when someone sends me a private message" → Always / Only when away / Never
   - Receive mailing list mode → Yes / No (receive every post as an email)
   - Receive digest emails → Yes / No (receive summary of popular topics when inactive)

### 5.3 Admin Configuration of Default Notifications

Admins can set default notification settings for all new users:

**Settings → Notifications**:
- `digest_email_enabled`: Default whether digest emails are sent
- `digest_email_interval`: How often (daily, weekly, etc.)
- `notifications_default_on_anonymous`: Notifications for non-logged-in users
- `digest_email_html_template`: (Advanced) Customize digest email HTML

**Use for research**: You might disable digest emails by default to avoid overwhelming participants, or enable them to encourage re-engagement if users go inactive.

### 5.4 Activity Summary (Digest) Emails

Activity summary emails are sent to inactive users (haven't visited in X days) with a summary of popular topics, trending tags, and new topics in their watched categories.

**Admin settings**:
- `suppress_digest_email_after_days`: Don't send digests if user hasn't visited in X days (e.g., 365)
- `digest_email_interval`: How often to send (daily, weekly, monthly)
- `digest_min_excerpt_length`: How much of each topic to include

**Use case**: If you want to keep participants engaged, enable digest emails to remind them of ongoing discussions. If you want to minimize notification fatigue, disable or reduce frequency.

### 5.5 @Mentions and Pings

When someone @mentions another user (e.g., `@john`), that user receives:
- An in-forum notification badge
- An email notification (configurable per user)

**Group mentions**: You can mention a group by name (e.g., `@study-a-respondents`) to notify all members.

**Use case**: Researchers/moderators can @mention a specific group to notify them of new stimulus, phase transitions, or important updates.

### 5.6 Watching & Tracking Topics/Categories

Users can set notification levels per topic or category:
- **Watching**: Get notified of all activity (in-forum + email)
- **Tracking**: Get notified of new replies (in-forum + email)
- **Normal**: Notified only if mentioned or replied to
- **Muted**: No notifications (but still can read)

**Admin can set defaults**: Go to User Preferences → Notifications and set defaults for new users in your study.

### 5.7 Mailing List Mode (Advanced)

If `mailing_list_mode` is enabled by admin, users can opt into receiving every post as an individual email (like an old-school mailing list). 

**Use case**: Some researchers prefer email-first workflows. You can enable mailing list mode and let participants opt in if they want email-only engagement.

---

## 6. Running Multiple Studies on One Instance

### 6.1 Multi-Study Architecture

You can run multiple research studies on a single Discourse instance by using groups and categories for isolation.

**Pattern**:
```
Instance: CLEAgora-research.example.com
├── Study A (category tree + group)
├── Study B (category tree + group)
├── Study C (category tree + group)
└── Admin/Meta (private category for researchers only)
```

### 6.2 Category-Based Isolation

1. **Create a parent category per study**: `Study A`, `Study B`, `Study C`
2. **Set category permissions** so that Study A group can only see Study A categories, etc.
3. **Use subcategories** for phases, topics, etc. within each study

**Example permission setup**:

| Category | Group | Permission | Notes |
|----------|-------|-----------|-------|
| Study A Discussion | study-a-respondents | See + Reply | Participants |
| Study A Discussion | staff | See + Reply + Edit | Mods can edit/manage |
| Study B Discussion | study-b-respondents | See + Reply | Participants |
| Study B Discussion | staff | See + Reply + Edit | Mods can edit/manage |
| Admin Notes | staff | See + Reply | Only researchers |

**Result**: Study A participants can only see Study A categories. They cannot browse Study B. Staff can see everything.

### 6.3 Potential Issues & Mitigation

**Issue 1: Participant confusion**  
If you have hundreds of category hierarchies, the sidebar becomes overwhelming.

*Mitigation*: 
- Use clear naming conventions (`study-a-`, `study-b-`)
- Hide non-relevant categories from users (via permissions)
- Use the top-level category as a "hub" with links to active studies

**Issue 2: Cross-contamination in search**  
If Study A and Study B both have a category named "Phase 1", search can be ambiguous.

*Mitigation*: 
- Use unique names per study (`Study A - Phase 1`)
- Use tags to label by study (tag: `study-a`, `study-b`)

**Issue 3: Admin complexity**  
Managing groups and category permissions for 10+ concurrent studies gets complex.

*Mitigation*:
- Document the permission matrix in a spreadsheet or in your backlog
- Use the API to automate user/group assignment (see section 2.4)
- Consider creating a custom Discourse plugin if you need very complex conditional logic

### 6.4 Per-Category Isolation Feature Request

**Note**: There's a Discourse Meta discussion about "per-category isolation" that suggests a plugin or feature for stronger isolation (preventing admins from seeing into certain categories without explicit permission). As of February 2025, this is not a core feature, but may be available via third-party plugins or custom development.

If you need true admin-proof isolation (admins cannot accidentally leak Study A data to Study B), consult with the Discourse community or consider a custom plugin.

---

## 7. Practical Implementation: Phase-Based Study Structure

### 7.1 Example: A 4-Week Study with 3 Phases

**Structure**:
```
Study A - Healthcare Futures

├── Getting Started (parent category)
│   ├── Welcome & Logistics (pinned topic)
│   ├── Meet the Team (introductions)
│   └── FAQ (wiki post)
│
├── Phase 1: Problem Discovery (subcategory)
│   ├── [Topic Template: Share your current experience]
│   ├── [Pinned: Stimulus - article on future of healthcare]
│   └── [Auto-tagged: phase-1]
│
├── Phase 2: Solution Exploration (subcategory)
│   ├── [Topic Template: What's your initial reaction?]
│   ├── [Pinned: Stimulus - 3 possible scenarios]
│   └── [Auto-tagged: phase-2]
│
├── Phase 3: Evaluation & Synthesis (subcategory)
│   ├── [Topic Template: Which direction do you prefer?]
│   ├── [Pinned: Stimulus - summary of community insights]
│   └── [Auto-tagged: phase-3]
│
└── Housekeeping (private, staff only)
    ├── Research Notes (wiki post, for researcher coding/analysis)
    ├── Schedule & Reminders (coordinator notes)
    └── Data Export Log (audit trail)
```

### 7.2 User Enrollment Flow

1. **Researcher** creates a CSV with participant emails:
   ```
   email,groups
   alice@example.com,study-a-respondents,healthcare-futures-2026
   bob@example.com,study-a-respondents,healthcare-futures-2026
   ```

2. **Admin uploads CSV** via Admin → Users → Send Invite
   - Each email gets an invitation
   - Upon signup, user is auto-added to `study-a-respondents` and `healthcare-futures-2026` groups

3. **User receives email**, clicks link, creates account, is redirected to Study A homepage

4. **User sees only Study A categories** (permissions enforcement)

5. **User starts in "Getting Started"**, reads welcome, introduces themselves

6. **After 1 week**, admin pins a new stimulus in Phase 1, mentions `@study-a-respondents` in a post → everyone gets notified

7. **Participants discuss** in Phase 1 topics, reply to each other, use the provided topic template

8. **After 2 weeks**, admin transitions to Phase 2: archives Phase 1 (makes read-only if desired), pins stimulus 2, creates discussion topics

### 7.3 Researcher Data Access & Analysis

**Raw data export**:
- Admin → Tools → Export → "Export user list", "Export topics and posts" (CSV/JSON)

**In-forum coding** (lightweight):
- Use private wiki posts in the "Research Notes" category
- Researchers (staff) can create code summaries, themes, quotes
- Reference topics by link

**Advanced analysis** (via extraction pipeline):
- Use the Discourse API to fetch all posts from a study: `GET /category/{id}/latest.json`, paginate to fetch all
- Or use `GET /search.json?q=category:study-a-discussion` to search
- Extract metadata: topic title, post content, author, timestamp, post number
- Pipeline enriches and structures for analysis tools (Arcade, etc.)

---

## 8. API Quick Reference

### 8.1 Key Endpoints for CLEAgora

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/invites.json` | POST | Create a single invite |
| `/groups/{id}/members.json` | PUT | Add users to a group (bulk) |
| `/users.json` | POST | Create a user account (if not using invites) |
| `/categories.json` | GET | List all categories |
| `/categories/{id}.json` | GET | Get category details and permissions |
| `/posts.json` | GET | Search/list posts |
| `/search.json` | GET | Full-text search (e.g., `q=category:study-a`) |
| `/latest.json` | GET | List latest topics across all categories |
| `/c/{category_id}/latest.json` | GET | Latest topics in a specific category |
| `/admin/users.json` | GET | List users (admin only) |
| `/admin/users/{id}.json` | GET | Get user details (admin only) |
| `/admin/groups.json` | GET | List groups (admin only) |

### 8.2 Example: Fetch All Posts from a Study

```python
import requests

DISCOURSE_URL = "https://discourse.example.com"
API_KEY = "your_api_key"

# Search for all posts in "Study A Discussion" category
def fetch_study_posts(study_category_id):
    posts = []
    page = 0
    while True:
        response = requests.get(
            f"{DISCOURSE_URL}/search.json",
            headers={"Api-Key": API_KEY},
            params={
                "q": f"category:{study_category_id}",
                "page": page
            }
        )
        data = response.json()
        posts.extend(data.get("posts", []))
        
        if not data.get("more_full_page_results"):
            break
        page += 1
    
    return posts

study_posts = fetch_study_posts(1)  # Replace 1 with actual category ID
for post in study_posts:
    print(f"Post #{post['id']}: {post['raw'][:100]}...")
```

### 8.3 Admin API Key Setup

1. Go to Admin → API → API Keys
2. Create a new key, assign it to a user (or "All users" for full access)
3. Copy the key
4. Use in HTTP header: `Api-Key: your_key_here`

---

## 9. Security & Privacy Considerations

### 9.1 Data Encryption

- **Discourse in transit**: Use HTTPS/TLS (standard setup)
- **At rest**: Discourse stores posts, PMs, and user data in a database (typically PostgreSQL). Encryption at rest depends on your hosting/infrastructure setup.
- **Private messages**: PMs between users are stored as topics and are readable by admins. If you need true end-to-end encryption, Discourse doesn't provide this natively; you'd need a custom plugin.

### 9.2 Admin Access & Audit

- **Admins can see everything**: Including private messages, user emails, group memberships, IP addresses.
- **Audit logs**: Admin → Logs → Staff Action Logs (tracks deletions, edits, group changes, etc.)
- **PII**: Discourse stores usernames, email addresses, and IP addresses. Consider GDPR/privacy implications.

### 9.3 Access Control Best Practices

1. **Limit admin/staff access**: Don't make everyone an admin. Use moderators (limited privileges) when possible.
2. **Document permissions**: Keep a matrix of who can see what (as mentioned in 6.4).
3. **Test isolation**: Periodically verify that Study A members can't see Study B content (try viewing as a non-admin in Study A).
4. **Audit group changes**: Keep a log of when users are added to or removed from groups (API calls can be logged).

### 9.4 Data Retention & Deletion

- **User account deletion**: Admin → Users → [User] → Delete. This removes the user but may leave posts/PMs intact (depending on settings).
- **Post deletion**: Individual posts can be deleted or permanently destroyed.
- **Topic deletion**: Can be soft-deleted (hidden) or permanently destroyed.
- **Setting**: `delete_all_posts_and_topics_allowed_max_age_days` controls if users can nuke their own content.

For research data retention, decide upfront:
- How long do you keep data after study completion?
- How do you comply with GDPR right to deletion?
- Do you archive anonymized transcripts separately?

---

## 10. Troubleshooting & Common Issues

### 10.1 Users Can't See Categories They Should

**Check**:
1. Is the user in the right group? Admin → Groups → [Group] → Members
2. Are category permissions set correctly? Admin → Categories → [Category] → Security
3. Is `login_required` on? If so, users must be logged in.

**Fix**: Verify group membership and category permissions match your intent.

### 10.2 Invites Aren't Being Sent

**Check**:
1. Is email configured correctly? Admin → Email → Check "Mail" and SMTP settings
2. Are emails bouncing? Check your mail server logs
3. Is the invitee's email on a blocklist? Admin → Settings → Email → blocked_email_domains

**Fix**: Test with a known-good email address, check mail server logs, verify SMTP credentials.

### 10.3 New Users See Other Studies' Categories

**Check**:
1. Did you forget to restrict category permissions? Admin → Categories → [Category] → Security should list only the intended group
2. Is "everyone" included in category permissions? (Default: new categories visible to "Everyone")

**Fix**: Explicitly set category permissions to the study group only; remove "everyone" if it's there.

### 10.4 Performance: Many Topics Slow to Load

**Mitigation**:
1. Archive old topics/categories (make read-only)
2. Use pagination (Discourse does this by default)
3. Optimize database (contact your hosting provider)
4. Consider horizontal scaling if Discourse instance is very active

---

## 11. Resources & Documentation

### Official Documentation
- [Discourse Meta (meta.discourse.org)](https://meta.discourse.org): Community forum, best practices, troubleshooting
- [Discourse API Docs (docs.discourse.org)](https://docs.discourse.org/): Official API reference
- [Discourse Blog (blog.discourse.org)](https://blog.discourse.org/): Announcements, features, guides

### Key Meta Topics Referenced in This Guide
- [Configuring Discourse for a Closed or Private Community](https://meta.discourse.org/t/configuring-discourse-for-a-closed-or-private-community/27014)
- [Understanding Groups and Category Permissions](https://meta.discourse.org/t/understanding-groups-and-category-permissions/87678)
- [Creating and Using Invites](https://meta.discourse.org/t/creating-and-using-invites/263314)
- [Using Topic Templates for Categories](https://meta.discourse.org/t/using-topic-templates-for-categories/38295)
- [Discobot: Who is Discobot?](https://meta.discourse.org/t/who-is-discobot/69003)
- [Understanding Email Notification Settings](https://meta.discourse.org/t/understanding-email-notification-settings/44721)
- [Configuring How Users Can Create and Send Invites](https://meta.discourse.org/t/configuring-how-users-can-create-and-send-invites-for-others-to-join-your-community/124096)

### Third-Party Tools & Integrations
- **Zapier**: Automate invite sending based on external events
- **CSV bulk import**: Built-in Admin UI
- **Data Explorer plugin**: Write SQL queries to extract custom data (e.g., "all posts by study-a-respondents in phase 2")
- **Webhooks**: Trigger external actions on Discourse events (new post, new user, etc.)

---

## 12. Summary: CLEAgora Setup Checklist

- [ ] **Closed registration**: Set `invite_only: ON`, consider `login_required: ON`
- [ ] **Create study groups**: One per study (e.g., `study-a-respondents`)
- [ ] **Create category structure**: Parent category per study, subcategories per phase
- [ ] **Set category permissions**: Restrict to study groups (exclude "everyone")
- [ ] **Create topic templates**: Guide responses for stimulus/phase discussions
- [ ] **Customize welcome**: Pinned welcome topic + Discobot customization
- [ ] **Prepare invite CSV**: Email + group assignments per participant
- [ ] **Test**: Try inviting a test user, verify they see only their study's categories
- [ ] **Configure notifications**: Set defaults (digest, mention, reply notifications)
- [ ] **Plan API automation**: Script for bulk user creation, data export, group assignment
- [ ] **Document permissions**: Spreadsheet or table of who can see what
- [ ] **Set up research workflow**: How will you access, code, and export study data?
- [ ] **Test isolation**: As a Study A user, verify you can't browse Study B

---

**End of guide.**
