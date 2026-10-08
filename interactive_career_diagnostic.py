"""Run the Model 2 career diagnostic interactively in a terminal."""

from pathlib import Path

import joblib
import numpy as np

from career_diagnostic import QUESTIONS

MODEL_PATH = Path(__file__).resolve().with_name("career_diagnostic_pipeline.joblib")


def main() -> None:
    if not MODEL_PATH.is_file():
        raise SystemExit("Model file not found. Run generate_career_dataset.py and train_career_model.py first.")
    print("\nIT Career Diagnostic — ရွေးချယ်မှုတစ်ခုစီအတွက် 0 မှ 4 အထိ ရိုက်ထည့်ပါ။\n")
    answers: list[int] = []
    for index, item in enumerate(QUESTIONS, 1):
        print(f"Q{index}: {item['question']}")
        for option_index, option in enumerate(item["options"]):
            print(f"  {option_index}: {option}")
        while True:
            value = input("သင့်အဖြေ (0-4): ").strip()
            try:
                answer = int(value)
                if 0 <= answer <= 4:
                    answers.append(answer)
                    break
            except ValueError:
                pass
            print("ကျေးဇူးပြု၍ 0 မှ 4 အထိ ကိန်းပြည့်တစ်ခု ထည့်ပါ။")
        print()

    model = joblib.load(MODEL_PATH)
    sample = np.asarray(answers, dtype=int).reshape(1, -1)
    predicted_role = str(model.predict(sample)[0])
    probabilities = model.predict_proba(sample)[0]
    classes = model.named_steps["classifier"].classes_
    confidence = float(probabilities[list(classes).index(predicted_role)])
    print(f"သင့်အတွက် အကြံပြုထားသော အလုပ်အကိုင်: {predicted_role}")
    print(f"Confidence: {confidence:.1%}")
    print("Role probabilities:")
    for role, probability in sorted(zip(classes, probabilities), key=lambda pair: pair[1], reverse=True):
        print(f"  {role}: {probability:.1%}")


if __name__ == "__main__":
    main()
