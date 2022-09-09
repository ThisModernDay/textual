import sys

from rich.syntax import Syntax
from rich.traceback import Traceback

from textual.app import App, ComposeResult
from textual.layout import Container, Vertical
from textual.reactive import Reactive
from textual.widgets import DirectoryTree, Footer, Header, Static


class CodeBrowser(App):
    """Textual code browser app."""

    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
        ("q", "quit", "Quit"),
    ]

    show_tree = Reactive.init(True)

    def watch_show_tree(self, show_tree: bool) -> None:
        """Called when show_tree is modified."""
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        path = "./" if len(sys.argv) < 2 else sys.argv[1]
        yield Header()
        yield Container(
            Vertical(DirectoryTree(path), id="tree-view"),
            Vertical(Static(id="code"), id="code-view"),
        )
        yield Footer()

    def on_directory_tree_file_click(self, event: DirectoryTree.FileClick) -> None:
        """Called when the user click a file in the directory tree."""
        code_view = self.query_one("#code", Static)
        try:
            syntax = Syntax.from_path(
                event.path,
                line_numbers=True,
                word_wrap=True,
                indent_guides=True,
                theme="monokai",
            )
        except Exception:
            code_view.update(Traceback(theme="monokai", width=None))
            self.sub_title = "ERROR"
        else:
            code_view.update(syntax)
            self.query_one("#code-view").scroll_home(animate=False)
            self.sub_title = event.path

    def action_toggle_files(self) -> None:
        self.show_tree = not self.show_tree


app = CodeBrowser(css_path="code_browser.css")
if __name__ == "__main__":
    app.run()
