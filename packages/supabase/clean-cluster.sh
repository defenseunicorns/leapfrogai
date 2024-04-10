kubectl delete deployments --all -n leapfrogai
helm uninstall supabase -n leapfrogai
zarf package remove supabase --confirm