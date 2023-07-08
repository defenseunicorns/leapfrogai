package hf

type GenerateRequest struct {
	Inputs     string             `json:"inputs"`
	Parameters GenerateParameters `json:"parameters"`
	Stream     bool               `json:"stream"`
}

type GenerateParameters struct {
	BestOf              *int     `json:"best_of,omitempty"`
	DecoderInputDetails bool     `json:"decoder_input_details,omitempty"`
	Details             bool     `json:"details,omitempty"`
	DoSample            bool     `json:"do_sample,omitempty"`
	MaxNewTokens        int      `json:"max_new_tokens,omitempty"`
	RepetitionPenalty   *float32 `json:"repetition_penalty,omitempty"`
	ReturnFullText      *bool    `json:"return_full_text,omitempty"`
	Seed                *int64   `json:"seed,omitempty"`
	Stop                []string `json:"stop,omitempty"`
	Temperature         *float32 `json:"temperature,omitempty"`
	TopK                *int     `json:"top_k,omitempty"`
	TopP                *float32 `json:"top_p,omitempty"`
	Truncate            *int     `json:"truncate,omitempty"`
	TypicalP            *float32 `json:"typical_p,omitempty"`
	Watermark           bool     `json:"watermark,omitempty"`
}

type Token struct {
	ID      int     `json:"id"`
	Text    string  `json:"text"`
	Logprob float32 `json:"logprob"`
	Special bool    `json:"special"`
}

type GenerateStreamResponse struct {
	Token         *Token      `json:"token"`
	GeneratedText string      `json:"generated_text"` // Assuming it can be of any type, hence using `interface{}`
	Details       interface{} `json:"details"`        // Assuming it can be of any type, hence using `interface{}`
}

type GenerateResponse struct {
	Details       *Details `json:"details"`
	GeneratedText string   `json:"generated_text"`
}

type Details struct {
	BestOfSequences []BestOfSequence `json:"best_of_sequences"`
	FinishReason    string           `json:"finish_reason"`
	GeneratedTokens int              `json:"generated_tokens"`
	Prefill         []Token          `json:"prefill"`
	Seed            int              `json:"seed"`
	Tokens          []Token          `json:"tokens"`
}

type BestOfSequence struct {
	FinishReason    string  `json:"finish_reason"`
	GeneratedText   string  `json:"generated_text"`
	GeneratedTokens int     `json:"generated_tokens"`
	Prefill         []Token `json:"prefill"`
	Seed            int     `json:"seed"`
	Tokens          []Token `json:"tokens"`
}
