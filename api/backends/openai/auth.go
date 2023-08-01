package openai

import (
	"crypto/rand"
	"crypto/sha512"
	"database/sql"
	"encoding/base64"
	"log"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

const customDictionary = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
const apiKeyLength = 64

// Hash the raw API key using SHA-512 and Base64 encode it
func base64Sha512Hash(apiKey string) string {
	hash := sha512.Sum512([]byte(apiKey))
	return base64.StdEncoding.EncodeToString(hash[:])
}

// apiKeyMiddleware checks the SHA-512 hash of the API key against the stored hashes in the PostgreSQL database.
func apiKeyMiddleware(h *DBHandler) gin.HandlerFunc {
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
		apiKeyHashBase64 := base64Sha512Hash(apiKey)

		// Query the database to get the username associated with the hashed API key
		var userID string // Change the data type to match your database schema
		err := h.db.QueryRow("SELECT username FROM api_keys WHERE api_key_sha512_base64 = $1", apiKeyHashBase64).Scan(&userID)
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
		// Add the username to the Gin context for later use in the request processing pipeline.
		c.Set("username", userID)

		// If the API key hash exists in the database, the key is valid.
		// You can pass control to the next middleware or route handler.
		c.Next()
	}
}

// Generate a random 64 character API Key
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

func (h *DBHandler) insertAPIKey(username, apiKey string) error {
	// Hash the API key using SHA-512
	apiKeyHashBase64 := base64Sha512Hash(apiKey)

	// Prepare the SQL statement
	stmt, err := h.db.Prepare("INSERT INTO api_keys (api_key_sha512_base64, username) VALUES ($1, $2)")
	if err != nil {
		return err
	}
	defer stmt.Close()

	// Execute the SQL statement
	_, err = stmt.Exec(apiKeyHashBase64, username)
	if err != nil {
		return err
	}

	return nil
}

func (o *OpenAIHandler) registerUser(c *gin.Context) {
	// Get the username from the request body
	var reqBody struct {
		UserID string `json:"username"`
	}
	if err := c.ShouldBindJSON(&reqBody); err != nil {
		c.JSON(400, gin.H{"error": "Invalid request body"})
		return
	}
	// Generate the API key
	apiKey, err := generateAPIKey()
	if err != nil {
		log.Println("Failed to generate API key...rng generation was unsuccessful")
		c.JSON(500, gin.H{"error": "Failed to generate API key"})
		return
	}

	err = o.Database.insertAPIKey(reqBody.UserID, apiKey)
	if err != nil {
		log.Println("Failed to generate API key...new user record insertion failed")
		c.JSON(500, gin.H{"error": "Failed to generate API key"})
	}

	c.JSON(200, gin.H{"api_key": apiKey})
}
