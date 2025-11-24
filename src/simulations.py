# src/simulations.py
import numpy as np
from typing import Tuple

from .config_abtest import (
    MAX_RETENTION_DAYS,
    ARPDAU_A_BASE,
    ARPDAU_B_BASE,
    DAILY_PURCHASE_RATIO_A,
    DAILY_PURCHASE_RATIO_B,
    ADS_REV_PER_DAU_A,
    ADS_REV_PER_DAU_B,
)
from .dau_helpers import (
    compute_dau_single_source,
    compute_dau_old_with_mix,
    compute_dau_new_source,
)
from .retention_curves import get_new_retention_func


def simulate_base(days: int ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Base case:
    - Single (old) user source
    - 20k installs/day
    - No sale
    - No new source
    """
    totalA = 0.0
    totalB = 0.0
    dailyA, dailyB = [], []
    cumA, cumB = [], []

    for day in range(1, days + 1):
        dau_A = compute_dau_single_source(day, variant="A", max_days=MAX_RETENTION_DAYS)
        dau_B = compute_dau_single_source(day, variant="B", max_days=MAX_RETENTION_DAYS)

        revA = dau_A * ARPDAU_A_BASE
        revB = dau_B * ARPDAU_B_BASE

        totalA += revA
        totalB += revB

        dailyA.append(revA)
        dailyB.append(revB)
        cumA.append(totalA)
        cumB.append(totalB)

    return (
        np.arange(1, days + 1),
        np.array(dailyA),
        np.array(dailyB),
        np.array(cumA),
        np.array(cumB),
    )


def simulate_sale(days: int = 30,
                  sale_start: int = 15,
                  sale_end: int = 24,
                  boost: float = 0.01):
    """
    Scenario with a 10-day sale:
    - Day sale_start–sale_end: purchase ratio is +boost for both variants.
    - Only the original user source (20k installs/day).
    """
    totalA = 0.0
    totalB = 0.0
    dailyA, dailyB = [], []
    cumA, cumB = [], []

    for day in range(1, days + 1):
        dau_A = compute_dau_single_source(day, "A", MAX_RETENTION_DAYS)
        dau_B = compute_dau_single_source(day, "B", MAX_RETENTION_DAYS)

        # Adjust purchase ratios during sale
        if sale_start <= day <= sale_end:
            prA = DAILY_PURCHASE_RATIO_A + boost
            prB = DAILY_PURCHASE_RATIO_B + boost
        else:
            prA = DAILY_PURCHASE_RATIO_A
            prB = DAILY_PURCHASE_RATIO_B

        arpdau_A = ADS_REV_PER_DAU_A + prA
        arpdau_B = ADS_REV_PER_DAU_B + prB

        revA = dau_A * arpdau_A
        revB = dau_B * arpdau_B

        totalA += revA
        totalB += revB

        dailyA.append(revA)
        dailyB.append(revB)
        cumA.append(totalA)
        cumB.append(totalB)

    return (
        np.arange(1, days + 1),
        np.array(dailyA),
        np.array(dailyB),
        np.array(cumA),
        np.array(cumB),
    )


def simulate_new_source(days: int = 30):
    """
    Scenario with an additional user source from Day 20:
    - Day 1–19: 20k installs/day from old source.
    - Day 20–N: 12k installs/day from old source + 8k installs/day from new source.
    - No sale, but new source has its own retention curve.
    """
    totalA = 0.0
    totalB = 0.0
    dailyA, dailyB = [], []
    cumA, cumB = [], []

    A_new_ret = get_new_retention_func("A")
    B_new_ret = get_new_retention_func("B")

    for day in range(1, days + 1):
        # Old source contribution (with changed install counts after day 20)
        dau_A_old = compute_dau_old_with_mix(day, "A", MAX_RETENTION_DAYS)
        dau_B_old = compute_dau_old_with_mix(day, "B", MAX_RETENTION_DAYS)

        # New source contribution (starts at day 20)
        dau_A_new = compute_dau_new_source(day, A_new_ret)
        dau_B_new = compute_dau_new_source(day, B_new_ret)

        dau_A = dau_A_old + dau_A_new
        dau_B = dau_B_old + dau_B_new

        revA = dau_A * ARPDAU_A_BASE
        revB = dau_B * ARPDAU_B_BASE

        totalA += revA
        totalB += revB

        dailyA.append(revA)
        dailyB.append(revB)
        cumA.append(totalA)
        cumB.append(totalB)

    return (
        np.arange(1, days + 1),
        np.array(dailyA),
        np.array(dailyB),
        np.array(cumA),
        np.array(cumB),
    )
