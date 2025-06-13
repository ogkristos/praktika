/**
 * Word-by-word translator script
 * This script processes text content on the page and wraps each word in a span
 * with translation attributes to enable word-by-word translation.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get current language from Django context
    const currentLanguage = document.documentElement.lang || 'en';
    
    // Skip if language is English (source language)
    if (currentLanguage === 'en') {
        return;
    }
    
    // Dictionary for storing translations
    const translations = {};
    
    // Function to check if element should be ignored
    function shouldIgnoreElement(element) {
        // Ignore script, style, input elements, etc.
        const ignoreTags = ['SCRIPT', 'STYLE', 'INPUT', 'TEXTAREA', 'SELECT', 'OPTION', 'CODE', 'PRE'];
        if (ignoreTags.includes(element.tagName)) {
            return true;
        }
        
        // Ignore elements with specific classes or attributes
        if (element.classList.contains('no-translate') || 
            element.hasAttribute('data-no-translate') ||
            element.classList.contains('translated-word')) {
            return true;
        }
        
        return false;
    }
    
    // Function to process text nodes and wrap each word in a span
    function processTextNodes(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            const text = node.nodeValue.trim();
            if (text.length > 0) {
                // Skip if parent is already a translated-word
                if (node.parentNode && node.parentNode.classList && 
                    node.parentNode.classList.contains('translated-word')) {
                    return;
                }
                
                // Split text into words and wrap each in a span
                const words = text.split(/(\s+)/); // Keep spaces as separate items
                if (words.length > 1) {
                    const fragment = document.createDocumentFragment();
                    
                    words.forEach((word, index) => {
                        // Skip empty words
                        if (!word) return;
                        
                        // If it's just whitespace, add it as is
                        if (/^\s+$/.test(word)) {
                            fragment.appendChild(document.createTextNode(word));
                            return;
                        }
                        
                        // Extract punctuation
                        const punctRegex = /^([^\w]*)(\w+)([^\w]*)$/;
                        const match = word.match(punctRegex);
                        
                        if (match) {
                            const [_, prefix, wordOnly, suffix] = match;
                            
                            // Add prefix punctuation
                            if (prefix) {
                                fragment.appendChild(document.createTextNode(prefix));
                            }
                            
                            // Create span for the word
                            const span = document.createElement('span');
                            span.className = 'translated-word';
                            span.setAttribute('data-original', wordOnly);
                            span.textContent = wordOnly;
                            
                            // Create tooltip with original word
                            const tooltip = document.createElement('span');
                            tooltip.className = 'word-tooltip';
                            tooltip.textContent = wordOnly;
                            span.appendChild(tooltip);
                            
                            fragment.appendChild(span);
                            
                            // Add suffix punctuation
                            if (suffix) {
                                fragment.appendChild(document.createTextNode(suffix));
                            }
                        } else {
                            // If no match, just add the word as is
                            const span = document.createElement('span');
                            span.className = 'translated-word';
                            span.setAttribute('data-original', word);
                            span.textContent = word;
                            
                            // Create tooltip with original word
                            const tooltip = document.createElement('span');
                            tooltip.className = 'word-tooltip';
                            tooltip.textContent = word;
                            span.appendChild(tooltip);
                            
                            fragment.appendChild(span);
                        }
                    });
                    
                    // Replace original text node with the fragment
                    node.parentNode.replaceChild(fragment, node);
                }
            }
        } else if (node.nodeType === Node.ELEMENT_NODE && !shouldIgnoreElement(node)) {
            // Process child nodes (make a copy of childNodes as it's a live collection)
            Array.from(node.childNodes).forEach(processTextNodes);
        }
    }
    
    // Start processing from body with a delay to ensure all content is loaded
    setTimeout(() => {
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
    }, 500);
});