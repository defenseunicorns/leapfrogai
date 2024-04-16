kubectl delete deployments supabase-* -n leapfrogai
helm uninstall supabase -n leapfrogai
zarf package remove supabase --confirm
