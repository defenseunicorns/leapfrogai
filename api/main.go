package main

import (
	"log"
	"os"
	"time"

	"github.com/defenseunicorns/leapfrogai/api/config"
	"github.com/defenseunicorns/leapfrogai/pkg/client/generate"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"github.com/sashabaranov/go-openai"
)

var cfg config.Config

func main() {
	var err error
	modelPath := os.Getenv("CONFIG_PATH")
	if modelPath == "" {
		modelPath = "models.toml"
	}
	cfg, err = config.LoadConfig(modelPath)
	if err != nil {
		log.Fatalf("Error loading model config file: %v", err)
	}

	r := gin.Default()

	r.GET("/models", showModels)
	r.GET("/models/:model_id", showModel)
	r.POST("/completions", complete)
	// Define other routes...

	r.Run() // Run on default port 8080
}

func showModels(c *gin.Context) {
	// Implement the logic to show models here
	// Send the response with c.JSON(), c.XML(), etc.
	models := make([]string, len(cfg))
	for k, _ := range cfg {
		models = append(models, k)
	}
	c.JSON(200, models)
}

// r.GET("/models/:model_id", showModel)
func showModel(c *gin.Context) {
	// Get path parameter with c.Param()
	modelID := c.Param("model_id")

	// Implement the logic to show a specific model here, using modelID
	var m config.Model
	var ok bool
	if m, ok = cfg[modelID]; !ok {
		c.JSON(404, nil)
		return
	}
	c.JSON(200, m)
	// Send the response
}

func complete(c *gin.Context) {
	// Bind JSON body to a struct with c.BindJSON()
	var input openai.CompletionRequest
	if err := c.BindJSON(&input); err != nil {
		// Handle error
		c.JSON(500, err)
		return
	}
	m, ok := cfg[input.Model]
	if !ok {
		c.JSON(404, "Model not found")
		return
	}
	url := m.Network.URL
	conn, err := grpc.Dial(url, grpc.WithTransportCredentials(insecure.NewCredentials()), grpc.WithBlock())
	if err != nil {
		c.JSON(500, err)
	}
	client := generate.NewCompletionServiceClient(conn)
	// Implement the completion logic here, using the data from `input`
	response, err := client.Complete(c.Request.Context(), &generate.CompletionRequest{})
	if err != nil {
		c.JSON(500, err)
		return
	}
	id, _ := uuid.NewRandom()
	resp := openai.CompletionResponse{
		ID:      id.String(),
		Created: time.Now().Unix(),
		Model:   input.Model,
		Choices: []openai.CompletionChoice{
			{
				Text: response.GetCompletion(),
			},
		},
	}
	c.JSON(200, resp)
	// Send the response
}
