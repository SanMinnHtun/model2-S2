"""Shared question bank, role names, and scoring rules for Model 2."""

from __future__ import annotations

from typing import Final, Sequence

TARGET_ROLES: Final[list[str]] = [
    "Backend / API Engineer",
    "AI / ML / Data Science Engineer",
    "Frontend / UI-UX Developer",
    "Data & Database Architect",
    "Knowledge Graph / Ontology Specialist",
    "DevOps & Cloud Infrastructure Manager",
    "Cyber Security Specialist",
    "Game / Embedded Systems Developer",
    "Full-Stack / Software Engineer",
]

# Index is the answer value (0–4); each entry is the exact mapped target role.
QUESTIONS: Final[list[dict[str, object]]] = [
    {"question": "Software project တစ်ခု ဖန်တီးတဲ့အခါ ဘယ်အပိုင်းကို လုပ်ရတာ အစိတ်လှုပ်ရှားဆုံးလဲ?", "options": [
        "AI Model များကို Train ခြင်း၊ Dataset များ ပြင်ဆင်ခြင်း",
        "Visual Layout၊ UI Interaction များ ဖန်တီးခြင်း",
        "Domain Logic နှင့် Ontology/Rules များ စီစဉ်ခြင်း",
        "Server Code နှင့် API Logic များ ရေးသားခြင်း",
        "Database Schema ဒီဇိုင်းထုတ်ခြင်းနှင့် Data Flow ကိုင်တွယ်ခြင်း",
    ], "roles": [TARGET_ROLES[1], TARGET_ROLES[2], TARGET_ROLES[4], TARGET_ROLES[0], TARGET_ROLES[3]]},
    {"question": "App မှာ Error တက်လို့ Debug လုပ်ရတော့မယ်ဆိုရင် ဘာကို ပထမဆုံး စစ်လဲ?", "options": [
        "Server Log, API Request Payload, Error Traceback", "Entity Mapping သို့မဟုတ် Logical Relationships",
        "Browser DevTools, CSS Layout, Component State", "Dataset cleanliness သို့မဟုတ် Model Feature",
        "Database Query performance နှင့် Slow Queries",
    ], "roles": [TARGET_ROLES[0], TARGET_ROLES[4], TARGET_ROLES[2], TARGET_ROLES[1], TARGET_ROLES[3]]},
    {"question": "Data များကို သိမ်းဆည်း စီမံရမယ်ဆိုရင် ဘယ်ပုံစံ ပိုကြိုက်လဲ?", "options": [
        "SQL Tables (Foreign Keys, Indexes)", "Graph / Mind Map (Nodes, Relationships)",
        "Matrices, Vector Embeddings", "Client-side State, Local Storage, UI Props",
        "JSON Documents, Key-Value Stores (REST API friendly)",
    ], "roles": [TARGET_ROLES[3], TARGET_ROLES[4], TARGET_ROLES[1], TARGET_ROLES[2], TARGET_ROLES[0]]},
    {"question": "Terminal / CLI မှာ ဘာလုပ်လေ့ရှိလဲ?", "options": [
        "Vite/React Dev Server, Git, UI Packages", "Linux Commands, Docker Containers, SSH, Deployments",
        "Python venv, PyTorch, Pandas, Jupyter Notebook", "Database Migrations, Seed Scripts, SQL Shell",
        "Knowledge Graph Queries, Ontologies Parsing",
    ], "roles": [TARGET_ROLES[2], TARGET_ROLES[5], TARGET_ROLES[1], TARGET_ROLES[3], TARGET_ROLES[4]]},
    {"question": "Weekend Personal Project ဆိုရင် ဘာဆောက်ချင်လဲ?", "options": [
        "REST/GraphQL Backend API Service with Auth", "Knowledge Graph Recommendation Engine",
        "Interactive Web App with Dark Mode & Animations", "Image Classifier, Object Detector, Local LLM Agent",
        "Data Scraper Pipeline & Data Warehouse Integration",
    ], "roles": [TARGET_ROLES[0], TARGET_ROLES[4], TARGET_ROLES[2], TARGET_ROLES[1], TARGET_ROLES[3]]},
    {"question": "ဘယ်လို သင်္ချာ/Logic မျိုး သုံးရတာ ပိုသဘောကျလဲ?", "options": [
        "Statistics, Probability, Matrices, Linear Algebra", "Discrete Math, Binary Logic, Cryptography",
        "Spatial Geometry, Responsive Math, Color Ratios", "Logic Diagrams, ER Maps, Ontologies",
        "Relational Algebra, Set Theory, SQL Join Logic",
    ], "roles": [TARGET_ROLES[1], TARGET_ROLES[6], TARGET_ROLES[2], TARGET_ROLES[4], TARGET_ROLES[3]]},
    {"question": "Online မတင်မီ ဘယ်အချက်ကို အရည်အသွေး အမြင့်ဆုံးထားမလဲ?", "options": [
        "Speed & Performance (Mobile/Desktop responsiveness)", "Auth, JWT Tokens, API Security",
        "AI Accuracy, No Hallucination, Reasoning precision", "Data Integrity, No Data Loss/Duplication",
        "Cloud Uptime, Server Resources, Container management",
    ], "roles": [TARGET_ROLES[2], TARGET_ROLES[6], TARGET_ROLES[4], TARGET_ROLES[3], TARGET_ROLES[5]]},
    {"question": "YouTube နည်းပညာ ဗီဒီယို ဘာကြည့်မလဲ?", "options": [
        "Scalable Data Pipeline for millions of records", "Production-Ready REST APIs & Microservices",
        "Knowledge Graph & RAG without Hallucination", "React Animations & Tailwind UI Components",
        "Fine-tuning Local AI Models with Python",
    ], "roles": [TARGET_ROLES[3], TARGET_ROLES[0], TARGET_ROLES[4], TARGET_ROLES[2], TARGET_ROLES[1]]},
    {"question": "သဘောကျဆုံး Tech Stacks?", "options": [
        "Frontend Stacks (React, Vite, Tailwind, TypeScript)", "Knowledge Graph (Neo4j), Semantic Frameworks, RAG Engines",
        "Backend Frameworks (FastAPI, Spring Boot, Express, Postman)",
        "Python Data Science (Jupyter, Pandas, PyTorch, Scikit-Learn)",
        "Linux CLI, Docker, Kubernetes, CI/CD Pipelines",
    ], "roles": [TARGET_ROLES[2], TARGET_ROLES[4], TARGET_ROLES[0], TARGET_ROLES[1], TARGET_ROLES[5]]},
    {"question": "အနာဂတ် ရည်မှန်းချက် အလုပ်အကိုင်?", "options": [
        "Fast, Secure Backend APIs & Server Logic Developer", "Domain Information & Rules Manager for Smart AI",
        "Interactive & Beautiful UI/Web Apps Developer", "Data-driven Problem Solver & AI Model Trainer",
        "Data Pipelines & Database Architect",
    ], "roles": [TARGET_ROLES[0], TARGET_ROLES[4], TARGET_ROLES[2], TARGET_ROLES[1], TARGET_ROLES[3]]},
]


def calculate_role_scores(answers: Sequence[int], low_level_indicator: bool = False) -> dict[str, int]:
    """Apply the specified +3 answer weights and hybrid/low-level adjustments."""
    if len(answers) != len(QUESTIONS):
        raise ValueError(f"Expected {len(QUESTIONS)} answers, received {len(answers)}")
    scores = {role: 0 for role in TARGET_ROLES}
    for question, answer in zip(QUESTIONS, answers):
        if isinstance(answer, bool) or not isinstance(answer, int) or not 0 <= answer <= 4:
            raise ValueError("Every answer must be an integer from 0 to 4")
        scores[question["roles"][answer]] += 3  # type: ignore[index]

    backend = (answers[0] == 3 or answers[9] == 0)
    frontend = (answers[0] == 1 or answers[9] == 2)
    if backend and frontend:
        scores["Full-Stack / Software Engineer"] += 2
    if low_level_indicator:
        scores["Game / Embedded Systems Developer"] += 3
    return scores


def predict_rule_role(answers: Sequence[int]) -> str:
    scores = calculate_role_scores(answers)
    # Stable tie break follows TARGET_ROLES order.
    return max(TARGET_ROLES, key=lambda role: scores[role])
