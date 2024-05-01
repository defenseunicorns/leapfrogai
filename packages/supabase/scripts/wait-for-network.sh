#!/bin/bash
DEPLOYMENT_NAME="kong"
NAMESPACE="leapfrogai"
DESIRED_PHASE="Running"
DESIRED_READY_STATUS="True"

get_pod_status() {
    POD_STATUSES=$(kubectl get pods -l app.kubernetes.io/name=$DEPLOYMENT_NAME -n $NAMESPACE -o jsonpath='{range .items[*]}{.status.phase}{" "}{.status.containerStatuses[*].ready}{" "}{end}')
}

check_deployment_status() {
    get_pod_status
    # Check if all pods are in the desired phase and ready status
    if [[ "$POD_STATUSES" == *"$DESIRED_PHASE"* ]] && [[ "$POD_STATUSES" == *"$DESIRED_READY_STATUS"* ]] && ! [[ "$POD_STATUSES" == *"Pending"* ]]; then
        echo "All pods of deployment $DEPLOYMENT_NAME are in the $DESIRED_PHASE phase and ready."
        return 0 # Return success
    else
        echo "Not all pods of deployment $DEPLOYMENT_NAME are in the $DESIRED_PHASE phase and ready. Current status: $POD_STATUSES"
        return 1 # Return failure
    fi
}

check_deployment_status
if [ $? -eq 0 ]; then
    echo "Script completed successfully."
    exit 0
fi

# Keep checking the deployment status until all pods are in the desired phase and ready
while true; do
    check_deployment_status
    if [ $? -eq 0 ]; then
        break # Exit the loop if all pods are in the desired phase and ready
    fi
    sleep 5 # Wait for 5 seconds before checking again
done

echo "Script completed successfully."