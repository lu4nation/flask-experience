$('.remover').click(event => {
  event.preventDefault();
  let lixeira = $(event.target);
  title = lixeira.attr('title');
  $.get($SCRIPT_ROOT + '/deletar/' + title)
    .done(success =>
        lixeira.closest('tr').remove()
    )
    .fail(err => {
        console.log(err)
        alert('Não foi possível concluir a requisição')
    });
});