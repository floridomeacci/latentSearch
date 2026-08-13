# LatentSearch

[LatentSearch](https://latentsearch.net) is a search-engine experiment where the results are generated at request time instead of retrieved from a crawled index. It can produce text results, image results, and a generated preview for a selected result.

[![LatentSearch preview](assets/preview.png)](https://latentsearch.net)

## How it works

The browser sends a query to the Python API. The API keeps provider credentials on the server, moderates the query, requests generated results from Replicate, and returns the response to the browser. Text search, images, and page previews use separate model endpoints.

## Tech stack

| Area | Technology |
|---|---|
| Interface | Vanilla HTML, CSS, and JavaScript |
| Local server | Python 3 standard library and `ThreadingHTTPServer` |
| Serverless adapter | Python on Vercel |
| Text generation | Meta Llama 4 Scout through Replicate |
| Image generation | z-image-turbo through Replicate |
| Page previews | DeepSeek V3 through Replicate |
| Moderation | Llama Guard 3 through Replicate |
| Touch feedback | web-haptics |

[![Tech stack: Python, JavaScript, HTML, and CSS](https://skillicons.dev/icons?i=py,js,html,css)](https://skillicons.dev)

## Run locally

The server has no third-party Python dependencies.

```bash
git clone https://github.com/floridomeacci/latentSearch.git
cd latentSearch
cp .env.example .env
python3 server.py
```

Add a valid `REPLICATE_API_TOKEN` to `.env`, then open <http://localhost:8180>. Do not commit `.env` or any generated request logs.

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `REPLICATE_API_TOKEN` | Required provider token | None |
| `ADMIN_TOKEN` | Protects the local search-log endpoint | Disabled when empty |
| `PORT` | Local HTTP port | `8180` |
| `DAILY_SEARCH_LIMIT` | Daily text-search cap | `500` |
| `DAILY_PAGE_LIMIT` | Daily page-preview cap | `200` |
| `DAILY_IMAGE_LIMIT` | Daily image-request cap | `400` |
| `GEN_LOG_FILE` | Generated-content log path | `query_generations.log` |

The application also applies a per-IP request limit and response security headers. These controls supplement, but do not replace, protection at the hosting layer.

## Project structure

```text
api/index.py   Vercel adapter for the Python handler
server.py      API proxy, local server, moderation, and request limits
index.html     Search home page
search.html    Text-results page
images.html    Image-results page
js/            Browser behavior and API client code
css/           Site styles
```

The Vercel configuration serves static files from the repository and rewrites `/api/*` requests to the Python adapter.

## Support

[![Buy Me A Coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/floridomeacci)
