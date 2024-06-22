# Repositories
Romanian LLM Github Repository: https://github.com/Andrei481/licenta

Romanian Chatbot Mobile Application Repository: https://github.com/Andrei481/RomanianChatbot

My Huggingface account (where the models and datasets can be found): https://huggingface.co/Andrei481

# Romanian LLM Testing
1. Install text-generation-webui using the installation steps: https://github.com/oobabooga/text-generation-webui?tab=readme-ov-file#how-to-install
2. From text-generation-webui, download and load one of the models (_Andrei481/Llama-2-13b-chat-open-instruct-v1-ro_ / _Andrei481/llama-3-8b-unsloth-corpus-open-instruct-ro-16b_ / _Andrei481/llama-3-8b-instruct-unsloth-open-instruct-ro-16b_ / _Andrei481/Mistral-7B-Instruct-v0.2-open-instruct-ro_) from my Huggingface account.
3. Test the model's inference (use the appropriate prompt format from the model card on the Huggingface page for the best results).

# Romanian Chatbot Mobile Application
1. Connect through SSH to the Google Cloud VM instance and start the application's backend using the ```./start_server.sh``` script.

2. From the LLM virtual machine, open a terminal and use only the first 2 GPU's using the command:

```export CUDA_VISIBLE_DEVICES=0,1```

3. Activate the appropriate environment using the command: 

```conda activate mobile-app```.

4. Start the vLLM inference server with the _Andrei481/llama-3-8b-instruct-unsloth-open-instruct-ro-16b_ model, on both GPUs, on port 8001 using the command:

```python -m vllm.entrypoints.api_server --model Andrei481/llama-3-8b-instruct-unsloth-open-instruct-ro-16b --tensor-parallel-size=2 --port 8001```

5. Open another terminal and use only the third GPU using the command:

```export CUDA_VISIBLE_DEVICES=2```

6. Repeat step 3.

7. Start the FastAPI LLM server on port 8000 using the command: 

```uvicorn main:app --host 0.0.0.0 --port 8000```

8. Download and install the latest release from: [https://github.com/Andrei481/RomanianChatbot/releases](https://github.com/Andrei481/RomanianChatbot/releases)

9. Connect to the UPT network using OpenVPN.

10. Enjoy the app!
