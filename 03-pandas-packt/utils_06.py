import pandas as pd
import re

class FirstNameExtractor:

    def __init__(self, 
                 pattern_string=r',\s*([A-Z\-]+)'):
        # Compile the regex pattern to match the first name
        self.pattern = re.compile(pattern_string)

    def extract_first_name(self, name):
        match = self.pattern.search(name)
        if match:
            return match.group(1).title()  # Capitalize nicely
        return None
    
def test_first_name_extractor():
    extractor = FirstNameExtractor()
    test_names = [
        "AARON,  ELVIA J",
        "AARON,  JEFFERY M",
        "AARON,  KARINA",
        "AARON,  KIMBERLEI R",
        "ABAD JR,  VICENTE M",
        "ABARCA,  ANABEL",
        "ABARCA,  EMMANUEL",
        "ABASCAL,  REECE E",
        "ABBASI,  CHRISTOPHER",
        "ABBATACOLA,  ROBERT J"
    ]
    expected = [
        "Elvia",
        "Jeffery",
        "Karina",
        "Kimberlei",
        "Vicente",
        "Anabel",
        "Emmanuel",
        "Reece",
        "Christopher",
        "Robert"
    ]
    results = [extractor.extract_first_name(name) for name in test_names]
    assert results == expected #, f"Expected {expected}, got {results}"
    # print("All tests passed.")

# if __name__ == "__main__":
#     test_first_name_extractor()