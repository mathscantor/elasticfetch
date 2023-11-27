from typing import *


class Parser:

    def __init__(self):
        self.__keyword_sentences_dict = dict()
        return

    '''
    Currently only supports the following keywords:
    "is",
    "is_not",
    "is_gte",
    "is_gt",
    "is_lte",
    "is_lt",
    "is_one_of"
    "is_not_gte",
    "is_not_gt",
    "is_not_lte",
    "is_not_lt"
    "is_not_one_of"
    '''

    def parse_filter_raw(self,
                         filter_raw: str) -> Dict[str, List[str]]:
        """
        Parse a raw filter string and convert it into a dictionary representation.

        Example:
        ```
        "dst.port is_one_of 53,80,443; event.code is_not 4928; src.port is_not 3728;"
        =
        {
            "is_one_of": ['dst.port is_one_of 53,80,443],
            "is_not": ['event.code is_not 4928', 'src.port is_not 3728']
            "is": [],
            "is_not_one_of" = [],
            .
            .
            .
        }
        ```

        :param filter_raw: The raw filter string to be parsed.
        :type filter_raw: str

        :return: A dictionary representation of the parsed filter string, with field names as keys and
                 associated values as lists.
        :rtype: Dict[str, List[str]]
        """

        is_not_list = []
        is_not_gte_list = []
        is_not_lte_list = []
        is_not_gt_list = []
        is_not_lt_list = []
        is_not_one_of_list = []

        is_list = []
        is_gte_list = []
        is_lte_list = []
        is_gt_list = []
        is_lt_list = []
        is_one_of_list = []
        filter_raw_tokens = filter_raw.strip().split(";")[0:-1]
        for filter_raw_token in filter_raw_tokens:
            if "is_not_gte" in filter_raw_token:
                is_not_gte_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is_not_lte" in filter_raw_token:
                is_not_lte_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is_not_gt" in filter_raw_token:
                is_not_gt_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is_not_lt" in filter_raw_token:
                is_not_lt_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is_not_one_of" in filter_raw_token:
                is_not_one_of_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is_not" in filter_raw_token:
                is_not_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is_gte" in filter_raw_token:
                is_gte_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is_lte" in filter_raw_token:
                is_lte_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is_gt" in filter_raw_token:
                is_gt_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is_lt" in filter_raw_token:
                is_lt_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is_one_of" in filter_raw_token:
                is_one_of_list.append(' '.join(filter_raw_token.strip().split()))
            elif "is" in filter_raw_token:
                is_list.append(' '.join(filter_raw_token.strip().split()))
        self.__keyword_sentences_dict["is_not_gte"] = is_not_gte_list
        self.__keyword_sentences_dict["is_not_lte"] = is_not_lte_list
        self.__keyword_sentences_dict["is_not_gt"] = is_not_gt_list
        self.__keyword_sentences_dict["is_not_lt"] = is_not_lt_list
        self.__keyword_sentences_dict["is_not_one_of"] = is_not_one_of_list
        self.__keyword_sentences_dict["is_not"] = is_not_list
        self.__keyword_sentences_dict["is_gte"] = is_gte_list
        self.__keyword_sentences_dict["is_lte"] = is_lte_list
        self.__keyword_sentences_dict["is_gt"] = is_gt_list
        self.__keyword_sentences_dict["is_lt"] = is_lt_list
        self.__keyword_sentences_dict["is_one_of"] = is_one_of_list
        self.__keyword_sentences_dict["is"] = is_list
        return self.__keyword_sentences_dict

    @property
    def keyword_sentences_dict(self) -> Dict[str, List[str]]:
        """
        Get a dictionary mapping keywords to lists of associated sentences.

        Each keyword is associated with a list of sentences where it appears.

        :return: A dictionary where keys are keywords and values are lists of associated sentences.
        :rtype: Dict[str, List[str]]
        """
        return self.__keyword_sentences_dict
