import json
import os

def extract_title_and_content(data):
    """Extract title and content blocks from the JSON"""
    title = data.get("name", "Untitled")
    content_blocks = []

    if "messages" in data:
        for message in data["messages"]:
            if "versions" in message:
                for version in message["versions"]:
                    if "steps" in version:
                        for step in version["steps"]:
                            if step.get("type") == "contentBlock" and "content" in step:
                                for content in step["content"]:
                                    if "text" in content:
                                        content_blocks.append(content["text"])

    return title, content_blocks

def title_and_content_to_markdown(title, content_blocks):
    """Convert title and content blocks to Markdown format"""
    markdown = f"# {title}\n\n"
    for i, block in enumerate(content_blocks, 1):
        markdown += f"## Content Block {i}\n\n{block}\n\n"
    return markdown

def main():
    # Prompt user for the input file
    input_file = input("Enter the path to the JSON file: ").strip()

    # Ensure the file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    # Generate output file name
    output_file = os.path.splitext(input_file)[0] + "_content.md"

    # Read the JSON data
    with open(input_file, "r") as file:
        try:
            json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON file. {e}")
            return

    # Extract title and content blocks
    title, content_blocks = extract_title_and_content(json_data)

    if not content_blocks:
        print("No 'contentBlock' entries found in the JSON file.")
        return

    # Convert to Markdown
    markdown_content = title_and_content_to_markdown(title, content_blocks)

    # Write the Markdown to the output file
    with open(output_file, "w") as file:
        file.write(markdown_content)

    print(f"Markdown file generated: {output_file}")

if __name__ == "__main__":
    main()
