# import traceback, cv2, os
# from paddleocr import PPStructureV3, PaddleOCR
# # engine = PPStructureV3(lang='en')

# class Invoice_OCR:

#     def __init__(self):
#         self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'ocr_output')
#         os.makedirs(self.output_dir, exist_ok=True)

#     def image_ocr(self, img_path):
#         try:
#             output = engine.predict(img_path)
#             for res in output:
#                 res.save_to_json(save_path=self.output_dir)

#             print("\nOCR Done! Check folder:", output_dir)

#             return self.output_dir
#         except Exception as e:
#             traceback.print_exc()
#             print(f"Exception in image_ocr {e}")
#             return ''


#     def pdf_text_extract(self):
#         try:
#             pass
#         except Exception as e:
#             traceback.print_exc()
#             print(f"Exception in image_ocr {e}")
#             return ''