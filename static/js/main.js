// Main JavaScript file for Хром-КЗ Logistics System

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializePopovers();
    initializeFormValidation();
    initializeAutoRefresh();
    initializePhoneFormatting();
    initializeTableSorting();
    initializeNotifications();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize Bootstrap popovers
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Form validation enhancements
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
            
            form.classList.add('was-validated');
        }, false);
    });

    // Real-time validation for specific fields
    const phoneFields = document.querySelectorAll('input[type="tel"]');
    phoneFields.forEach(function(field) {
        field.addEventListener('blur', function() {
            validatePhone(this);
        });
    });

    const emailFields = document.querySelectorAll('input[type="email"]');
    emailFields.forEach(function(field) {
        field.addEventListener('blur', function() {
            validateEmail(this);
        });
    });
}

// Phone number validation
function validatePhone(field) {
    const phoneRegex = /^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$/;
    const isValid = phoneRegex.test(field.value) || field.value === '';
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
    
    return isValid;
}

// Email validation
function validateEmail(field) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(field.value) || field.value === '';
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
    
    return isValid;
}

// Auto-refresh functionality for dashboards
function initializeAutoRefresh() {
    const refreshInterval = 300000; // 5 minutes
    const currentPath = window.location.pathname;
    
    // Only auto-refresh dashboard and analytics pages
    if (currentPath.includes('/admin') || currentPath.includes('/analytics')) {
        setInterval(function() {
            // Check if user is still active (no typing in forms)
            const activeElement = document.activeElement;
            const isTyping = activeElement && (
                activeElement.tagName === 'INPUT' || 
                activeElement.tagName === 'TEXTAREA' || 
                activeElement.tagName === 'SELECT'
            );
            
            if (!isTyping) {
                location.reload();
            }
        }, refreshInterval);
    }
}

// Phone number formatting for Kazakhstan numbers
function initializePhoneFormatting() {
    const phoneInputs = document.querySelectorAll('input[type="tel"], input[name*="phone"]');
    
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            formatPhoneNumber(e.target);
        });
        
        input.addEventListener('keydown', function(e) {
            // Allow: backspace, delete, tab, escape, enter
            if ([46, 8, 9, 27, 13].indexOf(e.keyCode) !== -1 ||
                // Allow: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
                (e.keyCode === 65 && e.ctrlKey === true) ||
                (e.keyCode === 67 && e.ctrlKey === true) ||
                (e.keyCode === 86 && e.ctrlKey === true) ||
                (e.keyCode === 88 && e.ctrlKey === true) ||
                // Allow: home, end, left, right
                (e.keyCode >= 35 && e.keyCode <= 39)) {
                return;
            }
            // Ensure that it is a number and stop the keypress
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });
    });
}

// Format phone number to Kazakhstan format
function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    
    // Convert 8 to 7 for Kazakhstan numbers
    if (value.startsWith('8')) {
        value = '7' + value.slice(1);
    }
    
    // Format Kazakhstan number: +7 (XXX) XXX-XX-XX
    if (value.startsWith('7') && value.length <= 11) {
        let formatted = '+7';
        if (value.length > 1) formatted += ' (' + value.slice(1, 4);
        if (value.length > 4) formatted += ') ' + value.slice(4, 7);
        if (value.length > 7) formatted += '-' + value.slice(7, 9);
        if (value.length > 9) formatted += '-' + value.slice(9, 11);
        input.value = formatted;
    } else if (value.length > 11) {
        // Prevent input of more than 11 digits
        input.value = input.value.slice(0, -1);
    }
}

// Table sorting functionality
function initializeTableSorting() {
    const sortableHeaders = document.querySelectorAll('th[data-sort]');
    
    sortableHeaders.forEach(function(header) {
        header.style.cursor = 'pointer';
        header.innerHTML += ' <i class="fas fa-sort text-muted"></i>';
        
        header.addEventListener('click', function() {
            sortTable(this);
        });
    });
}

// Sort table by column
function sortTable(header) {
    const table = header.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    const sortType = header.getAttribute('data-sort');
    const currentOrder = header.getAttribute('data-order') || 'asc';
    const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
    
    // Update header attributes
    header.setAttribute('data-order', newOrder);
    
    // Update sort icons
    table.querySelectorAll('th i').forEach(function(icon) {
        icon.className = 'fas fa-sort text-muted';
    });
    
    const icon = header.querySelector('i');
    icon.className = newOrder === 'asc' ? 'fas fa-sort-up text-primary' : 'fas fa-sort-down text-primary';
    
    // Sort rows
    rows.sort(function(a, b) {
        const aVal = a.children[columnIndex].textContent.trim();
        const bVal = b.children[columnIndex].textContent.trim();
        
        let result = 0;
        
        switch (sortType) {
            case 'number':
                result = parseFloat(aVal.replace(/[^\d.-]/g, '')) - parseFloat(bVal.replace(/[^\d.-]/g, ''));
                break;
            case 'date':
                result = new Date(aVal) - new Date(bVal);
                break;
            default: // text
                result = aVal.localeCompare(bVal, 'ru');
                break;
        }
        
        return newOrder === 'asc' ? result : -result;
    });
    
    // Re-append rows
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}

// Notification system
function initializeNotifications() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Utility function to show toast notifications
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    const toastId = 'toast-' + Date.now();
    
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Loading state management
function setLoadingState(element, loading = true) {
    if (loading) {
        element.classList.add('loading');
        element.setAttribute('data-original-text', element.textContent);
        if (element.tagName === 'BUTTON') {
            element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Загрузка...';
            element.disabled = true;
        }
    } else {
        element.classList.remove('loading');
        const originalText = element.getAttribute('data-original-text');
        if (originalText && element.tagName === 'BUTTON') {
            element.textContent = originalText;
            element.disabled = false;
        }
    }
}

// Confirmation dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Format currency for display
function formatCurrency(amount) {
    return new Intl.NumberFormat('ru-KZ', {
        style: 'currency',
        currency: 'KZT',
        minimumFractionDigits: 0
    }).format(amount);
}

// Format date for display
function formatDate(date, includeTime = false) {
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    };
    
    if (includeTime) {
        options.hour = '2-digit';
        options.minute = '2-digit';
    }
    
    return new Date(date).toLocaleDateString('ru-RU', options);
}

// Copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Скопировано в буфер обмена', 'success');
    }).catch(function() {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('Скопировано в буфер обмена', 'success');
    });
}

// Print functionality
function printElement(elementId) {
    const printContent = document.getElementById(elementId);
    const windowPrint = window.open('', '', 'left=0,top=0,width=800,height=900,toolbar=0,scrollbars=0,status=0');
    
    windowPrint.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Печать</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                @media print {
                    .no-print { display: none !important; }
                    .card { border: 1px solid #dee2e6 !important; }
                }
            </style>
        </head>
        <body>
            ${printContent.innerHTML}
        </body>
        </html>
    `);
    
    windowPrint.document.close();
    windowPrint.focus();
    windowPrint.print();
    windowPrint.close();
}

// Export table data to CSV
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    const rows = table.querySelectorAll('tr');
    const csvContent = [];
    
    rows.forEach(function(row) {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        
        cols.forEach(function(col) {
            rowData.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
        });
        
        csvContent.push(rowData.join(','));
    });
    
    const blob = new Blob([csvContent.join('\n')], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl + K for global search
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[name="tracking_number"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Esc to close modals
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(function(modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
});

// Expose utility functions globally
window.HromKZ = {
    showToast,
    setLoadingState,
    confirmAction,
    formatCurrency,
    formatDate,
    copyToClipboard,
    printElement,
    exportTableToCSV,
    formatPhoneNumber: function(value) {
        const input = { value: value };
        formatPhoneNumber(input);
        return input.value;
    }
};

// Service Worker registration for offline functionality
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/sw.js').then(function(registration) {
            console.log('SW registered: ', registration);
        }).catch(function(registrationError) {
            console.log('SW registration failed: ', registrationError);
        });
    });
}
