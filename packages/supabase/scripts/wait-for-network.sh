#!/bin/bash

DEPLOYMENT_NAME="kong"
NAMESPACE="leapfrogai"
DESIRED_PHASE="Running"

get_pod_status() {
    POD_STATUSES=$(kubectl get pods -l app.kubernetes.io/name=$DEPLOYMENT_NAME -n $NAMESPACE -o jsonpath='{range .items[*]}{.status.phase}{" "}{end}')
}

check_deployment_status() {
    get_pod_status
    # Check if all pods are in the desired phase
    if [[ "$POD_STATUSES" == *"$DESIRED_PHASE"* ]] && ! [[ "$POD_STATUSES" == *"Pending"* ]]; then
        echo "All pods of deployment $DEPLOYMENT_NAME are in the $DESIRED_PHASE phase."
        return 0 # Return success
    else
        echo "Not all pods of deployment $DEPLOYMENT_NAME are in the $DESIRED_PHASE phase. Current status: $POD_STATUSES"
        return 1 # Return failure
    fi
}

# Keep checking the deployment status until all pods are in the desired phase
while true; do
    check_deployment_status
    if [ $? -eq 0 ]; then
        break # Exit the loop if all pods are in the desired phase
    fi
    sleep 5 # Wait for 5 seconds before checking again
done

echo "Script completed successfully."