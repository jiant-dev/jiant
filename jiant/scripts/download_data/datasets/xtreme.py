import os
import shutil

import jiant.scripts.download_data.utils as download_utils
import jiant.utils.python.datastructures as datastructures
import jiant.utils.python.io as py_io


def download_xnli_data_and_write_config(task_data_base_path: str, task_config_base_path: str):
    xnli_temp_path = py_io.get_dir(task_data_base_path, "xnli_temp")
    download_utils.download_and_unzip(
        "https://dl.fbaipublicfiles.com/XNLI/XNLI-1.0.zip", xnli_temp_path,
    )
    full_val_data = py_io.read_jsonl(os.path.join(xnli_temp_path, "XNLI-1.0", "xnli.dev.jsonl"))
    val_data = datastructures.group_by(full_val_data, key_func=lambda elem: elem["language"])
    full_test_data = py_io.read_jsonl(os.path.join(xnli_temp_path, "XNLI-1.0", "xnli.test.jsonl"))
    test_data = datastructures.group_by(full_test_data, lambda elem: elem["language"])
    languages = sorted(list(val_data))
    assert len(languages) == 15
    for lang in languages:
        task_name = f"xnli_{lang}"
        task_data_path = py_io.get_dir(task_data_base_path, task_name)
        val_path = os.path.join(task_data_path, "val.jsonl")
        test_path = os.path.join(task_data_path, "test.jsonl")
        py_io.write_jsonl(data=val_data[lang], path=val_path)
        py_io.write_jsonl(data=test_data[lang], path=test_path)
        py_io.write_json(
            data={
                "task": "xnli",
                "paths": {"val": val_path, "test": test_path,},
                "name": task_name,
            },
            path=os.path.join(task_config_base_path, f"{task_name}_config.json"),
        )
    shutil.rmtree(xnli_temp_path)
