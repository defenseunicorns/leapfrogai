package openai

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"strings"
	"time"

	"github.com/defenseunicorns/leapfrogai/pkg/client/completion"
	"github.com/defenseunicorns/leapfrogai/pkg/util"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/sashabaranov/go-openai"
)

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
		log.Printf("Attempting to stream for model %v\n", input.Model)
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
			// remove StopToken from the returned text
			t := strings.ReplaceAll(response.Choices[i].GetText(), StopToken, "")
			choice := openai.CompletionChoice{
				Text:         t,
				FinishReason: strings.ToLower(response.Choices[i].GetFinishReason().Enum().String()),
				Index:        i,
			}
			resp.Choices[i] = choice
		}

		c.JSON(200, resp)
	}
	// Send the response
}
