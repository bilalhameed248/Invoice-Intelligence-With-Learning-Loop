import os, re, traceback, json
class DataExtraction:

    def __init__(self):
        pass


    def rule_based_extraction(self, json_path):
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            rec_texts = data['overall_ocr_res']['rec_texts']
            extracted = {
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
                    extracted['vendor_name'] = line.split(':', 1)[1].strip() if ':' in line else line.replace('Payable To', '').strip()
                    last_key = None
                elif any(x in lower for x in ['invoice no', 'inv no', 'invoice#', 'inv-']):
                    extracted['invoice_number'] = line.split(':', 1)[1].strip() if ':' in line else line.split(':', 1)[-1].strip()
                    last_key = None
                elif 'date' in lower and any(c in line for c in ['/', '-']):  # rough date check
                    extracted['invoice_date'] = line.split(':', 1)[1].strip() if ':' in line else line
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
                        extracted['tax_amount'] = line
                    elif last_key == 'total':
                        extracted['total_amount'] = line
                    last_key = None  # reset after consuming value


            print(extracted)
            return extracted
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