class CsvProcessor:
    def __init__(self, customers_path, invoices_path, invoice_items_path):
        self.customers_path = customers_path
        self.invoices_path = invoices_path
        self.invoice_items_path = invoice_items_path

    def process_files(self, input_file_path):
        customer_ids = set()
        with open(input_file_path, "r") as input_file:
            header = input_file.readline()
            for line in input_file:
                customer_id = line.replace('"', "").strip()
                customer_ids.add(customer_id)

        self._process_file(self.customers_path, "CUSTOMER_CODE", customer_ids, "customers_selected.csv")
        invoices = self._process_file(self.invoices_path, "CUSTOMER_CODE", customer_ids, "invoices_selected.csv")

        invoice_codes = {invoice["INVOICE_CODE"] for invoice in invoices}
        self._process_file(self.invoice_items_path, "INVOICE_CODE", invoice_codes, "invoice_items_selected.csv")

    @staticmethod
    def _process_file(input_file_path, required_ids_column_name: str, required_ids: set, output_file_name):
        formatted_outputs = list()
        with open(input_file_path, "r") as input_file, open(f"outputs/{output_file_name}", "w") as output_file:
            header = input_file.readline()
            if not header:
                print("Missing header")
                return
            output_file.write(f"{header}")

            header = header.strip().replace('"', "").split(",")
            required_id_index = header.index(required_ids_column_name)
            outputs = list()

            for line in input_file:
                print(line)
                data = line.strip().replace('"', "").split(",")
                if len(data) != len(header):
                    print(f"Invalid line: {line}, skipping")
                    continue
                if data[required_id_index] in required_ids:
                    outputs.append(line)
                    formatted_output = dict()
                    for i in range(0, len(header)):
                        formatted_output[header[i]] = data[i]
                    formatted_outputs.append(formatted_output)

            output_file.writelines(outputs)
            return formatted_outputs
