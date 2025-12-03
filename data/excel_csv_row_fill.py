import csv

input_file = "Global Wellbeing Initiative Dataset.csv"
output_file = "better_wellbeing.csv"

with open(input_file, "r", newline="", encoding="latin-1") as f_in, \
     open(output_file, "w", newline="", encoding="utf-8") as f_out:

    reader = csv.reader(f_in)
    writer = csv.writer(f_out)

    last_col_a = ""
    last_col_b = ""

    for row in reader:
        # Ensure at least 2 columns
        while len(row) < 2:
            row.append("")

        # Column A
        if row[0].strip() != "":
            last_col_a = row[0]
        else:
            row[0] = last_col_a

        # Column B
        if row[1].strip() != "":
            last_col_b = row[1]
        else:
            row[1] = last_col_b

        writer.writerow(row)

print("Done! Wrote filled CSV to:", output_file)
