package openai

import (
	"database/sql"
	"fmt"
	"os"

	_ "github.com/lib/pq"
)

func ConnectDB() (*sql.DB, error) {
	// Read database configuration from environment variables
	dbUser := os.Getenv("DB_USER")
	dbPass := os.Getenv("DB_PASS")
	dbHost := os.Getenv("DB_HOST")
	dbPort := os.Getenv("DB_PORT")
	dbName := os.Getenv("DB_NAME")

	// Check if any required environment variables are missing
	if dbUser == "" || dbPass == "" || dbHost == "" || dbPort == "" || dbName == "" {
		return nil, fmt.Errorf("one or more required environment variables are not set")
	}

	// Create the connection string
	connectionString := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable", dbUser, dbPass, dbHost, dbPort, dbName)

	db, err := sql.Open("postgres", connectionString)
	if err != nil {
		return nil, fmt.Errorf("error connecting to the database: %w", err)
	}

	// Check the connection
	err = db.Ping()
	if err != nil {
		db.Close()
		return nil, fmt.Errorf("error pinging the database: %w", err)
	}

	fmt.Println("Successfully connected to the database!")
	return db, nil
}
