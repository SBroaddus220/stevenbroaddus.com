// ****
// Loads courses from JSON file and loads sorted based on various criteria

const json2html = require('node-json2html');

let template = {"<>":"div","class":"card col-md-3 col-12 mx-3","html":[
                {"<>":"div","class":"row g-0","html":[
                    {"<>":"div","class":"col-4","html":[
                        {"<>":"img","src":"${image}","class":"card-img img-fluid card h-100","alt":"...","style":"object-fit: cover;","html":""}
                    ]},
                    {"<>":"div","class":"col-8","html":[
                        {"<>":"div","class":"card-body","html":[
                            {"<>":"h5","class":"card-title","html":[
                                {"<>":"p","class":"text-black text-start fs-5","html":"${course-title}"}
                            ]},
                            {"<>":"p","class":"card-text text-black fs-5 text-start small","html":"${course-description}"}
                        ]},
                        {"<>":"div","class":"card-footer text-end text-muted small py-0","html":"\n${time-taken}\n"}
                    ]}
                ]}
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

function generateCourses() {
    document.getElementById("collapse-osu-coursework").innerHTML = "";
    courseworkArray.sort(getOrder("grade"));
    for (var course in courseworkArray) {
        document.getElementById("collapse-osu-coursework").innerHTML += courseworkArray[course]["course-title"];
    }
}

var courseworkArray = [
    {
        "course-title": "Linear Algebra",
        "course-descrption": "kljsadlaksjdlasjdlaksdj",
        "time-taken": "August 2022 - Present",
        "grade": 4,
        "image": "https://via.placeholder.com/150"
    },
    {
        "course-title": "Software 2",
        "course-description": "asdasdasdasdasd",
        "time-taken": "August 2022 - Present",
        "grade": 3,
        "image": "https://via.placeholder.com/150"
    }
];



