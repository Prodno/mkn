import subprocess


def test_proto_out() -> None:
    subprocess.run('/usr/local/bin/protoc --python_out=. schema.proto', shell=True, check=True)

    with open('./generated_schema.py', 'r') as fin:
        etalon = fin.read()
        etalon = etalon.replace('# type: ignore\n', '')
        etalon = etalon.replace('# flake8: noqa\n', '')

    with open('./schema_pb2.py', 'r') as fin:
        generated = fin.read()

    assert generated == etalon
