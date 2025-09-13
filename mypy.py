import subprocess
import sys

result: subprocess.CompletedProcess[str] = subprocess.run(
    ["mypy", "."], capture_output=True, text=True
)

print(result.stdout)
print(result.stderr, file=sys.stderr)

sys.exit(result.returncode)
