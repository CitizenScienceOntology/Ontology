import pypdf2
def getPDFContent(path):
    with open(path, "rb") as f:
        content = ""
        # Load PDF into pyPDF
        pdf = PyPDF2.PdfFileReader(f)

        #Check for number of pages, prevents out of bounds errors
        max = 0
        if pdf.numPages > 3:
            max = 3
        else:
            max = (pdf.numPages - 1)

        # Iterate pages
        for i in range(0, max):
            # Extract text from page and add to content
            content += pdf.getPage(i).extractText() + "\n"
        # Collapse whitespace
        content = " ".join(content.replace(u"\xa0", " ").strip().split())
        return content
