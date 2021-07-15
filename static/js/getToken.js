$('.getToken').click(function(){
  let token = $(this).attr('data-id');
  $.ajax({
      url: '/getToken/'+token,
      type: 'GET',
      dataType: 'json',
      success: function(data, textStatus, xhr) {
        console.log(data.values)
        $('#id-textarea').html(data.values)
      },  
      error: function(xhr, textStatus, errorThrown) {  
          console.log('Error in Database');  
      }  
  });  
});
