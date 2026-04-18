from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures",
    "outlook.pdf": "This document presents the projected future performance of the system",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment"
}

@mcp.tool(
        title="read_document",
        description="Read the contents of a document and return it as a string")
def read_document(
    doc_id:str=Field(description="read the content of the document of this doc_id")
):
    if doc_id not in docs:
        raise ValueError(f"document of {doc_id} not found")
    return docs[doc_id]

@mcp.tool(
    title="edit_document",
    description="edit the content of the document with the given string"
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"document of {doc_id} not found")
    document=docs[doc_id]
    if old_str in document:
        document=document.replace(old_str,new_str)
        docs[doc_id] = document
    else:
        raise ValueError(f"no text as {old_str} found")
    return docs[doc_id]
if __name__ == "__main__":
    mcp.run(transport="stdio")