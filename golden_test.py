import os
import subprocess
import tempfile

import pytest


@pytest.mark.golden_test("tests/*.yml")
def test_translator_and_machine(golden):
    with tempfile.TemporaryDirectory() as tmpdir:
        source = os.path.join(tmpdir, "source.txt")
        target = os.path.join(tmpdir, "target")
        target_mnem = os.path.join(tmpdir, "mnem_target.txt")
        input_1 = os.path.join(tmpdir, "input_1.json")
        input_2 = os.path.join(tmpdir, "input_2.json")
        output_1 = os.path.join(tmpdir, "output_1.json")
        output_2 = os.path.join(tmpdir, "output_2.json")
        log = os.path.join(tmpdir, "log.txt")

        with open(source, mode="w", encoding="utf-8") as f:
            f.write(golden["in_source"])
        with open(input_1, mode="w", encoding="utf-8") as f:
            f.write(golden["in_1_stdin"])
        with open(input_2, mode="w", encoding="utf-8") as f:
            f.write(golden["in_2_stdin"])

        subprocess.Popen(["python", "./translator/translator.py", source, target]).wait()
        subprocess.Popen(["python", "./CPU/main.py", target, input_1, input_2, output_1, output_2, log]).wait()

        with open(target_mnem, "r") as f:
            code = f.read()
            print(code)
        with open(output_2, "r") as f:
            output_2 = f.read()
        with open(output_1, "r") as f:
            output_1 = f.read()
        with open(log, "r") as f:
            log = f.read()

        assert code == golden["out_code"]
        assert output_2 == golden["out_2_stdout"]
        assert output_1 == golden["out_1_stdout"]
        assert log == golden["out_log"]