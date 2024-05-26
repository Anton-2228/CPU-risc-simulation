import os
import subprocess
import tempfile

import pytest

@pytest.mark.golden_test("tests/*.yml")
def test_translator_and_machine(golden):
    with tempfile.TemporaryDirectory() as tmpdir:
        source = os.path.join(tmpdir, "source.txt")
        target = os.path.join(tmpdir, "target.txt")
        input_str = os.path.join(tmpdir, "input_str.json")
        input_int = os.path.join(tmpdir, "input_int.json")
        output_str = os.path.join(tmpdir, "output_str.json")
        output_int = os.path.join(tmpdir, "output_int.json")
        log = os.path.join(tmpdir, "log.txt")

        with open(source, mode="w", encoding="utf-8") as f:
            f.write(golden["in_source"])
        with open(input_str, mode="w", encoding="utf-8") as f:
            f.write(golden["in_str_stdin"])
        with open(input_int, mode="w", encoding="utf-8") as f:
            f.write(golden["in_int_stdin"])

        subprocess.Popen(["python", "./translator/translator.py", source, target]).wait()
        subprocess.Popen(["python", "./CPU/main.py", target, input_str, input_int, output_str, output_int, log]).wait()

        with open(target, "r") as f:
            code = f.read()
        with open(output_int, "r") as f:
            output_int = f.read()
        with open(output_str, "r") as f:
            output_str = f.read()
        with open(log, "r") as f:
            log = f.read()

        assert code == golden["out_code"]
        assert output_int == golden["out_int_stdout"]
        assert output_str == golden["out_str_stdout"]
        assert log == golden["out_log"]