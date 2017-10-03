$('.remover').click(event => {
  event.preventDefault();
  let lixeira = $(event.target);
  title = lixeira.attr('title');
  $.get($SCRIPT_ROOT + '/deletar/' + title)
    .done(success => {
        if (success.id) {
            lixeira.closest('tr').remove()
        } else {
            alert('Você não pode remover este jogo.')
        }
    }
    )
    .fail(err => {
        console.log(err)
        alert('Não foi possível remover este jogo.')
    });
});


$('form input[type="file"]').change(event => {
  console.log(event.target.files)
  let arquivos = event.target.files;
  if(arquivos.length === 0) {
    console.log('sem imagem pra mostrar')
  } else {
      if(arquivos[0].type == 'image/jpeg') {
        $('#foto_jogo').remove();
        let imagem = $('<img id="foto_jogo" class="img-responsive">');
        imagem.attr('src', window.URL.createObjectURL(arquivos[0]));
        $('figure').prepend(imagem);
      } else {
        alert('Formato não suportado')
      }
  }
});