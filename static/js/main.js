// Main JavaScript for LLC Directory

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize mobile sticky banner
    initializeMobileStickyBanner();
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Search functionality
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            performSearch(this.value);
        }, 300));
    }

    // Filter change handlers
    const stateSelect = document.querySelector('select[name="state"]');
    const citySelect = document.querySelector('select[name="city"]');
    const categorySelect = document.querySelector('select[name="category"]');

    if (stateSelect) {
        stateSelect.addEventListener('change', function() {
            updateCityOptions(this.value);
        });
    }

    if (citySelect) {
        citySelect.addEventListener('change', function() {
            // Auto-submit form when city is selected
            if (this.value) {
                this.closest('form').submit();
            }
        });
    }

    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            // Auto-submit form when category is selected
            if (this.value) {
                this.closest('form').submit();
            }
        });
    }

    // Phone number formatting
    const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    phoneLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Track phone clicks if analytics is available
            if (typeof gtag !== 'undefined') {
                gtag('event', 'phone_click', {
                    'event_category': 'engagement',
                    'event_label': this.href
                });
            }
        });
    });

    // Website link tracking
    const websiteLinks = document.querySelectorAll('a[target="_blank"]');
    websiteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Track external link clicks if analytics is available
            if (typeof gtag !== 'undefined') {
                gtag('event', 'external_link_click', {
                    'event_category': 'engagement',
                    'event_label': this.href
                });
            }
        });
    });

    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loading"></span> Searching...';
            }
        });
    });

    // Initialize search suggestions
    initializeSearchSuggestions();
});

// Debounce function for search input
function debounce(func, wait, immediate) {
    var timeout;
    return function executedFunction() {
        var context = this;
        var args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Perform search with AJAX
function performSearch(query) {
    if (query.length < 2) return;

    fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchSuggestions(data);
        })
        .catch(error => {
            console.error('Search error:', error);
        });
}

// Display search suggestions
function displaySearchSuggestions(suggestions) {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput) return;

    // Remove existing suggestions
    const existingSuggestions = document.querySelector('.search-suggestions');
    if (existingSuggestions) {
        existingSuggestions.remove();
    }

    if (suggestions.length === 0) return;

    // Create suggestions container
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-suggestions position-absolute bg-white border rounded shadow-sm';
    suggestionsContainer.style.top = '100%';
    suggestionsContainer.style.left = '0';
    suggestionsContainer.style.right = '0';
    suggestionsContainer.style.zIndex = '1000';
    suggestionsContainer.style.maxHeight = '300px';
    suggestionsContainer.style.overflowY = 'auto';

    // Add suggestions
    suggestions.forEach(suggestion => {
        const suggestionItem = document.createElement('div');
        suggestionItem.className = 'p-2 border-bottom cursor-pointer';
        suggestionItem.innerHTML = `
            <div class="fw-bold">${suggestion.name}</div>
            <div class="small text-muted">${suggestion.city}, ${suggestion.state}</div>
        `;
        suggestionItem.addEventListener('click', () => {
            searchInput.value = suggestion.name;
            suggestionsContainer.remove();
            searchInput.closest('form').submit();
        });
        suggestionsContainer.appendChild(suggestionItem);
    });

    // Position suggestions
    const searchContainer = searchInput.closest('.position-relative') || searchInput.parentElement;
    searchContainer.style.position = 'relative';
    searchContainer.appendChild(suggestionsContainer);

    // Close suggestions when clicking outside
    document.addEventListener('click', function closeSuggestions(e) {
        if (!searchContainer.contains(e.target)) {
            suggestionsContainer.remove();
            document.removeEventListener('click', closeSuggestions);
        }
    });
}

// Update city options based on selected state
function updateCityOptions(selectedState) {
    const citySelect = document.querySelector('select[name="city"]');
    if (!citySelect) return;

    // Reset city options
    citySelect.innerHTML = '<option value="">All Cities</option>';

    if (!selectedState) return;

    // Fetch cities for selected state
    fetch(`/api/cities?state=${encodeURIComponent(selectedState)}`)
        .then(response => response.json())
        .then(cities => {
            cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching cities:', error);
        });
}

// Initialize search suggestions
function initializeSearchSuggestions() {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput) return;

    // Add event listeners for search input
    searchInput.addEventListener('focus', function() {
        if (this.value.length >= 2) {
            performSearch(this.value);
        }
    });

    searchInput.addEventListener('blur', function() {
        // Delay hiding suggestions to allow for clicks
        setTimeout(() => {
            const suggestions = document.querySelector('.search-suggestions');
            if (suggestions) {
                suggestions.remove();
            }
        }, 200);
    });
}

// Utility function to format phone numbers
function formatPhoneNumber(phoneNumber) {
    const cleaned = phoneNumber.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return '(' + match[1] + ') ' + match[2] + '-' + match[3];
    }
    return phoneNumber;
}

// Utility function to truncate text
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

// LLC Formation Cost Calculator
function calculateLLCCosts() {
    const stateSelect = document.getElementById('stateSelect');
    const serviceProvider = document.getElementById('serviceProvider');
    const registeredAgent = document.getElementById('registeredAgent');
    const ein = document.getElementById('ein');
    const operatingAgreement = document.getElementById('operatingAgreement');
    
    // Get state filing fee from selected option
    const stateOption = stateSelect.options[stateSelect.selectedIndex];
    const stateFeeText = stateOption.text;
    const stateFee = parseInt(stateFeeText.match(/\$(\d+)/)?.[1] || 0);
    
    // Get service provider fee
    const serviceFee = parseInt(serviceProvider.value || 0);
    
    // Calculate optional services
    let optionalFee = 0;
    if (registeredAgent.checked) {
        optionalFee += parseInt(registeredAgent.value || 0);
    }
    if (ein.checked) {
        optionalFee += parseInt(ein.value || 0);
    }
    if (operatingAgreement.checked) {
        optionalFee += parseInt(operatingAgreement.value || 0);
    }
    
    // Calculate total
    const totalCost = stateFee + serviceFee + optionalFee;
    
    // Update display
    document.getElementById('stateFee').textContent = `$${stateFee}`;
    document.getElementById('serviceFee').textContent = `$${serviceFee}`;
    document.getElementById('optionalFee').textContent = `$${optionalFee}`;
    document.getElementById('totalCost').textContent = `$${totalCost}`;
    
    // Show results
    document.getElementById('costResults').style.display = 'block';
    
    // Scroll to results
    document.getElementById('costResults').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
    });
}

// LLC vs. S-Corp Tax Savings Calculator
function calculateTaxSavings() {
    const businessProfit = parseFloat(document.getElementById('businessProfit').value) || 0;
    const plannedSalary = parseFloat(document.getElementById('plannedSalary').value) || 0;
    const taxStateSelect = document.getElementById('taxState');
    
    if (!businessProfit || !plannedSalary || !taxStateSelect.value) {
        alert('Please fill in all required fields.');
        return;
    }
    
    // Get state tax rate from selected option
    const stateOption = taxStateSelect.options[taxStateSelect.selectedIndex];
    const stateTaxRate = parseFloat(stateOption.text.match(/(\d+\.?\d*)%/)?.[1] || 0) / 100;
    
    // Calculate LLC (Default Taxation)
    const llcSETax = businessProfit * 0.153; // 15.3% self-employment tax
    const llcFederalTax = calculateFederalTax(businessProfit);
    const llcStateTax = businessProfit * stateTaxRate;
    const llcTotalTax = llcSETax + llcFederalTax + llcStateTax;
    
    // Calculate S-Corp
    const scorpPayrollTax = plannedSalary * 0.153; // 15.3% payroll tax on salary only
    const scorpFederalTax = calculateFederalTax(businessProfit); // Same federal tax
    const scorpStateTax = businessProfit * stateTaxRate; // Same state tax
    const scorpTotalTax = scorpPayrollTax + scorpFederalTax + scorpStateTax;
    
    // Calculate savings
    const taxSavings = llcTotalTax - scorpTotalTax;
    
    // Update display
    document.getElementById('llcSE').textContent = `$${Math.round(llcSETax).toLocaleString()}`;
    document.getElementById('llcFederal').textContent = `$${Math.round(llcFederalTax).toLocaleString()}`;
    document.getElementById('llcState').textContent = `$${Math.round(llcStateTax).toLocaleString()}`;
    document.getElementById('llcTotal').textContent = `$${Math.round(llcTotalTax).toLocaleString()}`;
    
    document.getElementById('scorpPayroll').textContent = `$${Math.round(scorpPayrollTax).toLocaleString()}`;
    document.getElementById('scorpFederal').textContent = `$${Math.round(scorpFederalTax).toLocaleString()}`;
    document.getElementById('scorpState').textContent = `$${Math.round(scorpStateTax).toLocaleString()}`;
    document.getElementById('scorpTotal').textContent = `$${Math.round(scorpTotalTax).toLocaleString()}`;
    
    document.getElementById('taxSavings').textContent = `$${Math.round(taxSavings).toLocaleString()}`;
    
    // Show results
    document.getElementById('taxResults').style.display = 'block';
    
    // Scroll to results
    document.getElementById('taxResults').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
    });
}

// Calculate federal income tax (simplified progressive tax brackets)
function calculateFederalTax(income) {
    if (income <= 11600) return income * 0.10;
    if (income <= 47150) return 1160 + (income - 11600) * 0.12;
    if (income <= 100525) return 5428 + (income - 47150) * 0.22;
    if (income <= 191950) return 17196 + (income - 100525) * 0.24;
    if (income <= 243725) return 39104 + (income - 191950) * 0.32;
    if (income <= 609350) return 55944 + (income - 243725) * 0.35;
    return 183647 + (income - 609350) * 0.37;
}

// Foreign Qualification Cost Calculator
function calculateForeignQualCosts() {
    const homeState = document.getElementById('homeState').value;
    const targetStatesSelect = document.getElementById('targetStates');
    const certificateOfGoodStanding = document.getElementById('certificateOfGoodStanding');
    const expeditedFiling = document.getElementById('expeditedFiling');
    const complianceMonitoring = document.getElementById('complianceMonitoring');
    
    if (!homeState || targetStatesSelect.selectedOptions.length === 0) {
        alert('Please select your home state and at least one target state.');
        return;
    }
    
    // Get selected target states
    const selectedStates = Array.from(targetStatesSelect.selectedOptions);
    const selectedStatesList = selectedStates.map(option => option.text.split(' - ')[0]);
    
    // Calculate foreign qualification fees
    let qualFees = 0;
    let agentFees = 0;
    let additionalFees = 0;
    let annualCompliance = 0;
    
    selectedStates.forEach(option => {
        const stateName = option.text.split(' - ')[0];
        const stateFee = parseInt(option.text.match(/\$(\d+)/)?.[1] || 0);
        
        // Skip if it's the same as home state
        if (stateName.toLowerCase() === homeState) {
            return;
        }
        
        qualFees += stateFee;
        agentFees += 125; // Average registered agent fee per state
        
        // Additional services
        if (certificateOfGoodStanding.checked) {
            additionalFees += 50;
        }
        if (expeditedFiling.checked) {
            additionalFees += 100;
        }
        if (complianceMonitoring.checked) {
            annualCompliance += 200;
        }
    });
    
    // Calculate total
    const totalCost = qualFees + agentFees + additionalFees;
    
    // Update display
    document.getElementById('qualFees').textContent = `$${qualFees.toLocaleString()}`;
    document.getElementById('agentFees').textContent = `$${agentFees.toLocaleString()}`;
    document.getElementById('additionalFees').textContent = `$${additionalFees.toLocaleString()}`;
    document.getElementById('annualCompliance').textContent = `$${annualCompliance.toLocaleString()}`;
    document.getElementById('totalForeignCost').textContent = `$${totalCost.toLocaleString()}`;
    
    // Update selected states list
    const statesListElement = document.getElementById('selectedStatesList');
    statesListElement.innerHTML = selectedStatesList.map(state => 
        `<span class="badge bg-primary me-1 mb-1">${state}</span>`
    ).join('');
    
    // Show results
    document.getElementById('foreignQualResults').style.display = 'block';
    
    // Scroll to results
    document.getElementById('foreignQualResults').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
    });
}

// Add cursor pointer class
document.addEventListener('DOMContentLoaded', function() {
    const cursorPointerElements = document.querySelectorAll('.cursor-pointer');
    cursorPointerElements.forEach(element => {
        element.style.cursor = 'pointer';
    });
});

// Mobile Sticky Banner Functions
function initializeMobileStickyBanner() {
    const banner = document.getElementById('mobileNwBanner');
    if (!banner) return;
    
    // Banner is always visible - no need for show/hide logic
    // The banner will be visible by default due to CSS transform: translateY(0)
}

function hideMobileBanner() {
    // Function kept for compatibility but doesn't do anything
    // Banner will always remain visible
}

// Global function for the onclick handler
window.hideMobileBanner = hideMobileBanner;
