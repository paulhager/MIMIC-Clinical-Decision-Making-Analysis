from os.path import join
from transformers import AutoModelForCausalLM, AutoTokenizer, GPTQConfig

base_models = "."  # Path to the directory containing the huggingface model download
model_name = "ClinicalCamel-70B"
base_model = join(base_models, model_name)

quantization_config = GPTQConfig(
    bits=4, group_size=32, dataset="wikitext2", desc_act=True, model_seqlen=4096
)

tokenizer = AutoTokenizer.from_pretrained(base_model)
quant_model = AutoModelForCausalLM.from_pretrained(
    base_model, quantization_config=quantization_config, device_map="auto"
)

quant_model.save_pretrained(join(base_models, "./ClinicalCamel-70B-GPTQ"))
