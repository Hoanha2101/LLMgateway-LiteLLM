# 🚀 LiteLLM Gateway - Google Vertex AI Setup

Unified gateway to manage Google Vertex AI models (Gemini 2.5, Embeddings) through a single API endpoint with automatic load balancing and fallback support.

## 📦 Installation

### 1. Download required files

```bash
curl -L https://raw.githubusercontent.com/BerriAI/litellm/main/docker-compose.yml -o docker-compose.yml
curl -o prometheus.yml https://raw.githubusercontent.com/BerriAI/litellm/main/prometheus.yml
echo "# LiteLLM config" > config.yaml
```

### 2. Create .env file

```bash
echo LITELLM_MASTER_KEY=sk-master-1234 >> .env
echo LITELLM_SALT_KEY=sk-salt-1234 >> .env
echo UI_USERNAME=admin >> .env
echo UI_PASSWORD=admin >> .env
```

⚠️ **Remember to change these values for production!**

### 3. Edit docker-compose.yml

Find and uncomment this section:

```yaml
#########################################
## Uncomment these lines to start proxy with a config.yaml file ##
# volumes:
#  - ./config.yaml:/app/config.yaml
# command:
#  - "--config=/app/config.yaml"
##############################################
```

Change to:

```yaml
volumes:
  - ./config.yaml:/app/config.yaml

command:
  - "--config=/app/config.yaml"
```

### 4. Create config.yaml - [Example]

```yaml
general_settings:
  master_key: "sk-master-1234" # Change this in production!

litellm_settings:
  # Drop incompatible params when switching between providers
  drop_params: True
  # Monitor success/failure through Prometheus
  success_callbacks: ["prometheus"]
  failure_callbacks: ["prometheus"]

router_settings:
  # Route to least-loaded model instance
  routing_strategy: least-busy
  # Auto-fallback if primary model fails
  fallbacks:
    - { "gemini-2.5-flash-lite": ["gemini-2.5-flash"] }

model_list:
  # Chat Models - Gemini 2.5 (Load Balanced)
  - model_name: gemini-2.5-flash-lite
    litellm_params:
      model: vertex_ai/gemini-2.5-flash-lite
      rpm: 100 # 100 requests/minute rate limit
      vertex_project: "gen-lang-client-0106782583"
      vertex_location: "us-central1"

  - model_name: gemini-2.5-flash
    litellm_params:
      model: vertex_ai/gemini-2.5-flash
      rpm: 100
      vertex_project: "gen-lang-client-0106782583"
      vertex_location: "us-central1"

  # Embedding Models - For RAG & Vector Search
  - model_name: text-embedding-004
    litellm_params:
      model: vertex_ai/text-embedding-004
      vertex_project: "gen-lang-client-0106782583"
      vertex_location: "us-central1"

  - model_name: text-multilingual-embedding-002
    litellm_params:
      model: vertex_ai/text-multilingual-embedding-002
      vertex_project: "gen-lang-client-0106782583"
      vertex_location: "us-central1"

  # Catch-all: forward any other model to Vertex AI
  - model_name: "*"
    litellm_params:
      model: vertex_ai/*
      vertex_project: "gen-lang-client-0106782583"
      vertex_location: "us-central1"
```

📚 [See full config options](https://docs.litellm.ai/docs/proxy/config_settings)

### 5. Start the gateway

```bash
docker compose up -d
```

## 🎯 Usage

### Web UI

- URL API: http://localhost:4000
- URL UI: http://localhost:4000/ui
- Login: admin / admin

### Test with cURL

**Chat Completion:**

```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer sk-master-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash",
    "messages": [{"role": "user", "content": "Explain AI in 50 words"}]
  }'
```

**Embeddings (RAG):**

```bash
curl -X POST http://localhost:4000/embeddings \
  -H "Authorization: Bearer sk-master-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-004",
    "input": ["This is a test document"]
  }'
```

### Python

**Chat:**

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-master-1234",
    base_url="http://localhost:4000"
)

# Uses gemini-2.5-flash (or falls back to gemini-2.5-flash-lite)
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[{"role": "user", "content": "Explain AI"}]
)
print(response.choices[0].message.content)
```

**Embeddings (for RAG):**

```python
embedding_response = client.embeddings.create(
    model="text-embedding-004",
    input="Document to embed"
)
vectors = embedding_response.data[0].embedding
print(f"Embedding dimension: {len(vectors)}")
```

## 🔧 Key Features

- **Load Balancing**: Distributes requests between gemini-2.5-flash and gemini-2.5-flash-lite
- **Auto Fallback**: If flash fails, automatically retries with flash-lite
- **Embedding Support**: Dedicated endpoints for embeddings (/v1/embeddings)
- **Multilingual**: Support for 100+ languages via text-multilingual-embedding-002
- **Monitoring**: Real-time metrics via Prometheus (http://localhost:9090)
- **Unified API**: Single master key for all models

## 🐛 Troubleshooting

```bash
# View logs
docker compose logs -f litellm

# Restart
docker compose restart

# Check health
curl http://localhost:4000/health
```

## 📚 Resources

- [Docs](https://docs.litellm.ai)
- [GitHub](https://github.com/BerriAI/litellm)
- [Supported Providers](https://docs.litellm.ai/docs/providers)

## 📁 Repository Layout

- `docker-compose.yml` — Docker setup for LiteLLM proxy + Prometheus monitoring
- `config.yaml` — Main configuration with Vertex AI models and routing rules ⭐
- `config.example.yaml` — Template configuration (safe to commit)
- `.env` — Environment variables & secrets (⚠️ DO NOT commit)
- `prometheus.yml` — Prometheus metrics scraper configuration
- `credential/` — Google Cloud service account JSON (⚠️ DO NOT commit)
- `requirements.txt` — Python dependencies
- `db_pg.py` — PostgreSQL database integration (optional)
- `emb.py` — Embedding utility script
- `main.py` — Main application entry point

Notes:

- Keep secrets out of the repository. Use `config.yaml.example` and `.env.example` for shareable samples.
- Populate `mao/README.md` with any guidance for contributors using the `mao` workspace.
