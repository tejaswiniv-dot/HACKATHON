import json
CATEGORY_WEIGHTS = {
    "Privacy": 0.40,
    "Accessibility": 0.30,
    "Learning Quality": 0.30,
}

CHECKS = [
    # ---------- PRIVACY ----------
    {"id": "location", "category": "Privacy",
     "question": "No precise location collected", "points": 30,
     "why": "Children's location can reveal where they live or study."},
    {"id": "trackers", "category": "Privacy",
     "question": "No third-party ad or analytics trackers", "points": 30,
     "why": "Trackers follow children across apps to profile and target them."},
    {"id": "parental_consent", "category": "Privacy",
     "question": "Clear parental consent flow", "points": 25,
     "why": "Children cannot meaningfully agree to data collection themselves."},
    {"id": "data_deletion", "category": "Privacy",
     "question": "Easy request to delete data", "points": 15,
     "why": "Families should be able to remove a child's data at any time."},

    # ---------- ACCESSIBILITY ----------
    {"id": "screen_reader", "category": "Accessibility",
     "question": "Works with screen readers", "points": 40,
     "why": "Blind and low-vision learners cannot use the app without it."},
    {"id": "captions", "category": "Accessibility",
     "question": "Captions or transcripts for audio and video", "points": 30,
     "why": "Deaf and hard-of-hearing learners need text for spoken content."},
    {"id": "text_contrast", "category": "Accessibility",
     "question": "Adjustable text size and contrast", "points": 30,
     "why": "Readable text helps learners with low vision or dyslexia."},

    # ---------- LEARNING QUALITY ----------
    {"id": "objectives", "category": "Learning Quality",
     "question": "States clear learning objectives", "points": 35,
     "why": "Learners and teachers should know what a lesson teaches."},
    {"id": "feedback", "category": "Learning Quality",
     "question": "Gives meaningful feedback on answers", "points": 35,
     "why": "Feedback is how learners find and fix their mistakes."},
    {"id": "progress", "category": "Learning Quality",
     "question": "Tracks learner progress", "points": 30,
     "why": "Progress tracking shows whether the learner is improving."},
]


if __name__ == "__main__":
    print(f"{len(CHECKS)} checks loaded")
    for category in CATEGORY_WEIGHTS:
        total = sum(c["points"] for c in CHECKS if c["category"] == category)
        print(f"  {category}: {total} points")
        assert total == 100, f"{category} should total 100!"
    assert abs(sum(CATEGORY_WEIGHTS.values()) - 1) < 1e-9
    print("All good.")

def score_app(app):
    scores = {
    "Privacy": 0,
    "Accessibility": 0,
    "Learning Quality": 0
    }
    reasons=[]
    for check in CHECKS:
        answer = app["checks"][check["id"]]
        if answer == "yes":
            earned = check["points"]
        elif answer=="partial":
            earned = (check["points"])/2
        else:
            earned=0
        scores[check["category"]] += earned
        lost = check["points"] - earned
        if lost>0:
           reasons.append(f'{check["question"]}: lost {lost} points. {check["why"]}')
    
    trust_score = sum(
        scores[category] * weight
        for category, weight in CATEGORY_WEIGHTS.items()
    )

    return {
        "Privacy": scores["Privacy"],
        "Accessibility": scores["Accessibility"],
        "Learning Quality": scores["Learning Quality"],
        "Trust Score": round(trust_score, 2),
        "reasons": reasons
    }


with open("data/apps.json", "r") as file:
    apps = json.load(file)

for app in apps:
    result = score_app(app)
    print(app["name"], result["Trust Score"])

def find_alternatives(app):
    alternatives = []
    current_score = score_app(app)["Trust Score"]

    for other in apps:
        if other["name"] != app["name"] and other["category"] == app["category"]:
            other_score = score_app(other)["Trust Score"]

            if other_score > current_score:
                alternatives.append({
                    "name": other["name"],
                    "Trust Score": other_score
                })

    return alternatives


alternatives = find_alternatives(app)

print("Alternatives:")
if alternatives:
    for alt in alternatives:
        print(f'  - {alt["name"]} (Trust Score: {alt["Trust Score"]})')
else:
    print("  No better alternatives found.")
    print()
