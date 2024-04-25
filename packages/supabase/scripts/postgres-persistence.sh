if ! kubectl get secret "supabase-postgresql-backup" -n "leapfrogai" &>/dev/null; then
    if kubectl get secret "supabase-postgresql" -n "leapfrogai" &>/dev/null; then
        kubectl get secret "supabase-postgresql" -n "leapfrogai" -o yaml | \
            sed "s/name: supabase-postgresql/name: supabase-postgresql-backup/" | \
            kubectl apply --namespace="leapfrogai" -f -
    else
        exit 1
    fi
fi