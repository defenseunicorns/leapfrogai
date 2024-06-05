FROM cgr.dev/chainguard/bash:latest
ARG version="1.169.8"
ENV version=${version}

# Download the supabase cli
RUN mkdir /usr/local/bin
RUN curl -LO https://github.com/supabase/cli/releases/download/v${version}/supabase_linux_amd64.tar.gz
RUN tar -xzf supabase_linux_amd64.tar.gz -C /usr/local/bin/
RUN rm supabase_linux_amd64.tar.gz

# 65532 is the UID of the `nonroot` user in chainguard/static.  See: https://edu.chainguard.dev/chainguard/chainguard-images/reference/static/overview/#users
USER 65532:65532

# Download the migration scripts
COPY --chown=65532:65532 migrations/*.sql supabase/migrations/
