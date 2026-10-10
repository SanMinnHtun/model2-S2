# Codex prompt: connect the career quiz frontend to the API

Copy the prompt below into Codex while the frontend project is open. The question bank and API contract are included so the implementation has a reliable source of truth.

---

## Prompt

Please inspect this project and finish the frontend-to-backend connection for the Burmese IT career diagnostic quiz. Make the necessary frontend changes in the existing app, following its framework, file layout, and visual conventions. Do not replace the app with a new scaffold. First identify the frontend entry point, current quiz/question state, API configuration, and any existing backend integration. Reuse what is already working and make the smallest complete changes needed for a working flow.

### Backend API contract

The FastAPI backend exposes:

- `GET {API_BASE_URL}/api/v1/career/questions`
- `POST {API_BASE_URL}/api/v1/career/predict`

The questions endpoint returns this shape, with all ten questions and five options per question:

```json
{
  "questions": [
    {
      "id": "Q1",
      "text": "question text",
      "options": [
        { "value": 0, "label": "option text" },
        { "value": 1, "label": "option text" },
        { "value": 2, "label": "option text" },
        { "value": 3, "label": "option text" },
        { "value": 4, "label": "option text" }
      ]
    }
  ]
}
```

Load the questions from the API as the runtime source for the quiz. The canonical question text and options are listed below for checking the UI and understanding the meaning of answer values. Do not hardcode a second question bank if the API can be reached. Do not change option ordering or map option values to roles in the frontend.

Submit exactly ten selected option values in Q1-to-Q10 order. The request must be JSON with `Content-Type: application/json`:

```http
POST {API_BASE_URL}/api/v1/career/predict
Content-Type: application/json
```

```json
{
  "answers": [3, 0, 4, 1, 0, 1, 1, 1, 2, 0]
}
```

Each answer must be a JSON integer from 0 through 4, selected from that question's option `value`. Do not send option labels, question text, strings such as `"3"`, booleans, or a list ordered by navigation history. Store an answer against its question ID/index so Back navigation cannot reorder answers. Block submission until all ten answers are selected.

A successful response has this shape (the values here are illustrative):

```json
{
  "predicted_role": "Backend / API Engineer",
  "confidence": 0.73,
  "probabilities": {
    "Backend / API Engineer": 0.73,
    "AI / ML / Data Science Engineer": 0.11,
    "Frontend / UI-UX Developer": 0.08,
    "Data & Database Architect": 0.04,
    "Knowledge Graph / Ontology Specialist": 0.02,
    "DevOps & Cloud Infrastructure Manager": 0.02,
    "Cyber Security Specialist": 0.0,
    "Game / Embedded Systems Developer": 0.0,
    "Full-Stack / Software Engineer": 0.0
  }
}
```

Show the predicted role and confidence, and display the probabilities for all roles if the app has or can naturally support a results visualization. These are fractions from 0 to 1; format them as percentages for display. Keep the returned role names as supplied by the API. The backend may return HTTP 422 for invalid answers, 503 if its trained model artifact is missing, and other errors if prediction fails. Show a useful error state and preserve answers so the user can retry.

### Canonical questions and option values

Render Burmese text and option labels from `GET /questions`. Option values below are zero-based answer integers sent in the `answers` array.

#### Q1 — Software project တစ်ခု ဖန်တီးတဲ့အခါ ဘယ်အပိုင်းကို လုပ်ရတာ အစိတ်လှုပ်ရှားဆုံးလဲ?

- `0`: AI Model များကို Train ခြင်း၊ Dataset များ ပြင်ဆင်ခြင်း
- `1`: Visual Layout၊ UI Interaction များ ဖန်တီးခြင်း
- `2`: Domain Logic နှင့် Ontology/Rules များ စီစဉ်ခြင်း
- `3`: Server Code နှင့် API Logic များ ရေးသားခြင်း
- `4`: Database Schema ဒီဇိုင်းထုတ်ခြင်းနှင့် Data Flow ကိုင်တွယ်ခြင်း

#### Q2 — App မှာ Error တက်လို့ Debug လုပ်ရတော့မယ်ဆိုရင် ဘာကို ပထမဆုံး စစ်လဲ?

- `0`: Server Log, API Request Payload, Error Traceback
- `1`: Entity Mapping သို့မဟုတ် Logical Relationships
- `2`: Browser DevTools, CSS Layout, Component State
- `3`: Dataset cleanliness သို့မဟုတ် Model Feature
- `4`: Database Query performance နှင့် Slow Queries

#### Q3 — Data များကို သိမ်းဆည်း စီမံရမယ်ဆိုရင် ဘယ်ပုံစံ ပိုကြိုက်လဲ?

- `0`: SQL Tables (Foreign Keys, Indexes)
- `1`: Graph / Mind Map (Nodes, Relationships)
- `2`: Matrices, Vector Embeddings
- `3`: Client-side State, Local Storage, UI Props
- `4`: JSON Documents, Key-Value Stores (REST API friendly)

#### Q4 — Terminal / CLI မှာ ဘာလုပ်လေ့ရှိလဲ?

- `0`: Vite/React Dev Server, Git, UI Packages
- `1`: Linux Commands, Docker Containers, SSH, Deployments
- `2`: Python venv, PyTorch, Pandas, Jupyter Notebook
- `3`: Database Migrations, Seed Scripts, SQL Shell
- `4`: Knowledge Graph Queries, Ontologies Parsing

#### Q5 — Weekend Personal Project ဆိုရင် ဘာဆောက်ချင်လဲ?

- `0`: REST/GraphQL Backend API Service with Auth
- `1`: Knowledge Graph Recommendation Engine
- `2`: Interactive Web App with Dark Mode & Animations
- `3`: Image Classifier, Object Detector, Local LLM Agent
- `4`: Data Scraper Pipeline & Data Warehouse Integration

#### Q6 — ဘယ်လို သင်္ချာ/Logic မျိုး သုံးရတာ ပိုသဘောကျလဲ?

- `0`: Statistics, Probability, Matrices, Linear Algebra
- `1`: Discrete Math, Binary Logic, Cryptography
- `2`: Spatial Geometry, Responsive Math, Color Ratios
- `3`: Logic Diagrams, ER Maps, Ontologies
- `4`: Relational Algebra, Set Theory, SQL Join Logic

#### Q7 — Online မတင်မီ ဘယ်အချက်ကို အရည်အသွေး အမြင့်ဆုံးထားမလဲ?

- `0`: Speed & Performance (Mobile/Desktop responsiveness)
- `1`: Auth, JWT Tokens, API Security
- `2`: AI Accuracy, No Hallucination, Reasoning precision
- `3`: Data Integrity, No Data Loss/Duplication
- `4`: Cloud Uptime, Server Resources, Container management

#### Q8 — YouTube နည်းပညာ ဗီဒီယို ဘာကြည့်မလဲ?

- `0`: Scalable Data Pipeline for millions of records
- `1`: Production-Ready REST APIs & Microservices
- `2`: Knowledge Graph & RAG without Hallucination
- `3`: React Animations & Tailwind UI Components
- `4`: Fine-tuning Local AI Models with Python

#### Q9 — သဘောကျဆုံး Tech Stacks?

- `0`: Frontend Stacks (React, Vite, Tailwind, TypeScript)
- `1`: Knowledge Graph (Neo4j), Semantic Frameworks, RAG Engines
- `2`: Backend Frameworks (FastAPI, Spring Boot, Express, Postman)
- `3`: Python Data Science (Jupyter, Pandas, PyTorch, Scikit-Learn)
- `4`: Linux CLI, Docker, Kubernetes, CI/CD Pipelines

#### Q10 — အနာဂတ် ရည်မှန်းချက် အလုပ်အကိုင်?

- `0`: Fast, Secure Backend APIs & Server Logic Developer
- `1`: Domain Information & Rules Manager for Smart AI
- `2`: Interactive & Beautiful UI/Web Apps Developer
- `3`: Data-driven Problem Solver & AI Model Trainer
- `4`: Data Pipelines & Database Architect

### Implementation requirements

1. Put the API base URL in the project's existing environment/config pattern, in one place. If none exists, add a clear configuration module and document the variable name. Do not assume `localhost` works on a physical phone. Make the local URL configurable for a computer/browser, Android emulator, iOS simulator, and physical device as appropriate for this app. Do not commit secrets.
2. Add or fix a typed API client for fetching questions and submitting answers. Set JSON headers, check `response.ok`, parse server error detail when available, and handle network failures.
3. Validate the question response enough to avoid rendering a broken quiz. It must contain ten questions and each question must have five options with integer values 0–4. Keep option labels/text Unicode intact.
4. Build or repair the quiz flow to show one question at a time (or preserve the existing presentation), selected state, progress, and usable Back/Continue controls. Answers must remain attached to question order when navigating.
5. Submit `{ answers: number[] }` in Q1–Q10 order. Disable repeat submission while pending. On failure, keep answers and let the user retry.
6. Display the result using API data. Format fractions as percentages. Provide a way to retake the quiz that resets answers and result.
7. Include loading, empty/error/retry, submission, and result states. Keep the UI consistent with this project's existing design and support Burmese text.
8. Keep frontend and backend contracts aligned. Inspect the backend/API config in this workspace if available. Change backend code only if a concrete incompatibility prevents this flow; preserve the request and response contract above and explain any backend change.
9. Finish by summarizing changed files, required API URL/environment configuration, and how to run the connected app. Run only checks that are already part of this project's normal workflow; report checks that could not be run and why.

---
