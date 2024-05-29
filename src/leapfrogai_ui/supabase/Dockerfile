FROM alpine:latest

WORKDIR /home

ARG USER=leapfrogai
USER root

ARG version="1.169.8"
ENV version=${version}
RUN apk add --update sudo
RUN apk add --no-cache libc6-compat

# Install the supabase cli
RUN wget https://github.com/supabase/cli/releases/download/v${version}/supabase_${version}_linux_amd64.apk
RUN apk add --no-cache --allow-untrusted supabase_${version}_linux_amd64.apk
RUN rm supabase_${version}_linux_amd64.apk

# Add a new (non-root) user to run as
RUN adduser -D $USER \
        && echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER \
        && chmod 0440 /etc/sudoers.d/$USER
RUN chown -R leapfrogai:leapfrogai /home
USER $USER

# Copy all migration scripts
COPY migrations/*.sql supabase/migrations/
