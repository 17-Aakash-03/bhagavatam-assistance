"""Builds train.jsonl from every scenarios_*.py file in this folder.
Run:  python make_dataset.py"""
import glob
import importlib.util
import json
from pathlib import Path

from main import is_info_question, ollama_system_prompt

HERE = Path(__file__).parent
records = []


def add(turns, final):
    """turns = alternating user/assistant texts, starting and ending with a user message."""
    n_users = (len(turns) + 1) // 2
    mode = "answer" if (n_users >= 4 or (n_users == 1 and is_info_question(turns[0]))) else "ask"
    messages = [{"role": "system", "content": ollama_system_prompt(mode, n_users)}]
    for i, text in enumerate(turns):
        messages.append({"role": "user" if i % 2 == 0 else "assistant", "content": text})
    messages.append({"role": "assistant", "content": json.dumps(final, ensure_ascii=False)})
    records.append({"messages": messages})


for path in sorted(glob.glob(str(HERE / "scenarios_*.py"))):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    for s in getattr(mod, "SCENARIOS", []):
        u, a = s["users"], s["asks"]
        assert len(u) == 4 and len(a) == 3, f"{path}: each scenario needs 4 users and 3 asks"
        add([u[0]], {"message": a[0]})
        add([u[0], a[0], u[1]], {"message": a[1]})
        add([u[0], a[0], u[1], a[1], u[2]], {"message": a[2]})
        add([u[0], a[0], u[1], a[1], u[2], a[2], u[3]],
            {"message": s["message"], "steps": s["steps"]})

    for q in getattr(mod, "INFO", []):
        add([q["question"]], {"message": q["message"], "steps": q["steps"]})

out = HERE / "train.jsonl"
with open(out, "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

asks = sum(1 for r in records if '"steps"' not in r["messages"][-1]["content"])
print(f"Wrote {len(records)} examples ({asks} questions, {len(records) - asks} answers) to {out.name}")