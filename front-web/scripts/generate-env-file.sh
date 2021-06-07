#!/bin/bash

env_var_prefix="VUE_APP"

usage() {
  echo "Usage: $0 [-o OUTPUT_DIRECTORY]"
  echo "  -o OUTPUT_DIRECTORY specify output directory"
  echo "  -h displays usage"
  exit 1
}

check_dir_exists() {
  if [[ -z $1 ]]; then
    echo "Output directory does not specified"
    exit 1
  fi

  if [[ ! -d $1 ]]; then
    echo "Specified directory does not exists"
    exit 1
  fi
}

# https://www.freecodecamp.org/news/how-to-implement-runtime-environment-variables-with-create-react-app-docker-and-nginx-7f9d42a91d70/
output_dir=$1

while getopts :o: opt; do
  case $opt in
    o)
      output_dir=$OPTARG
      check_dir_exists $output_dir
      ;;
    h)
      usage
      exit 1
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      exit 1
      ;;
  esac
done

check_dir_exists $output_dir

output_file="$output_dir/env-config.js"

# Recreate config file
rm -rf $output_file
touch $output_file

# Add assignment
echo "window.__ENV__ = {" >> $output_file

# Read each environment variable
env |
while read -r line || [[ -n "$line" ]];
do
  # Skip string that does not starts from REACT_APP
  if [[ $line != "$env_var_prefix"* ]]; then
    continue
  fi

  # Split env variables by character `=`
  if printf '%s\n' "$line" | grep -q -e '='; then
    varname=$(printf '%s\n' "$line" | sed -e 's/=.*//')
    varvalue=$(printf '%s\n' "$line" | sed -e 's/^[^=]*=//')

    # Append configuration property to JS file
    echo "  "$varname": \"$varvalue\"," >> $output_file

    echo "setting env var $varname=$varvalue"
  fi
done

echo "};" >> $output_file
