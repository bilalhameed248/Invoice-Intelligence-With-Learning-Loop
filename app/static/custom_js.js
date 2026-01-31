document.addEventListener('DOMContentLoaded', function() 
{
  let extractedResult = null;
  document.getElementById('uploadBtn').addEventListener('click', async function() 
  {
    const fileInput = document.getElementById('invoiceFile');
    const file = fileInput.files[0];
    const statusDiv = document.getElementById('uploadStatus');
    
    if (!file) 
    {
      statusDiv.innerHTML = '<div class="alert alert-warning">Please select a file first</div>';
      return;
    }

    this.disabled = true;
    this.textContent = 'Processing...';
    statusDiv.innerHTML = '<div class="alert alert-info">Uploading and extracting data...</div>';

    const formData = new FormData();
    formData.append('file', file);

    try 
    {
      const response = await fetch('/api/invoice/upload', 
      {
        method: 'POST',
        body: formData
      });
      
      console.log(response)
      const result = await response.json();

      if (response.ok) 
      {
        statusDiv.innerHTML = '<div class="alert alert-success">Invoice extracted successfully!</div>';
        console.log(result);
        
        extractedResult = result;
        if (result.extracted_data) 
        {
          const vendorName = document.getElementById('vendor_name');
          const invoiceNumber = document.getElementById('invoice_number');
          const invoiceDate = document.getElementById('invoice_date');
          const taxAmount = document.getElementById('tax_amount');
          const totalAmount = document.getElementById('total_amount');

          if (vendorName) vendorName.value = result.extracted_data.vendor_name || '';
          if (invoiceNumber) invoiceNumber.value = result.extracted_data.invoice_number || '';
          
          // Convert date DD/MM/YYYY to YYYY-MM-DD
          if (invoiceDate && result.extracted_data.invoice_date) 
          {
            const dateStr = result.extracted_data.invoice_date;
            const parts = dateStr.split('/');
            if (parts.length === 3) 
            {
              const formattedDate = `${parts[2]}-${parts[1].padStart(2, '0')}-${parts[0].padStart(2, '0')}`;
              invoiceDate.value = formattedDate;
            }
          }
          
          // Remove commas from numeric values
          if (taxAmount) taxAmount.value = result.extracted_data.tax_amount ? result.extracted_data.tax_amount.replace(/,/g, '') : '';
          if (totalAmount) totalAmount.value = result.extracted_data.total_amount ? result.extracted_data.total_amount.replace(/,/g, '') : '';
        }

        // Update confidence score
        if (result.confidence_score) 
        {
          const confidenceSpan = document.querySelector('.confidence-low, .confidence-high');
          if (confidenceSpan) 
          {
            confidenceSpan.textContent = result.confidence_score.toFixed(2);
            confidenceSpan.className = result.confidence_score >= 0.8 ? 'confidence-high' : 'confidence-low';
            if (result.confidence_score < 0.8) 
            {
              document.getElementById('manual_review_badge').style.display = 'inline-block';
            }
          }
        }

        // Update accounting proposal
        if (result.accounting_proposal) 
            {
            renderAccountingEntry(result.accounting_proposal);
          }
      } 
      else 
      {
        statusDiv.innerHTML = `<div class="alert alert-danger">Error: ${result.error || 'Upload failed'}</div>`;
      }
    } 
    catch (error) 
    {
      statusDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
      console.error('Upload error:', error);
    } 
    finally 
    {
      this.disabled = false;
      this.textContent = 'Upload & Extract';
    }
  });


  function renderAccountingEntry(entry) 
  {
    const tbody = document.getElementById("journalEntries");
    if (!tbody) return;
    tbody.innerHTML = "";
    // Debit rows
    if (entry.debit && Array.isArray(entry.debit)) 
    {
      entry.debit.forEach(d => {
        tbody.innerHTML += `
          <tr>
            <td>Debit</td>
            <td>
              <input type="text" class="form-control" value="${d.account}">
            </td>
            <td>
              <input type="number" class="form-control" value="${d.amount}">
            </td>
          </tr>
        `;
      });
    }

    // Credit rows
    if (entry.credit && Array.isArray(entry.credit)) 
    {
      entry.credit.forEach(c => {
        tbody.innerHTML += `
          <tr>
            <td>Credit</td>
            <td>
              <input type="text" class="form-control" value="${c.account}" disabled>
            </td>
            <td>
              <input type="number" class="form-control" value="${c.amount}">
            </td>
          </tr>
        `;
      });
    }
  }


  document.getElementById('save_corrections_btn').addEventListener('click', async function() 
  {
      if (!extractedResult || !extractedResult.extracted_data) 
      {
          alert('Please upload and extract an invoice first!');
          return;
      }

      const statusDiv = document.getElementById('uploadStatus');

      const correctedFields = 
      {
          vendor_name: document.getElementById('vendor_name')?.value.trim() || '',
          invoice_number: document.getElementById('invoice_number')?.value.trim() || '',
          invoice_date: document.getElementById('invoice_date')?.value || '',
          tax_amount: parseFloat(document.getElementById('tax_amount')?.value) || null,
          total_amount: parseFloat(document.getElementById('total_amount')?.value) || null
      };

      const correctedAccounting = {
          debit: [],
          credit: []
      };

      document.querySelectorAll('#journalEntries tr').forEach(row => {
          const type = row.cells[0].textContent.trim();
          const accountInput = row.querySelector('input[type="text"]');
          const amountInput = row.querySelector('input[type="number"]');

          if (accountInput && amountInput) 
          {
              const entry = {
                  account: accountInput.value.trim(),
                  amount: parseFloat(amountInput.value) || 0
              };

              if (type === 'Debit')
             {
                  correctedAccounting.debit.push(entry);
              } 
              else if (type === 'Credit') 
              {
                  correctedAccounting.credit.push(entry);
              }
          }
      });

      const payload = 
      {
          invoice_id: correctedFields.invoice_number || extractedResult.extracted_data.invoice_number || 'unknown',
          model_version: "v1.0",
          predicted_fields: extractedResult.extracted_data || {},
          corrected_fields: {
              ...correctedFields,
              accounting: correctedAccounting
          },
          confidence: extractedResult.confidence_score || 0.0,
          ocr_text: extractedResult.ocr_text || ""
      };
      console.log(payload)

      try 
      {
          const response = await fetch('/api/invoice/feedback', 
          {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(payload)
          });

          const result = await response.json();
          if (response.ok) 
          {
              statusDiv.innerHTML = '<div class="alert alert-success">Corrections saved successfully! Thank you for your feedback.</div>';
              alert('Feedback saved successfully!');
          } 
          else 
          {
              statusDiv.innerHTML = `<div class="alert alert-danger">Error saving feedback: ${result.detail || 'Unknown error'}</div>`;
              alert('Failed to save feedback: ' + (result.detail || 'Unknown error'));
          }
      } 
      catch (err) 
      {
          statusDiv.innerHTML = '<div class="alert alert-danger">Network error while saving feedback</div>';
          console.error('Feedback save error:', err);
          alert('Failed to connect to server');
      }
  });


  // Preview uploaded file
  document.getElementById('invoiceFile').addEventListener('change', function(e) 
  {
    const file = e.target.files[0];
    const preview = document.getElementById('documentPreview');
    
    if (file) 
    {
      const fileType = file.type;
      
      if (fileType === 'application/pdf') 
      {
        const fileURL = URL.createObjectURL(file);
        preview.innerHTML = `
          <iframe src="${fileURL}" 
                  style="width: 100%; height: 600px; border: none; border-radius: 8px;">
          </iframe>
        `;
      } 
      
      else if (fileType.startsWith('image/')) 
      {
        const reader = new FileReader();
        reader.onload = function(event) {
          preview.innerHTML = `
            <img src="${event.target.result}" 
                 class="img-fluid" 
                 style="max-height: 600px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
          `;
        };
        reader.readAsDataURL(file);
      } 
      else 
      {
        preview.innerHTML = `
          <div class="d-flex align-items-center justify-content-center h-100">
            <p class="text-danger">Unsupported file type. Please upload PDF or image files.</p>
          </div>
        `;
      }
    }
  });

});