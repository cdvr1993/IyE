$('#reg-form').bind('submit')


window.register_new_user = (event) ->
  pass = $('#reg input[name=pass]').val();
  if (pass.length < 5)
    alert 'El password debe ser de al menos 5 carácteres'
    event.preventDefault()
  else if (pass != $('#reg input[name=pass-re]').val())
    alert 'Los passwords no coinciden'
    event.preventDefault()


_check_cart = () ->
  data = new Object()
  $("#cart_body tr").each( (key, row) ->
    name = $(row).attr('name')
    data[name] = new Object();
    delete_item = true
    new_qty = $(row).find("input[name='qty']").val()
    if new_qty != $(row).find("input#hidden_qty").val()
      data[name]['qty'] = $(row).find("input[name='qty']").val()
      delete_item = false
    is_checked = $(row).find("input[name='delete']")[0].checked
    if is_checked
      data[name]['delete'] = true
      delete_item = false
    if delete_item
      delete data[name]
  )
  return data


_update_indexes = (data) ->
  for item in data
    index = 1
    $("#cart_body tr").each( (key, row) ->
      if $(row).attr('name') == item['id']
        item['id'] = index
        return
      index++
    )

window.update_quantity = () ->
  data = _check_cart()
  $.post('',
    'csrfmiddlewaretoken': $("#form_cart input[name='csrfmiddlewaretoken']")[0].value
    'data': JSON.stringify(data),
    (data) ->
      $('div#alert_messages').remove()
      html = '<div id="alert_messages" onclick=\"$(this).remove();\">'
      msg = 0
      reload = false
      if data[0]['id'] == undefined
        html_content = "<div class=\"alert-#{data[0].type}\">#{data[0].info}</div>"
        msg++
      else
        html_content = ''
        _update_indexes(data)
        for item in data
          html_content += "<div class=\"alert-#{item.type}\">Producto #{item.id}: #{item.info}</div>"
          msg++
          if not reload and item.type == 'success'
            reload = true
      html += "#{html_content}</div>"
      if msg > 0
        $('#id_main_section').append(html)
      if reload
        setTimeout(() ->
          window.location.reload()
        , 1200 * msg)
      return null
  )
  return null


window.check_unisex = () ->
  if $('#select_kind option:selected').attr('data-unisex') == 'True'
    $('#select_gender').hide()
    $('#label_gender').hide()
  else
    $('#select_gender').show()
    $('#label_gender').show()


window.get_colors = () ->
  $gender = $('#select_gender')
  $kind = $('#select_kind')
  $('#product_price').text(' $' + $("#price_#{$kind.val()}").val())
  $.get("/colors?kind=#{$kind.val()}&gender=#{$gender.val()}", (data) ->
    $div_colors = $('div#colors')
    $div_colors.empty()
    $select_colors = $('select#select_colors')
    if $select_colors.length
      $select_colors.empty()
    thumbnails = ''
    options = ''
    $(data).each(() ->
      f = this.fields
      thumbnails += ('<img class="shirt" title="' + f.name + '" src="/static/img/store/color/' + f.image_name + '.jpg" />')
      if $select_colors.length
        options += ('<option value="' + this.pk + '">' + f.name + '</option>')
    )
    $div_colors.html(thumbnails)
    if $select_colors.length
      $select_colors.html(options)
  )


window.checkout = () ->
  if confirm("¿Seguro que desea realizar el pedido?") == true
    $.post('/cart/checkout',
      {'csrfmiddlewaretoken': $("#form_checkout input[name='csrfmiddlewaretoken']").val()},
      (data) ->
        $div_msg = $('#msg_checkout')
        $div_msg.empty()
        if data == 'True'
          html = '<div class="alert alert-success" onclick="$(this).remove();">Pedido realizado con éxito</div>'
          setTimeout(() ->
            window.location.reload()
          , 2000)
        else
          html = '<div class="alert alert-error" onclick="$(this).remove();">' +
            'Ocurrió un error a la hora de levantar el pedido</div>'
        $div_msg.append(html)
    )