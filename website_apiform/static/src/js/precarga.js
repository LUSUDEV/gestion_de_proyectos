(function() {
    //eliminamos el scroll de la pagina
        $("body").css({"overflow-y":"hidden"});
        //guardamos en una variable el alto del que tiene tu browser que no es lo mismo que del DOM
        var alto=$(window).height();
        //agregamos en el body un div que sera que ocupe toda la pantalla y se muestra encima de todo
        $("body").append("<div id='pre-load-web'><div id='imagen-load'><img src='/website_apiform/static/src/images/Filling circles.gif'  /><br /><h5 style='font-family:sans-serif;'>Cargando...</h5></div>");
        //le damos el alto
        $("#pre-load-web").css({height:alto+"px"});
        //esta sera la capa que esta dento de la capa que muestra un gif
        $("#imagen-load").css({"margin-top":(alto/2)-30+"px"});

        $(window).load(function(){
                $("#pre-load-web").fadeOut(1000,function()
                { 
                   //eliminamos la capa de precarga
                   $(this).remove();
                   //permitimos scroll
                   $("body").css({"overflow-y":"auto"}); 
                });   
                
        });


})();
