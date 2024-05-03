import pip._vendor.requests as requests
import csv
import re
import config
from datetime import datetime


def get_configurations():
    configs = config.configurations
    github_access_token = configs["token"]
    sorting_criteria = configs['sorting_criteria']
    search_keyword = configs['search_keyword']
    labels_for_filtering = configs['labels_for_filtering']
    number_of_issues_to_be_extracted = configs['N']

    return github_access_token, sorting_criteria, search_keyword, labels_for_filtering, number_of_issues_to_be_extracted


def get_all_urls():
    urls = []
    tools = []
    with open("LATEST_extact_issues/repository_of_tools.csv", "r") as f:
        reader = csv.reader(f)

        for row in reader:
            urls.append(row[0])
            tools.append(row[1])
    return urls, tools


def get_all_comments(issue_comments_url, access_token):
    headers = {
		"Authorization": "Bearer " + access_token
	}

    response = requests.get(issue_comments_url, headers=headers)
    comments_list = []

    if response.status_code == 200:
        jsonResponse = response.json()

        for idx, comment in enumerate(jsonResponse):
            comment_body =  remove_comments_new_lines(comment["body"])
            comment_data = {
                "comment_id": idx,
                "comment": comment_body
            }
            comments_list.append(comment_data)
    else:
        print(f"Error: {response.status_code}")
    return comments_list


def get_issues_with_label(repo_owner, repo_name, required_labels, access_token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {"Authorization": "Bearer " + access_token}
    issues = []
    page = 1
    per_page = 100
    while True:
        params = {
            "state": "all",
            "page": page,
            "per_page": per_page
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                jsonResponse = response.json()
                issues.extend(jsonResponse)
                if len(jsonResponse) < per_page:
                    break
                page += 1
            else:
                print(f"Error: {response.status_code}")
                break
        except Exception as err:
            print(f'Other error occurred: {err}')
            break

    
    if not required_labels:
        return issues

    filtered_issues = []
    # print("1-*- "*25,"\n", len(issues))

    for issue in issues:
	    if len(issue["labels"]) > 0:
              for label in issue["labels"]:
                   if any(keyword in label["name"].lower() for keyword in required_labels):
                       filtered_issues.append(issue)

    # print(len(filtered_issues))
    return filtered_issues


def remove_comments_new_lines(input_string):
	pattern = re.compile(r'<!--.*?-->', re.DOTALL) 

	if input_string is not None:
		result = re.sub(pattern, '', input_string)
		
		new_result = " ".join(result.splitlines())
		new_result = re.sub(r'\s+', ' ', new_result)

		return new_result
	else:
		return input_string


def write_issues_details_in_file(issues_list, csv_filename, tool_name, access_token):
    fields = ["ID", "Tool_Name", "Repository_URL", "Issue_HTML_URL", "Title", "Description", "Labels", "State", "State_Reason", "Comments", "Comments_Count", "Created_At", "Updated_At", "Closed_At", "Reactions_Count"]

    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fields)

        for idx, issue in enumerate(issues_list):
            row = []
            comments = get_all_comments(issue["comments_url"], access_token)
            comments_count = len(comments)
            reactions_count = issue["reactions"]["total_count"]
            labels = ", ".join(label["name"] for label in issue["labels"])
            description = remove_comments_new_lines(issue["body"])

            row.append(f"{tool_name}_{idx}")
            row.append(tool_name)
            row.append(issue["repository_url"])
            row.append(issue["html_url"])
            row.append(issue["title"])
            row.append(description)
            row.append(labels)
            row.append(issue["state"])
            row.append(issue["state_reason"])
            row.append(comments)
            row.append(comments_count)
            row.append(issue["created_at"])
            row.append(issue["updated_at"])
            row.append(issue["closed_at"])
            row.append(reactions_count)

            try:
                writer.writerow(row)
            except csv.Error as e:
                print(f"Error writing row {row}: {e}")


if __name__ == "__main__":
    repo_urls, tool_names = get_all_urls()
    github_access_token, sorting_criteria, search_and_filter_keyword, labels_for_filtering, N = get_configurations()

    for i, url in enumerate(repo_urls):
        repo_owner, repo_name = url.split("/")[-2:]
        # print("\nFetching issues from repository:", repo_owner + "/" + repo_name)
        all_issues = get_issues_with_label(repo_owner, repo_name, labels_for_filtering, github_access_token)

        # Filtering issues based on user-provided keyword
        if search_and_filter_keyword:
            filtered_issues = [issue for issue in all_issues if search_and_filter_keyword in issue["title"].lower() or search_and_filter_keyword in issue["body"].lower()]
        else:
            filtered_issues = all_issues

        # Sorting issues based on sorting criteria
        if sorting_criteria == "1":  
            sorted_issues = sorted(filtered_issues, key=lambda x: len(get_all_comments(x["comments_url"])), reverse=True)
        else:  
            sorted_issues = sorted(filtered_issues, key=lambda x: x["reactions"]["total_count"], reverse=True)

        # Extract top N and bottom N issues
        if N <= len(sorted_issues):
            top_N_issues = sorted_issues[:N]
            if N * 2 > len(sorted_issues):
                bottom_N_issues = sorted_issues[-(len(sorted_issues) - N):]
            else:
                bottom_N_issues = sorted_issues[-N:]
        else:
            top_N_issues = sorted_issues
            bottom_N_issues = []


        # print(f"TOOL:{tool_names[i]} || Top:{len(top_N_issues)} | bottom:{len(bottom_N_issues)}")
        combined_issues = top_N_issues + bottom_N_issues

        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y_%H:%M:%S")

        csv_filename = f"LATEST_extact_issues/{repo_owner}_{tool_names[i]}_issues_{current_time}.csv"
        write_issues_details_in_file(combined_issues, csv_filename, tool_names[i], github_access_token)
