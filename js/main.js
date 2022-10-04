// ****
// Coursework data

let template = {"<>":"div","class":"card col-md-3 col-12 my-3 mx-3","style":"border-width: 0 0 0 0.5rem; border-color: ${color};","html":[
                    {"<>":"div","class":"card-header fw-semibold","html":[
                        {"<>":"p","class":"text-black text-start my-0","style":"font-size: medium;","html":"${title}"}
                    ]},
                    {"<>":"div","class":"card-body","html":[
                        {"<>":"p","class":"card-text text-black text-start text-muted py-0","style":"font-size: 0.9rem;","html":"Credits: ${creditNum} | Grade: ${grade}"}
                    ]},
                    {"<>":"div","class":"card-footer text-end text-muted small py-0","style":"bottom:0;","text": function(obj,index){
                            let dStart = new Date(this.startDate);
                            let dEnd = new Date(this.endDate);
                            let startDuration = (dStart.getMonth() + 1) + "/" + dStart.getFullYear();

                            // Replaces end date with 'present' if it's the current month and year
                            let currentTime = new Date();
                            let endDuration = "";
                            if ((currentTime.getFullYear() === dEnd.getFullYear()) && (currentTime.getMonth() === dEnd.getMonth())) {
                                endDuration = "present";
                            } else {
                                endDuration = (dEnd.getMonth() + 1) + "/" + dEnd.getFullYear();
                            }

                            let duration = startDuration + " - " + endDuration;
                            return (duration);
                            }
                    }
                ]};      

// Comparator function
function getOrder(property) {
    return function(a, b) {
    let comparison = 0;
    if (a[property] > b[property]) {
        comparison = 1;
    } else if (a[property] < b[property]) {
        comparison = -1;
    }
    return comparison;
    }
}

function getReverseOrder(property) {
    return function(a, b) {
    let comparison = 0;
    if (a[property] < b[property]) {
        comparison = 1;
    } else if (a[property] > b[property]) {
        comparison = -1;
    }
    return comparison;
    }
}

var sortMethod = "endDate";
function changeSortMethod(newSortMethod) {
    sortMethod = newSortMethod;
}

function generateCourses() {
    targetLoc = document.getElementById("collapse-osu-coursework");
    targetLoc.innerHTML = "";
    if (!targetLoc.classList.contains("show")) {
        courseworkArray.sort(getReverseOrder(sortMethod));
        targetLoc.innerHTML += json2html.render(courseworkArray, template);
    }
}

let courseworkArray = [
    // NOTE: REMEMBER THAT MONTHS ARE 0-11
    {
    "title": "Fundamentals of Engineering for Honors I",
    "courseNumber": "ENGR 1282.01H",
    "creditNum": 5,
    "startDate": new Date(2021, 7), // August
    "endDate": new Date(2021, 11), // December
    "grade": "A",
    "color": "#0d6efd"
    },
    {
    "title": "Engineering Calculus A",
    "courseNumber": "MATH 1172",
    "creditNum": 5,
    "startDate": new Date(2021, 7),
    "endDate": new Date(2021, 11),
    "grade": "A",
    "color": "#0d6efd"
    },
    {
    "title": "FEH Physics: Mechanics",
    "courseNumber": "PHYSICS 1260",
    "creditNum": 5,
    "startDate": new Date(2021, 7),
    "endDate": new Date(2021, 11),
    "grade": "A",
    "color": "#0d6efd"
    },
    {
    "title": "Software I: Software Components",
    "courseNumber": "CSE 2221",
    "creditNum": 4,
    "startDate": new Date(2022, 0),
    "endDate": new Date(2022, 4),
    "grade": "A",
    "color": "#0d6efd"
    },
    {
    "title": "Fundamentals of Engineering Honors - Robot Project",
    "courseNumber": "ENGR 1282.01H",
    "creditNum": 3,
    "startDate": new Date(2022, 0),
    "endDate": new Date(2022, 4),
    "grade": "A",
    "color": "#0d6efd"
    },
    {
    "title": "FEH Physics: E&M",
    "courseNumber": "PHYSICS 1261",
    "creditNum": 5,
    "startDate": new Date(2022, 0),
    "endDate": new Date(2022, 4),
    "grade": "A-",
    "color": "#0d6efd"
    },
    {
    "title": "American Atitudes about Tech. (GE)",
    "courseNumber": "ENGR 2367",
    "creditNum": 3,
    "startDate": new Date(2022, 0),
    "endDate": new Date(2022, 4),
    "grade": "A",
    "color": "#0d6efd"
    },
    {
    "title": "Software 2: Software Dev. and Design",
    "courseNumber": "CSE 2231",
    "creditNum": 4,
    "startDate": new Date(2022, 7),
    "endDate": new Date(),
    "grade": "IP",
    "color": "#0d6efd"
    },
    {
    "title": "Foundations 1: Discrete Structures",
    "courseNumber": "CSE 2321",
    "creditNum": 3,
    "startDate": new Date(2022, 7),
    "endDate": new Date(),
    "grade": "IP",
    "color": "#0d6efd"
    },
    {
    "title": "Statistics for Engineers",
    "courseNumber": "MATH 3470",
    "creditNum": 3,
    "startDate": new Date(2022, 7),
    "endDate": new Date(),
    "grade": "IP",
    "color": "#0d6efd"
    },
    {
    "title": "Intro to Digital Logic",
    "courseNumber": "ECE 2060",
    "creditNum": 3,
    "startDate": new Date(2022, 7),
    "endDate": new Date(),
    "grade": "IP",
    "color": "#0d6efd"
    },
    {
    "title": "Linear Algebra",
    "courseNumber": "MATH 2568",
    "creditNum": 3,
    "startDate": new Date(2022, 7),
    "endDate": new Date(),
    "grade": "IP",
    "color": "#0d6efd"
    }
];

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