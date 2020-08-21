$(document).ready(function(){
  function TagToLink(){
    $(".media-body").each(function(data){
      var hashTagRegex = /(^||\s)#([\w\d-]+)/g
      var userRegex = /(^||\s)@([\w\d-]+)/g
      var newText;
      newText = $(this).html().replace(hashTagRegex, "$1<a href='/tags/$2'>#$2</a>")
      newText = newText.replace(userRegex, "$1<a href='accounts/user/$2'>@$2</a>")
      $(this).html(newText)
    })
  }

  TagToLink()

});
