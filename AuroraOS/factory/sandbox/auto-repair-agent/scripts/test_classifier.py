"""Testes para o classificador de modo de sandbox."""
from classify_mode import classify_mode, classify_from_string, SandboxMode


def test_pytest_is_worktree():
    assert classify_mode(["pytest", "-q", "tests/"]) == SandboxMode.WORKTREE


def test_python_is_worktree():
    assert classify_mode(["python", "-m", "pytest"]) == SandboxMode.WORKTREE


def test_docker_is_container():
    assert classify_mode(["docker", "run", "test"]) == SandboxMode.CONTAINER


def test_curl_is_container():
    assert classify_mode(["curl", "http://localhost"]) == SandboxMode.CONTAINER


def test_empty_is_memory():
    assert classify_mode([]) == SandboxMode.MEMORY


def test_unknown_binary_is_memory():
    assert classify_mode(["echo", "hello"]) == SandboxMode.MEMORY


# CORREÇÃO E6: Regressões que a OS original teria
def test_no_false_positive_on_import():
    """'python -c import pytest' NÃO deve dar match em 'import'."""
    result = classify_mode(["python", "-c", "import pytest"])
    assert result == SandboxMode.WORKTREE  # Match por 'python', não 'import'


def test_no_false_positive_on_docker_in_filename():
    """'python test_docker_config.py' deve ser worktree, não container."""
    result = classify_mode(["python", "test_docker_config.py"])
    assert result == SandboxMode.WORKTREE


def test_string_classifier_handles_quotes():
    result = classify_from_string('pytest -q "tests/unit/"')
    assert result == SandboxMode.WORKTREE


def test_string_classifier_handles_malformed():
    result = classify_from_string("unclosed 'quote")
    assert result == SandboxMode.MEMORY  # Fallback seguro


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
        except AssertionError as e:
            print(f"  ❌ {t.__name__}: {e}")
            exit(1)
    print(f"\n{len(tests)} testes passaram.")
