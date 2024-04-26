_format_version: "1.1"

    consumers:
      - username: DASHBOARD
      - username: anon
        keyauth_credentials:
            - key: {{SUPABASE_ANON_KEY}}
      - username: service_role
        keyauth_credentials:
            - key: {{SUPABASE_SERVICE_KEY}}

    ###
    ### Dashboard credentials
    ###
    basicauth_credentials:
      - consumer: DASHBOARD
        username: ###ZARF_CONST_DASHBOARD_USERNAME###
        password: ###ZARF_VAR_DASHBOARD_PASSWORD###

    acls:
      - consumer: anon
        group: anon
      - consumer: service_role
        group: admin

    services:
      - name: auth-v1-open
        url: http://supabase-auth:80/verify
        routes:
          - name: auth-v1-open
            strip_path: true
            paths:
              - /auth/v1/verify
        plugins:
          - name: cors
      - name: auth-v1-open-callback
        url: http://supabase-auth:80/callback
        routes:
          - name: auth-v1-open-callback
            strip_path: true
            paths:
              - /auth/v1/callback
        plugins:
          - name: cors
      - name: auth-v1-open-authorize
        url: http://supabase-auth:80/authorize
        routes:
          - name: auth-v1-open-authorize
            strip_path: true
            paths:
              - /auth/v1/authorize
        plugins:
          - name: cors

      - name: auth-v1
        _comment: "GoTrue: /auth/v1/* -> http://supabase-auth:80/*"
        url: http://supabase-auth:80
        routes:
          - name: auth-v1-all
            strip_path: true
            paths:
              - /auth/v1/
        plugins:
          - name: cors
          - name: key-auth
            config:
              hide_credentials: false
          - name: acl
            config:
              hide_groups_header: true
              allow:
                - admin
                - anon

      - name: rest-v1
        _comment: "PostgREST: /rest/v1/* -> http://supabase-rest:80/*"
        url: http://supabase-rest:80/
        routes:
          - name: rest-v1-all
            strip_path: true
            paths:
              - /rest/v1/
        plugins:
          - name: cors
          - name: key-auth
            config:
              hide_credentials: true
          - name: acl
            config:
              hide_groups_header: true
              allow:
                - admin
                - anon

      - name: realtime-v1
        _comment: "Realtime: /realtime/v1/* -> ws://supabase-realtime:80/socket/*"
        url: http://supabase-realtime:80/socket
        routes:
          - name: realtime-v1-all
            strip_path: true
            paths:
              - /realtime/v1/
        plugins:
          - name: cors
          - name: key-auth
            config:
              hide_credentials: false
          - name: acl
            config:
              hide_groups_header: true
              allow:
                - admin
                - anon

      - name: storage-v1
        _comment: "Storage: /storage/v1/* -> http://supabase-storage:80/*"
        url: http://supabase-storage:80/
        routes:
          - name: storage-v1-all
            strip_path: true
            paths:
              - /storage/v1/
        plugins:
          - name: cors

      - name: meta
        _comment: "pg-meta: /pg/* -> http://supabase-meta:80/*"
        url: http://supabase-meta:80/
        routes:
          - name: meta-all
            strip_path: true
            paths:
              - /pg/
        plugins:
          - name: key-auth
            config:
              hide_credentials: false
          - name: acl
            config:
              hide_groups_header: true
              allow:
                - admin

      ## Protected Dashboard - catch all remaining routes
      - name: dashboard
        _comment: 'Studio: /* -> http://studio:3000/*'
        url: http://supabase-studio:80/
        routes:
          - name: dashboard-all
            strip_path: true
            paths:
              - /
        plugins:
          - name: cors
          - name: basic-auth
            config:
              hide_credentials: false