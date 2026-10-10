# Model 2: IT Career Diagnostic — Frontend Integration Guide

## Deploy the API on Render and connect a Vercel frontend

This repository is the FastAPI backend. Deploy it as a **Render Web Service**, then set the deployed API URL in your frontend project on Vercel. The frontend itself should be deployed separately from its own repository or project directory.

### 1. Create the Render Web Service

1. Push this backend repository to GitHub, GitLab, or Bitbucket and connect it to Render.
2. In Render, choose **New → Web Service** and select this repository.
3. Use these settings (set **Root Directory** to the backend folder if this repository is inside a monorepo):

   | Setting | Value |
   | --- | --- |
   | Runtime | Python 3 |
   | Build Command | `pip install -r requirements.txt && python generate_career_dataset.py && python train_career_model.py` |
   | Start Command | `uvicorn app:app --host 0.0.0.0 --port $PORT` |

The build command creates `career_diagnostic_dataset.csv` and the required `career_diagnostic_pipeline.joblib` model artifact on each deploy. The generated files do not need to be committed. Render's `$PORT` environment variable is required for the service to receive traffic.

After the first deploy, copy the service's public URL, such as `https://your-api.onrender.com`. Check that URL in a browser; `/` should return a JSON response with `"status":"ok"`. API docs are at `/docs`.

### 2. Point the Vercel frontend at Render

In the Vercel project, open **Settings → Environment Variables** and add the variable your frontend reads for its API base URL. Use the deployed Render URL without a trailing slash:

| Frontend framework | Common environment variable | Example value |
| --- | --- | --- |
| Vite | `VITE_API_BASE_URL` | `https://your-api.onrender.com` |
| Next.js (browser code) | `NEXT_PUBLIC_API_BASE_URL` | `https://your-api.onrender.com` |
| Create React App | `REACT_APP_API_BASE_URL` | `https://your-api.onrender.com` |

Use the variable name already expected by your frontend if it differs. In browser code, call the API using that configured base URL, for example:

```js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL; // Vite example
const response = await fetch(`${API_BASE_URL}/api/v1/career/questions`);
```

For Next.js, read `process.env.NEXT_PUBLIC_API_BASE_URL` instead. Set the variable for the relevant Vercel environments (Production, Preview, and/or Development), then redeploy so the new value is included in the frontend build. These public variables are visible to browser users; use them for the API URL only, never secrets.

### 3. Verify the connection

- Open `https://your-api.onrender.com/api/v1/career/questions`; it should return the question list.
- Load the Vercel site and confirm its quiz can fetch questions and submit predictions.
- If the browser reports a CORS error, check that requests target the exact Render service URL and that the frontend is calling the API directly. This backend currently allows cross-origin requests from all origins. If you later restrict CORS, add the exact Vercel production and preview origins in `app.py` and redeploy.

Render free instances may sleep while idle and take time to respond on the first request after waking. For a production experience without that delay, choose a Render plan that keeps the service running.

### Local development

This repository provides the backend for a Burmese-language career quiz. Use this guide as the implementation contract for a React Native frontend (Expo or bare React Native). The app should load questions from the API, collect one answer per question, submit all ten answers, and show the predicted role plus a percentage chart of the model's role probabilities.

## What the backend provides

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | API health check |
| `GET` | `/api/v1/career/questions` | Burmese question text and answer options |
| `POST` | `/api/v1/career/predict` | Predicted role, confidence, and role probabilities |

The API permits cross-origin requests. React Native native apps generally do not enforce browser CORS, but the setting is useful if this same API is called from a web frontend.

## 1. Start the backend

From the backend repository root, create the model artifact before starting the API:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python generate_career_dataset.py
python train_career_model.py
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Keep the terminal running. Check `http://127.0.0.1:8000/` from the backend computer; it should return `{"status":"ok", ...}`. The trained model file is required or prediction requests return HTTP 503.

### Choose the correct API base URL

Do not use `localhost` on a physical phone: it points to the phone itself. Set one base URL per development environment:

| Frontend runs on | Example base URL |
| --- | --- |
| Same computer / iOS Simulator | `http://127.0.0.1:8000` |
| Android Studio emulator | `http://10.0.2.2:8000` |
| Physical phone on same Wi-Fi | `http://<computer-LAN-IP>:8000` |

For a physical phone, allow local network access through the computer firewall and ensure both devices are on the same network. Use HTTPS and an appropriately secured backend when deploying beyond local development.

Keep the URL in one configuration value (for example `src/config/api.ts`) so it can be switched for local, staging, and production builds. Do not scatter it across screens.

## 2. Suggested frontend structure

```text
src/
  api/
    careerApi.ts       # fetch questions and submit answers
  components/
    ProgressBar.tsx
    ProbabilityChart.tsx
  screens/
    QuizScreen.tsx
    ResultScreen.tsx
  types/
    career.ts
  config/
    api.ts
```

Use React Navigation or the routing system already in the app. The essential screens are:

1. **Quiz screen**: one Burmese question at a time, five clearly selectable options, progress (for example `3 / 10`), Back and Continue buttons.
2. **Submitting state**: prevent duplicate submissions and show a clear loading indicator.
3. **Result screen**: prominent predicted role, confidence percentage, and a chart showing probabilities for all nine roles. Include a Retake action that clears prior answers.
4. **Error state**: preserve answers if submission fails and let the user retry.

Store answers by question index or ID, not only as a sequence of taps. When submitting, construct the array in Q1–Q10 order; navigating Back must not change which answer belongs to which question.

## 3. Fetch and display the questions

`GET /api/v1/career/questions` returns the following shape:

```json
{
  "questions": [
    {
      "id": "Q1",
      "text": "Software project တစ်ခု ဖန်တီးတဲ့အခါ ဘယ်အပိုင်းကို လုပ်ရတာ အစိတ်လှုပ်ရှားဆုံးလဲ?",
      "options": [
        { "value": 0, "label": "AI Model များကို Train ခြင်း၊ Dataset များ ပြင်ဆင်ခြင်း" },
        { "value": 1, "label": "Visual Layout၊ UI Interaction များ ဖန်တီးခြင်း" },
        { "value": 2, "label": "Domain Logic နှင့် Ontology/Rules များ စီစဉ်ခြင်း" },
        { "value": 3, "label": "Server Code နှင့် API Logic များ ရေးသားခြင်း" },
        { "value": 4, "label": "Database Schema ဒီဇိုင်းထုတ်ခြင်းနှင့် Data Flow ကိုင်တွယ်ခြင်း" }
      ]
    }
  ]
}
```

The actual response contains all ten questions. Option `value` is the answer sent to the API (integer 0–4); it is not a question number. Render the `label` as text and submit the `value`. Fetch once when entering the quiz, keep the response in screen/app state, and show an error/retry state if the request fails.

## 4. Submit the quiz

Send exactly ten integers in Q1-to-Q10 order:

```http
POST /api/v1/career/predict
Content-Type: application/json
```

```json
{
  "answers": [3, 0, 4, 1, 0, 1, 1, 1, 2, 0]
}
```

Example using the built-in `fetch` API:

```ts
const response = await fetch(`${API_BASE_URL}/api/v1/career/predict`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ answers }),
});

if (!response.ok) {
  const detail = await response.json().catch(() => null);
  throw new Error(detail?.detail ?? `Request failed (${response.status})`);
}

const result: CareerPrediction = await response.json();
```

Validate locally before sending: there must be ten answers and every answer must be an integer from 0 to 4. The backend validates this too and returns HTTP 422 for invalid request data.

## 5. Result contract and percentage chart

Successful prediction response:

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

The values above are illustrative. The API returns all nine role keys, including `0.0` for a class the trained model did not learn. `confidence` is the predicted role's probability. Each probability is a fraction from 0 to 1; multiply by 100 for a percentage. For example, `0.73` displays as `73%`.

For a chart:

1. Convert `Object.entries(result.probabilities)` into `{ role, percent }` rows using `percent = probability * 100`.
2. Sort from highest to lowest probability for readability.
3. Render all nine roles. A horizontal bar chart works well with long role names; show the role label and a rounded percentage next to each bar.
4. Give the predicted role a distinct color or badge, and label it as the model's result.
5. Use a consistent 0–100% scale. Avoid rounding the underlying values before sorting or drawing bars.

The values are Random Forest class probability estimates from a synthetic training dataset. Present them as model estimates or likelihoods, not as guaranteed real-world career suitability or measured labor-market probabilities. The chart probabilities are not the deterministic weighted score breakdown for the user's answers.

The question bank and answer mappings are fixed by the backend. The frontend should not recompute the prediction or translate answer indices into roles; submit the answers and display the API result.

## 6. TypeScript types

```ts
export type CareerOption = { value: number; label: string };
export type CareerQuestion = {
  id: `Q${number}`;
  text: string;
  options: CareerOption[];
};
export type CareerQuestionsResponse = { questions: CareerQuestion[] };
export type CareerPrediction = {
  predicted_role: string;
  confidence: number;
  probabilities: Record<string, number>;
};
```

## 7. Loading, errors, and usability

- `GET /` unavailable: show that the service cannot be reached and offer retry.
- `GET /api/v1/career/questions` failure: do not start an empty quiz; show retry.
- `POST /api/v1/career/predict` HTTP 422: show a validation message; this usually means the frontend sent malformed answers.
- `POST /api/v1/career/predict` HTTP 503: model artifact is missing; generate and train it on the backend, then retry.
- Network timeout or offline: keep all selected answers and provide a retry action.
- Disable Continue until the current question has an answer. Disable submit while the request is in flight.
- Make option controls large enough to tap, indicate the selected state without color alone, and support Burmese Unicode fonts.
- Add accessible labels to choices and chart rows. The result must remain understandable if chart colors are not distinguishable.

## Backend review notes and current limitations

- The backend now provides `GET /api/v1/career/questions` so the frontend can use the canonical question text/options.
- The prediction response has a stable set of all nine role names for chart rendering.
- The supplied answer choices have no C/C++ or low-level systems option. Consequently the `Game / Embedded Systems Developer` class receives no generated training examples and its chart value will be zero with the current dataset/model. Add a relevant quiz option and update its role mapping before expecting the model to recommend that role.
- The training dataset is synthetic and the model is trained to reproduce the scoring labels. The result is suitable as a project diagnostic/demo, not as a validated career assessment.

## Backend repository commands

```bash
python generate_career_dataset.py
python train_career_model.py
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

API documentation is available at `http://127.0.0.1:8000/docs` while the server is running.
