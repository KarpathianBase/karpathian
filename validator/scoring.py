"""
Scoring — the `score = quality + benchmark + stability - cost - complexity -
regression` formula from whitepaper §5.5.

For Phase 0 we keep it minimal and tunable: only quality and cost terms are
implemented; stability, complexity, regression are zero placeholders with
hooks so we can wire them in once we have multi-seed runs.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScoreReport:
    val_bpb: float
    benchmark_accuracy: float
    quality_gain: float
    benchmark_gain: float
    compute_cost: float
    score: float
    king_val_bpb: float | None
    king_benchmark: float | None
    decisively_beats_king: bool


def _hours_to_normalized_h100(
    matmul_ms: float,
    wall_clock_s: float,
    h100_matmul_ms_ref: float = 5.0,
) -> float:
    """Translate wall-clock into normalized H100-hours via the calibration
    benchmark's matmul timing. The miner's machine took (matmul_ms / h100_ref)
    times as long as an H100 would have, so each wall-clock hour counts as
    (h100_ref / matmul_ms) normalized H100-hours.

    Reference: h100_matmul_ms_ref is the matmul_ms on an H100 for the
    calibration workload, to be measured in Phase 0.5 and pinned in this file.
    The 5.0 default is a placeholder.
    """
    if matmul_ms <= 0:
        return wall_clock_s / 3600.0
    speed_factor = h100_matmul_ms_ref / matmul_ms
    return (wall_clock_s / 3600.0) * speed_factor


def score_bundle(
    val_bpb: float,
    benchmark_accuracy: float,
    king_val_bpb: float | None,
    king_benchmark: float | None,
    noise_floor_margin: float,
    matmul_ms: float,
    wall_clock_s: float,
    bpb_weight: float = 1.0,
    benchmark_weight: float = 1.0,
    cost_weight: float = 0.1,
) -> ScoreReport:
    """
    Quality gain on val_bpb is computed as (king - challenger) since lower
    val_bpb is better. Benchmark gain is (challenger - king) since higher
    accuracy is better. Compute cost is normalized H100-hours.

    The "decisively beats king" predicate (§5.7) is true if the quality gain
    exceeds the noise-floor margin on at least one of the metrics, AND no
    other metric materially regresses.
    """
    if king_val_bpb is None:
        # First baseline run — no king to beat, returned for noise-floor calibration.
        quality_gain = 0.0
        benchmark_gain = 0.0
        decisively = False
    else:
        quality_gain = (king_val_bpb - val_bpb)  # positive == improvement
        benchmark_gain = (benchmark_accuracy - (king_benchmark or 0.0))
        decisively = (
            (quality_gain > noise_floor_margin and benchmark_gain >= -noise_floor_margin)
            or
            (benchmark_gain > noise_floor_margin and quality_gain >= -noise_floor_margin)
        )

    cost_h100h = _hours_to_normalized_h100(matmul_ms, wall_clock_s)
    score = (
        bpb_weight * quality_gain
        + benchmark_weight * benchmark_gain
        - cost_weight * cost_h100h
    )

    return ScoreReport(
        val_bpb=val_bpb,
        benchmark_accuracy=benchmark_accuracy,
        quality_gain=quality_gain,
        benchmark_gain=benchmark_gain,
        compute_cost=cost_h100h,
        score=score,
        king_val_bpb=king_val_bpb,
        king_benchmark=king_benchmark,
        decisively_beats_king=decisively,
    )
