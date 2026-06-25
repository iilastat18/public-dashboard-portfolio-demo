from __future__ import annotations

SHORT_DESCRIPTION = (
    "A dashboard concept centered on KPI monitoring, exception review, "
    "data validation, workflow support, and scenario analysis. "
    "This version focuses on modular analytics pages, generic operating concepts, "
    "and synthetic datasets."
)


SAMPLE_METRICS = [
    {"label": "Active modules", "value": "10", "delta": "+3 rebuilt"},
    {"label": "Synthetic KPI cards", "value": "24", "delta": "+8 added"},
    {"label": "Review workflows", "value": "5", "delta": "multi-step"},
    {"label": "Data sources", "value": "Mock + CSV", "delta": "portfolio-ready"},
]


APP_HIGHLIGHTS = [
    {
        "title": "Structured analytics thinking",
        "body": "Show how you move from messy operational questions to clear metrics, filters, and decision-focused views.",
    },
    {
        "title": "Multi-module product design",
        "body": "Demonstrate that you can design a dashboard as a system of tools, not just a single chart page.",
    },
    {
        "title": "Safe public storytelling",
        "body": "Present the same problem-solving strength using synthetic data and renamed modules that read clearly to an external audience.",
    },
]


SAMPLE_TIMELINE = [
    {
        "step": "Morning review",
        "body": "Open the dashboard, scan KPIs, and spot anomalies or workflow blockers from a single landing page.",
    },
    {
        "step": "Focused investigation",
        "body": "Use filters and drill-down modules to inspect exceptions, quality issues, and operational bottlenecks.",
    },
    {
        "step": "Decision support",
        "body": "Compare scenarios, validate assumptions, and prepare the next action through workflow-oriented modules.",
    },
]


MODULE_GROUPS = [
    {
        "name": "Core Monitoring",
        "modules": [
            {
                "name": "Performance Monitoring",
                "description": "A landing view for headline KPIs, daily changes, and drill-down entry points.",
                "signals": ["KPI cards", "trend views", "daily summary"],
            },
            {
                "name": "Exception Review",
                "description": "A structured review surface for anomalies, flagged records, and follow-up actions.",
                "signals": ["case list", "filters", "detail panel"],
            },
            {
                "name": "Execution Quality Analysis",
                "description": "A comparison workspace for spreads, quality metrics, and segment-based analysis.",
                "signals": ["benchmarking", "segments", "comparisons"],
            },
        ],
    },
    {
        "name": "Data And Validation",
        "modules": [
            {
                "name": "Universe Explorer",
                "description": "A searchable explorer for entities, metadata, and coverage checks across datasets.",
                "signals": ["search", "mapping", "coverage"],
            },
            {
                "name": "Data Quality And Validation",
                "description": "A validation page for consistency checks, missing values, and pipeline health signals.",
                "signals": ["validation", "quality checks", "health"],
            },
            {
                "name": "Optimization And Scenario Analysis",
                "description": "A model-facing page for running experiments, reviewing results, and comparing scenarios.",
                "signals": ["optimizer", "history", "validation"],
            },
        ],
    },
    {
        "name": "Workflow Support",
        "modules": [
            {
                "name": "Data Operations Workflow",
                "description": "A task-oriented surface for intake, review, and structured update flows.",
                "signals": ["workflow", "intake", "review"],
            },
            {
                "name": "Import And Export Toolkit",
                "description": "A controlled workspace for loading packages, transforming outputs, and sharing artifacts.",
                "signals": ["upload", "download", "packaging"],
            },
            {
                "name": "Operations Playbook",
                "description": "A guided response page for time-sensitive events, role split, and communication steps.",
                "signals": ["playbook", "timer", "handoff"],
            },
            {
                "name": "Document Intake Assistant",
                "description": "A helper page for converting uploaded documents into structured text or review tasks.",
                "signals": ["OCR", "intake", "automation"],
            },
        ],
    },
]
PRIVACY_PRINCIPLES = [
    "Do not copy internal screenshots, data files, cache outputs, or exact workflow text.",
    "Rename modules so the product structure reads clearly to an external audience.",
    "Use synthetic or public datasets only, even when the internal structure feels reusable.",
    "Rewrite logic independently instead of editing exported internal code.",
    "Avoid internal abbreviations, hostnames, channel names, and compliance references.",
    "Describe the product in terms of reusable patterns such as monitoring, validation, and workflow support.",
]
