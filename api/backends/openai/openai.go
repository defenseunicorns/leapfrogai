package openai

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"reflect"
	"strings"
	"time"

	"github.com/defenseunicorns/leapfrogai/api/config"
	"github.com/defenseunicorns/leapfrogai/pkg/client/audio"
	"github.com/defenseunicorns/leapfrogai/pkg/client/completion"
	embedding "github.com/defenseunicorns/leapfrogai/pkg/client/embeddings"
	"github.com/defenseunicorns/leapfrogai/pkg/util"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/sashabaranov/go-openai"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type OpenAIHandler struct {
	Prefix string
}

func (o *OpenAIHandler) Routes(r *gin.Engine) {
	sr := r.Group(o.Prefix)
	{
		sr.GET("/models", o.showModels)
		sr.GET("/models/:model_id", o.showModel)
		sr.POST("/completions", o.complete)
		sr.POST("/embeddings", o.createEmbeddings)
		sr.POST("/engines/:model_id/embeddings", o.createEngineEmbeddings)
		sr.POST("/audio/transcriptions", o.audioTranscriptions)
		sr.POST("/audio/translations", o.audioTranslations)
	}
}

// @app.post("/engines/{model_id}/embeddings")
// async def embed2(
//     model_id: str, body: Annotated[EngineEmbedding, Body(example=dummy_engine)]
// ):
//     llm = get_model(model_id=model_id, task="embed")
//     encoding = tiktoken.model.encoding_for_model(model_id)

//     body.prompt = [encoding.decode(input) for input in body.input]
//     logger.error(f"Decoded: { body.prompt}")

//     results = llm.embed(inputs=body.prompt)
//     output = format_embeddings_results(model_name=llm.name, embeddings=results)
//     return output

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
	client := embedding.NewEmbeddingsServiceClient(conn)
	request := embedding.EmbeddingRequest{
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

type AudioRequest struct {
	Model          string  `form:"model"`
	Prompt         string  `form:"prompt"`
	ResponseFormat string  `form:"prompt"`
	Temperature    float32 `form:"temperature"`
	InputLanguage  string  `form:"language"`
}

func (o *OpenAIHandler) audioTranscriptions(c *gin.Context) {
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
	conn := o.getModelClient(c, r.Model)
	client := audio.NewAudioClient(conn)
	stream, err := client.Transcribe(context.Background())

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
func (o *OpenAIHandler) audioTranslations(c *gin.Context) {
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
	conn := o.getModelClient(c, r.Model)
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

func (o *OpenAIHandler) complete(c *gin.Context) {
	// Bind JSON body to a struct with c.BindJSON()
	var input openai.CompletionRequest
	if err := c.BindJSON(&input); err != nil {
		log.Printf("500: Error marshalling input to object: %v\n", err)
		// Handle error
		c.JSON(500, err)
		return
	}
	conn := o.getModelClient(c, input.Model)
	if conn == nil {
		return
	}
	id, _ := uuid.NewRandom()

	if input.Stream {
		chanStream := make(chan *completion.CompletionResponse, 10)
		client := completion.NewCompletionStreamServiceClient(conn)
		stream, err := client.CompleteStream(context.Background(), &completion.CompletionRequest{
			Prompt:       input.Prompt.(string),
			MaxNewTokens: util.Int32(int32(input.MaxTokens)),
			Temperature:  util.Float32(input.Temperature),
		})

		if err != nil {
			c.JSON(500, err)
			return
		}

		go func() {
			defer close(chanStream)
			for {
				cResp, err := stream.Recv()
				if err == io.EOF {
					break
				}
				chanStream <- cResp
			}
		}()
		c.Stream(func(w io.Writer) bool {
			if msg, ok := <-chanStream; ok {

				// OpenAI places a space in between the data key and payload in HTTP. So, I guess we're bug-for-bug compatible.
				res, err := json.Marshal(openai.CompletionResponse{
					ID:      id.String(),
					Created: time.Now().Unix(),
					Model:   input.Model,
					Object:  "text_completion",
					Choices: []openai.CompletionChoice{
						{
							Index: 0,
							Text:  msg.GetChoices()[0].GetText(),
						},
					},
				})
				if err != nil {
					return false
				}
				c.SSEvent("", fmt.Sprintf(" %s", res))
				return true
			}
			c.SSEvent("", " [DONE]")
			return false
		})
	} else {

		logit := make(map[string]int32)
		for k, v := range input.LogitBias {
			logit[k] = int32(v)
		}

		client := completion.NewCompletionServiceClient(conn)

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
			response, err := client.Complete(c.Request.Context(), &completion.CompletionRequest{
				Prompt:           input.Prompt.(string),
				Suffix:           util.String(input.Suffix),
				MaxNewTokens:     util.Int32(int32(input.MaxTokens)),
				Temperature:      util.Float32(input.Temperature),
				TopP:             util.Float32(input.TopP),
				Logprobs:         util.Int32(int32(input.LogProbs)),
				Echo:             util.Bool(input.Echo),
				Stop:             input.Stop,
				PresencePenalty:  util.Float32(input.PresencePenalty),
				FrequencePenalty: util.Float32(input.FrequencyPenalty),
				BestOf:           util.Int32(int32(input.BestOf)),
				LogitBias:        logit,
			})
			if err != nil {
				log.Printf("500: Error completing via backend(%v): %v\n", input.Model, err)
				c.JSON(500, err)
				return
			}

			choice := openai.CompletionChoice{
				Text:         response.Choices[i].GetText(),
				FinishReason: strings.ToLower(response.Choices[i].GetFinishReason().Enum().String()),
				Index:        i,
			}
			resp.Choices[i] = choice
		}

		c.JSON(200, resp)
	}
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
