from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def get_performance_timeseries() -> pd.DataFrame:
    rng = np.random.default_rng(14)
    dates = pd.date_range(date.today() - timedelta(days=89), periods=90, freq="D")
    teams = ["Core Platform", "Operations", "Coverage", "Automation"]
    records: list[dict[str, object]] = []

    for offset, current_date in enumerate(dates):
        seasonal = np.sin(offset / 8) * 3.2
        for index, team in enumerate(teams):
            throughput = 92 + index * 6 + seasonal + rng.normal(0, 4)
            accuracy = 95.5 - index * 0.7 + np.cos(offset / 9) * 0.9 + rng.normal(0, 0.7)
            queue_hours = 18 + index * 3 + rng.normal(0, 2.4)
            health_score = accuracy - queue_hours * 0.28 + throughput * 0.12
            records.append(
                {
                    "date": current_date,
                    "team": team,
                    "throughput": round(float(throughput), 1),
                    "accuracy": round(float(np.clip(accuracy, 89, 99.7)), 2),
                    "queue_hours": round(float(max(queue_hours, 6)), 1),
                    "health_score": round(float(health_score), 2),
                }
            )

    return pd.DataFrame(records)


@st.cache_data
def get_exception_cases() -> pd.DataFrame:
    rng = np.random.default_rng(23)
    owners = ["A. Chen", "L. Park", "N. Ivanov", "S. Patel", "M. Rossi"]
    categories = ["Coverage gap", "Threshold breach", "Ingestion issue", "Validation drift", "Manual follow-up"]
    severities = ["Low", "Medium", "High", "Critical"]
    statuses = ["Open", "Investigating", "Monitoring", "Resolved"]
    modules = ["Performance Monitoring", "Exception Review", "Data Quality", "Operations Workflow"]
    now = pd.Timestamp.now().floor("h")

    records: list[dict[str, object]] = []
    for idx in range(160):
        severity = rng.choice(severities, p=[0.28, 0.36, 0.24, 0.12])
        status = rng.choice(statuses, p=[0.24, 0.31, 0.17, 0.28])
        created_at = now - pd.to_timedelta(float(rng.uniform(3, 420)), unit="h")
        impact_score = rng.uniform(40, 96) + severities.index(severity) * 4.5
        records.append(
            {
                "case_id": f"EX-{3400 + idx}",
                "category": rng.choice(categories),
                "module": rng.choice(modules),
                "severity": severity,
                "severity_rank": severities.index(severity),
                "status": status,
                "owner": rng.choice(owners),
                "created_at": created_at,
                "aging_hours": int((now - created_at).total_seconds() // 3600),
                "impact_score": round(float(np.clip(impact_score, 30, 99)), 1),
                "notes": "Synthetic review case for public portfolio demo.",
            }
        )

    return pd.DataFrame(records)


@st.cache_data
def get_quality_checks() -> pd.DataFrame:
    rng = np.random.default_rng(31)
    datasets = [
        "entity_master",
        "reference_prices",
        "daily_positions",
        "event_calendar",
        "coverage_registry",
        "workflow_state",
    ]
    statuses = ["Healthy", "Watch", "Blocked"]
    records: list[dict[str, object]] = []

    for idx, dataset in enumerate(datasets):
        freshness = int(max(6, rng.normal(34 + idx * 8, 11)))
        missing_rate = max(0.0, rng.normal(0.6 + idx * 0.35, 0.45))
        failed_checks = int(max(0, rng.poisson(0.8 + idx * 0.55)))
        if failed_checks >= 4 or freshness > 80:
            status = "Blocked"
        elif failed_checks >= 2 or missing_rate > 1.6:
            status = "Watch"
        else:
            status = "Healthy"

        records.append(
            {
                "dataset": dataset,
                "owner": ["Platform", "Analytics", "Ops", "Automation", "Analytics", "Ops"][idx],
                "freshness_minutes": freshness,
                "missing_rate": round(float(missing_rate), 2),
                "failed_checks": failed_checks,
                "status": status,
                "status_rank": statuses.index(status),
                "row_count": int(12000 + rng.integers(6000, 88000)),
                "schema_changes": int(rng.integers(0, 4)),
            }
        )

    return pd.DataFrame(records)


@st.cache_data
def get_quality_run_history() -> pd.DataFrame:
    rng = np.random.default_rng(41)
    runs = []
    for days_back in range(20, -1, -1):
        run_date = pd.Timestamp(date.today() - timedelta(days=days_back))
        runs.append(
            {
                "run_date": run_date,
                "passed_checks": int(46 + rng.integers(-3, 5)),
                "warnings": int(max(1, 7 + rng.integers(-2, 3))),
                "blocked": int(max(0, 2 + rng.integers(-1, 2))),
            }
        )
    return pd.DataFrame(runs)


@st.cache_data
def get_workflow_items() -> pd.DataFrame:
    rng = np.random.default_rng(57)
    lanes = ["Intake", "Review", "Validate", "Published"]
    task_types = ["Refresh request", "Coverage update", "Validation check", "Package export", "Scenario rerun"]
    owners = ["A. Chen", "L. Park", "N. Ivanov", "S. Patel", "M. Rossi"]
    priorities = ["Low", "Medium", "High"]
    records: list[dict[str, object]] = []

    for idx in range(28):
        lane = rng.choice(lanes, p=[0.24, 0.28, 0.26, 0.22])
        priority = rng.choice(priorities, p=[0.24, 0.48, 0.28])
        sla_hours_left = int(rng.integers(-6, 36))
        records.append(
            {
                "task_id": f"WF-{720 + idx}",
                "lane": lane,
                "lane_rank": lanes.index(lane),
                "task_type": rng.choice(task_types),
                "owner": rng.choice(owners),
                "priority": priority,
                "sla_hours_left": sla_hours_left,
                "automation_candidate": bool(rng.integers(0, 2)),
                "summary": "Synthetic workflow item created to demonstrate queue management and handoff design.",
            }
        )

    return pd.DataFrame(records)


@st.cache_data
def get_optimizer_runs() -> pd.DataFrame:
    rng = np.random.default_rng(71)
    buckets = ["LC1", "LC2", "LC3", "LC4"]
    scenarios = ["Balanced", "Coverage First", "Efficiency Tilt", "Capacity Guardrail"]
    records: list[dict[str, object]] = []

    for bucket_index, bucket in enumerate(buckets):
        base_coverage = 95.6 - bucket_index * 1.2
        for run_index in range(12):
            scenario = scenarios[run_index % len(scenarios)]
            run_date = pd.Timestamp(date.today() - timedelta(days=run_index * 4 + bucket_index))
            coverage = base_coverage + rng.normal(0, 0.8)
            expected_uplift = 3.8 + bucket_index * 0.7 + rng.normal(0, 0.9)
            risk_score = 5.8 + bucket_index * 0.9 + rng.normal(0, 0.6)
            stability = 93.0 - bucket_index * 1.1 + rng.normal(0, 1.4)
            score = coverage * 0.58 + expected_uplift * 2.6 + stability * 0.18 - risk_score * 1.4
            status = "Recommended" if score > 67 else ("Watch" if score > 63 else "Hold")
            records.append(
                {
                    "run_id": f"OPT-{bucket_index + 1}{run_index + 10}",
                    "bucket": bucket,
                    "scenario": scenario,
                    "run_date": run_date,
                    "coverage": round(float(np.clip(coverage, 88, 99.5)), 2),
                    "expected_uplift": round(float(expected_uplift), 2),
                    "risk_score": round(float(np.clip(risk_score, 3.8, 9.8)), 2),
                    "stability": round(float(np.clip(stability, 86, 98)), 2),
                    "score": round(float(score), 2),
                    "status": status,
                    "rebalance_count": int(max(1, rng.poisson(1.6 + bucket_index * 0.3))),
                }
            )

    return pd.DataFrame(records)


@st.cache_data
def get_validation_windows() -> pd.DataFrame:
    rng = np.random.default_rng(83)
    buckets = ["LC1", "LC2", "LC3", "LC4"]
    records: list[dict[str, object]] = []
    for bucket_index, bucket in enumerate(buckets):
        for offset in range(16):
            window_end = pd.Timestamp(date.today() - timedelta(days=(15 - offset) * 7))
            target = 97.4 - bucket_index * 0.8
            observed = target - rng.uniform(0.1, 1.8) + np.sin(offset / 2.8) * 0.35
            headroom = observed - (95.2 - bucket_index * 0.5)
            records.append(
                {
                    "bucket": bucket,
                    "window_end": window_end,
                    "observed_coverage": round(float(observed), 2),
                    "target_coverage": round(float(target), 2),
                    "headroom": round(float(headroom), 2),
                }
            )
    return pd.DataFrame(records)


@st.cache_data
def get_allocation_mix() -> pd.DataFrame:
    rng = np.random.default_rng(95)
    buckets = ["LC1", "LC2", "LC3", "LC4"]
    levers = ["Primary flow", "Fallback flow", "Manual review", "Risk buffer"]
    records: list[dict[str, object]] = []
    for bucket in buckets:
        weights = rng.dirichlet([5.4, 2.4, 1.7, 1.3])
        for lever, weight in zip(levers, weights):
            records.append(
                {
                    "bucket": bucket,
                    "lever": lever,
                    "weight": round(float(weight * 100), 2),
                }
            )
    return pd.DataFrame(records)


@st.cache_data
def get_universe_records() -> pd.DataFrame:
    rng = np.random.default_rng(101)
    asset_classes = ["Equity", "ETF", "ADR", "Closed-End Fund"]
    regions = ["Germany", "France", "Nordics", "US", "UK", "Southern Europe"]
    sectors = ["Tech", "Financials", "Industrials", "Healthcare", "Consumer", "Energy"]
    lifecycle = ["Core", "Review", "Gap", "Emerging"]
    coverage = ["Ready", "Partial", "Missing"]
    records: list[dict[str, object]] = []

    for idx in range(220):
        coverage_state = rng.choice(coverage, p=[0.58, 0.28, 0.14])
        readiness = 91 + rng.normal(0, 4.5)
        if coverage_state == "Partial":
            readiness -= rng.uniform(6, 12)
        elif coverage_state == "Missing":
            readiness -= rng.uniform(14, 24)

        liquidity = max(18, rng.normal(62, 18))
        records.append(
            {
                "instrument_id": f"UNI-{4800 + idx}",
                "display_name": f"Sample Instrument {idx + 1}",
                "asset_class": rng.choice(asset_classes, p=[0.52, 0.22, 0.14, 0.12]),
                "region": rng.choice(regions),
                "sector": rng.choice(sectors),
                "lifecycle": rng.choice(lifecycle, p=[0.46, 0.24, 0.14, 0.16]),
                "coverage_status": coverage_state,
                "readiness_score": round(float(np.clip(readiness, 48, 99)), 1),
                "liquidity_score": round(float(np.clip(liquidity, 12, 96)), 1),
                "avg_daily_turnover_m": round(float(max(4, rng.normal(38, 19))), 1),
                "mapping_gaps": int(max(0, rng.poisson(0.8 if coverage_state == "Ready" else 2.2))),
                "benchmark_family": rng.choice(["Large Cap", "Mid Cap", "Thematic", "Regional"]),
                "hedge_ready": coverage_state == "Ready" and liquidity > 34,
            }
        )

    return pd.DataFrame(records)
