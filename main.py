from SBChallenge import CsvProcessor
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    processor = CsvProcessor("customer_full.csv", "invoice_full.csv", "invoice_item_full.csv")
    processor.process_files("input_customers.csv")

