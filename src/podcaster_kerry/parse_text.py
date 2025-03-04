
def pdf_to_text(path):
    import tika
    from tika import parser
    parsed = parser.from_file(path)
    return parsed["content"]