# src/retention_curves.py
import numpy as np
from typing import Callable

# -----------------------------
# Old-source retention (given)
# -----------------------------
A_old = np.array([
    53.00, 37.83, 27.00, 24.05, 21.42, 19.08, 17.00, 14.65, 12.62, 10.88,
    9.38, 8.08, 6.96, 6.00, 5.17, 4.46, 3.84, 3.31, 2.85, 2.46,
    2.12, 1.82, 1.57, 1.36, 1.17, 1.01, 0.87, 0.75, 0.64, 0.56
]) / 100.0

B_old = np.array([
    48.00, 34.64, 25.00, 23.34, 21.79, 20.35, 19.00, 17.08, 15.35, 13.79,
    12.40, 11.14, 10.01, 9.00, 8.09, 7.27, 6.53, 5.87, 5.28, 4.74,
    4.26, 3.83, 3.44, 3.09, 2.78, 2.50, 2.25, 2.02, 1.81, 1.63
]) / 100.0


def get_old_retention(variant: str) -> np.ndarray:
    """
    Returns the old-source retention curve for a given variant ("A" or "B").
    """
    if variant.upper() == "A":
        return A_old
    elif variant.upper() == "B":
        return B_old
    else:
        raise ValueError("variant must be 'A' or 'B'")


# -----------------------------
# New-source retention functions (given formulas)
# -----------------------------
def A_new(day_of_life: int) -> float:
    """
    Variant A (new source) retention.
    day_of_life: 1,2,3,...
    """
    return 0.58 * np.exp(-0.12 * (day_of_life - 1))


def B_new(day_of_life: int) -> float:
    """
    Variant B (new source) retention.
    day_of_life: 1,2,3,...
    """
    return 0.52 * np.exp(-0.10 * (day_of_life - 1))


def get_new_retention_func(variant: str) -> Callable[[int], float]:
    """
    Returns the new-source retention function for a given variant.
    """
    if variant.upper() == "A":
        return A_new
    elif variant.upper() == "B":
        return B_new
    else:
        raise ValueError("variant must be 'A' or 'B'")
