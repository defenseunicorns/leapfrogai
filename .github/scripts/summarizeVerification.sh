#!/bin/bash

# Remove ANSI escape sequences from the data
clean_data=$(sed -E 's/\x1b\[[0-9;]*[a-zA-Z]//g')

# Initialize variables
package_name=""
failures_count=0
errors_count=0
warnings_count=0
failure_descriptions=()
error_descriptions=()
warning_descriptions=()

# Function to print package information
print_package_info() {
	if [[ -n $package_name ]]; then
		echo "-----------------------------"
		if [[ ${CI} == "true" ]]; then
			echo "::group::$package_name"
		fi
		echo "Package: $package_name"
		if ((failures_count > 0)); then
			if [[ ${CI} == "true" ]]; then
				printf "::error::"
			fi
			echo "⛔ Failures: $failures_count"
		else
			if ((errors_count > 0)); then
				if [[ ${CI} == "true" ]]; then
					printf "::error::"
				fi
				echo "❌ Errors: $errors_count"
			fi
			if ((warnings_count > 0)); then
				if [[ ${CI} == "true" ]]; then
					printf "::warning::"
				fi
				echo "⚠️  Warnings: $warnings_count"
			fi
		fi

		if ((failures_count > 0)); then
			echo
			echo "⛔ Failure Descriptions:"
			for desc in "${failure_descriptions[@]}"; do
				echo "  - $desc"
			done
		else
			if ((errors_count > 0)); then
				echo
				echo "❌ Error Descriptions:"
				for desc in "${error_descriptions[@]}"; do
					echo "  - $desc"
				done
			fi
			if ((warnings_count > 0)); then
				echo
				echo "⚠️  Warning Descriptions:"
				for desc in "${warning_descriptions[@]}"; do
					echo "  - $desc"
				done
			fi
		fi
	fi
	if [[ ${CI} == "true" ]]; then
		echo "::endgroup::"
	fi
}

# Process each line of the cleaned data
while IFS= read -r line; do
	# Remove leading and trailing whitespace
	line=$(echo "$line" | sed 's/^[ \t]*//;s/[ \t]*$//')

	# Match and extract the package name
	if [[ $line =~ ^ℹ️[[:space:]]+Package[[:space:]]+Name:[[:space:]]+(.*)$ ]]; then
		# Print the previous package's info before starting a new one
		print_package_info
		# Reset variables for the new package
		package_name="${BASH_REMATCH[1]}"
		failures_count=0
		errors_count=0
		warnings_count=0
		failure_descriptions=()
		error_descriptions=()
		warning_descriptions=()
	# Match and extract counts for failures, errors, and warnings
	elif [[ $line =~ ^(❌|⚠️|⛔)[[:space:]]+([0-9]+)[[:space:]]+([a-z]+)[[:space:]]+found$ ]]; then
		count="${BASH_REMATCH[2]}"
		type="${BASH_REMATCH[3]}"
		case "$type" in
		"errors")
			errors_count=$count
			;;
		"warnings")
			warnings_count=$count
			;;
		"failures")
			failures_count=$count
			;;
		esac
	# Match and collect issue descriptions
	elif [[ $line =~ ^(❌|⚠️|⛔)[[:space:]]+(.*)$ ]]; then
		emoji="${BASH_REMATCH[1]}"
		description="${BASH_REMATCH[2]}"
		case "$emoji" in
		"❌")
			error_descriptions+=("$description")
			;;
		"⚠️")
			warning_descriptions+=("$description")
			;;
		"⛔")
			failure_descriptions+=("$description")
			;;
		esac
	fi
done <<<"$clean_data"

# Print the last package's information
print_package_info
