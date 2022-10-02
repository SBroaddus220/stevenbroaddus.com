// ****
// Navbar items now collapse navbar when open
// https://stackoverflow.com/questions/42401606/how-to-hide-collapsible-bootstrap-navbar-on-click
const navLinks = document.querySelectorAll('.nav-item:not(.dropdown)'); 
const menuToggle = document.getElementById('main-nav-content'); 
const bsCollapse = new bootstrap.Collapse(menuToggle, {toggle: false}); 
navLinks.forEach( function(l) { l.addEventListener('click', function() { // avoid flickering on desktop 
    if (menuToggle.classList.contains('show')) { bsCollapse.toggle(); } 
}); }); 

// ****
// Enables Bootstrap tooltips 
// https://getbootstrap.com/docs/5.2/components/tooltips/#enable-tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))