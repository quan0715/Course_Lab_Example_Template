Lab Test Runner (C++)

Overview
- Minimal cross-platform test runner for simple C++ lab problems.
- Runs on macOS/Linux via `run_tests.sh` and on Windows via `run_tests.bat`.
- Discovers problems `p1..pN` from `src/` and tests against `tests/`.

Layout
- `src/pX.cpp`: solution sources (e.g., `p1.cpp`, `p2_name.cpp`).
- `tests/pX/inputs/*.in`: input files for problem `pX`.
- `tests/pX/outputs/*.out`: expected outputs for matching inputs.
- `build/`: compiled binaries, logs, and intermediate outputs.
- `config/points.conf`: optional scoring weights per problem.

Running
- All problems (Linux/macOS): `bash run_tests.sh`
- One problem: `bash run_tests.sh p2`
- Force color on/off (TTY): `bash run_tests.sh --color` or `--no-color`
- Windows (cmd): `run_tests.bat` or `run_tests.bat p2`

Scoring
- Default: full points for a problem only if all its cases pass.
- Configure per-problem points in `config/points.conf`:
  - `problem.p1=50`
  - Leave absent to default to 100.
- The runner writes per-problem artifacts:
  - `build/pX.cases`: `"<passed> <total>"`
  - `build/pX.score`: `"<gained> <total_points>"`

Output
- Build per problem, per-case PASS/FAIL, and on failure prints:
  - Full Expected and Got content
  - Full unified diff (Linux/macOS) or `fc` difference (Windows)
  - EOL info on Linux/macOS
- Summary Table lists: `Problem | pass_test | fail_test | score`, with a final `total` row.

Windows Notes
- The batch runner normalizes CRLF vs LF before comparison to avoid spurious diffs.
- If compilation fails for a problem, all its test cases are counted as failed and score is 0.

CI
- GitHub Actions workflow runs tests on Ubuntu and Windows on every push and PR.

Example
```
bash run_tests.sh
```

