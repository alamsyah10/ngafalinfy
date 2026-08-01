from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Sm2Result:
    new_ease: float
    new_interval: int
    new_repetitions: int
    new_lapses: int
    new_due_at: datetime


def sm2_schedule(
    *,
    now: datetime,
    quality: int,  # 0..5
    prev_ease: float,
    prev_interval: int,
    prev_repetitions: int,
    prev_lapses: int,
) -> Sm2Result:
    ef = prev_ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(1.3, ef)

    if quality < 3:
        reps = 0
        interval = 1
        lapses = prev_lapses + 1
    else:
        reps = prev_repetitions + 1
        lapses = prev_lapses
        if reps == 1:
            interval = 1
        elif reps == 2:
            interval = 6
        else:
            base = prev_interval if prev_interval > 0 else 1
            interval = max(1, int(round(base * ef)))

    due_at = now + timedelta(days=interval)
    return Sm2Result(ef, interval, reps, lapses, due_at)
