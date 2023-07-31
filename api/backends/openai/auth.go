package openai

import (
	"crypto/rand"
	"crypto/sha512"
	"database/sql"
	"encoding/base64"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

const customDictionary = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
const apiKeyLength = 64

// apiKeyMiddleware checks the SHA-512 hash of the API key against the stored hashes in the PostgreSQL database.
func apiKeyMiddleware(db *sql.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.GetHeader("Authorization")

		// Check if the Authorization header is provided
		if authHeader == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header missing"})
			c.Abort()
			return
		}

		// Check if the Authorization header starts with "Bearer "
		const bearerPrefix = "Bearer "
		if !strings.HasPrefix(authHeader, bearerPrefix) {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid authorization format"})
			c.Abort()
			return
		}

		// Extract the API key by removing the "Bearer " prefix
		apiKey := strings.TrimPrefix(authHeader, bearerPrefix)

		// Hash the incoming API key using SHA-512
		hash := sha512.Sum512([]byte(apiKey))
		hashedAPIKey := base64.StdEncoding.EncodeToString(hash[:])

		// Query the database to check the validity of the hashed API key
		var dbAPIKeyHash string
		err := db.QueryRow("SELECT api_key_hash FROM api_keys WHERE api_key_hash = $1", hashedAPIKey).Scan(&dbAPIKeyHash)
		if err != nil {
			if err == sql.ErrNoRows {
				c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid API key"})
				c.Abort()
				return
			}
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query database"})
			c.Abort()
			return
		}

		// If the API key hash exists in the database, the key is valid.
		// You can pass control to the next middleware or route handler.
		c.Next()
	}
}

func generateAPIKey() (string, error) {
	dictionaryLength := len(customDictionary)
	apiKeyBytes := make([]byte, apiKeyLength)
	_, err := rand.Read(apiKeyBytes)
	if err != nil {
		return "", err
	}

	for i := 0; i < apiKeyLength; i++ {
		apiKeyBytes[i] = customDictionary[int(apiKeyBytes[i])%dictionaryLength]
	}

	return string(apiKeyBytes), nil
}

func insertAPIKey(username, apiKey string) error {
	// Hash the API key using SHA-512
	hash := sha512.Sum512([]byte(apiKey))
	apiKeyHash := base64.StdEncoding.EncodeToString(hash[:])

	// Connect to the PostgreSQL database
	db, err := sql.Open("postgres", "user=yourdbuser password=yourdbpassword dbname=yourdbname sslmode=disable")
	if err != nil {
		return err
	}
	defer db.Close()

	// Prepare the SQL statement
	stmt, err := db.Prepare("INSERT INTO api_keys (api_key_hash, username) VALUES ($1, $2)")
	if err != nil {
		return err
	}
	defer stmt.Close()

	// Execute the SQL statement
	_, err = stmt.Exec(apiKeyHash, username)
	if err != nil {
		return err
	}

	return nil
}

func (o *OpenAIHandler) registerUser(c *gin.Context) {
	// Get the username from the request body
	var reqBody struct {
		Username string `json:"username"`
	}
	if err := c.ShouldBindJSON(&reqBody); err != nil {
		c.JSON(400, gin.H{"error": "Invalid request body"})
		return
	}
	// Generate the API key
	apiKey, err := generateAPIKey()
	if err != nil {
		c.JSON(500, gin.H{"error": "Failed to generate API key"})
		return
	}

	c.JSON(200, gin.H{"api_key": apiKey})
}
