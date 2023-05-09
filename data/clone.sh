#!/bin/bash

# The file containing the list of git repos, one per line
repo_list_file="github.txt"

# The base directory where the repositories will be cloned
clone_base_dir="git"

# Make sure the base directory exists
mkdir -p "$clone_base_dir"

while read -r repo_url; do

    # Extract the repo name from the URL
    repo_name=$(basename "$repo_url" .git)
     hostname=$(echo "$repo_url" | grep -oP '(?<=:\/\/)[^/]+')
    # Define the local repo directory
    local_repo_dir="$clone_base_dir/$hostname/$repo_name"
    
    # Check if the local repo directory exists
    if [[ -d "$local_repo_dir" ]]; then
        echo "Updating existing repo: $repo_name"
       
        cd "$local_repo_dir"
        git pull
        cd - >/dev/null
    else
        echo "Cloning new repo: $repo_name"
        git clone "$repo_url" "$local_repo_dir"
    fi
done < github.txt