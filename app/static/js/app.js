$(function() {
  var remover_jogo = function(e) {
    var lixeira = $(this);
    $.get($SCRIPT_ROOT + '/deletar/' + this.title,
    function(success) {
      lixeira.parent().parent().remove();
    });
    return false;
  };

  $('.remover').click(remover_jogo);
});