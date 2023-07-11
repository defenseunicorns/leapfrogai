package openai

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"strings"
	"time"

	"github.com/defenseunicorns/leapfrogai/pkg/client/chat"
	"github.com/defenseunicorns/leapfrogai/pkg/util"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/sashabaranov/go-openai"
)

// Turn a list of openai.ChatCompletionMessages into a list of chat.ChatItems that
// can be added to a ChatCompletionRequest proto that can submitted for inference
func ToChatItems(messages []openai.ChatCompletionMessage) ([]*chat.ChatItem, error) {
	var chatItems []*chat.ChatItem
	// iterate through the messages and convert the string role into an enum
	for _, jsonItem := range messages {
		var c chat.ChatItem
		switch {
		case jsonItem.Role == "system":
			c.Role = chat.ChatRole_SYSTEM
		case jsonItem.Role == "assistant":
			c.Role = chat.ChatRole_ASSISTANT
		case jsonItem.Role == "user":
			c.Role = chat.ChatRole_USER
		case jsonItem.Role == "function":
			c.Role = chat.ChatRole_FUNCTION
		default:
			return nil, fmt.Errorf("invalid ChatRole: %v", jsonItem.Role)
		}
		c.Content = jsonItem.Content
		chatItems = append(chatItems, &c)
	}
	return chatItems, nil
}

// Convert a single ChatItem from a ChatCompletionResponse proto into an
// openai.ChatCompletionMessage that can be serialized to json and sent back to the client
// This only operates on a single ChatItem because the response from the inference server
// should only be a single ChatItem per prompt. If you request N responses to your prompt,
// this will get called separately for each of them.
func ToJsonMessage(chatItem *chat.ChatItem) (openai.ChatCompletionMessage, error) {
	var message openai.ChatCompletionMessage
	// convert the enum role to a string
	switch {
	case chatItem.Role == chat.ChatRole_SYSTEM:
		message.Role = "system"
	case chatItem.Role == chat.ChatRole_ASSISTANT:
		message.Role = "assistant"
	case chatItem.Role == chat.ChatRole_USER:
		message.Role = "chat"
	case chatItem.Role == chat.ChatRole_FUNCTION:
		message.Role = "function"
	default:
		return message, fmt.Errorf("invalid ChatRole: %v", chatItem.Role.String())
	}
	// remove StopToken from the returned text
	message.Content = strings.ReplaceAll(chatItem.Content, StopToken, "")

	return message, nil
}

func (o *OpenAIHandler) chat(c *gin.Context) {
	// Bind JSON body to a struct with c.BindJSON()
	var input openai.ChatCompletionRequest
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
		chanStream := make(chan *chat.ChatCompletionResponse, 10)
		client := chat.NewChatCompletionStreamServiceClient(conn)
		items, err := ToChatItems(input.Messages)
		if err != nil {
			log.Printf("500: Bad message Role: %v\n", err)
			// Handle error
			c.JSON(500, err)
			return
		}
		stream, err := client.ChatCompleteStream(context.Background(), &chat.ChatCompletionRequest{
			ChatItems:    items,
			MaxNewTokens: int32(input.MaxTokens),
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
				m, err := ToJsonMessage(msg.Choices[0].GetChatItem())
				if err != nil {
					log.Printf("500: Bad message Role: %v\n", err)
					// Handle error
					c.JSON(500, err)
					return false
				}
				// OpenAI places a space in between the data key and payload in HTTP. So, I guess we're bug-for-bug compatible.
				res, err := json.Marshal(openai.ChatCompletionResponse{
					ID:      id.String(),
					Created: time.Now().Unix(),
					Model:   input.Model,
					Object:  "chat.completion",
					Choices: []openai.ChatCompletionChoice{
						{
							Index:   0,
							Message: m,
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

		client := chat.NewChatCompletionServiceClient(conn)

		if input.N == 0 {
			input.N = 1
		}
		resp := openai.ChatCompletionResponse{
			ID:      id.String(),
			Created: time.Now().Unix(),
			Model:   input.Model,
			Choices: make([]openai.ChatCompletionChoice, input.N),
		}

		// TODO: this doesn't really work for multiple N, but it mirrors the setup in
		// the completion.go file
		for i := 0; i < input.N; i++ {
			// convert the messages into ChatItems
			items, err := ToChatItems(input.Messages)
			if err != nil {
				log.Printf("500: Bad message Role: %v\n", err)
				// Handle error
				c.JSON(500, err)
				return
			}
			response, err := client.ChatComplete(c.Request.Context(), &chat.ChatCompletionRequest{
				ChatItems:       items,
				MaxNewTokens:    int32(input.MaxTokens),
				Temperature:     util.Float32(input.Temperature),
				TopP:            util.Float32(input.TopP),
				Stop:            input.Stop,
				PresencePenalty: util.Float32(input.PresencePenalty),
				LogitBias:       logit,
			})
			if err != nil {
				log.Printf("500: Error completing via backend(%v): %v\n", input.Model, err)
				c.JSON(500, err)
				return
			}
			m, err := ToJsonMessage(response.Choices[i].GetChatItem())
			if err != nil {
				log.Printf("500: Bad message Role: %v\n", err)
				// Handle error
				c.JSON(500, err)
				return
			}
			choice := openai.ChatCompletionChoice{
				Message: m,
				Index:   i,
			}
			resp.Choices[i] = choice
		}

		c.JSON(200, resp)
	}
	// Send the response
}
