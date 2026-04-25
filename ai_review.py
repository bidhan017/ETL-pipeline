import subprocess
import sys

MODEL = "deepseek-coder"


def get_diff():
    """Get git diff vs main branch"""
    try:
        result = subprocess.run(
            ["git", "diff", "origin/main"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except Exception as e:
        print(f"Error getting diff: {e}")
        sys.exit(1)


def build_prompt(diff: str) -> str:
    return f"""
You are a senior Python engineer reviewing a pull request.

Review ONLY the following code diff:

{diff}

Focus on:
- bugs or incorrect logic
- bad practices
- missing edge cases
- inefficient pandas usage
- SQL/data pipeline issues

Rules:
- Be concise
- Only comment on real issues
- Ignore formatting (ruff already handles that)
- If no issues, say: "No major issues found"

Output:
- Bullet points
"""


def run_ollama(prompt: str):
    try:
        process = subprocess.run(
            ["ollama", "run", MODEL],
            input=prompt,
            text=True,
            capture_output=True,
        )
        return process.stdout
    except Exception as e:
        return f"Error running Ollama: {e}"


def main():
    diff = get_diff()

    if not diff.strip():
        print("No changes detected.")
        return

    prompt = build_prompt(diff)
    review = run_ollama(prompt)

    print("\n=== AI CODE REVIEW ===\n")
    print(review)


if __name__ == "__main__":
    main()