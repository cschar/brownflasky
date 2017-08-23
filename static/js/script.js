(function() {

  var getSug = function(){
    var val = $('#shake').val();
    var nokeys = val.replace(/(0|1|\n)/g, '');
    $('#shake').val(nokeys);
    nokeys = $.trim(nokeys);
    var bits = nokeys.split(" ");
    var last = bits[bits.length -1];
    //$('#shake')

    $.get( "speare/api/"+last, function( data ) {
      console.log(data);
      $('#zero-sug').text(data.phrases[0].join(' '))
      $('#one-sug').text(data.phrases[1].join(' '))
      window.suggestions = data.phrases;
    })
  };

  $(document).keypress(function(e) {
    if(e.which == 13) {
        console.log('You pressed enter!');
        getSug()
    }
    if(e.which == 48){
      var v = $('#shake').val();
      var nokeys = v.replace(/(0|1|\n)/g, '');
      var sug = window.suggestions[0].join(' ')
      $('#shake').val(nokeys + ' ' + sug);
    }
    if(e.which == 49){
      var v = $('#shake').val();
      var nokeys = v.replace(/(0|1|\n)/g, '');
      var sug = window.suggestions[1].join(' ')
      $('#shake').val(nokeys + ' ' + sug);
    }
});

//$('#shake').change(function() {
////$('#shake').keyup(function() {
//
//}).done(function() {
//
//    console.log( "second success" );
//  })
//  .fail(function() {
//    console.log( "error" );
//  });
//});
}).call(this);
