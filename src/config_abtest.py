# src/config_abtest.py
import numpy as np

# -----------------------------
# Experiment configuration
# -----------------------------
MAX_RETENTION_DAYS = 30

# Installs (old source)
DAILY_INSTALLS_OLD = 20_000        # Day 1–19, old source
DAILY_INSTALLS_OLD_AFTER_20 = 12_000  # From Day 20 onwards (old source)
DAILY_INSTALLS_NEW = 8_000         # From Day 20 onwards (new source)

# -----------------------------
# Monetization parameters
# -----------------------------
# Given metrics (Task 1)
DAILY_PURCHASE_RATIO_A = 0.0305
DAILY_PURCHASE_RATIO_B = 0.0315

ECPM_A = 9.80
ECPM_B = 10.80

AD_IMPRESSIONS_PER_DAU_A = 2.3
AD_IMPRESSIONS_PER_DAU_B = 1.6

PURCHASE_VALUE = 1.0  # $ per purchase (assumption)

# Derived per-DAU ad revenue
ADS_REV_PER_DAU_A = AD_IMPRESSIONS_PER_DAU_A * ECPM_A / 1000.0
ADS_REV_PER_DAU_B = AD_IMPRESSIONS_PER_DAU_B * ECPM_B / 1000.0


def compute_arpdau(purchase_ratio: float,
                   ads_rev_per_dau: float,
                   purchase_value: float = PURCHASE_VALUE) -> float:
    """
    ARPDAU = ad revenue per DAU + purchase_ratio * purchase_value
    """
    return ads_rev_per_dau + purchase_ratio * purchase_value


# Base-case ARPDAU (no sale)
ARPDAU_A_BASE = compute_arpdau(DAILY_PURCHASE_RATIO_A, ADS_REV_PER_DAU_A)
ARPDAU_B_BASE = compute_arpdau(DAILY_PURCHASE_RATIO_B, ADS_REV_PER_DAU_B)
