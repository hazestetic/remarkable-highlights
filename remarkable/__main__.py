from remarkable.document import Document, sync_documents


def main():
    sync_documents()
    doc = Document()
    
    for highlight in doc.highlights:
        print(highlight)
    

if __name__ == "__main__":
    main()