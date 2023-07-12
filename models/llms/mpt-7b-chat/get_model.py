PRETRAINED_MODEL_NAME_OR_PATH = "mosaicml/mpt-7b-chat"
MODEL_SAVE_PATH = "./mpt-7b-chat-offline"
from transformers import AutoModelForCausalLM, AutoTokenizer

if __name__ == "__main__":
    """Load a model from a remote repository or local file path and save it in this directory
    so it can be copied into the container by the docker build script

    You also have to download the other 
    """
    tokenizer = AutoTokenizer.from_pretrained(
        PRETRAINED_MODEL_NAME_OR_PATH,
        trust_remote_code=True
    )
    tokenizer.save_pretrained(MODEL_SAVE_PATH)
    
    # load the model and save it to this directory in safetensors format
    model = AutoModelForCausalLM.from_pretrained(
        PRETRAINED_MODEL_NAME_OR_PATH,
        trust_remote_code=True
    )
    model.save_pretrained(MODEL_SAVE_PATH, use_safetensors=True)