helm uninstall supabase -n leapfrogai
zarf package remove supabase --confirm
kubectl delete pvc data-supabase-postgresql-0 -n leapfrogai
kubectl get crd --no-headers | awk '/konghq/ {print $1}' | xargs kubectl delete crd