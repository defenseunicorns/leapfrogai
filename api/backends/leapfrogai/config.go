package leapfrogai

import (
	"log"

	"github.com/defenseunicorns/leapfrogai/api/config"
	"github.com/defenseunicorns/leapfrogai/pkg/client/completion"
	"github.com/gin-gonic/gin"
	"github.com/golang/protobuf/ptypes/empty"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type configRequest struct {
	Model string `json:"model"`
}

func (l *LeapfrogHandler) Config(c *gin.Context) {
	var input configRequest
	if err := c.BindJSON(&input); err != nil {
		log.Printf("500: Error marshalling input to object: %v\n", err)
		// Handle error
		c.JSON(500, err)
		return
	}

	conn := l.getModelClient(c, input.Model)
	if conn == nil {
		return
	}

	client := completion.NewLLMConfigServiceClient(conn)
	res, err := client.LLMConfig(c.Request.Context(), &empty.Empty{})
	if err != nil {
		log.Printf("500: Error completing via backend(%v): %v\n", input.Model, err)
		c.JSON(500, err)
		return
	}
	c.JSON(200, res)
}

func (o *LeapfrogHandler) getModelClient(c *gin.Context, model string) *grpc.ClientConn {
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
