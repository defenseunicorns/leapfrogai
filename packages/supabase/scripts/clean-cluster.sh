zarf package remove supabase --confirm
helm uninstall supabase -n leapfrogai
helm uninstall supabase-bootstrap -n leapfrogai
helm uninstall supabase-secrets-generator -n leapfrogai
kubectl delete pvc data-supabase-postgresql-0 -n leapfrogai
kubectl get crd --no-headers | awk '/konghq/ {print $1}' | xargs kubectl delete crd
