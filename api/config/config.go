package config

import (
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/BurntSushi/toml"
	"github.com/fsnotify/fsnotify"
)

var DefaultConfig *Config = &Config{Models: map[string]*Model{}}

type Config struct {
	Models map[string]*Model
}

type Model struct {
	Metadata Metadata `toml:"metadata"`
	Network  Network  `toml:"network"`
}

type Metadata struct {
	OwnedBy     string   `toml:"owned_by"`
	Permission  []string `toml:"permission"`
	Description string   `toml:"description"`
	Tasks       []string `toml:"tasks"`
}

type Network struct {
	URL  string `toml:"url"`
	Type string `toml:"type"`
}

func loadConfigs(path string) (*Config, error) {
	// get all *.toml files in the path
	c := &Config{Models: map[string]*Model{}}
	files, err := os.ReadDir(path)
	if err != nil {
		return c, err
	}

	for _, file := range files {
		if file.IsDir() {
			continue
		}

		if filepath.Ext(file.Name()) != ".toml" {
			continue
		}
		fileName := filepath.Join(path, file.Name())
		fmt.Printf("Loading config from %v\n", fileName)
		var config Config
		_, err = toml.DecodeFile(fileName, &config.Models)
		if err != nil {
			fmt.Printf("Error loading toml file %v: %v", fileName, err)
			continue
		}
		for k, v := range config.Models {
			c.Models[k] = v
		}
	}

	return c, nil
}

func Watch() {
	var err error
	modelPath := os.Getenv("CONFIG_PATH")
	if modelPath == "" {
		modelPath = "."
	}
	fmt.Printf("Using config path: %v\n", modelPath)
	DefaultConfig, err = loadConfigs(modelPath)
	if err != nil {
		log.Fatalf("Error loading model config file: %v", err)
	}

	// Watch the config file
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatalf("Failed to create watcher: %v", err)
	}
	defer watcher.Close()
	err = watcher.Add(modelPath)
	if err != nil {
		log.Fatalf("Failed to add file to watcher: %v", err)
	}

	for {
		select {
		case event := <-watcher.Events:
			// Check if the file was modified
			if event.Op&fsnotify.Write == fsnotify.Write {
				fmt.Println("Configuration file changed, reloading...")

				// Reload the config file

				c, err := loadConfigs(modelPath)
				if err != nil {
					fmt.Printf("Error loading model config file: %v", err)
					fmt.Printf("Falling back to previous version")
					continue
				}
				DefaultConfig = c
			}
		case err := <-watcher.Errors:
			log.Printf("Watcher error: %v", err)
		}
	}
}
