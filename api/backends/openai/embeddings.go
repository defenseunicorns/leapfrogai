package openai

import (
	"fmt"
	"log"
	"reflect"

	"github.com/defenseunicorns/leapfrogai/pkg/client/embeddings"
	"github.com/gin-gonic/gin"
	"github.com/sashabaranov/go-openai"
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
	Model openai.EmbeddingModel `json:"model"`
	// A unique identifier representing your end-user, which will help OpenAI to monitor and detect abuse.
	User string `json:"user"`
}

func (o *OpenAIHandler) createEmbeddings(c *gin.Context) {
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

	conn := o.getModelClient(c, input.Model.String())
	if conn == nil {
		return
	}
	client := embeddings.NewEmbeddingsServiceClient(conn)
	request := embeddings.EmbeddingRequest{
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

func NewEmbeddingsServiceClient(conn *grpc.ClientConn) {
	panic("unimplemented")
}
