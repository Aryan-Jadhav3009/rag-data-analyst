class ContextBuilder:

    def build(self, results):
        sections = []

        for result in results:
            document = result["document"]

            sections.append(
                document.content
            )

        return "\n\n---\n\n".join(sections)