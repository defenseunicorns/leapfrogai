package openai

import (
	"fmt"
	"log"
	"reflect"

	"github.com/defenseunicorns/leapfrogai/pkg/client/embeddings"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
)

// TODO: this probably isn't necessary
// EmbeddingRequest is the input to a Create embeddings request.
type EmbeddingRequest struct {
	// Input is a slice of strings for which you want to completion an Embedding vector.
	// Each input must not exceed 2048 tokens in length.
	// OpenAPI suggests replacing newlines (\n) in your input with a single space, as they
	// have observed inferior results when newlines are present.
	// E.g.
	//	"The food was delicious and the waiter..."
	Input any `json:"input"`
	// ID of the model to use. You can use the List models API to see all of your available models,
	// or see our Model overview for descriptions of them.
	Model string `json:"model"`
	// A unique identifier representing your end-user, which will help OpenAI to monitor and detect abuse.
	User string `json:"user"`
}

type EmbeddingResponse struct {
	Object string      `json:"object"`
	Data   []Embedding `json:"data"`
	Model  string      `json:"model"`
	Usage  Usage       `json:"usage"`
}

type Embedding struct {
	Object    string    `json:"object"`
	Embedding []float32 `json:"embedding"`
	Index     int       `json:"index"`
}

type Usage struct {
	PromptTokens     int `json:"prompt_tokens"`
	CompletionTokens int `json:"completion_tokens"`
	TotalTokens      int `json:"total_tokens"`
}

func (o *OpenAIHandler) createEngineEmbeddings(c *gin.Context) {
	var input EmbeddingRequest
	// Get path parameter with c.Param()
	modelID := c.Param("model_id")
	log.Printf("Model from URL: %v\n", modelID)
	input.Model = modelID
	if err := c.BindJSON(&input); err != nil {
		log.Printf("500: Error marshalling input to object: %v\n", err)
		// Handle error
		c.JSON(500, err)
		return
	}
	o.doEmbedding(c, input)

}

func (o *OpenAIHandler) doEmbedding(c *gin.Context, req EmbeddingRequest) {
	input := req.Input
	inputs := make([]string, 0)
	log.Printf("DEBUG: INPUT TYPE: %v\n", reflect.TypeOf(input))
	switch v := input.(type) {
	case string:
		log.Printf("embedding request for string")
		inputs = []string{input.(string)}
	case []interface{}:
		log.Printf("embedding request for []interface")
		req.Input = make([]string, len(v))
		inputs = make([]string, len(v))
		for i, s := range v {
			str, _ := s.(string)
			inputs[i] = str
		}
	default:
		log.Printf("400: embedding request for unknown type: %v", v)
		c.JSON(400, fmt.Errorf("object Input was not of type string or []string: %v", v))
		return
	}

	conn := o.getModelClient(c, req.Model)
	if conn == nil {
		return
	}
	client := embeddings.NewEmbeddingsServiceClient(conn)
	request := embeddings.EmbeddingRequest{
		Inputs: inputs,
	}
	grpcResponse, err := client.CreateEmbedding(c, &request)
	if err != nil {
		log.Printf("500: Error creating embedding for %v: %v", req.Model, err)
		c.JSON(500, fmt.Errorf("error creating embedding: %v", err))
		return
	}

	response := EmbeddingResponse{
		// Don't know what this object is
		Object: "",
		Model:  req.Model,
		// No idea what this is for
		Usage: Usage{},
	}
	response.Data = make([]Embedding, len(grpcResponse.Embeddings))
	for i, e := range grpcResponse.Embeddings {
		embed := Embedding{
			Object:    "", //No idea what this should be
			Embedding: e.Embedding,
			Index:     i,
		}
		response.Data[i] = embed
	}
	c.JSON(200, response)
}

func (o *OpenAIHandler) createEmbeddings(c *gin.Context) {
	var input EmbeddingRequest
	// Get path parameter with c.Param()
	if err := c.BindJSON(&input); err != nil {
		log.Printf("500: Error marshalling input to object: %v\n", err)
		// Handle error
		c.JSON(500, err)
		return
	}
	o.doEmbedding(c, input)
}

func NewEmbeddingsServiceClient(conn *grpc.ClientConn) {
	panic("unimplemented")
}
