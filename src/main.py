import sys
import subprocess
from yaml import load, Loader
import argparse
from pathlib import Path
import json
from modules.secretmanagers import manage_secrets


def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--file", type=str, help="Path of encrypted file")
    parser.add_argument(
        "--gpg-gnupghome",
        type=str,
        help="Configured GPG home directory",
        default="{home_dir}/.gnupg".format(home_dir=Path.home()),
    )

    args = parser.parse_args(arguments)
    print(args)
    if args.file is None:
        raise Exception("File is required")

    # Decrypt with eyaml, gpg backend
    yaml_data = subprocess.run(
        [
            "eyaml",
            "decrypt",
            "-n",
            "gpg",
            "--gpg-gnupghome",
            args.gpg_gnupghome,
            "-f",
            args.file,
        ],
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8")

    secrets_data = load(yaml_data, Loader=Loader)

    print(json.dumps(secrets_data, indent=4))

    # for k in secrets_data:
    #     manage_secrets(secrets_data[k])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
