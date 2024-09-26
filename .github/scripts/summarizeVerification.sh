#!/bin/bash

# Initialize variables
in_package=false
package_name=""
error_count=0
warning_count=0
error_descriptions=()
warning_descriptions=()

# Function to strip ANSI escape sequences
strip_ansi() {
	echo -e "$1" | sed -r 's/\x1B\[[0-9;]*[a-zA-Z]//g'
}

while IFS= read -r line; do
	# Strip ANSI escape sequences
	clean_line=$(strip_ansi "$line")
	# Remove leading/trailing whitespace
	clean_line=$(echo "$clean_line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

	# Check for the start of a new package
	if [[ $clean_line =~ ^•[[:space:]]+Running\ \"Verify\ ([^\"]+)\"$ ]]; then
		new_package_name="${BASH_REMATCH[1]}"
		if [[ $new_package_name != "that the package meets UDS badging standards" ]]; then
			# If we're already in a package, print its summary
			if [ "$in_package" = true ]; then
				echo -e "Package: $package_name"
				echo -e "❌ Errors: $error_count"
				echo -e "⚠️  Warnings: $warning_count"
				if [ $error_count -gt 0 ]; then
					echo "❌ Error Descriptions:"
					for err in "${error_descriptions[@]}"; do
						echo "  - $err"
					done
				fi
				if [ $warning_count -gt 0 ]; then
					echo "⚠️  Warning Descriptions:"
					for warn in "${warning_descriptions[@]}"; do
						echo "  - $warn"
					done
				fi
				echo "-----------------------------"
			fi
			# Start new package
			in_package=true
			package_name="$new_package_name"
			error_count=0
			warning_count=0
			error_descriptions=()
			warning_descriptions=()
		fi
	fi

	# Capture error descriptions
	if [[ $in_package == true && $clean_line =~ ^❌ ]]; then
		# Ignore summary lines
		if [[ $clean_line =~ errors\ found$ ]]; then
			# Extract the error count from the line
			error_count_line=$(echo "$clean_line" | grep -oP '(?<=❌ )[0-9]+(?= errors found)')
			if [[ -n $error_count_line ]]; then
				error_count="$error_count_line"
			fi
		elif [[ $clean_line =~ ^❌[[:space:]][0-9]+ ]]; then
			continue
		else
			error_descriptions+=("$(echo "$clean_line" | sed 's/^❌[[:space:]]*//')")
			((error_count++))
		fi
	fi

	# Capture warning descriptions
	if [[ $in_package == true && $clean_line =~ ^⚠️ ]]; then
		# Ignore summary lines
		if [[ $clean_line =~ warnings\ found$ ]]; then
			# Extract the warning count from the line
			warning_count_line=$(echo "$clean_line" | grep -oP '(?<=⚠️  )[0-9]+(?= warnings found)')
			if [[ -n $warning_count_line ]]; then
				warning_count="$warning_count_line"
			fi
		elif [[ $clean_line =~ ^⚠️[[:space:]][0-9]+ ]]; then
			continue
		else
			warning_descriptions+=("$(echo "$clean_line" | sed 's/^⚠️[[:space:]]*//')")
			((warning_count++))
		fi
	fi

	# Check for the end of a package
	if [[ $in_package == true && $clean_line =~ ^✔[[:space:]]+Completed\ \"Verify\ $package_name\"$ ]]; then
		# Print summary
		echo -e "Package: $package_name"
		echo -e "❌ Errors: $error_count"
		echo -e "⚠️  Warnings: $warning_count"
		if [ $error_count -gt 0 ]; then
			echo "❌ Error Descriptions:"
			for err in "${error_descriptions[@]}"; do
				echo "  - $err"
			done
		fi
		if [ $warning_count -gt 0 ]; then
			echo "⚠️  Warning Descriptions:"
			for warn in "${warning_descriptions[@]}"; do
				echo "  - $warn"
			done
		fi
		echo "-----------------------------"
		in_package=false
	fi
done <output.txt

# If we're still in a package after the loop, print its summary
if [ "$in_package" = true ]; then
	echo -e "Package: $package_name"
	echo -e "❌ Errors: $error_count"
	echo -e "⚠️  Warnings: $warning_count"
	if [ $error_count -gt 0 ]; then
		echo "❌ Error Descriptions:"
		for err in "${error_descriptions[@]}"; do
			echo "  - $err"
		done
	fi
	if [ $warning_count -gt 0 ]; then
		echo "⚠️  Warning Descriptions:"
		for warn in "${warning_descriptions[@]}"; do
			echo "  - $warn"
		done
	fi
	echo "-----------------------------"
fi
