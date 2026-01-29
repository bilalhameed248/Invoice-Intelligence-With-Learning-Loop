document.getElementById('uploadBtn').addEventListener('click', async function() {
  const fileInput = document.getElementById('invoiceFile');
  const file = fileInput.files[0];
  const statusDiv = document.getElementById('uploadStatus');
  
  if (!file) {
    statusDiv.innerHTML = '<div class="alert alert-warning">Please select a file first</div>';
    return;
  }

  // Show loading state
  this.disabled = true;
  this.textContent = 'Processing...';
  statusDiv.innerHTML = '<div class="alert alert-info">Uploading and extracting data...</div>';

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/invoice/upload', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    if (response.ok) {
      statusDiv.innerHTML = '<div class="alert alert-success">Invoice extracted successfully!</div>';
      
      // Populate extracted fields
      if (result.extracted_data) {
        document.querySelector('input[value="ABC Traders Pvt Ltd"]').value = result.extracted_data.vendor_name || '';
        document.querySelector('input[value="INV-223"]').value = result.extracted_data.invoice_number || '';
        document.querySelector('input[type="date"]').value = result.extracted_data.invoice_date || '';
        document.querySelector('input[value="141.00"]').value = result.extracted_data.tax_amount || '';
        document.querySelector('input[value="2491.00"]').value = result.extracted_data.total_amount || '';
      }

      // Update confidence score
      if (result.confidence_score) {
        const confidenceSpan = document.querySelector('.confidence-low, .confidence-high');
        confidenceSpan.textContent = result.confidence_score.toFixed(2);
        confidenceSpan.className = result.confidence_score >= 0.8 ? 'confidence-high' : 'confidence-low';
      }

      // Update accounting proposal
      if (result.accounting_proposal) {
        document.querySelector('.form-select').value = result.accounting_proposal.debit_account || 'Office Expense';
      }
    } else {
      statusDiv.innerHTML = `<div class="alert alert-danger">Error: ${result.error || 'Upload failed'}</div>`;
    }
  } catch (error) {
    statusDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
  } finally {
    this.disabled = false;
    this.textContent = 'Upload & Extract';
  }
});