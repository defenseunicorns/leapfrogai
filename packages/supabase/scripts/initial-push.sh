docker pull supabase/studio:20230127-6bfd87b
docker tag supabase/studio:20230127-6bfd87b localhost:5000/supabase/studio:20230127-6bfd87b
docker push localhost:5000/supabase/studio:20230127-6bfd87b

docker pull supabase/postgres:14.1.0.105
docker tag supabase/postgres:14.1.0.105 localhost:5000/supabase/postgres:14.1.0.105
docker push localhost:5000/supabase/postgres:14.1.0.105

docker pull postgres:15-alpine
docker tag postgres:15-alpine localhost:5000/postgres:15-alpine
docker push localhost:5000/postgres:15-alpine

docker pull supabase/gotrue:v2.146.0
docker tag supabase/gotrue:v2.146.0 localhost:5000/supabase/gotrue:v2.146.0
docker push localhost:5000/supabase/gotrue:v2.146.0

docker pull postgrest/postgrest:latest
docker tag postgrest/postgrest:latest localhost:5000/postgrest/postgrest:latest
docker push localhost:5000/postgrest/postgrest:latest

docker pull supabase/realtime:v2.1.0
docker tag supabase/realtime:v2.1.0 localhost:5000/supabase/realtime:v2.1.0
docker push localhost:5000/supabase/realtime:v2.1.0

docker pull supabase/storage-api:v0.26.1
docker tag supabase/storage-api:v0.26.1 localhost:5000/supabase/storage-api:v0.26.1
docker push localhost:5000/supabase/storage-api:v0.26.1

docker pull kong:2.8.1
docker tag kong:2.8.1 localhost:5000/kong:2.8.1
docker push localhost:5000/kong:2.8.1

docker pull supabase/postgres-meta:latest
docker tag supabase/postgres-meta:latest localhost:5000/supabase/postgres-meta:latest
docker push localhost:5000/supabase/postgres-meta:latest