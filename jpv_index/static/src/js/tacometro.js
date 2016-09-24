$(document).ready(function(){
    console.debug("[tacometro] Custom JS for tacometro is loading...");
     var speedometer;
     $('#speedometer').css({"width":500,"height":500});
     var max_velocidad = $('#speedometer').attr("data-max_velocidad");
     console.log(max_velocidad);
     if (max_velocidad<20){
         Speedometer.themes['cfg_jp']['strings']='red'
         Speedometer.themes['cfg_jp']['hand']='red'
         Speedometer.themes['cfg_jp']['Black']='red'
         Speedometer.themes['cfg_jp']['handShine']='red'
         Speedometer.themes['cfg_jp']['marks']='red'
         Speedometer.themes['cfg_jp']['digits']='red'
         Speedometer.themes['cfg_jp']['ticks']='red'
         Speedometer.themes['cfg_jp']['handShineTo']='red'
         Speedometer.themes['cfg_jp']['rimArc']='red'
         }
    speedometer = new Speedometer ('speedometer', {
                theme: 'cfg_jp',
                min:0,
                max:100,
                value:1,
                meterTicksCount:10,
                meterMarksCount:5,
                });
            speedometer.draw ();
        
        function incrementalUpdate (){
            var target = speedometer.value () < speedometer.max () ?
                        max_velocidad : speedometer.min ();
            speedometer.animatedUpdate (target, 5000);
            }
        incrementalUpdate ();
        
    
    console.debug("[tacometro] Custom JS for tacometro is loading...");
    });
