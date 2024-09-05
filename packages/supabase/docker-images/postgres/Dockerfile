FROM supabase/postgres:15.6.1.116

RUN chown -R postgres:postgres /var/lib

# Switch to the non-root user
USER postgres

# Set the working directory
WORKDIR /home/postgres

# Add any additional commands or configurations here

# Expose the default PostgreSQL port
EXPOSE 5432