"""Capture real CLI stderr and process exit codes, including the injected probe."""
import os
import subprocess
import sys
from pathlib import Path

scratch, output = map(Path, sys.argv[1:])
cases = [
    ("""echo '{"name":"","category":"spirit","unit":"oz"}' | ./mixology ingredients create --stdin""",
     [str(scratch / 'mixology'), 'ingredients', 'create', '--stdin'], 10,
     '{"name":"","category":"spirit","unit":"oz"}'),
    ('./mixology ingredients create --category spirit --unit oz "London Dry Gin"',
     [str(scratch / 'mixology'), 'ingredients', 'create', '--category', 'spirit', '--unit', 'oz', 'London Dry Gin'], 40, None),
    ('./deck-error-probe # injected Internal failure from chapter 1.3',
     [str(scratch / 'deck-error-probe')], 50, None),
]
transcript = []
for command, args, code, stdin in cases:
    result = subprocess.run(args, env=os.environ | {"MIXOLOGY_LOG_FILE": str(scratch / "cli.log")}, input=stdin, capture_output=True, text=True, check=False)
    assert result.returncode == code, (command, result.returncode, result.stderr)
    assert not result.stdout, (command, result.stdout)
    assert 'database is locked' not in result.stderr
    transcript.extend([f'$ {command}', result.stderr.strip(), '$ echo $?', str(result.returncode), ''])
(output / 'cli-errors.txt').write_text('\n'.join(transcript))
