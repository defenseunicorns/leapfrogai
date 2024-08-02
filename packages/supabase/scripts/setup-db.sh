curl --insecure -L -X POST \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $SUPABASE_SERVICE_KEY" \
  -H "apiKey: $SUPABASE_SERVICE_KEY" \
  -d '{
    "tenant" : {
      "name": "supabase-realtime",
      "external_id": "supabase-realtime",
      "jwt_secret": "testenckeychaangethisforsuresure",
      "extensions": [
        {
          "type": "postgres_cdc_rls",
          "settings": {
            "db_name": "postgres",
            "db_host": "supabase-postgresql",
            "db_user": "supabase_admin",
            "db_password": "'$POSTGRESQL_PASSWORD'",
            "db_port": "5432",
            "region": "us-east-1",
            "publication": "supabase_realtime",
            "ssl_enforced": "false",
            "poll_interval_ms": "100",
            "poll_max_record_bytes": "1048576"
          }
        }
      ]
    }
  }' https://supabase-kong.leapfrogai.svc.cluster.local/realtime/v1/api/tenants