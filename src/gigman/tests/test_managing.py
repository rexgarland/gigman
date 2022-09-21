import os
import tempfile

from ..manager import DirectoryManager


def test_should_not_remove_previous_user_text():
    previous_text = "don't delete me!\nand this line, too!"

    name = "Node"
    content = "node_modules/"

    with tempfile.TemporaryDirectory() as tmpdir:
        with open(tmpdir + "/.gitignore", "w") as f:
            f.write(previous_text)

        # add a template
        manager = DirectoryManager(tmpdir)
        print(manager)
        manager.add_template(name, content)
        manager.save_gitignore()

        # remove the template
        manager2 = DirectoryManager(tmpdir)
        print(manager2)
        manager2.remove_template(name)
        manager2.save_gitignore()

        with open(tmpdir + "/.gitignore", "r") as f:
            new_text = f.read()

        assert new_text == previous_text


def test_should_not_add_duplicate_templates():
    template = "node_modules/\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = DirectoryManager(tmpdir)
        manager.add_template("Node", template)
        manager.add_template("Node", template)
        assert manager.get_existing_templates() == [
            "Node"
        ], "DirectoryManager allowed duplicate templates"


def test_should_remove_templates():
    template = "node_modules/\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = DirectoryManager(tmpdir)

        manager.add_template("Node", template)
        manager.save_gitignore()

        manager.remove_template("Node")
        manager.save_gitignore()

        m2 = DirectoryManager(tmpdir)
        assert m2.get_existing_templates() == [], "Could not remove Node template"


def test_should_see_previously_written_templates():
    template = "node_modules/\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = DirectoryManager(tmpdir)
        manager.add_template("Node", template)
        manager.save_gitignore()
        del manager

        m2 = DirectoryManager(tmpdir)
        assert m2.get_existing_templates() == [
            "Node"
        ], "Could not find previously added templates in ignore file"


def test_should_know_about_existing_templates():
    template = "node_modules/\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = DirectoryManager(tmpdir)
        manager.add_template("Node", template)
        assert manager.get_existing_templates() == [
            "Node"
        ], "Could not track a newly added template"


def test_should_not_overwrite_gitignore():
    text = "data"
    with tempfile.TemporaryDirectory() as tmpdir:
        ignorefile = tmpdir + "/.gitignore"
        with open(ignorefile, "w") as f:
            f.write(text)
        manager = DirectoryManager(tmpdir)
        manager.save_gitignore()
        with open(ignorefile, "r") as f:
            assert f.read() == text, "DirectoryManager overwrote the ignore file"


def test_should_create_gitignore():
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = DirectoryManager(tmpdir)
        manager.save_gitignore()
        assert ".gitignore" in os.listdir(
            tmpdir
        ), "Could not create an empty gitignore file"
