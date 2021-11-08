import os
import sys
import subprocess

from datetime import datetime


def get_complete_path(python_version):
    pv_storage_path = os.environ.get("RESULTS_PV_PATH", "./")
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    folder_name = dt_string + "_py" + str(python_version[0])
    complete_path = pv_storage_path + folder_name
    return complete_path


def main():
    python_version = sys.version_info
    if python_version[0] == 3:
        proc = subprocess.Popen(
            ["python3", "/app/application.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    elif python_version[0] == 2:
        proc = subprocess.Popen(
            ["python", "/app/application.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    else:
        sys.stderr.write("Unknown/Unsupported version of Python " + str(python_version) + ".X")
        return 1
    output, error = proc.communicate()
    if proc.returncode == 0 or proc.returncode == None:
        complete_path = get_complete_path(python_version)
        if not os.path.exists(complete_path):  # if for python2 (lack of support of exist_ok=True)
            os.makedirs(complete_path)  # create folder for artefacts
        with open(complete_path + "/stdout.txt", "w+") as text_file:  # don't handle exception let if fail
            text_file.write(output.decode("utf-8"))
        with open(complete_path + "/version.txt", "w+") as text_file:  # don't handle exception let if fail
            text_file.write(
                "Python " + str(python_version[0]) + "." + str(python_version[1]) + "." + str(python_version[2])
            )
        return 0
    else:
        sys.stderr.write(error)
        return 1


if __name__ == "__main__":
    main()
