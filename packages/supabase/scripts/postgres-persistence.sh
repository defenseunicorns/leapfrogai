if kubectl get secret "supabase-postgresql-backup" -n "leapfrogai" &>/dev/null; then
    echo "Secret already exists..."
else
    if kubectl get secret "supabase-postgresql" -n "leapfrogai" &>/dev/null; then
        kubectl get secret "supabase-postgresql" -n "leapfrogai" -o yaml | \
            sed "s/name: supabase-postgresql/name: supabase-postgresql-backup/" | \
            kubectl apply --namespace="leapfrogai" -f -
    else
        # Create an empty Secret if supabase-postgresql doesn't exist
        kubectl create secret generic "supabase-postgresql-backup" --from-literal=dummy=value --dry-run=client -o yaml | \
            kubectl apply --namespace="leapfrogai" -f -
    fi
fi