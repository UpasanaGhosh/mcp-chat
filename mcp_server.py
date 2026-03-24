from dataclasses import Field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
    )
def read_document(
    doc_id: str = Field(description="ID of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    return docs[doc_id]

@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing the string in the document content with a new string."
)
def edit_document(
    doc_id: str = Field(description="ID of the document to edit"),
    old_string: str = Field(description="The string to be replaced. Must match exactly with the string in the document content, including whitespace."),
    new_string: str = Field(description="The new string to replace the old string in the document content")
):
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    docs[doc_id] = docs[doc_id].replace(old_string, new_string)


@mcp.tool(
    name="list_docs",
    description="Return a list of all document IDs."
)
def list_docs():
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
