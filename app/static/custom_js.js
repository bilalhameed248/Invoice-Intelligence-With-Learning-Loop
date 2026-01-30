document.addEventListener('DOMContentLoaded', function() 
{

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
          }
        }

        // Update accounting proposal
        if (result.accounting_proposal) 
        {
          const debitSelect = document.querySelector('.form-select');
          if (debitSelect && result.accounting_proposal.debit_account) 
          {
            debitSelect.value = result.accounting_proposal.debit_account;
          }
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