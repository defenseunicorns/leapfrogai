package config

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/BurntSushi/toml"
)

type Config map[string]Model

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

func LoadConfigs(path string) (Config, error) {
	// get all *.toml files in the path
	c := make(Config)
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
		_, err = toml.DecodeFile(fileName, &config)
		if err != nil {
			fmt.Printf("Error loading toml file %v: %v", fileName, err)
			continue
		}
		for k, v := range config {
			c[k] = v
		}
	}

	return c, nil
}
