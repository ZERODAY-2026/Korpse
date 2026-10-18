
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:e2b"


def generate_response(
    prompt: str,
    output_format: str | None = None,
) -> str:
    """Generate a response using the locally running Ollama model."""

    payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False,
}

    if output_format is not None:
        payload["format"] = output_format

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180,
        )
        response.raise_for_status()
        result = response.json()
        return result["response"].strip()

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Cannot connect to Ollama. Make sure Ollama is running."
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "The model took too long to respond. Try a shorter prompt."
        ) from exc

    except (requests.exceptions.RequestException, KeyError, ValueError) as exc:
        raise RuntimeError(
            f"Failed to generate a model response: {exc}"
        ) from exc
