function delteSignal(signal){

  var $signal = $(signal)
  $(signal).parent().remove()
  var id = $signal.data('id')

  $.ajax({url: 'signal/delete/' + id,
         method: 'DELETE',
         beforeSend: function(xhr){
           xhr.setRequestHeader('X-CSRFToken', csrf_token)
         }
  })

}
