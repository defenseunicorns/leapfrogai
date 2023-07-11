package hf

import (
	"context"
	"encoding/json"
	"io"
	"log"
	"strings"

	"github.com/defenseunicorns/leapfrogai/api/config"
	"github.com/defenseunicorns/leapfrogai/pkg/client/completion"
	"github.com/defenseunicorns/leapfrogai/pkg/util"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

const StopToken = "<|im_end|>"

// Handler is a HuggingFace handler
type Handler struct {
	Prefix string
}

// Routes maps the routes
func (h *Handler) Routes(r *gin.Engine) {
	sr := r.Group(h.Prefix)
	{
		sr.POST("/models/:repo/:model", h.inference)
	}
}

func (h *Handler) inference(c *gin.Context) {
	model := c.Param("model")
	var input GenerateRequest

	if err := c.BindJSON(&input); err != nil {
		log.Printf("500: Error marshalling input to object: %v\n", err)
		c.JSON(500, err)
		return
	}

	conn := h.getModelClient(c, model)

	client := completion.NewCompletionStreamServiceClient(conn)

	if input.Stream {
		chanStream := make(chan *completion.CompletionResponse, 10)
		stream, err := client.CompleteStream(context.Background(), &completion.CompletionRequest{
			Prompt:       input.Inputs,
			MaxNewTokens: util.Int32(int32(input.Parameters.MaxNewTokens)),
			Temperature:  util.Float32(float32(*input.Parameters.Temperature)),
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
		generatedText := ""
		c.Stream(func(w io.Writer) bool {
			if msg, ok := <-chanStream; ok {

				// OpenAI places a space in between the data key and payload in HTTP. So, I guess we're bug-for-bug compatible.
				res, err := json.Marshal(&GenerateStreamResponse{
					Token: &Token{
						ID:      0,
						Text:    msg.Choices[0].GetText(),
						Logprob: 0.0,
						Special: false,
					},
					GeneratedText: "", // TODO: update proto to allow me to be nil; HF returns null for non-final tokens
					Details:       nil,
				})
				if err != nil {
					return false
				}
				generatedText = generatedText + msg.Choices[0].GetText()
				c.SSEvent("", string(res))
				return true
			}

			// remove the end of sequence token from the generated text we return
			generatedText = strings.ReplaceAll(generatedText, StopToken, "")
			r, _ := json.Marshal(&GenerateStreamResponse{
				Token: &Token{
					ID:      0,
					Text:    StopToken,
					Logprob: 0.0,
					Special: false,
				},
				GeneratedText: generatedText,
				Details: &Details{
					BestOfSequences: []BestOfSequence{
						{
							GeneratedText: generatedText,
						},
					},
				},
			})
			c.SSEvent("", string(r))
			return false
		})
	} else {
		client := completion.NewCompletionServiceClient(conn)

		gr, _ := client.Complete(c.Request.Context(), &completion.CompletionRequest{
			Prompt:       input.Inputs,
			MaxNewTokens: util.Int32(int32(input.Parameters.MaxNewTokens)),
			Temperature:  input.Parameters.Temperature,
		})

		// remove the end of sequence token from the generated text we return
		generatedText := strings.ReplaceAll(gr.Choices[0].Text, StopToken, "")
		r := &[]GenerateResponse{
			{
				GeneratedText: generatedText,
				Details: &Details{
					BestOfSequences: []BestOfSequence{
						{
							GeneratedText: generatedText,
						},
					},
				},
			},
		}

		c.JSON(200, r)
	}
}

// func (h *Handler) doGenerate(c *gin.Context, stream bool) {
// 	var input GenerateRequest

// }

// TODO: unify between backends
func (h *Handler) getModelClient(c *gin.Context, model string) *grpc.ClientConn {
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
