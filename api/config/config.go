package config

import (
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

func LoadConfig(path string) (Config, error) {
	var config Config
	_, err := toml.DecodeFile(path, &config)

	return config, err
}
