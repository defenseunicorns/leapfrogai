package main

import (
	"bufio"
	"context"
	"fmt"
	"log"
	"os"
	"reflect"
	"strings"
	"time"

	"github.com/defenseunicorns/leapfrogai/api/config"
	"github.com/defenseunicorns/leapfrogai/pkg/client/audio"
	embedding "github.com/defenseunicorns/leapfrogai/pkg/client/embeddings"
	"github.com/defenseunicorns/leapfrogai/pkg/client/generate"
	"github.com/fsnotify/fsnotify"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/penglongli/gin-metrics/ginmetrics"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"github.com/sashabaranov/go-openai"
)

var cfg config.Config

func main() {

	go watch_config()
	// gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	// Add promtheus endpoint for custom metrics
	// get global Monitor object
	m := ginmetrics.GetMonitor()

	// +optional set metric path, default /debug/metrics
	m.SetMetricPath("/metrics")

	m.Use(r)

	r.GET("/healthz")
	r.GET("/openai/models", showModels)
	r.GET("/openai/models/:model_id", showModel)
	r.POST("/openai/completions", complete)
	r.POST("/openai/embeddings", createEmbeddings)
	r.POST("/openai/audio/transcriptions", audioTranscriptions)
	r.POST("/openai/audio/translations", audioTranslations)
	// r.POST("/copilot/completion", copilotComplete)
	// Define other routes...

	r.Run()
	// r.Run("0.0.0.0:8080") // Run on default port 8080
}

func createEmbeddings(c *gin.Context) {
	var input openai.EmbeddingRequest
	var i2 EmbeddingRequest
	if err := c.BindJSON(&i2); err != nil {
		log.Printf("500: Error marshalling input to object: %v\n", err)
		// Handle error
		c.JSON(500, err)
		return
	}
	// input was just a string, so convert back to the openai object
	input = openai.EmbeddingRequest{
		Model: i2.Model,
		User:  i2.User,
	}
	log.Printf("DEBUG: INPUT TYPE: %v\n", reflect.TypeOf(i2.Input))
	switch v := i2.Input.(type) {
	case string:
		log.Printf("embedding request for string")
		input.Input = []string{i2.Input.(string)}
	case []interface{}:
		log.Printf("embedding request for []interface")
		input.Input = make([]string, len(v))
		for i, s := range v {
			input.Input[i] = s.(string)
		}

	default:
		log.Printf("400: embedding request for unknown type: %v", v)
		c.JSON(400, fmt.Errorf("object Input was not of type string or []string: %v", v))
	}

	conn := getModelClient(c, input.Model.String())
	if conn == nil {
		return
	}
	client := embedding.NewEmbeddingsServiceClient(conn)
	request := embedding.EmbeddingRequest{
		Inputs: input.Input,
	}
	grpcResponse, err := client.CreateEmbedding(c, &request)
	if err != nil {
		log.Printf("500: Error creating embedding for %v: %v", input.Model.String(), err)
		c.JSON(500, fmt.Errorf("error creating embedding: %v", err))
		return
	}

	response := openai.EmbeddingResponse{
		// Don't know what this object is
		Object: "",
		Model:  input.Model,
		// No idea what this is for
		Usage: openai.Usage{},
	}
	response.Data = make([]openai.Embedding, len(grpcResponse.Embeddings))
	for i, e := range grpcResponse.Embeddings {
		embed := openai.Embedding{
			Object:    "", //No idea what this should be
			Embedding: e.Embedding,
			Index:     i,
		}
		response.Data[i] = embed
	}
	c.JSON(200, response)
}

type AudioRequest struct {
	Model          string  `form:"model"`
	Prompt         string  `form:"prompt"`
	ResponseFormat string  `form:"prompt"`
	Temperature    float32 `form:"temperature"`
	InputLanguage  string  `form:"language"`
}

func audioTranscriptions(c *gin.Context) {
	var r AudioRequest
	c.Bind(&r)
	f, err := c.FormFile("file")
	if err != nil {
		c.JSON(500, err)
		return
	}

	file, err := f.Open()
	defer file.Close()
	if err != nil {
		c.JSON(500, err)
		return
	}
	conn := getModelClient(c, r.Model)
	client := audio.NewAudioClient(conn)
	stream, err := client.Transcribe(context.Background())
	if err != nil {
		log.Default().Printf("Error calling transcribe to %v: %v", r.Model, err)
		c.JSON(500, err)
	}
	if r.ResponseFormat == "" {
		r.ResponseFormat = "json"
	}
	responseFormat := audio.AudioMetadata_AudioFormat_value[strings.ToUpper(r.ResponseFormat)]

	stream.Send(&audio.AudioRequest{
		Request: &audio.AudioRequest_Metadata{
			Metadata: &audio.AudioMetadata{
				Prompt:        r.Prompt,
				Temperature:   r.Temperature,
				Inputlanguage: r.InputLanguage,
				Format:        audio.AudioMetadata_AudioFormat(responseFormat),
			},
		},
	})

	reader := bufio.NewReader(file)
	chunkSize := 1024

	for {
		chunk := make([]byte, chunkSize)
		n, err := reader.Read(chunk)

		if err != nil {
			if err.Error() == "EOF" {
				break
			}
			c.JSON(500, err)
			return
		}

		r := &audio.AudioRequest{
			Request: &audio.AudioRequest_ChunkData{
				ChunkData: chunk,
			},
		}

		if err = stream.Send(r); err != nil {
			c.JSON(500, err)
			return
		}

		if err == nil && n < chunkSize {
			break
		}
	}

	reply, err := stream.CloseAndRecv()
	if err != nil {
		c.JSON(500, err)
	}

	c.JSON(200, reply)
}

// # TODO abstract this and transcriptions
func audioTranslations(c *gin.Context) {
	var r AudioRequest
	c.Bind(&r)
	f, err := c.FormFile("file")
	if err != nil {
		c.JSON(500, err)
		return
	}

	file, err := f.Open()
	defer file.Close()

	if err != nil {
		c.JSON(500, err)
		return
	}
	conn := getModelClient(c, r.Model)
	client := audio.NewAudioClient(conn)
	stream, err := client.Translate(context.Background())

	if r.ResponseFormat == "" {
		r.ResponseFormat = "json"
	}
	responseFormat := audio.AudioMetadata_AudioFormat_value[strings.ToUpper(r.ResponseFormat)]

	stream.Send(&audio.AudioRequest{
		Request: &audio.AudioRequest_Metadata{
			Metadata: &audio.AudioMetadata{
				Prompt:        r.Prompt,
				Temperature:   r.Temperature,
				Inputlanguage: r.InputLanguage,
				Format:        audio.AudioMetadata_AudioFormat(responseFormat),
			},
		},
	})

	reader := bufio.NewReader(file)
	chunkSize := 1024

	for {
		chunk := make([]byte, chunkSize)
		n, err := reader.Read(chunk)

		if err != nil {
			if err.Error() == "EOF" {
				break
			}
			c.JSON(500, err)
			return
		}

		r := &audio.AudioRequest{
			Request: &audio.AudioRequest_ChunkData{
				ChunkData: chunk,
			},
		}

		if err = stream.Send(r); err != nil {
			c.JSON(500, err)
			return
		}

		if err == nil && n < chunkSize {
			break
		}
	}

	reply, err := stream.CloseAndRecv()
	if err != nil {
		c.JSON(500, err)
	}

	c.JSON(200, reply)
}

func showModels(c *gin.Context) {
	// Implement the logic to show models here
	// Send the response with c.JSON(), c.XML(), etc.
	var m openai.ModelsList
	m.Models = make([]openai.Model, 0)
	for k, model := range cfg {
		m.Models = append(m.Models, openai.Model{
			OwnedBy:    model.Metadata.OwnedBy,
			Permission: []openai.Permission{},
			ID:         k,
		})
	}
	c.JSON(200, m)
}

// r.GET("/models/:model_id", showModel)
func showModel(c *gin.Context) {
	// Get path parameter with c.Param()
	modelID := c.Param("model_id")

	// Implement the logic to show a specific model here, using modelID
	var m config.Model
	var ok bool
	if m, ok = cfg[modelID]; !ok {
		c.JSON(404, fmt.Errorf("model %v not found", modelID))
		return
	}
	model := openai.Model{
		OwnedBy:    m.Metadata.OwnedBy,
		Permission: []openai.Permission{},
		ID:         modelID,
	}

	c.JSON(200, model)
	// Send the response
}

func complete(c *gin.Context) {
	// Bind JSON body to a struct with c.BindJSON()
	var input openai.CompletionRequest
	if err := c.BindJSON(&input); err != nil {
		log.Printf("500: Error marshalling input to object: %v\n", err)
		// Handle error
		c.JSON(500, err)
		return
	}
	conn := getModelClient(c, input.Model)
	if conn == nil {
		return
	}

	logit := make(map[string]int32)
	for k, v := range input.LogitBias {
		logit[k] = int32(v)
	}

	client := generate.NewCompletionServiceClient(conn)

	id, _ := uuid.NewRandom()
	if input.N == 0 {
		input.N = 1
	}
	resp := openai.CompletionResponse{
		ID:      id.String(),
		Created: time.Now().Unix(),
		Model:   input.Model,
		Choices: make([]openai.CompletionChoice, input.N),
	}

	for i := 0; i < input.N; i++ {
		// Implement the completion logic here, using the data from `input`
		response, err := client.Complete(c.Request.Context(), &generate.CompletionRequest{
			Prompt:           input.Prompt.(string),
			Suffix:           input.Suffix,
			MaxTokens:        int32(input.MaxTokens),
			Temperature:      input.Temperature,
			TopP:             input.TopP,
			Stream:           input.Stream,
			Logprobs:         int32(input.LogProbs),
			Echo:             input.Echo,
			Stop:             input.Stop, // Wrong type here...
			PresencePenalty:  input.PresencePenalty,
			FrequencePenalty: input.FrequencyPenalty,
			BestOf:           int32(input.BestOf),
			LogitBias:        logit, // Wrong type here
		})
		if err != nil {
			log.Printf("500: Error completing via backend(%v): %v\n", input.Model, err)
			c.JSON(500, err)
			return
		}
		choice := openai.CompletionChoice{
			Text:         strings.TrimPrefix(response.GetCompletion(), input.Prompt.(string)),
			FinishReason: response.GetFinishReason(),
			Index:        i,
		}
		resp.Choices[i] = choice
	}

	c.JSON(200, resp)
	// Send the response
}

func getModelClient(c *gin.Context, model string) *grpc.ClientConn {
	m, ok := cfg[model]
	if !ok {
		log.Printf("404: Did not find requested model (%v) in list\n", model)
		c.JSON(404, "Model not found")
		return nil
	}
	url := m.Network.URL
	conn, err := grpc.Dial(url, grpc.WithTransportCredentials(insecure.NewCredentials()), grpc.WithBlock())
	if err != nil {
		log.Printf("500: Error connecting to backend(%v): %v\n", url, err)
		c.JSON(500, err)
		return nil
	}
	return conn
}

// EmbeddingRequest is the input to a Create embeddings request.
type EmbeddingRequest struct {
	// Input is a slice of strings for which you want to generate an Embedding vector.
	// Each input must not exceed 2048 tokens in length.
	// OpenAPI suggests replacing newlines (\n) in your input with a single space, as they
	// have observed inferior results when newlines are present.
	// E.g.
	//	"The food was delicious and the waiter..."
	Input any `json:"input"`
	// ID of the model to use. You can use the List models API to see all of your available models,
	// or see our Model overview for descriptions of them.
	Model openai.EmbeddingModel `json:"model"`
	// A unique identifier representing your end-user, which will help OpenAI to monitor and detect abuse.
	User string `json:"user"`
}

func watch_config() {
	var err error
	modelPath := os.Getenv("CONFIG_PATH")
	if modelPath == "" {
		modelPath = "."
	}
	fmt.Printf("Using config path: %v\n", modelPath)
	cfg, err = config.LoadConfigs(modelPath)
	if err != nil {
		log.Fatalf("Error loading model config file: %v", err)
	}
	// Watch the config file
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatalf("Failed to create watcher: %v", err)
	}
	defer watcher.Close()
	err = watcher.Add(modelPath)
	if err != nil {
		log.Fatalf("Failed to add file to watcher: %v", err)
	}

	for {
		select {
		case event := <-watcher.Events:
			// Check if the file was modified
			if event.Op&fsnotify.Write == fsnotify.Write {
				fmt.Println("Configuration file changed, reloading...")

				// Reload the config file

				c, err := config.LoadConfigs(modelPath)
				if err != nil {
					fmt.Printf("Error loading model config file: %v", err)
					fmt.Printf("Falling back to previous version")
					continue
				}
				cfg = c
			}
		case err := <-watcher.Errors:
			log.Printf("Watcher error: %v", err)
		}
	}
}
