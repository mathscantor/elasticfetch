class Parser():

    def __init__(self):
        self.description = "General Parser for any user inputs"

    '''
    Currently only supports "is" and "is_not" filter keywords.
    '''
    # TODO: Support other filter keywords
    def parse_filter_raw(self, filter_raw: str) -> dict:
        keyword_sentences_dict = {}
        is_not_list = []
        is_list = []
        filter_raw_tokens = filter_raw.strip().split(";")[0:-1]
        for filter_raw_token in filter_raw_tokens:
            if "is_not" in filter_raw_token:
                is_not_list.append(filter_raw_token.strip())
            elif "is" in filter_raw_token:
                is_list.append(filter_raw_token.strip())
        keyword_sentences_dict["is_not"] = is_not_list
        keyword_sentences_dict["is"] = is_list
        return keyword_sentences_dict
