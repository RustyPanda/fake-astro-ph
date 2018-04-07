import io

def load_text_from_txtfile(fname):
    # Get raw text as string.
    # Ensure the encoding is handled properly!

    with io.open(fname, "r", encoding="utf-8") as f:
        text = f.read()

    return text
