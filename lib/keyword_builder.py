class KeywordBuilder:
    def __init__(self):
        self.keywords = []

    def build(self, keywords):
        #check if | or /tcp is in the keyword, it means from nmap
        for keyword in keywords:
            if "|" in keyword or "/tcp" in keyword:
                keyword = keyword.split("|")
                self.keywords.append(f"{keyword[1]} {keyword[2]}")
            else:
                self.keywords.append(keyword)
        
        #remove duplicates and empty strings
        self.keywords = list(set(self.keywords))
        self.keywords = [x for x in self.keywords if x]            
            
