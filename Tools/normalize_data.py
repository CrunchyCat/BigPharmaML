import sys
import csv

# Fill in Data
if __name__ == "__main__":
    # Check for Missing Arguments
    if len(sys.argv) < 2:
        print("Missing Command-Line Arguments\n" +
        "Usage: python3 fill_data.py <Input File: CSV> <Output File: CSV>")
        sys.exit("Exiting...")

    # Initialize Writer to stdout
    with open(sys.argv[2], 'w') as f_out:
        writer = csv.writer(f_out, dialect='unix', quoting=csv.QUOTE_MINIMAL)

        # Read CSV & Fill in Data from USPS API
        with open(sys.argv[1], 'r') as f_in:
            for i, row in enumerate(csv.reader(f_in)):
                if len(''.join(row).strip()) < 5:   # Skip Empty/Too Small Lines
                    continue
                if i == 0:                          # Write First Header
                    header = row
                    writer.writerow([row[i] for i in range(len(row)) if i != 4 and i != 8 and i != 9 and i != 10 and i != 65])
                    continue

                population = int(row[15])           # Get Population
                row[3] = int(row[3]) / population   # Normalize "Prevalence of obesity"
                row[6] = int(row[6]) / population   # Normalize "Diabetes"
                row[11] = int(row[11]) / population # Normalize "HIV/AIDS"
                row[19] = int(row[19]) / population # Normalize "WHITE"
                row[20] = int(row[20]) / population # Normalize "BLACK"
                row[21] = int(row[21]) / population # Normalize "AMERI_ES"
                row[22] = int(row[22]) / population # Normalize "ASIAN"
                row[23] = int(row[23]) / population # Normalize "HAWN_PI"
                row[24] = int(row[24]) / population # Normalize "HISPANIC" NOTE: Hispanic total is included in the other race options
                row[25] = int(row[25]) / population # Normalize "OTHER"
                row[26] = int(row[26]) / population # Normalize "MULT_RACE"
                row[27] = int(row[27]) / population # Normalize "MALES"
                row[28] = int(row[28]) / population # Normalize "FEMALES"
                row[29] = int(row[29]) / population # Normalize "AGE_UNDER5"
                row[30] = int(row[30]) / population # Normalize "AGE_5_9"
                row[31] = int(row[31]) / population # Normalize "AGE_10_14"
                row[32] = int(row[32]) / population # Normalize "AGE_15_19"
                row[33] = int(row[33]) / population # Normalize "AGE_20_24"
                row[34] = int(row[34]) / population # Normalize "AGE_25_34"
                row[35] = int(row[35]) / population # Normalize "AGE_35_44"
                row[36] = int(row[36]) / population # Normalize "AGE_45_54"
                row[37] = int(row[37]) / population # Normalize "AGE_55_64"
                row[38] = int(row[38]) / population # Normalize "AGE_65_74"
                row[39] = int(row[39]) / population # Normalize "AGE_75_84"
                row[40] = int(row[40]) / population # Normalize "AGE_85_UP"

                # Remove Empty Columns: "Asthma", "COPD", "Kidney Disease", "Cancer" & Duplicate "State"
                writer.writerow([row[i] for i in range(len(row)) if i != 4 and i != 8 and i != 9 and i != 10 and i != 65])