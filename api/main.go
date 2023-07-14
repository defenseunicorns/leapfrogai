package main

import (
	"github.com/defenseunicorns/leapfrogai/api/backends/hf"
	"github.com/defenseunicorns/leapfrogai/api/backends/openai"
	"github.com/defenseunicorns/leapfrogai/api/config"
	"github.com/gin-gonic/gin"
	"github.com/penglongli/gin-metrics/ginmetrics"
)

func main() {
	go config.Watch()
	r := gin.Default()

	m := ginmetrics.GetMonitor()
	m.SetMetricPath("/metrics")

	m.Use(r)
	oaiHandler := &openai.OpenAIHandler{Prefix: "/openai/v1"}
	oaiHandler.Routes(r)
	r.GET("/healthz")

	hfHandler := &hf.Handler{Prefix: "/huggingface"}
	hfHandler.Routes(r)

	r.Run()
}
