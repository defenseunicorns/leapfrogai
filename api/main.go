package main

import (
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
	oaiHandler := &openai.OpenAIHandler{Prefix: "/openai"}
	oaiHandler.Routes(r)
	r.GET("/healthz")
	r.Run()
}
