from vllm import LLM, SamplingParams


prompts = [
    """<s>[INST] <<SYS>>
Sunteți un asistent util, respectuos și onest. Dacă o întrebare nu are niciun sens sau nu este coerentă din punct de vedere factual, explicați de ce în loc să răspundeți la ceva incorect. Dacă nu știți răspunsul la o întrebare, vă rugăm să nu împărtășiți informaţii false. Trebuie sa răspundeți doar în limba română.
<</SYS>>

Care este capitala Romaniei?[/INST]
"""
]
sampling_params = SamplingParams(temperature=0.95, top_p=0.95, max_tokens=200)
# !!! MULTI GPU !!!
# => tensor_parallel_size = number of gpu's
llm = LLM(model="Andrei481/Llama-2-13b-chat-hakurei-ro-v0.3", tensor_parallel_size=3, max_model_len=512)
outputs = llm.generate(prompts, sampling_params)
# generated_text = outputs[0].text
# print(outputs)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"\nPrompt: {prompt!r}, Generated text: {generated_text!r}\n")