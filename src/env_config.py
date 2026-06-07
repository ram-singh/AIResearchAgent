"""Runtime environment configuration for notebooks and CLI entrypoints."""

from __future__ import annotations

import os
import ssl
import warnings
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENV_PATH = ROOT / ".env"


def _env_file_values(env_path: Path | None = None) -> dict[str, str | None]:
    path = env_path or DEFAULT_ENV_PATH
    if not path.exists():
        return {}
    return dotenv_values(path)


def _should_verify_ssl(env_values: dict[str, str | None]) -> bool:
    explicit = str(env_values.get("SSL_VERIFY", os.getenv("SSL_VERIFY", "true"))).lower()
    if explicit in ("false", "0", "no"):
        return False
    if explicit in ("true", "1", "yes"):
        return True

    ssl_cert = os.environ.get("SSL_CERT_FILE", "")
    if ssl_cert and not Path(ssl_cert).exists():
        # Broken corporate cert path (common with Zscaler) — fall back to no verify.
        return False

    return True


def _apply_env_file_overrides(env_values: dict[str, str | None]) -> None:
    """Prefer project .env values over stale system environment variables."""
    for key in (
        "SERPER_API_KEY",
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_MODEL",
        "LLM_PROVIDER",
        "OPENAI_API_KEY",
        "OPENAI_MODEL",
        "SSL_VERIFY",
    ):
        value = env_values.get(key)
        if value:
            os.environ[key] = value


def _configure_langsmith(env_values: dict[str, str | None]) -> None:
    langsmith_key = env_values.get("LANGSMITH_API_KEY")
    langsmith_tracing = str(env_values.get("LANGSMITH_TRACING", "")).lower() in (
        "true",
        "1",
        "yes",
    )

    if langsmith_tracing and langsmith_key:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_API_KEY"] = langsmith_key
        project = env_values.get("LANGSMITH_PROJECT") or "DeepAgent"
        os.environ["LANGCHAIN_PROJECT"] = project
        os.environ["LANGSMITH_PROJECT"] = project
        return

    for var in (
        "LANGCHAIN_TRACING_V2",
        "LANGSMITH_TRACING",
        "LANGSMITH_API_KEY",
        "LANGCHAIN_API_KEY",
        "LANGCHAIN_PROJECT",
        "LANGSMITH_PROJECT",
        "LANGCHAIN_ENDPOINT",
    ):
        os.environ.pop(var, None)

    os.environ["LANGCHAIN_TRACING_V2"] = "false"
    os.environ["LANGSMITH_TRACING"] = "false"


def _configure_ssl(verify_ssl: bool) -> None:
    ssl_cert = os.environ.get("SSL_CERT_FILE", "")
    if ssl_cert and not Path(ssl_cert).exists():
        os.environ.pop("SSL_CERT_FILE", None)

    custom_bundle = os.getenv("REQUESTS_CA_BUNDLE") or os.getenv("SSL_CA_BUNDLE")
    if verify_ssl and custom_bundle and Path(custom_bundle).exists():
        os.environ["SSL_CERT_FILE"] = custom_bundle
        os.environ["REQUESTS_CA_BUNDLE"] = custom_bundle
        return

    if verify_ssl:
        return

    os.environ["SSL_VERIFY"] = "false"
    ssl._create_default_https_context = ssl._create_unverified_context  # noqa: SLF001
    _patch_langchain_httpx_clients()


def _patch_langchain_httpx_clients() -> None:
    import functools

    from langchain_anthropic import _client_utils as anthropic_utils
    from langchain_anthropic import chat_models as anthropic_chat_models

    sync_wrapper = anthropic_utils._SyncHttpxClientWrapper
    async_wrapper = anthropic_utils._AsyncHttpxClientWrapper
    not_given = anthropic_utils._NOT_GIVEN

    @functools.lru_cache
    def patched_sync(
        *,
        base_url: str | None,
        timeout: object = not_given,
        anthropic_proxy: str | None = None,
    ):
        kwargs: dict[str, object] = {
            "base_url": base_url
            or os.environ.get("ANTHROPIC_BASE_URL")
            or "https://api.anthropic.com",
            "verify": False,
        }
        if timeout is not not_given:
            kwargs["timeout"] = timeout
        if anthropic_proxy is not None:
            kwargs["proxy"] = anthropic_proxy
        return sync_wrapper(**kwargs)

    @functools.lru_cache
    def patched_async(
        *,
        base_url: str | None,
        timeout: object = not_given,
        anthropic_proxy: str | None = None,
    ):
        kwargs: dict[str, object] = {
            "base_url": base_url
            or os.environ.get("ANTHROPIC_BASE_URL")
            or "https://api.anthropic.com",
            "verify": False,
        }
        if timeout is not not_given:
            kwargs["timeout"] = timeout
        if anthropic_proxy is not None:
            kwargs["proxy"] = anthropic_proxy
        return async_wrapper(**kwargs)

    anthropic_utils._get_default_httpx_client = patched_sync  # type: ignore[assignment]
    anthropic_utils._get_default_async_httpx_client = patched_async  # type: ignore[assignment]
    anthropic_chat_models._get_default_httpx_client = patched_sync  # type: ignore[assignment]
    anthropic_chat_models._get_default_async_httpx_client = patched_async  # type: ignore[assignment]


def configure_runtime_env(env_path: Path | str | None = None) -> dict[str, str]:
    """Apply SSL and LangSmith settings before making external API calls."""
    path = Path(env_path) if env_path else DEFAULT_ENV_PATH
    env_values = _env_file_values(path)
    _apply_env_file_overrides(env_values)

    verify_ssl = _should_verify_ssl(env_values)
    _configure_langsmith(env_values)
    _configure_ssl(verify_ssl)

    if not verify_ssl:
        warnings.warn(
            "SSL certificate verification is disabled (SSL_VERIFY=false or missing "
            "corporate cert). Use only on trusted networks.",
            stacklevel=2,
        )

    return {
        "ssl_verify": str(verify_ssl).lower(),
        "langsmith_tracing": os.getenv("LANGCHAIN_TRACING_V2", "false"),
    }
