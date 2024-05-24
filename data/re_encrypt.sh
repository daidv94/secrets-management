#!/usr/bin/env bash

set -e

recrypt() {
  file=$1
  echo "---> Recrypting: ${file}."
  eyaml recrypt -d gpg ${file} --gpg-always-trust --gpg-recipients-file=recipients
  echo "${file} recryped!!!"
}

# Get all variable files
for file in $(find . -type f -name "*.yaml"); do
  recrypt ${file}
done

echo "##### All hieradata recrypted #####"
