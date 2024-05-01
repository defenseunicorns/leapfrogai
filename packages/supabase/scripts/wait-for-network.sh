#!/bin/bash

RESOURCE_NAME="supabase-studio"
RESOURCE_TYPE="packages.uds.dev"
DESIRED_PHASE="Ready"

# Function to check the resource status
check_resource_status() {
    RESOURCE_STATUS=$(kubectl get $RESOURCE_TYPE $RESOURCE_NAME -o jsonpath='{.status.phase}')

    # Check if the resource is in the desired phase
    if [ "$RESOURCE_STATUS" == "$DESIRED_PHASE" ]; then
        echo "Resource $RESOURCE_NAME is in the $DESIRED_PHASE phase."
        return 0  # Return success
    else
        echo "Resource $RESOURCE_NAME is not in the $DESIRED_PHASE phase. Current status: $RESOURCE_STATUS"
        return 1  # Return failure
    fi
}

# Keep checking the resource status until it's in the desired phase
while true; do
    check_resource_status
    if [ $? -eq 0 ]; then
        break  # Exit the loop if the resource is in the desired phase
    fi
    sleep 5  # Wait for 5 seconds before checking again
done

echo "Script completed successfully."