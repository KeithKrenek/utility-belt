# %%
import sys
import requests
from bs4 import BeautifulSoup, Comment

# %%
def fetch_html(url):
    """
    Fetch the HTML content of the URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        sys.exit(f"Error fetching URL: {e}")

def clean_soup(soup):
    """
    Remove scripts, styles, comments, and unwanted tags from the soup.
    Also remove extraneous attributes from allowed tags.
    """
    # Remove all <script> and <style> tags
    for element in soup(["script", "style", "noscript", "iframe", "footer", "header", "form"]):
        element.decompose()

    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Define allowed tags and attributes
    allowed_tags = {
        "p": [],
        "br": [],
        "h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": [],
        "ul": [], "ol": [], "li": [],
        "a": ["href", "title"],
        "strong": [],
        "em": [],
        "blockquote": [],
        "img": ["src", "alt"],  # optionally allow images with minimal attributes
    }

    def recursive_clean(tag):
        if tag.name is not None:
            # If the tag is not in allowed_tags and has a parent, unwrap it.
            if tag.name not in allowed_tags and tag.parent is not None:
                tag.unwrap()
                return  # Once unwrapped, stop processing this branch.
            elif tag.name in allowed_tags:
                # Only keep allowed attributes
                allowed_attrs = allowed_tags[tag.name]
                tag.attrs = {key: value for key, value in tag.attrs.items() if key in allowed_attrs}
        # Iterate over a copy of children because the structure might change during iteration.
        for child in list(tag.children):
            if hasattr(child, 'children'):
                recursive_clean(child)

    recursive_clean(soup)
    return soup

def build_minimal_html(soup):
    """
    Construct a minimal HTML document with a proper doctype and clean head/body.
    """
    minimal_html = BeautifulSoup("", "html.parser")

    # Create DOCTYPE manually; BeautifulSoup does not manage doctype so we prepend it later.
    doctype = "<!DOCTYPE html>\n"

    # Create html, head, and body elements
    html_tag = minimal_html.new_tag("html")
    minimal_html.append(html_tag)

    head_tag = minimal_html.new_tag("head")
    html_tag.append(head_tag)
    # Use the original page title if available
    orig_title = soup.title.string if soup.title and soup.title.string else "Minimal HTML"
    title_tag = minimal_html.new_tag("title")
    title_tag.string = orig_title
    head_tag.append(title_tag)

    body_tag = minimal_html.new_tag("body")
    html_tag.append(body_tag)

    # We assume that most of the main content is in the original <body>
    original_body = soup.body if soup.body else soup

    # Append the cleaned content from the original body into our new document.
    for child in original_body.contents:
        # Note: Extract and append each child so that our new document's body
        # consists only of cleaned elements.
        body_tag.append(child)

    # Prepend the doctype and return a string
    return doctype + minimal_html.prettify()
# %%
def main():
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python minimal_html.py <URL>")

    # url = sys.argv[1]
    url = "https://bam.elementsist.com/coach"
    html_content = fetch_html(url)

    # Parse fetched HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Clean the soup by removing unwanted elements and attributes
    clean = clean_soup(soup)

    # Build a new minimal HTML document
    minimal_html = build_minimal_html(clean)

    # For demonstration, print the minimal HTML to stdout.
    # You can also save it to a file if you prefer.
    print(minimal_html)

if __name__ == "__main__":
    main()
