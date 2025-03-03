#!/bin/bash

/bin/ollama serve &
pid=$!

sleep 5

echo " 🔴 Retrieve mxbai-embed-large embeddings"
ollama pull mxbai-embed-large
echo "🟢 Model has been downloaded"

sleep 5

echo " 🔴 Retrieve llama3 8b model"
ollama run llama3:8b
echo "🟢 Model has been downloaded"

wait $pid



