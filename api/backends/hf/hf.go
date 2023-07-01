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

// Handler is a HuggingFace handler
type Handler struct {
	Prefix string
}

// https://ab2e29d8f299.ngrok.app/
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
		c.Stream(func(w io.Writer) bool {
			var text []string
			if msg, ok := <-chanStream; ok {

				// OpenAI places a space in between the data key and payload in HTTP. So, I guess we're bug-for-bug compatible.
				res, err := json.Marshal(&GenerateStreamResponse{
					Token: &Token{
						ID:      0,
						Text:    msg.Choices[0].GetText(),
						Logprob: 0.0,
						Special: false,
					},
					GeneratedText: "",
					Details:       nil,
				})
				if err != nil {
					return false
				}
				text = append(text, msg.Choices[0].GetText())
				c.SSEvent("", string(res))
				return true
			}

			gt := strings.Join(text, "")
			r, _ := json.Marshal(&GenerateStreamResponse{
				Token: &Token{
					ID:      0,
					Text:    "<|im_end|>",
					Logprob: 0.0,
					Special: false,
				},
				GeneratedText: gt,
				Details: &Details{
					BestOfSequences: []BestOfSequence{
						{
							GeneratedText: gt,
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

		r := &[]GenerateResponse{
			{
				GeneratedText: gr.Choices[0].Text,
				Details: &Details{
					BestOfSequences: []BestOfSequence{
						{
							GeneratedText: gr.Choices[0].Text,
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
