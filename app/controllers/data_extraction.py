import os, re, traceback, json
import pandas as pd
class DataExtraction:

    def __init__(self):
        pass
        
    def invoice_table_to_dataframe(self, json_data):
        try:
            table_block = next((b for b in json_data.get("parsing_res_list", []) if b["block_label"] == "table"), None)
            if not table_block or not table_block.get("block_content"):
                return pd.DataFrame()
            df = pd.read_html(table_block["block_content"])[0]
            if df.iloc[0].isna().sum() == 0:
                df.columns = df.iloc[0]
                df = df[1:].reset_index(drop=True)
            return df
            
        except Exception as e:
            traceback.print_exc()
            print(f"Exception in rule_based_extraction {e}")
            return ''

    def rule_based_extraction(self, json_path):
        try:
            with open(json_path, "r") as f:
                json_data = json.load(f)

            invoice_table = self.invoice_table_to_dataframe(json_data)

            rec_texts = json_data['overall_ocr_res']['rec_texts']
            extracted_data = {
                'vendor_name': None,
                'invoice_number': None,
                'invoice_date': None,
                'tax_amount': None,
                'total_amount': None
            }

            last_key = None

            for line in rec_texts:
                line = line.strip()
                if not line:
                    continue
                
                lower = line.lower()
                
                # Label detection (set state)
                if 'payable to' in lower:
                    extracted_data['vendor_name'] = line.split(':', 1)[1].strip() if ':' in line else line.replace('Payable To', '').strip()
                    last_key = None
                elif any(x in lower for x in ['invoice no', 'inv no', 'invoice#', 'inv-']):
                    extracted_data['invoice_number'] = line.split(':', 1)[1].strip() if ':' in line else line.split(':', 1)[-1].strip()
                    last_key = None
                elif 'date' in lower and any(c in line for c in ['/', '-']):  # rough date check
                    extracted_data['invoice_date'] = line.split(':', 1)[1].strip() if ':' in line else line
                    last_key = None
                
                # Summary section keywords
                elif any(k in lower for k in ['tax', 'gst', 'vat']):
                    last_key = 'tax'
                elif any(k in lower for k in ['total', 'grand total', 'amount due', 'payable']):
                    last_key = 'total'
                elif any(k in lower for k in ['subtotal', 'sub total']):
                    last_key = 'subtotal'
                
                # Value detection (numeric + currency-like)
                elif last_key and (line.replace(',', '').replace('.', '').isdigit() or 
                                re.match(r'^\d{1,3}(,\d{3})*(\.\d{2})?$', line)):
                    if last_key == 'tax':
                        extracted_data['tax_amount'] = line
                    elif last_key == 'total':
                        extracted_data['total_amount'] = line
                    last_key = None  # reset after consuming value


            # print(extracted_data)
            accounting_entries = self.propose_accounting_entry(extracted_data, invoice_table)
            # print(accounting_entries)
            return {"basic_invoice_data": extracted_data, "ocr_text": ' | '.join(rec_texts), "accounting_entry": accounting_entries, "confidence_score": 0.85}
        except Exception as e:
            traceback.print_exc()
            print(f"Exception in rule_based_extraction {e}")
            return {"basic_invoice_data": None, "accounting_entry": None}


    def propose_accounting_entry(self, extracted_data, line_items):
        try:
            total = float(extracted_data["total_amount"].replace(',', ''))
            tax = float(extracted_data["tax_amount"].replace(',', '')) if extracted_data.get("tax_amount") else 0.0
            debit_buckets = {}
            for _, row in line_items.iterrows():
                desc = row["Description"].lower()
                amount = float(row["Amount"])                                 # Can use AI model here for classification,
                if any(k in desc for k in ["supply", "cartridge", "stationery"]):
                    account = "Office Supplies Expense"
                elif any(k in desc for k in ["laptop", "computer", "printer"]):
                    account = "IT Equipment"
                else:
                    account = "General Expense"
                debit_buckets[account] = debit_buckets.get(account, 0) + amount
            entry = { "debit": [], "credit": []}
            
            for account, amount in debit_buckets.items():
                entry["debit"].append({"account": account,"amount": round(amount, 2)})
            if tax > 0:
                entry["debit"].append({"account": "Tax Receivable","amount": round(tax, 2)})
            entry["credit"].append({"account": "Accounts Payable", "amount": round(total, 2) })

            return entry
        except Exception as e:
            traceback.print_exc()
            print(f"Exception in rule_based_extraction {e}")
            return ''

    def model_extraction(self):
        try:
            pass
        except Exception as e:
            traceback.print_exc()
            print(f"Exception in model_extraction {e}")
            return ''