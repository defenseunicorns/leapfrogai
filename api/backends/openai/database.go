package openai

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	_ "github.com/lib/pq"
	"github.com/sashabaranov/go-openai"
)

type DBHandler struct {
	db                        *sql.DB
	insertChatCompletionQuery *sql.Stmt
}

func ConnectDB() (*DBHandler, error) {
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

	// Set the maximum number of open connections in the pool
	db.SetMaxOpenConns(10)

	// Set the maximum number of idle connections in the pool
	db.SetMaxIdleConns(5)

	// Check the connection
	err = db.Ping()
	if err != nil {
		db.Close()
		return nil, fmt.Errorf("error pinging the database: %w", err)
	}

	// Define the chat_completion INSERT query
	chatCompletionInsertQuery := "INSERT INTO chat_completion (request_timestamp, username, model_name, messages, response) " +
		"VALUES ($1, $2, $3, $4, $5)"

	// Prepare the statement
	chatCompletionInsertStatement, err := db.Prepare(chatCompletionInsertQuery)
	if err != nil {
		log.Fatal(err)
	}

	dbHandler := DBHandler{db, chatCompletionInsertStatement}

	fmt.Println("Successfully connected to the database!")
	return &dbHandler, nil
}

func (h *DBHandler) saveChat(username string, modelName string, messages []openai.ChatCompletionMessage, response string) error {
	// Get the current UTC time as a time.Time value
	currentTime := time.Now().UTC()

	// Format the time as a string in the desired timestamp format (e.g., "2006-01-02 15:04:05")
	timestamp := currentTime.Format("2006-01-02 15:04:05")
	messagesJSONBytes, err := json.Marshal(messages)
	if err != nil {
		log.Printf("Failed to marshal request messages to json")
		return err
	}
	responseJSONBytes, err := json.Marshal(fmt.Sprintf(`{"role": "assistant", "content": "%s"}`, response))
	if err != nil {
		log.Printf("Failed to marshal response messages to json")
		return err
	}

	// Execute the query with the provided data
	_, err = h.insertChatCompletionQuery.Exec(timestamp, username, modelName, messagesJSONBytes, responseJSONBytes)
	if err != nil {
		log.Printf("Failed to insert chat completion log into db")
		return err
	}
	return nil
}
