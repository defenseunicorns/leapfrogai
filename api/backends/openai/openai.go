package openai

import (
	"fmt"
	"log"

	"github.com/defenseunicorns/leapfrogai/api/config"
	"github.com/gin-gonic/gin"
	"github.com/sashabaranov/go-openai"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type OpenAIHandler struct {
	Prefix string
}

// TODO: this should get factored out into the .toml files for each model, but this is an intermediate fix
const StopToken = "<|im_end|>"

func (o *OpenAIHandler) Routes(r *gin.Engine) {
	sr := r.Group(o.Prefix)
	{
		sr.GET("/models", o.showModels)
		sr.GET("/models/:model_id", o.showModel)
		sr.POST("/chat/completions", o.chat)
		sr.POST("/completions", o.complete)
		sr.POST("/embeddings", o.createEmbeddings)
		sr.POST("/engines/:model_id/embeddings", o.createEngineEmbeddings)
		sr.POST("/audio/transcriptions", o.audioTranscriptions)
		sr.POST("/audio/translations", o.audioTranslations)
	}
}

func (o *OpenAIHandler) showModels(c *gin.Context) {
	// Implement the logic to show models here
	// Send the response with c.JSON(), c.XML(), etc.
	var m openai.ModelsList
	m.Models = make([]openai.Model, 0)
	for k, model := range config.DefaultConfig.Models {
		m.Models = append(m.Models, openai.Model{
			OwnedBy:    model.Metadata.OwnedBy,
			Permission: []openai.Permission{},
			ID:         k,
		})
	}
	c.JSON(200, m)
}

// r.GET("/models/:model_id", showModel)
func (o *OpenAIHandler) showModel(c *gin.Context) {
	// Get path parameter with c.Param()
	modelID := c.Param("model_id")

	// Implement the logic to show a specific model here, using modelID
	var m *config.Model
	var ok bool
	if m, ok = config.DefaultConfig.Models[modelID]; !ok {
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

func (o *OpenAIHandler) getModelClient(c *gin.Context, model string) *grpc.ClientConn {
	m, ok := config.DefaultConfig.Models[model]
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
