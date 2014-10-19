$('#reg-form').bind('submit')

window.register_new_user = (event) ->
  pass = $('#reg input[name=pass]').val();
  if (pass.length < 5)
    alert 'El password debe ser de al menos 5 carácteres'
    event.preventDefault()
  else if (pass != $('#reg input[name=pass-re]').val())
    alert 'Los passwords no coinciden'
    event.preventDefault()