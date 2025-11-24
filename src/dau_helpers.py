# src/dau_helpers.py
import numpy as np
from typing import Callable
from .config_abtest import (
    MAX_RETENTION_DAYS,
    DAILY_INSTALLS_OLD,
    DAILY_INSTALLS_OLD_AFTER_20,
    DAILY_INSTALLS_NEW,
)
from .retention_curves import get_old_retention


def compute_dau_single_source(day: int,
                              variant: str,
                              max_days: int = MAX_RETENTION_DAYS,
                              daily_installs: int = DAILY_INSTALLS_OLD) -> float:
    """
    Computes DAU on a given calendar day (1..N) for the original source only,
    assuming a constant number of installs per day and a given retention curve.
    """
    retention = get_old_retention(variant)
    dau = 0.0

    # Age index = 0 for day_of_life=1
    max_age = min(day, len(retention), max_days)
    for age in range(1, max_age + 1):
        age_idx = age - 1
        dau += daily_installs * retention[age_idx]

    return dau


def compute_dau_old_with_mix(day: int,
                             variant: str,
                             max_days: int = MAX_RETENTION_DAYS) -> float:
    """
    DAU from the old source with changed installs after day 20:
    - day < 20: 20k/day
    - day >= 20: 12k/day
    """
    retention = get_old_retention(variant)
    dau = 0.0

    max_age = min(day, len(retention), max_days)
    for age in range(1, max_age + 1):
        age_idx = age - 1
        cohort_day = day - age + 1

        if cohort_day < 20:
            cohort_size = DAILY_INSTALLS_OLD
        else:
            cohort_size = DAILY_INSTALLS_OLD_AFTER_20

        dau += cohort_size * retention[age_idx]

    return dau


def compute_dau_new_source(day: int,
                           retention_func: Callable[[int], float]) -> float:
    """
    DAU contribution from the new source (which starts at day 20).
    For each cohort from day 20 up to 'day', we apply the new retention curve.
    """
    if day < 20:
        return 0.0

    dau = 0.0
    for cohort_day in range(20, day + 1):
        age = day - cohort_day + 1  # day-of-life
        dau += DAILY_INSTALLS_NEW * retention_func(age)

    return dau
