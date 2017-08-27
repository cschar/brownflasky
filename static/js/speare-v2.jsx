
//TODO: use a component/controller
//https://mithril.js.org/archive/v0.2.5/mithril.component.html#optional-controller
var words_available = [];

var state2 = {
  value: 'nay',
  title: 'a',
  phrases: [],
  last: 'nay',
}

var set_check_text_input_value = function(v){
  console.log(v)
  let char = v[v.length -1]
  //
  if (char == '1' || char == '2' || char == '3'){
    //knock off that number
    v = v.slice(0, v.length-1)
  }
  state2.value = v;
  let words = v.trim().split(' ')
  let last = words[words.length -1]
  state2.last = last;
}

var get_suggestions = function(word){
  console.log('suggestions now: ' + state2.phrases.length)
  m.request({
        method: "GET",
        url: "/speare/api/"+word,
    })
    .then(function(response) {
        state2.phrases = response.phrases;
    })
    m.redraw()
}

var keyp = function(){
  console.log('callback')
}
function withKey(callback) {
  return function(e) {
    var ch = String.fromCharCode(e.keyCode)
    if (ch == ' ') {
      get_suggestions(state2.last)
    }
    if (ch == '1'){
      state2.value = state2.value + state2.phrases[0].slice(1,4).join(' ') + ' '
      get_suggestions(state2.phrases[0][3])

    }
    if (ch == '2'){
      state2.value = state2.value + state2.phrases[1].slice(1,4).join(' ') + ' '
      get_suggestions(state2.phrases[1][3])
    }
    if (ch == '3'){
      state2.value = state2.value + state2.phrases[2].slice(1,4).join(' ') + ' '
      get_suggestions(state2.phrases[2][3])
    }
  }
}



var getPhrase = function(index){
  if (state2.phrases.length-1  >= index ){
    return state2.phrases[index].join(" ")
  }else{
    return ""
  }
}

//TODO: figure out how to have it separate but still redrawn
//would have liked to use but m.render wont redraw if not explicitly part of code below
//var option_bar_view = m("div",[
//    "start typing, try using those words",
//    m("div", {class: "side-1"}, getPhrase(0)),
//    m("div", {class: "side-2"}, getPhrase(1)),
//    m("div", {class: "side-3"}, getPhrase(2)),
//    ]
//)

var Hello = {
  view: function () {
    return m("div", {class: "site", onkeypress: withKey(keyp)}, [
      m("div", {class: "page-title"}, [
          m("nav",[
                m("a", {href: "/"}, "home"),
                m("a", {href: "/words"}, "brown"),
              m("a", {href: "/speare"}, "speare"),
              m("a", {href: "/speare-v2"}, "speare-v2"),
                m("a", {href: "#!/splash"}, "splash"),

          ]),
          ]),

        m("div", {class: "header"}, [m("textarea",
        {rows: "5", class: "inputbox", oninput: m.withAttr("value", set_check_text_input_value)},
        state2.value)]),
      m("div", {class: "optionbar"},
          [
        "start typing, try using those words",
    m("div", {class: "side-1" }, "Press 1 to insert: "+ getPhrase(0)),
    m("div", {class: "side-2" }, "Press 2 to insert: "+ getPhrase(1)),
    m("div", {class: "side-3" }, "Press 3 to insert: "+ getPhrase(2)),
    ]),
      m("div", {class: "main-content"},
          'suggestions available: ' + words_available),

      m("div", {class: "footer"}, [

        m("h1", "brown flasky - speare v2"),
        m("img#drag1", {src: '/static/img/celtic_drag1.png'}),

      ]),

    ])
  }
}

var Splash = {
  view: function () {
    return m("div", [
      m("a", {href: "#!/hello"}, "Enter!"),
      m('img', {src: "/static/img/r0117.jpg"})
        ])
  }
}


//initialize data here
let root = document.getElementById('app')
m.request({
      url: 'speare/api/available'
    })
    .then((response) => {
      console.log(response);
      words_available = response.data.join(', ');
      // m.mount(, Hello);
      m.route(root, "/hello", {
        "/splash": Splash,
        "/hello": Hello,
      })
    });

