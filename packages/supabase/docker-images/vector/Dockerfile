FROM timberio/vector:0.34.0-alpine

# Create a new user named vector
RUN adduser -D vector

RUN chown -R vector:vector /var/lib/vector/

# Switch to the non-root user
USER vector
