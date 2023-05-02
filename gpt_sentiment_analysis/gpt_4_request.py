curl https://api.openai.com/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{"prompt": "https://t.co/f93xEd2 Excited to share my latest blog post! ->", "max_tokens": 1, "model": "YOUR_FINE_TUNED_MODEL_NAME"}'
