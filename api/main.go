package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/defenseunicorns/leapfrogai/api/backends/hf"
	"github.com/defenseunicorns/leapfrogai/api/backends/openai"
	"github.com/defenseunicorns/leapfrogai/api/config"
	"github.com/gin-gonic/gin"
	"github.com/penglongli/gin-metrics/ginmetrics"
)

func main() {
	noDB := flag.Bool("nodb", false, "Run the API server without a database (no authentication or request logging performed)")
	flag.Parse()

	go config.Watch()
	r := gin.Default()

	m := ginmetrics.GetMonitor()
	m.SetMetricPath("/metrics")

	m.Use(r)
	var oaiHandler *openai.OpenAIHandler
	// check if database connection is desired
	if *noDB {
		oaiHandler = &openai.OpenAIHandler{Prefix: "/openai/v1", Database: nil}
		fmt.Print(noDB)
	} else {
		oaiDatabase, err := openai.ConnectDB()
		if err != nil {
			fmt.Printf("ERROR: %v\n", err)
			os.Exit(-1)
		}
		oaiHandler = &openai.OpenAIHandler{Prefix: "/openai/v1", Database: oaiDatabase}
	}
	oaiHandler.Routes(r)
	r.GET("/healthz")

	hfHandler := &hf.Handler{Prefix: "/huggingface"}
	hfHandler.Routes(r)

	r.Run()
}
