# 🚀 LiteLLM Gateway - Quick Setup

Unified gateway to manage multiple LLM providers (OpenAI, DeepSeek, Gemini...) through a single API endpoint.

## 📦 Installation

### 1. Download required files

```bash
curl -L https://raw.githubusercontent.com/BerriAI/litellm/main/docker-compose.yml -o docker-compose.yml
curl -o prometheus.yml https://raw.githubusercontent.com/BerriAI/litellm/main/prometheus.yml
echo "# LiteLLM config" > config_llmgateway.yaml
```

### 2. Create .env file

```bash
echo "LITELLM_MASTER_KEY=sk-master-1234" >> .env
echo "LITELLM_SALT_KEY=sk-salt-1234" >> .env
echo "UI_USERNAME=admin" >> .env
echo "UI_PASSWORD=admin" >> .env
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
  - ./config_llmgateway.yaml:/app/config.yaml

command:
  - "--config=/app/config.yaml"
```

### 4. Create config_llmgateway.yaml - [Example]

```yaml
model_list:
  # GPT-4o (Premium)
  - model_name: smart-shop-gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: YOUR_OPENAI_KEY
    tags: ["premium", "vision", "high-speed"]

  # DeepSeek (Cost-Effective)
  - model_name: smart-shop-deepseek-r1
    litellm_params:
      model: deepseek/deepseek-r1
      api_key: YOUR_DEEPSEEK_KEY
    tags: ["standard", "long-context"]

  # Gemini 2.0 Flash (Ultra Fast)
  - model_name: smart-shop-gemini-2.0-flash
    litellm_params:
      model: gemini/gemini-2.0-flash-exp
      api_key: YOUR_GOOGLE_KEY
    tags: ["fast", "cost-effective"]

router_settings:
  routing_strategy: least-busy  # Load balancing
  allowed_fails: 3              # Allow 3 fails before cooldown
  cooldown_time: 30             # 30s cooldown after failures
  request_timeout: 60           # 60s timeout
  
  # Auto fallback
  fallbacks:
    - smart-shop-gpt-4o:
        - smart-shop-deepseek-r1
        - smart-shop-gemini-2.0-flash
  
  content_policy_fallbacks:
    - smart-shop-deepseek-r1:
        - smart-shop-gpt-4o
```

📚 [See full config options](https://docs.litellm.ai/docs/proxy/config_settings)

### 5. Start the gateway

```bash
docker compose up -d
```

## 🎯 Usage

### Web UI
- URL: http://localhost:4000
- Login: admin / admin

### Test with cURL

```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer sk-master-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smart-shop-gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Python

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-master-1234",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="smart-shop-gpt-4o",
    messages=[{"role": "user", "content": "Explain AI"}]
)
print(response.choices[0].message.content)
```

## 🔧 Key Features

- **Load Balancing**: Automatic load distribution across models
- **Auto Fallback**: Switch models on failure
- **Cost Tracking**: Monitor costs via Prometheus (http://localhost:9090)
- **Unified API**: Single API key for all models

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

## 📁 Repository layout

- `docker-compose.yml` — Primary docker-compose manifest for local and production deployments.
- `config_llmgateway.yaml` — Gateway runtime configuration (contains backend definitions and routing rules). This file is ignored by `.gitignore` to avoid committing secrets.
- `.env` — Local environment variables and secrets (DO NOT commit).
- `prometheus.yml` — Prometheus scrape configuration for gateway metrics.
- `mao/` — Workspace folder for local scripts, plugins, or experimental assets. This folder is intentionally empty by default; add a `README.md` inside `mao/` to document its purpose for your project.
- `.gitignore` — Added to ignore local secrets, virtual environments, and runtime configs.

Notes:
- Keep secrets out of the repository. Use `config_llmgateway.yaml.example` and `.env.example` for shareable samples.
- Populate `mao/README.md` with any guidance for contributors using the `mao` workspace.