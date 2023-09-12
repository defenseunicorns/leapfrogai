package openai

import (
	"bufio"
	"context"
	"strings"

	"github.com/defenseunicorns/leapfrogai/api/logger"
	"github.com/defenseunicorns/leapfrogai/pkg/client/audio"
	"github.com/gin-gonic/gin"
)

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
		logger.Logger.Printf("Failed to get file from form: %v", err)
		c.JSON(500, err)
		return
	}

	file, err := f.Open()
	if err != nil {
		logger.Logger.Printf("Failed to open file from form: %v", err)
		c.JSON(500, err)
	}
	defer file.Close()

	conn := o.getModelClient(c, r.Model)
	client := audio.NewAudioClient(conn)
	stream, err := client.Transcribe(context.Background())
	if err != nil {
		logger.Logger.Printf("Failed to create transcription client: %v", err)
		c.JSON(500, err)
	}

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
			logger.Logger.Printf("Failed to read bytes from file: %v", err)
			c.JSON(500, err)
			return
		}

		r := &audio.AudioRequest{
			Request: &audio.AudioRequest_ChunkData{
				ChunkData: chunk,
			},
		}

		if err = stream.Send(r); err != nil {
			logger.Logger.Printf("Failed to send inference request to gRPC server: %v", err)
			c.JSON(500, err)
			return
		}

		if err == nil && n < chunkSize {
			break
		}
	}

	reply, err := stream.CloseAndRecv()
	if err != nil {
		logger.Logger.Printf("Failed to get transcription reply from gRPC server: %v", err)
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
		logger.Logger.Printf("Failed to get file from form: %v", err)
		c.JSON(500, err)
		return
	}

	file, err := f.Open()
	if err != nil {
		logger.Logger.Printf("Failed to open file from form: %v", err)
		c.JSON(500, err)
		return
	}
	defer file.Close()

	conn := o.getModelClient(c, r.Model)
	client := audio.NewAudioClient(conn)
	stream, err := client.Translate(context.Background())
	if err != nil {
		logger.Logger.Printf("Failed to create translation client: %v", err)
		c.JSON(500, err)
	}

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
			logger.Logger.Printf("Failed to read bytes from file: %v", err)
			c.JSON(500, err)
			return
		}

		r := &audio.AudioRequest{
			Request: &audio.AudioRequest_ChunkData{
				ChunkData: chunk,
			},
		}

		if err = stream.Send(r); err != nil {
			logger.Logger.Printf("Failed to send inference request to gRPC server: %v", err)
			c.JSON(500, err)
			return
		}

		if err == nil && n < chunkSize {
			break
		}
	}

	reply, err := stream.CloseAndRecv()
	if err != nil {
		logger.Logger.Printf("Failed to get translation reply from gRPC server: %v", err)
		c.JSON(500, err)
	}

	c.JSON(200, reply)
}
