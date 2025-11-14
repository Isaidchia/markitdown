from docling.document_converter import DocumentConverter

source = "textbook.pdf"
converter = DocumentConverter()
result = converter.convert(source)

markdown_output = result.document.export_to_markdown()
output_path = "textbook_docling.md"

with open(output_path, "w", encoding="utf-8") as destination_file:
    destination_file.write(markdown_output)

print(f"Wrote Markdown to {output_path}")