$(function () {
        "use strict";

        // AREA CHART
        var area = new Morris.Area({
          element: 'revenue-chart',
          resize: true,
          data: [
            {y: '2014 Q1', item1: 2666, item2: 2666},
            {y: '2014 Q2', item1: 2778, item2: 2294},
            {y: '2014 Q3', item1: 4912, item2: 1969},
            {y: '2014 Q4', item1: 3767, item2: 3597},
            {y: '2015 Q1', item1: 15000, item2: 1914},
            {y: '2015 Q2', item1: 5670, item2: 4293},
            {y: '2015 Q3', item1: 4820, item2: 3795},
            {y: '2016 Q4', item1: 19073, item2: 8267},
            {y: '2016 Q1', item1: 10687, item2: 4460},
            {y: '2016 Q2', item1: 8432, item2: 5713}
          ],
          xkey: 'y',
          ykeys: ['item1', 'item2'],
          labels: ['Proyectos', 'En Ejecución'],
          lineColors: ['#a0d0e0', '#3c8dbc'],
          hideHover: 'auto'
        });

       
      });