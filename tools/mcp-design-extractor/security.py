"""
security.py — Módulo de Segurança Anti-SSRF, Sanitização e Roteamento Seguro
para o CDP Design System Extractor no Google Antigravity IDE.
"""

import ipaddress
import os
import re
import socket
from typing import Any, List, Optional, Set, Tuple
from urllib.parse import urlparse

# Faixas de IP privado e reservado (IPv4 e IPv6)
BLOCKED_IPV4_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("224.0.0.0/4"),
    ipaddress.ip_network("240.0.0.0/4"),
]

BLOCKED_IPV6_NETWORKS = [
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("::/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
    ipaddress.ip_network("ff00::/8"),
]

ALLOWED_SCHEMES: Set[str] = {"http", "https"}


class SecurityViolationError(Exception):
    """Lançada quando uma requisição viola a política de segurança anti-SSRF."""
    pass


class InvalidSchemeError(SecurityViolationError):
    """Lançada quando a URL utiliza um esquema não permitido."""
    pass


class SSRFSecurityError(SecurityViolationError):
    """Lançada quando a URL aponta para um endereço privado, loopback ou reservado."""
    pass


def is_test_mode_enabled() -> bool:
    """Verifica se o modo de teste interno foi autorizado via variável de ambiente."""
    return os.environ.get("CDP_TEST_MODE") == "1"


def is_private_or_reserved_ip(ip_str: str) -> bool:
    """Verifica se um endereço IP pertence a faixas privadas, loopback ou reservadas."""
    try:
        ip = ipaddress.ip_address(ip_str)
        if ip.version == 4:
            for net in BLOCKED_IPV4_NETWORKS:
                if ip in net:
                    return True
        elif ip.version == 6:
            for net in BLOCKED_IPV6_NETWORKS:
                if ip in net:
                    return True
        return False
    except ValueError:
        return True


def is_host_private_or_reserved(hostname: str) -> bool:
    """
    Verifica se um hostname (IP literal ou nome de domínio DNS)
    pertence ou resolve para faixas de rede privada, loopback ou reservada.
    """
    if not hostname or not isinstance(hostname, str):
        return True
    clean_host = hostname.strip().lower()
    if clean_host in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
        return True

    # 1. Se for diretamente um IP literal (IPv4 ou IPv6)
    try:
        ip = ipaddress.ip_address(clean_host)
        return is_private_or_reserved_ip(str(ip))
    except ValueError:
        pass

    # 2. Se for nome de domínio, resolve via DNS e inspeciona cada endereço retornado
    try:
        addr_info = socket.getaddrinfo(clean_host, None, proto=socket.IPPROTO_TCP)
        for _, _, _, _, sockaddr in addr_info:
            ip_candidate = sockaddr[0]
            if is_private_or_reserved_ip(ip_candidate):
                return True
        return False
    except Exception:
        # Se a resolução de DNS falhar ou for inacessível, bloqueia por padrão (fail-closed)
        return True


def validate_url(url: str) -> str:
    """
    Valida rigorosamente uma URL de entrada contra SSRF, esquemas maliciosos
    e destinos em redes locais/privadas.
    """
    if not url or not isinstance(url, str):
        raise InvalidSchemeError("A URL fornecida é nula ou inválida.")

    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower()

    if scheme not in ALLOWED_SCHEMES:
        raise InvalidSchemeError(
            f"Esquema '{scheme}' proibido. Apenas protocolos HTTP e HTTPS são permitidos."
        )

    hostname = parsed.hostname
    if not hostname:
        raise InvalidSchemeError("URL inválida: hostname ausente.")

    # Se estiver em modo de teste estrito, autoriza loopback local
    if is_test_mode_enabled() and hostname in ("localhost", "127.0.0.1", "::1"):
        return url

    # Bloqueio imediato de hostnames literais de loopback
    if hostname.lower() in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
        raise SSRFSecurityError(
            f"Acesso bloqueado: '{hostname}' é um endereço de loopback proibido."
        )

    # Resolução de DNS com checagem de todos os IPs retornados (IPv4 e IPv6)
    try:
        addr_info = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
        for _, _, _, _, sockaddr in addr_info:
            ip_candidate = sockaddr[0]
            if is_private_or_reserved_ip(ip_candidate):
                raise SSRFSecurityError(
                    f"Acesso bloqueado: O host '{hostname}' resolveu para o IP privado '{ip_candidate}'."
                )
    except socket.gaierror as e:
        raise SSRFSecurityError(f"Falha na resolução de DNS para '{hostname}': {e}")

    return url


def sanitize_text(text: str) -> str:
    """Sanitiza strings para prevenir injeções de HTML/XSS."""
    if not text:
        return ""
    text = str(text)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def sanitize_css_value(value: Any, fallback: str = "") -> str:
    """
    Sanitiza rigorosamente valores de propriedades CSS para inserção segura
    em blocos inline <style>, prevenindo quebras de contexto (</style>) e XSS.
    Elimina blocos <script> inteiros, tags HTML, caracteres de controle e escapes CSS.
    """
    if value is None:
        return fallback
    val_str = str(value).strip()
    if not val_str:
        return fallback

    # 1. Remove qualquer bloco <script>...</script> completo (tags e conteúdo executável)
    cleaned = re.sub(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", "", val_str, flags=re.IGNORECASE | re.DOTALL)
    # 2. Remove qualquer tag <style>...</style> ou tags de fechamento/abertura residuais
    cleaned = re.sub(r"<\s*/?\s*style[^>]*>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<\s*/?\s*script[^>]*>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    # 3. Remove pseudo-protocolos perigosos em CSS
    cleaned = re.sub(r"javascript\s*:", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"expression\s*\(", "", cleaned, flags=re.IGNORECASE)
    # 4. Remove caracteres de delimitação estrutural que permitem injeção CSS
    cleaned = (
        cleaned.replace("<", "")
        .replace(">", "")
        .replace(";", "")
        .replace("{", "")
        .replace("}", "")
        .strip()
    )
    return cleaned if cleaned else fallback


def sanitize_css_property(prop: str, value: str) -> Tuple[str, str]:
    """Sanitiza propriedades e valores CSS contra injeção de tags ou escapes."""
    clean_prop = re.sub(r"[^a-zA-Z0-9\-_]", "", str(prop).strip())
    clean_val = sanitize_css_value(value)
    return clean_prop, clean_val


async def security_route_guard(route) -> None:
    """
    Guarda de roteamento do Playwright: intercepta toda requisição secundária
    (iframe, fetch, stylesheet, script, websocket) e aborta se for destino interno/privado.
    """
    req_url = route.request.url
    try:
        parsed = urlparse(req_url)
        scheme = parsed.scheme.lower()
        if scheme not in ALLOWED_SCHEMES and scheme not in ("data", "about"):
            await route.abort("accessdenied")
            return

        if scheme in ALLOWED_SCHEMES:
            hostname = parsed.hostname
            if hostname:
                # Permite loopback apenas em modo teste autorizado
                if is_test_mode_enabled() and hostname in ("localhost", "127.0.0.1", "::1"):
                    await route.continue_()
                    return
                if is_host_private_or_reserved(hostname):
                    await route.abort("accessdenied")
                    return

        await route.continue_()
    except Exception:
        await route.abort("accessdenied")
