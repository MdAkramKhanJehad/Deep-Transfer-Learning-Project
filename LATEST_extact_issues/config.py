configurations = {
    "token": "",    # write your GitHub access token
    "sorting_criteria": 1,  # 1 for sort by comments count, 0 for sort by reactions count
    "search_keyword": "",   # Write the keyword, which will search and filter the issues for that keyword. It will search in the title and description of the issues
    "labels_for_filtering": ["bug"],     #e.g., ["bug", "false-positive"]
    "N": 5  # Enter how many issues do you want to extract after sorting. It will extract top N and bottom N issue and merge them together in the output file
}