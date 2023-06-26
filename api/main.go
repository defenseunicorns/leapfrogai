package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/defenseunicorns/leapfrogai/api/config"
	"github.com/defenseunicorns/leapfrogai/pkg/client/audio"
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

	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	r.GET("/models", showModels)
	r.GET("/models/:model_id", showModel)
	r.POST("/completions", complete)
	// r.POST("/audio", audio)
	r.POST("/audio/transcriptions", audioTranscriptions)
	r.POST("/audio/translations", audioTranslations)
	// Define other routes...

	r.Run()
	// r.Run("0.0.0.0:8080") // Run on default port 8080
}

func audioTranscriptions(c *gin.Context) {
	var input openai.AudioRequest
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
	client := audio.NewAudioClient(conn)

	// get the data from the request

	request := audio.AudioRequest{
		Model:         input.Model,
		Data:          []byte{},
		Prompt:        input.Prompt,
		Temperature:   input.Temperature,
		Inputlanguage: input.Language,
		Format:        string(input.Format),
	}

	grpcResponse, err := client.Transcribe(context.Background(), &request)
	if err != nil {
		log.Printf("500: Error transcribing via %v: %v", input.Model, err)
		c.JSON(500, err)
		return
	}

	response := openai.AudioResponse{
		Task:     grpcResponse.Task,
		Language: grpcResponse.Language,
		Duration: grpcResponse.Duration,
		Text:     grpcResponse.Text,
	}
	response.Segments = make([]struct {
		ID               int     "json:\"id\""
		Seek             int     "json:\"seek\""
		Start            float64 "json:\"start\""
		End              float64 "json:\"end\""
		Text             string  "json:\"text\""
		Tokens           []int   "json:\"tokens\""
		Temperature      float64 "json:\"temperature\""
		AvgLogprob       float64 "json:\"avg_logprob\""
		CompressionRatio float64 "json:\"compression_ratio\""
		NoSpeechProb     float64 "json:\"no_speech_prob\""
		Transient        bool    "json:\"transient\""
	}, 0)
	for i, seg := range grpcResponse.Segments {
		response.Segments = append(response.Segments,
			struct {
				ID               int     "json:\"id\""
				Seek             int     "json:\"seek\""
				Start            float64 "json:\"start\""
				End              float64 "json:\"end\""
				Text             string  "json:\"text\""
				Tokens           []int   "json:\"tokens\""
				Temperature      float64 "json:\"temperature\""
				AvgLogprob       float64 "json:\"avg_logprob\""
				CompressionRatio float64 "json:\"compression_ratio\""
				NoSpeechProb     float64 "json:\"no_speech_prob\""
				Transient        bool    "json:\"transient\""
			}{
				ID:               int(seg.Id),
				Seek:             int(seg.Seek),
				Start:            seg.Start,
				End:              seg.End,
				Text:             seg.Text,
				Temperature:      seg.Temperature,
				AvgLogprob:       seg.AvgLogprob,
				CompressionRatio: seg.CompressionRatio,
				NoSpeechProb:     seg.NoSpeechProb,
				Transient:        seg.Transient,
			},
		)
		// convert int32 to int
		tokens := make([]int, len(seg.Tokens))
		for i, t := range seg.Tokens {
			tokens[i] = int(t)
		}
		response.Segments[i].Tokens = tokens
	}

	c.JSON(200, response)

}

func audioTranslations(c *gin.Context) {
	var input openai.AudioRequest
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
	client := audio.NewAudioClient(conn)

	// get the data from the request

	request := audio.AudioRequest{
		Model:         input.Model,
		Data:          []byte{},
		Prompt:        input.Prompt,
		Temperature:   input.Temperature,
		Inputlanguage: input.Language,
		Format:        string(input.Format),
	}

	grpcResponse, err := client.Translate(context.Background(), &request)
	if err != nil {
		log.Printf("500: Error translating via %v: %v", input.Model, err)
		c.JSON(500, err)
		return
	}

	response := openai.AudioResponse{
		Task:     grpcResponse.Task,
		Language: grpcResponse.Language,
		Duration: grpcResponse.Duration,
		Text:     grpcResponse.Text,
	}
	response.Segments = make([]struct {
		ID               int     "json:\"id\""
		Seek             int     "json:\"seek\""
		Start            float64 "json:\"start\""
		End              float64 "json:\"end\""
		Text             string  "json:\"text\""
		Tokens           []int   "json:\"tokens\""
		Temperature      float64 "json:\"temperature\""
		AvgLogprob       float64 "json:\"avg_logprob\""
		CompressionRatio float64 "json:\"compression_ratio\""
		NoSpeechProb     float64 "json:\"no_speech_prob\""
		Transient        bool    "json:\"transient\""
	}, 0)
	for i, seg := range grpcResponse.Segments {
		response.Segments = append(response.Segments,
			struct {
				ID               int     "json:\"id\""
				Seek             int     "json:\"seek\""
				Start            float64 "json:\"start\""
				End              float64 "json:\"end\""
				Text             string  "json:\"text\""
				Tokens           []int   "json:\"tokens\""
				Temperature      float64 "json:\"temperature\""
				AvgLogprob       float64 "json:\"avg_logprob\""
				CompressionRatio float64 "json:\"compression_ratio\""
				NoSpeechProb     float64 "json:\"no_speech_prob\""
				Transient        bool    "json:\"transient\""
			}{
				ID:               int(seg.Id),
				Seek:             int(seg.Seek),
				Start:            seg.Start,
				End:              seg.End,
				Text:             seg.Text,
				Temperature:      seg.Temperature,
				AvgLogprob:       seg.AvgLogprob,
				CompressionRatio: seg.CompressionRatio,
				NoSpeechProb:     seg.NoSpeechProb,
				Transient:        seg.Transient,
			},
		)
		// convert int32 to int
		tokens := make([]int, len(seg.Tokens))
		for i, t := range seg.Tokens {
			tokens[i] = int(t)
		}
		response.Segments[i].Tokens = tokens
	}

	c.JSON(200, response)
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
	client := generate.NewCompletionServiceClient(conn)
	// Implement the completion logic here, using the data from `input`
	response, err := client.Complete(c.Request.Context(), &generate.CompletionRequest{
		Prompt:      input.Prompt.(string),
		Suffix:      input.Suffix,
		MaxTokens:   int32(input.MaxTokens),
		Temperature: input.Temperature,
		TopP:        input.TopP,
		N:           int32(input.N),
		Stream:      input.Stream,
		Logprobs:    int32(input.LogProbs),
		Echo:        input.Echo,
		// Stop:             input.Stop, // Wrong type here...
		PresencePenalty:  input.PresencePenalty,
		FrequencePenalty: input.FrequencyPenalty,
		BestOf:           int32(input.BestOf),
		// LogitBias:        input.LogitBias, // Wrong type here
	})
	if err != nil {
		log.Printf("500: Error completing via backend(%v): %v\n", input.Model, err)
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
