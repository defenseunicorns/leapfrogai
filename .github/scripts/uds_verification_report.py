#!/usr/bin/env python3

import os
import re
import sys

# Explicitly set the encoding, mainly for emoji handling
sys.stdin = open(sys.stdin.fileno(), mode="r", encoding="utf-8", errors="ignore")


def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)


# CI environment variable enables GitHub annotations
def print_package_info(
    package_name,
    failures_count,
    errors_count,
    warnings_count,
    failure_descriptions,
    error_descriptions,
    warning_descriptions,
):
    if package_name:
        print("-----------------------------")
        if os.getenv("CI") == "true":
            print(f"::group::{package_name}")
        print(f"Package: {package_name}\n")
        if failures_count > 0:
            if os.getenv("CI") == "true":
                print("::error::", end="")
            print(f"⛔ Failures: {failures_count}")
        else:
            if errors_count > 0:
                if os.getenv("CI") == "true":
                    print("::error::", end="")
                print(f"❌ Errors: {errors_count}")
            if warnings_count > 0:
                if os.getenv("CI") == "true":
                    print("::warning::", end="")
                print(f"⚠️  Warnings: {warnings_count}")
        if failures_count > 0:
            print("\n⛔ Failure Descriptions:")
            for desc in failure_descriptions:
                print(f"  - {desc}")
        else:
            if errors_count > 0:
                print("\n❌ Error Descriptions:")
                for desc in error_descriptions:
                    print(f"  - {desc}")
            if warnings_count > 0:
                print("\n⚠️  Warning Descriptions:")
                for desc in warning_descriptions:
                    print(f"  - {desc}")
        if os.getenv("CI") == "true":
            print("::endgroup::")


def main():
    # Read data from stdin
    data = sys.stdin.read()
    # Remove ANSI escape sequences
    clean_data = remove_ansi_escape_sequences(data)
    # Initialize variables
    package_name = ""
    failures_count = 0
    errors_count = 0
    warnings_count = 0
    failure_descriptions = []
    error_descriptions = []
    warning_descriptions = []
    previous_package_name = None

    # Process each line
    for line in clean_data.splitlines():
        # Remove leading and trailing whitespace
        line = line.strip()

        # Match and extract the package name
        match = re.match(r"^ℹ️\s+Package\s+Name:\s+(.*)$", line)
        if match:
            # Print the previous package's info before starting a new one
            if previous_package_name is not None:
                print_package_info(
                    previous_package_name,
                    failures_count,
                    errors_count,
                    warnings_count,
                    failure_descriptions,
                    error_descriptions,
                    warning_descriptions,
                )
            # Reset variables for the new package
            package_name = match.group(1)
            failures_count = 0
            errors_count = 0
            warnings_count = 0
            failure_descriptions = []
            error_descriptions = []
            warning_descriptions = []
            previous_package_name = package_name
            continue

        # Match and extract counts for failures, errors, and warnings
        match = re.match(r"^(❌|⚠️|⛔)\s+(\d+)\s+([a-z]+)\s+found$", line)
        if match:
            count = int(match.group(2))
            type_ = match.group(3)
            if type_ == "errors":
                errors_count = count
            elif type_ == "warnings":
                warnings_count = count
            elif type_ == "failures":
                failures_count = count
            continue

        # Match and collect issue descriptions
        match = re.match(r"^(❌|⚠️|⛔)\s+(.*)$", line)
        if match:
            emoji = match.group(1)
            description = match.group(2)
            if emoji == "❌":
                error_descriptions.append(description)
            elif emoji == "⚠️":
                warning_descriptions.append(description)
            elif emoji == "⛔":
                failure_descriptions.append(description)
            continue

    # Print the last package's information
    if previous_package_name is not None:
        print_package_info(
            previous_package_name,
            failures_count,
            errors_count,
            warnings_count,
            failure_descriptions,
            error_descriptions,
            warning_descriptions,
        )


if __name__ == "__main__":
    main()
