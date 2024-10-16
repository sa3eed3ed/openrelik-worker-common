# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Helper methods for reporting."""

import json
from enum import IntEnum


class MarkdownDocument:
    """A class to represent a Markdown document.

    Attributes:
        title(string): The title of the report.
        sections(list): A list of MarkdownDocumentSection objects.
    """

    def __init__(self, title: str = None):
        """Initializes a MarkdownDocument object.

        Args:
            title(string): The title of the document (optional).
        """
        self.title: str = title
        self.sections: list[MarkdownDocumentSection] = []
        self.fmt = MarkdownFormatter()

    def add_section(self):
        """Adds a new section to the document.

        Args:
            title(string): The title of the section (optional).
        """
        section = MarkdownDocumentSection()
        self.sections.append(section)
        return section

    def to_markdown(self):
        """Generates a Markdown representation of the document.

        Returns:
            string: A Markdown representation of the document.
        """
        if self.title:
            markdown_text = f"{self.fmt.title(text=self.title)}\n"

        for section in self.sections:
            markdown_text += f"\n{section.to_markdown()}"

        return markdown_text

    def to_dict(self):
        """Generates a dictionary representation of the document.

        Returns:
            dict: A dictionary representation of the document.
        """
        return {
            "title": self.title,
            "summary": self.summary,
            "content": self.to_markdown(),
            "priority": self.priority.value,
        }

    def to_json(self):
        """Generates a JSON representation of the document.

        Returns:
            string: A JSON representation of the document.
        """
        return json.dumps(self.to_dict())

    def __str__(self) -> str:
        """String representation of the document.

        Returns:
            string: A string representation of the document.
        """
        return self.to_markdown()


class MarkdownDocumentSection:
    """A class to represent a section of a markdown document.

    Attributes:
        content(list): A list of strings representing the content of the section.
        markdown(MarkdownFormatter): An instance of the MarkdownFormatter class.
    """

    def __init__(self):
        """Initializes a MarkdownDocumentSection object."""
        self.content = []
        self.fmt = MarkdownFormatter()

    def add_header(self, text, level=2):
        """Adds a header to the section.

        Args:
            text(string): The text of the header.
            level(int): The level of the header (corresponds to h1-h5) (optional).
        """
        self.content.append(self.fmt.heading(text=text, level=level))

    def add_bullet(self, text, level=1):
        """Adds a bullet point to the section.

        Args:
            text(string): The text of the bullet point.
            level(int): The indentation level of the bullet point (optional).
        """
        self.content.append(self.fmt.bullet(text, level=level))

    def add_code(self, text):
        """Add text formatted as code to the section.

        Args:
            text(string): The text of the code.
        """
        self.content.append(self.fmt.code(text))

    def add_code_block(self, text):
        """Add text formatted as a code block to the section.

        Args:
            text(string): The text of the code block.
        """
        self.content.append(self.fmt.code_block(text))

    def add_paragraph(self, text):
        """Add text formatted as a paragraph to the section.

        Args:
            text(string): The text of the paragraph.
        """
        self.content.append(self.fmt.paragraph(text))

    def add_blockquote(self, text):
        """Add text formatted as a blockquote to the section.

        Args:
            text(string): The text of the blockquote.
        """
        self.content.append(self.fmt.blockquote(text))

    def add_horizontal_rule(self):
        """Add a horizontal rule to the section."""
        self.content.append(self.fmt.horizontal_rule())

    def add_table(self, table):
        """Add a table to the section.

        Args:
            table(MarkdownTable): The table to add.
        """
        return self.content.append(table.to_markdown())

    def to_markdown(self):
        """Generates a Markdown representation of the section.

        Returns:
            string: A Markdown representation of the section.
        """
        markdown_text = ""
        markdown_text += "\n".join(self.content)

        return markdown_text


class TaskReport(MarkdownDocument):
    """A class to represent a task report, inheriting from MarkdownDocument.

    Attributes:
        priority (int): The priority of the report.
        summary (str): A summary of the report.
    """

    def __init__(self, title):
        """Initializes a TaskReport object.

        Args:
            title (str): The title of the report.
        """
        super().__init__(title)
        self.priority = Priority.LOW
        self.summary = ""

    def to_dict(self):
        """Generates a dictionary representation of the report.

        Returns:
            dict: A dictionary representation of the report.
        """
        return {
            "title": self.title,
            "summary": self.summary,
            "content": self.to_markdown(),
            "priority": self.priority.value,
        }

    def to_json(self):
        """Generates a JSON representation of the report.

        Returns:
            str: A JSON representation of the report.
        """
        return json.dumps(self.to_dict())


class Priority(IntEnum):
    """Reporting priority enum to store common values.

    Priorities can be anything in the range of 0-100, where 0 is the highest
    priority.
    """

    LOW = 80
    MEDIUM = 50
    HIGH = 20
    CRITICAL = 10


class MarkdownFormatter:
    def bold(self, text):
        """Formats text as bold in Markdown format.

        Args:
          text(string): Text to format

        Return:
          string: Formatted text.
        """
        return f"**{text.strip():s}**"

    def heading(self, text, level=2):
        """Formats text as a heading in Markdown format.

        Args:
          text(string): Text to format
          level(int): Heading level (1-5)

        Return:
          string: Formatted text.
        """
        if not 1 <= level <= 5:
            raise ValueError("Heading level must be between 1 and 5")
        return f"{'#' * level} {text.strip()}"

    def title(self, text):
        """Create a H1 heading to use as page title.

        Args:
          text(string): Text to format

        Return:
          string: Formatted text.
        """
        return self.heading(text=text, level=1)

    def bullet(self, text, level=1):
        """Formats text as a bullet in Markdown format.

        Args:
          text(string): Text to format
          level(int): Indentation level

        Return:
          string: Formatted text.
        """
        return f"{'    ' * (level - 1):s}* {text.strip():s}"

    def code(self, text):
        """Formats text as code in Markdown format.

        Args:
          text(string): Text to format

        Return:
          string: Formatted text.
        """
        return f"`{text.strip():s}`"

    def code_block(self, text):
        """Formats text as a code block in Markdown format.

        Args:
          text(string): Text to format

        Return:
          string: Formatted text.
        """
        return f"```\n{text.strip()}\n```"

    def paragraph(self, text):
        """Formats text as a paragraph of text in Markdown format.

        Args:
          text(string): Text to format

        Return:
          string: Formatted text.
        """
        return f"\n{text.strip()}\n"

    def blockquote(self, text):
        """Formats text as a blockquote of text in Markdown format.

        Args:
          text(string): Text to format

        Return:
          string: Formatted text.
        """
        return f"> {text.strip()}\n"

    def horizontal_rule(self):
        """Formats a horizontal rule in Markdown format.

        Return:
          string: Formatted text.
        """
        return "\n---\n"


class MarkdownTable:
    def __init__(self, columns):
        """Initializes a MarkdownTable object.

        Args:
            columns(list): A list of strings representing the column names.
        """
        self.columns = columns
        self.rows = []

    def add_row(self, row_data):
        """Adds a row of data to the table.

        Args:
            row_data(list): A list of strings representing the row data.
        """
        if len(row_data) != len(self.columns):
            raise ValueError(
                "Number of columns in row data does not match table columns."
            )
        self.rows.append(row_data)

    def to_markdown(self):
        """Generates a Markdown representation of the table.

        Returns:
            string: A Markdown representation of the table.
        """
        markdown_text = "\n"
        markdown_text += "|" + "|".join(self.columns) + "|\n"
        markdown_text += "|" + "|".join(["---" for _ in self.columns]) + "|\n"
        for row in self.rows:
            markdown_text += "|" + "|".join(row) + "|\n"
        return markdown_text
