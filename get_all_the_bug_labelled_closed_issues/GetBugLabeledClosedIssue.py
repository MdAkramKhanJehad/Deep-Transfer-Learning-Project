import requests
import auth_token as auth_token
import csv
import re

def get_all_urls():
	urls = []
	tools = []
	with open("get_all_the_bug_labelled_closed_issues/sast_tools.csv", "r") as f:
		reader = csv.reader(f)

		# Skip the first row.
		next(reader)

		for row in reader:
			urls.append(row[1])
			tools.append(row[0])

	return urls, tools

def get_all_the_comments(url):

	headers = {
		"Authorization": "Bearer " + auth_token.TOKEN
	}

	response = requests.get(url, headers=headers)
	all_comment = ""

	if response.status_code == 200:
		jsonResponse = response.json()
		commentCounter = 1
		for comment in jsonResponse:
			# print(commentCounter, ":", comment["body"])
			all_comment = all_comment + " \n " + str(comment["body"])
			# print(comment["html_url"])
			commentCounter += 1

	else:
		print(f"Error: {response.status_code}")

	# print("comment")
	return all_comment



def get_all_issues_with_bug_label(repo_link):
	repo_owner, repo_name = repo_link.split("/")[-2:]

	url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
	headers = {
		"Authorization": "Bearer " + auth_token.TOKEN
	}

	all_issues = []
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

				all_issues.extend(jsonResponse)

				if len(jsonResponse) < per_page:
					break
				page += 1

			else:
				print(f"Error: {response.status_code}")
				break

		except Exception as err:
			print(f'Other error occurred: {err}')
			break


	filtered_issues = []
	print("Total: ", len(all_issues))
	for issue in all_issues:
		if len(issue["labels"]) > 0:

			for label in issue["labels"]:
				if any(keyword in label["name"].lower() for keyword in ["bug", "enhancement", "feature", "proposal"]) and issue["state"] == "closed":
				# if any(keyword in label["name"].lower() for keyword in ["false positive", "false negative", "wontfix","wont fix", "won't fix"]) and issue["state"] == "closed":
					filtered_issues.append(issue)


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


def write_issue_details_in_file(issue_list, csv_filename, tool_name):
	# Check if the CSV file exists.
#   if not os.path.exists(csv_filename):
#     # Create the CSV file.
#     with open(csv_filename, "w") as f:
#       writer = csv.writer(f)
#       writer.writerow(fields)

  # Open the CSV file in append mode.
	with open(csv_filename, "a") as f:
		writer = csv.writer(f)

		fields = ["tool_name", "repository_url", "issue_html_url", "title", "descriptipon", "labels", "state", "state_reason", "comments", "comments_count", "created_at", "updated_at", "closed_at"]
		
		issueCounter = 0
		for issue in issue_list:
			row = []
			comments = get_all_the_comments(issue["comments_url"])
			comments =  remove_comments_new_lines(comments)
			# print("************************----", issue["comments_url"])
			# print(comments)

			row.append(tool_name)
			row.append(issue["repository_url"])
			row.append(issue["html_url"])
			row.append(issue["title"])
			description = remove_comments_new_lines(issue["body"])
			row.append(description)
			row.append(comments)
			row.append(issue["comments"])


			all_labels = ""
			for each_label in issue["labels"]:
				if all_labels != "":
					all_labels = all_labels + ", " + each_label["name"]
				else:	
					all_labels = each_label["name"]
			
			row.append(all_labels)
			row.append(issue["state"])
			row.append(issue["state_reason"])
			row.append(issue["created_at"])
			row.append(issue["updated_at"])
			row.append(issue["closed_at"])
			
			try:
				writer.writerow(row)
			except csv.Error as e:
				print(f"Error writing row {row}: {e}")

			issueCounter += 1
		


repo_urls, tool_names = get_all_urls()

counter = 0
for url in repo_urls:
	all_issues_with_bug_label = get_all_issues_with_bug_label(url)

	print("Total Bug labelled Closed Issues:", len(all_issues_with_bug_label))	
	
	write_issue_details_in_file(all_issues_with_bug_label, "get_all_the_bug_labelled_closed_issues/updated_issues.csv", tool_names[counter])
	

	print(counter)
	counter += 1