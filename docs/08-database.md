# SlipSmart AI – Database Design

## Purpose

This document defines the initial PostgreSQL database design for SlipSmart AI.

The database must support matches, predictions, generated slips, slip items, users, and future analytics.

---

# Database Choice

SlipSmart AI will use **PostgreSQL**.

## Reason

The application has highly relational data:

* Users create slips.
* Slips contain multiple slip items.
* Slip items reference predictions.
* Predictions belong to matches.
* Matches belong to competitions.
* Matches contain teams.

PostgreSQL is a better fit than a document database because the system will require joins, filtering, reporting, and reliable transactions.

---

# Entity Relationship Diagram

![ER Diagram](images/database/er-diagram.png)

The diagram above illustrates the relationships between the core entities of the application.
# Core Tables

## users

Stores registered users.

```text
id
email
password_hash
full_name
created_at
updated_at
```

---

## competitions

Stores leagues and competitions.

```text
id
name
country
sport
created_at
updated_at
```

Example:

```text
Premier League
Bundesliga
Champions League
La Liga
```

---

## teams

Stores teams.

```text
id
name
short_name
country
sport
created_at
updated_at
```

---

## matches

Stores upcoming and completed matches.

```text
id
competition_id
home_team_id
away_team_id
kickoff_time
status
home_score
away_score
created_at
updated_at
```

Status examples:

```text
scheduled
live
finished
cancelled
postponed
```

---

## predictions

Stores prediction outputs for each match and market.

```text
id
match_id
market
pick
probability
odds
risk_level
model_version
created_at
updated_at
```

Example markets:

```text
1X2
BTTS
Over 2.5
Draw No Bet
Correct Score
```

---

## slips

Stores generated betting slips.

```text
id
user_id
budget
strategy
number_of_slips
max_overlap
created_at
updated_at
```

For MVP without login, `user_id` can be nullable.

---

## slip_items

Stores individual picks inside each generated slip.

```text
id
slip_id
prediction_id
stake
total_odds
potential_return
average_probability
risk_score
created_at
updated_at
```

Note:

In a later version, we may split `slips` and `generated_slip_groups` more clearly. For MVP, this structure is enough.

---

## ai_explanations

Stores AI-generated explanations for generated slips.

```text
id
slip_id
explanation
model_provider
model_name
created_at
```

---

# Relationships

```text
competitions 1 → many matches

teams 1 → many matches as home_team

teams 1 → many matches as away_team

matches 1 → many predictions

users 1 → many slips

slips 1 → many slip_items

predictions 1 → many slip_items

slips 1 → many ai_explanations
```

---

# Initial ER Diagram

```text
users
  |
  | 1 to many
  v
slips
  |
  | 1 to many
  v
slip_items
  |
  | many to 1
  v
predictions
  |
  | many to 1
  v
matches
  |
  | many to 1
  v
competitions

matches
  |
  | many to 1
  v
teams
```

---

# Indexes

Important indexes:

```text
users.email

matches.kickoff_time

matches.status

matches.competition_id

predictions.match_id

slips.user_id

slip_items.slip_id

slip_items.prediction_id
```

These indexes support common queries such as:

* Find upcoming matches.
* Find predictions for a match.
* Find saved slips for a user.
* Find slip items for a generated slip.

---

# Future Tables

These tables are not required for MVP but may be added later.

## user_preferences

```text
id
user_id
favorite_sports
favorite_teams
default_budget
default_strategy
created_at
updated_at
```

## prediction_results

Tracks model performance after matches finish.

```text
id
prediction_id
actual_result
was_correct
settled_at
```

## bankroll_entries

Tracks user bankroll history.

```text
id
user_id
amount
entry_type
note
created_at
```

## api_usage

Tracks API usage for future paid API access.

```text
id
user_id
endpoint
request_count
created_at
```

## model_versions

Tracks prediction model versions.

```text
id
model_name
version
training_dataset
accuracy
log_loss
created_at
```

---

# MVP Database Scope

For the first working MVP, the minimum tables are:

```text
competitions
teams
matches
predictions
slips
slip_items
ai_explanations
```

Authentication and user accounts can be added later.

---

# Design Principles

* Use UUIDs or integer IDs consistently.
* Store timestamps for every important entity.
* Keep predictions separate from matches.
* Keep generated slips separate from predictions.
* Do not store secrets in the database.
* Use migrations with Alembic.
* Keep database logic inside repository classes.
