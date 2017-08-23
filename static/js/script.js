(function() {
/**
 * Shuffles array in place.
 * @param {Array} a items The array containing the items.
 */
function shuffle(a) {
    var j, x, i;
    for (i = a.length; i; i--) {
        j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }
}

  var getSug = function(word){
    if( word == null) {
      var val = $('#shake').val();
      //val = val.replace(/(0|1)/g, '');
      //$('#shake').val(val);
      val = $.trim(val);
      var bits = val.split(" ");
      word = bits[bits.length - 1];
    }

    $.get( "speare/api/"+word, function( data ) {
      console.log(data);
      var maxSuggestions = 3;
      shuffle(data.phrases)
      for (var i = 0; i < maxSuggestions; i++) {
        var id = '#suggestion-'+ String(i+1);
        if (i < data.phrases.length ) {
          $(id).text(data.phrases[i].join(' '))
        }else{
          $(id).text(' ')
        }

      }

      window.suggestions = data.phrases;
    })
  };

  $('#shake').keyup(function() {
    var v = $('#shake').val();
    v = v.replace(/\d/g, '');
    $('#shake').val(v);
  });

  var setSuggestionBox = function(number){
    // number 1,2,3...
    if (window.suggestions.length >= number) {
        var v = $('#shake').val();
        var sug = window.suggestions[number-1].slice(1, 4).join(' ')
        $('#shake').val(v + ' ' + sug);
        getSug(window.suggestions[number-1][3])
      }
  }

  $(document).keypress(function(e) {
    if(e.which == 13) {
        console.log('You pressed enter!');
        getSug()
    }
    if(e.which == 32) {
        console.log('You pressed spacebar');
        getSug()
    }
    if(e.which == 49){
      setSuggestionBox(1)
    }
    if(e.which == 50){
      setSuggestionBox(2)
    }
    if(e.which == 51){
      setSuggestionBox(3)
    }
});



}).call(this);
