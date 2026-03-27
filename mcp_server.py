from ast import Add

from pydantic import Field

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

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
    return docs[doc_id]


@mcp.resource("docs://documents", mime_type="application/json")
def list_documents()-> list[str]:
    return list(docs.keys())

@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def get_document(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrite a document in markdown format. The document content is provided as input and the output should be the rewritten document in markdown format."
)
def format_document(
    doc_id: str = Field(description="ID of the document to format")
) -> list[base.Message]:    
    # For simplicity, this example just wraps the content in markdown code block syntax.
    # In a real implementation, you would use a library or more complex logic to convert the document to markdown format.

    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.
    The id of the document you need to reformat is:

    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
    Use the 'edit_document' tool to edit the document. After the document has been reformatted...
    """

    return [base.UserMessage(prompt)]

# TODO: Write a prompt to summarize a doc
@mcp.prompt(
    name="summarize",
    description="Summarize the content of a document. The document content is provided as input and the output should be a concise summary of the document."
)
def summarize_document(
    doc_id: str = Field(description="ID of the document to summarize")
) -> list[base.Message]:    
    prompt = f"""
    Your goal is to summarize a document into 2-3 lines. The id of the document you need to summarize is:

    <document_id>
    {doc_id}
    </document_id>

    Read through the document and provide a concise summary of the key points and information contained in the document.
    """

    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
