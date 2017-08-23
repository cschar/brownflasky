(function() {

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
      for (var i = 0; i < maxSuggestions; i++) {
        var id = '#suggestion-'+ String(i);
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
    v = v.replace(/(0|1)/g, '');
    $('#shake').val(v);
  });

  $(document).keypress(function(e) {
    if(e.which == 13) {
        console.log('You pressed enter!');
        getSug()
    }
    if(e.which == 32) {
        console.log('You pressed spacebar');
        getSug()
    }
    if(e.which == 48){
      if (window.suggestions.length > 0) {
        var v = $('#shake').val();
        var sug = window.suggestions[0].slice(1, 4).join(' ')
        $('#shake').val(v + ' ' + sug);
        getSug(window.suggestions[0][3])
      }
    }
    if(e.which == 49){
      var v = $('#shake').val();
      if (window.suggestions.length > 1) {
        var sug = window.suggestions[1].slice(1, 4).join(' ')
        $('#shake').val(v + ' ' + sug);
        getSug(window.suggestions[1][3])
      }
    }
    if(e.which == 50){
      var v = $('#shake').val();
      if (window.suggestions.length > 1) {
        var sug = window.suggestions[2].slice(1, 4).join(' ')
        $('#shake').val(v + ' ' + sug);
        getSug(window.suggestions[2][3])
      }
    }
});

//$('#shake').change(function() {


//}).done(function() {
//
//    console.log( "second success" );
//  })
//  .fail(function() {
//    console.log( "error" );
//  });
//});
}).call(this);
