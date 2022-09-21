from ..provider import GithubTemplatesProvider


def test_should_provide_a_template():
    name = "Node"
    provider = GithubTemplatesProvider()
    template = provider.get_template(name)
    assert template, f"Could not find template for name '{name}'"
    lines = template.text.split("\n")
    assert len(lines) == 131, "Expected 131 lines from Node.gitignore"


def test_should_retrieve_template_options():
    provider = GithubTemplatesProvider()
    options = provider.get_options()
    assert "Python" in options
