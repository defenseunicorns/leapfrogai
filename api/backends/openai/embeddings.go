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

func (o *OpenAIHandler) createEngineEmbeddings(c *gin.Context) {
	var input openai.EmbeddingRequest
	var i2 EmbeddingRequest
	// Get path parameter with c.Param()
	modelID := c.Param("model_id")
	log.Printf("Model from URL: %v\n", modelID)
	// var m *openai.EmbeddingModel
	// err := m.UnmarshalText([]byte(modelID))
	//XXX do this lookup
	m := openai.AdaEmbeddingV2
	// if err != nil {
	// 	log.Printf("500: Model ID didn't map to an Embedding Model: %v", err)
	// 	c.JSON(500, err)
	// }
	if err := c.BindJSON(&i2); err != nil {
		log.Printf("500: Error marshalling input to object: %v\n", err)
		// Handle error
		c.JSON(500, err)
		return
	}
	// input was just a string, so convert back to the openai object
	input = openai.EmbeddingRequest{
		Model: m,
		User:  i2.User,
	}
	o.doEmbedding(c, input, i2.Input)

}

func (o *OpenAIHandler) doEmbedding(c *gin.Context, req openai.EmbeddingRequest, input any) {

	log.Printf("DEBUG: INPUT TYPE: %v\n", reflect.TypeOf(input))
	switch v := input.(type) {
	case string:
		log.Printf("embedding request for string")
		req.Input = []string{input.(string)}
	case []interface{}:
		log.Printf("embedding request for []interface")
		req.Input = make([]string, len(v))
		for i, s := range v {
			str, _ := s.(string)
			// if !ok {
			// 	log.Printf("%v is not a string", s)
			// 	ar := s.([]interface{})
			// 	log.Printf("Printing Array:\n")
			// 	for i, a := range ar {
			// 		log.Printf("(%v,%v): %v\n", i, a, reflect.TypeOf(a))
			// 	}
			// }
			req.Input[i] = str
		}

	default:
		log.Printf("400: embedding request for unknown type: %v", v)
		c.JSON(400, fmt.Errorf("object Input was not of type string or []string: %v", v))
	}

	conn := o.getModelClient(c, req.Model.String())
	if conn == nil {
		return
	}
	client := embeddings.NewEmbeddingsServiceClient(conn)
	request := embeddings.EmbeddingRequest{
		Inputs: req.Input,
	}
	grpcResponse, err := client.CreateEmbedding(c, &request)
	if err != nil {
		log.Printf("500: Error creating embedding for %v: %v", req.Model.String(), err)
		c.JSON(500, fmt.Errorf("error creating embedding: %v", err))
		return
	}

	response := openai.EmbeddingResponse{
		// Don't know what this object is
		Object: "",
		Model:  req.Model,
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
	o.doEmbedding(c, input, i2.Input)
}

func NewEmbeddingsServiceClient(conn *grpc.ClientConn) {
	panic("unimplemented")
}
