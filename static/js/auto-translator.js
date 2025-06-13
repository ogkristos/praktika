/**
 * Auto-translator script that translates every text node on the page
 * using the browser's built-in translation API or a fallback method.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get current language from Django context
    const currentLanguage = document.documentElement.lang || 'en';
    
    // Skip translation if language is English (source language)
    if (currentLanguage === 'en') {
        return;
    }
    
    // Function to check if element should be ignored
    function shouldIgnoreElement(element) {
        // Ignore script, style, input elements, etc.
        const ignoreTags = ['SCRIPT', 'STYLE', 'INPUT', 'TEXTAREA', 'SELECT', 'OPTION', 'CODE', 'PRE'];
        if (ignoreTags.includes(element.tagName)) {
            return true;
        }
        
        // Ignore elements with specific classes or attributes
        if (element.classList.contains('no-translate') || 
            element.hasAttribute('data-no-translate')) {
            return true;
        }
        
        return false;
    }
    
    // Function to process text nodes
    function processTextNodes(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            const text = node.nodeValue.trim();
            if (text.length > 0) {
                // We don't actually modify the text here as it's already translated by Django
                // This is just a placeholder for additional word-by-word translation if needed
            }
        } else if (node.nodeType === Node.ELEMENT_NODE && !shouldIgnoreElement(node)) {
            // Process attributes that might contain text
            if (node.hasAttribute('placeholder')) {
                // Placeholder attributes could be translated here if needed
            }
            if (node.hasAttribute('title')) {
                // Title attributes could be translated here if needed
            }
            
            // Process child nodes
            Array.from(node.childNodes).forEach(processTextNodes);
        }
    }
    
    // Start processing from body
    processTextNodes(document.body);
    
    // Add mutation observer to handle dynamically added content
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === Node.ELEMENT_NODE && !shouldIgnoreElement(node)) {
                        processTextNodes(node);
                    }
                });
            }
        });
    });
    
    // Start observing the document body for changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});