# SM-2 Spaced Repetition Algorithm

## Overview

**SM-2** (Super Memory 2) is a widely-used spaced repetition algorithm designed to optimize long-term retention and minimize study time. It was created by Piotr Wozniak and forms the foundation of many modern flashcard systems (Anki, SuperMemory, etc.).

The algorithm calculates optimal review intervals based on how well a user performed on each card, ensuring that difficult material is reviewed more frequently than easy material.

## Core Concepts

### 1. **Ease Factor (EF)**
- A multiplier that determines how quickly review intervals grow
- **Range**: 1.3 to 5.0+ (default: 2.5)
- **Interpretation**:
  - EF < 1.3: Card is too difficult; review more frequently
  - EF = 1.3: Minimum; interval barely increases
  - EF = 2.5: Standard; interval doubles with each successful repetition
  - EF > 2.5: Easy cards; intervals grow faster
- **Adjusted after each review** based on user response quality

### 2. **Interval**
- Number of days until the next review
- **Progression for a well-learned card** (quality ≥ 3):
  - After 1st repetition: 1 day
  - After 2nd repetition: 3 days
  - After 3rd repetition: EF × 6 days
  - Subsequent: Previous interval × EF
- **Reset to 0** when user forgets (quality < 3)

### 3. **Repetitions (Learning Stage)**
- Counter tracking how many consecutive successful reviews
- **Learning stages**:
  - Reps 0: New cards (never reviewed)
  - Reps 1-10: Learning phase (frequent reviews)
  - Reps 11+: Review phase (increasingly spaced)
- **Resets to 0** when user forgets the card

### 4. **Lapses**
- Counter tracking how many times the user forgot a card
- Used for statistics and optional interval penalties
- Increments when quality < 3 (wrong answer)

### 5. **Due Date (due_at)**
- Timestamp when the card is next due for review
- Calculated as: `now + interval (days)`
- Cards with `due_at ≤ now` appear in study sessions

### 6. **Quality (0-5)**
User's response quality for each review:
- **0**: Answer was completely wrong
- **1**: Correct answer after serious difficulty
- **2**: Correct answer after some hesitation
- **3**: Correct answer with some difficulty (minimum to avoid reset)
- **4**: Correct answer with acceptable response time
- **5**: Perfect response (best possible)

## The Algorithm: Step by Step

### Initial State (New Card)
```
ease_factor = 2.5
interval = 0
repetitions = 0
lapses = 0
due_at = tomorrow (midnight UTC)
```

### After Each Review

Given a user's quality response (0-5):

#### Step 1: Update Ease Factor
```
EF := max(1.3, EF + (0.1 - (5 - q) × (0.08 + (5 - q) × 0.02)))
```
Where `q` is the quality (0-5). In simplified form:
- If quality ≥ 3: EF increases slightly
- If quality < 3: EF decreases

**Practical interpretation**:
- Quality 5: EF increases by ~0.1
- Quality 4: EF unchanged (~0.0)
- Quality 3: EF decreases by ~0.14
- Quality 0: EF decreases significantly

#### Step 2: Update Interval
- **If quality < 3** (forgot the card):
  - interval := 0
  - repetitions := 0  ← ⚠️ Reset learning
  - lapses := lapses + 1
  
- **If quality ≥ 3** (remembered the card):
  - If repetitions = 0:
    - interval := 1 day
  - Else if repetitions = 1:
    - interval := 3 days
  - Else:
    - interval := round(previous_interval × EF)
  - repetitions := repetitions + 1

#### Step 3: Calculate Next Due Date
```
due_at := now + interval (days)
```

## Example Walkthrough

### Scenario: Learning the word "犬" (inu = dog)

**Day 1 - Card Created**
```
Card State:
  ease_factor: 2.5
  interval: 0
  repetitions: 0
  due_at: Tomorrow (Day 2)
  Status: NEW
```

**Day 2 - First Review: Quality = 5 (Perfect)**
```
Calculation:
  new_EF = 2.5 + (0.1 - 0 × 0.08) = 2.6
  new_interval = 1 (first successful review)
  new_repetitions = 1
  new_due_at = Day 2 + 1 = Day 3

Card State:
  ease_factor: 2.6
  interval: 1
  repetitions: 1
  due_at: Day 3
  Status: LEARNING
```

**Day 3 - Second Review: Quality = 4 (Acceptable)**
```
Calculation:
  new_EF = 2.6 + (0.1 - 0.4 × 0.12) = 2.55 ≈ 2.55
  new_interval = 3 (second successful review)
  new_repetitions = 2
  new_due_at = Day 3 + 3 = Day 6

Card State:
  ease_factor: 2.55
  interval: 3
  repetitions: 2
  due_at: Day 6
  Status: LEARNING
```

**Day 6 - Third Review: Quality = 3 (With Difficulty)**
```
Calculation:
  new_EF = 2.55 + (0.1 - 1.4 × 0.136) = 2.55 - 0.19 = 2.36
  new_interval = round(3 × 2.55) = 7 (beyond learning phase)
  new_repetitions = 3
  new_due_at = Day 6 + 7 = Day 13

Card State:
  ease_factor: 2.36
  interval: 7
  repetitions: 3
  due_at: Day 13
  Status: REVIEW ← Entered review phase (reps ≥ 3)
```

**Day 10 - Fourth Review: Quality = 1 (Wrong!)**
```
Calculation:
  User answered incorrectly - quality < 3
  new_EF = 2.36 + (0.1 - 3.9 × 0.188) = 2.36 - 0.73 = 1.63
  new_interval = 0 ← Reset!
  new_repetitions = 0 ← Reset!
  lapses = 1
  new_due_at = Day 10 + 1 = Day 11 (back to 1 day)

Card State:
  ease_factor: 1.63 (decreased due to wrong answer)
  interval: 0
  repetitions: 0
  due_at: Day 11
  Status: LEARNING ← Back to learning phase
  lapses: 1
```

**Day 11 - Fifth Review: Quality = 4 (Correct after reset)**
```
Calculation:
  new_EF = 1.63 + (0.1 - 0.4 × 0.12) = 1.63 + 0.05 = 1.68
  new_interval = 1 (first again, but with lower EF)
  new_repetitions = 1
  new_due_at = Day 11 + 1 = Day 12

Card State:
  ease_factor: 1.68 (recovering)
  interval: 1
  repetitions: 1
  due_at: Day 12
  Status: LEARNING
  lapses: 1
```

## Key Implementation Details

### 1. **Timezone Awareness**
All timestamps are stored in **UTC** to ensure consistency:
```python
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
```

### 2. **Due Date Calculation**
Due dates are midnight UTC of the target day:
```python
def calculate_due_at(now, interval_days):
    future = now + timedelta(days=interval_days)
    # Set to midnight UTC
    return future.replace(hour=0, minute=0, second=0, microsecond=0)
```

### 3. **Suspended Cards**
Cards can be temporarily suspended (paused) to skip them during reviews:
- Suspended cards appear in stats but not in daily review queues
- Use PATCH `/decks/{deck_id}/cards/{card_id}/suspend` to toggle

### 4. **Reset Scheduling**
Sometimes you may want to restart a card from scratch:
- Use POST `/decks/{deck_id}/cards/{card_id}/reset` 
- Resets to: EF = 2.5, interval = 0, reps = 0, due_at = tomorrow

### 5. **Learning Phases (Based on Repetitions)**
```
Repetitions  Status      Interval Multiplier
0            New         1 day (hardcoded)
1            Learning    3 days (hardcoded)
2-10         Learning    interval × EF
11+          Review      interval × EF (increasingly spaced)
```

## API Endpoints for SM-2 Management

### Studying Cards
- **GET** `/decks/{deck_id}/study/next` - Get next due card
- **POST** `/decks/{deck_id}/study/answer` - Submit answer (applies SM-2)

### Statistics
- **GET** `/decks/{deck_id}/cards/stats/summary` - Deck overview (new/learning/review counts)
- **GET** `/decks/{deck_id}/review_logs` - View all review history

### Card Management
- **PATCH** `/decks/{deck_id}/cards/{card_id}/suspend` - Pause a card
- **POST** `/decks/{deck_id}/cards/{card_id}/reset` - Reset to new state

## Best Practices

### For Users
1. **Answer honestly**: The algorithm only works if you rate accurately
2. **Consistent review timing**: Study at the same time daily for best retention
3. **Avoid long breaks**: Lapses reset your progress; smaller intervals are better
4. **Monitor stats**: Use deck stats to identify struggling cards

### For Developers
1. **Always use UTC**: Never mix timezones in interval calculations
2. **Transaction safety**: Combine card updates + review log writes atomically
3. **Validate quality**: Only accept 0-5 ratings
4. **Min EF enforcement**: Always enforce EF ≥ 1.3 to prevent degradation

## Research References

- **Original SM-2 Paper**: Wozniak, P. A. (1990). "Optimization of learning"
- **Modern Application**: Anki's spaced repetition documentation
- **Variations**: Some systems use SM-17 or modified algorithms for specific use cases

## Related Code

- **Algorithm Implementation**: [src/usecase/study/sm2.py](src/usecase/study/sm2.py)
- **Study Usecase**: [src/usecase/study/study_writeable_usecase.py](src/usecase/study/study_writeable_usecase.py)
- **Card Model**: [src/domain/model/card/card.py](src/domain/model/card/card.py)
- **Review Log Model**: [src/domain/model/review_log/review_log.py](src/domain/model/review_log/review_log.py)
