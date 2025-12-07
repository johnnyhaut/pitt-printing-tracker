function fixPrinter(printerId) {
    currentBaseUrl = window.location.href;
    fetch(`/admin/fix_printer/${printerId}`, { method: 'POST' }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Failed to fix the printer.');
        }
    });
}