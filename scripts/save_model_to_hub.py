import torch
import locale

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from accelerate import Accelerator


model_name = "mistralai/Mistral-7B-v0.1"
new_model = "Mistral-7B-v0.1-Romanian"
# device_map = {"": 0}
#device_map = {"": Accelerator().process_index}
cache_directory = "/mnt/storage/tmp"
print("BEfore from_pretrained")
base_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map='auto',
    cache_dir=cache_directory
)
print("Got to this part")
model = PeftModel.from_pretrained(base_model, new_model)
model = model.merge_and_unload()

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, cache_dir=cache_directory)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

locale.getpreferredencoding = lambda: "UTF-8"

model.push_to_hub("Andrei481/Mistral-7B-v0.1-Romanian", check_pr=True)

tokenizer.push_to_hub("Andrei481/Mistral-7B-v0.1-Romanian",check_pr=True)