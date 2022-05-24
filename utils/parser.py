class Parser():

    def __init__(self):
        self.description = "General Parser for any user inputs"

    '''
    Currently only supports the following keywords:
    "is",
    "is_not",
    "is_gte",
    "is_gt",
    "is_lte",
    "is_lt",
    "is_not_gte",
    "is_not_gt",
    "is_not_lte",
    "is_not_lt"
    '''
    # TODO: Support other filter keywords
    def parse_filter_raw(self, filter_raw: str) -> dict:
        keyword_sentences_dict = {}
        is_not_list = []
        is_not_gte_list = []
        is_not_lte_list = []
        is_not_gt_list = []
        is_not_lt_list = []

        is_list = []
        is_gte_list = []
        is_lte_list = []
        is_gt_list = []
        is_lt_list = []
        filter_raw_tokens = filter_raw.strip().split(";")[0:-1]
        for filter_raw_token in filter_raw_tokens:
            if "is_not_gte" in filter_raw_token:
                is_not_gte_list.append(filter_raw_token.strip())
            elif "is_not_lte" in filter_raw_token:
                is_not_lte_list.append(filter_raw_token.strip())
            elif "is_not_gt" in filter_raw_token:
                is_not_gt_list.append(filter_raw_token.strip())
            elif "is_not_lt" in filter_raw_token:
                is_not_lt_list.append(filter_raw_token.strip())
            elif "is_not" in filter_raw_token:
                is_not_list.append(filter_raw_token.strip())
            elif "is_gte" in filter_raw_token:
                is_gte_list.append(filter_raw_token.strip())
            elif "is_lte" in filter_raw_token:
                is_lte_list.append(filter_raw_token.strip())
            elif "is_gt" in filter_raw_token:
                is_gt_list.append(filter_raw_token.strip())
            elif "is_lt" in filter_raw_token:
                is_lt_list.append(filter_raw_token.strip())
            elif "is" in filter_raw_token:
                is_list.append(filter_raw_token.strip())
        keyword_sentences_dict["is_not_gte"] = is_not_gte_list
        keyword_sentences_dict["is_not_lte"] = is_not_lte_list
        keyword_sentences_dict["is_not_gt"] = is_not_gt_list
        keyword_sentences_dict["is_not_lt"] = is_not_lt_list
        keyword_sentences_dict["is_not"] = is_not_list
        keyword_sentences_dict["is_gte"] = is_gte_list
        keyword_sentences_dict["is_lte"] = is_lte_list
        keyword_sentences_dict["is_gt"] = is_gt_list
        keyword_sentences_dict["is_lt"] = is_lt_list
        keyword_sentences_dict["is"] = is_list
        return keyword_sentences_dict
