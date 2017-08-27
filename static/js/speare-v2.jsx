
var count = 0;
var increment = function() {
    m.request({
        method: "PUT",
        url: "//rem-rest-api.herokuapp.com/api/tutorial/1",
        data: {count: count + 1},
        withCredentials: true,
    })
    .then(function(data) {
        count = parseInt(data.count)
    })
}


var Hello = {
    view: function() {
        return m("main", [
            m("h1", {class: "title"}, "My first app"),
            m("button", "A button"),
            m("button", {onclick: increment}}, count + " clicks"),

        ])
    }
}

var Splash = {
    view: function() {
        return m("a", {href: "#!/hello"}, "Enter!")
    }
}

let root = document.getElementById('app')
m.request({
	url: 'https://rem-rest-api.herokuapp.com/api/users'})
.then((response) => {
  console.log(response);
  // m.mount(, Hello);
  m.route(root, "/splash", {
    "/splash": Splash,
    "/hello": Hello,
})
});