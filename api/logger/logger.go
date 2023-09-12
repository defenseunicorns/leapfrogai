package logger

import (
	"log"
	"os"
)

var Logger = log.New(os.Stdout, "[LeapfrogAI] ", log.Ldate|log.Ltime)
