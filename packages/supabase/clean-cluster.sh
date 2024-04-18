helm uninstall supabase -n leapfrogai
zarf package remove supabase --confirm
kubectl delete data-supabase-postgresql-0 -n leapfrogai
