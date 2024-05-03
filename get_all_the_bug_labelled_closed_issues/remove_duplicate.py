import sys
import csv

csv.field_size_limit(sys.maxsize)

def remove_duplicate(input_file, output_file):


  seen = []
  duplicate_count = 0

  with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)

    for row in reader:
      if row not in seen:
        writer.writerow(row)
        seen.append(row)
      else:
        duplicate_count += 1

  return duplicate_count


if __name__ == "__main__":
  input_file = "get_all_the_bug_labelled_closed_issues/issue_dataset.csv"
  output_file = "get_all_the_bug_labelled_closed_issues/output.csv"

  duplicate_count = remove_duplicate(input_file, output_file)

  print("The number of duplicate rows removed:", duplicate_count)
