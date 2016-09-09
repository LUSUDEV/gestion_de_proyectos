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
            {y: '2015 Q1', item1: 6810, item2: 1914},
            {y: '2015 Q2', item1: 5670, item2: 4293},
            {y: '2015 Q3', item1: 4820, item2: 3795},
            {y: '2015 Q4', item1: 15073, item2: 5967},
            {y: '2016 Q1', item1: 10687, item2: 4460},
            {y: '2016 Q2', item1: 8432, item2: 5713},
            {y: '2016 Q3', item1: 10687, item2: 4460},
            {y: '2016 Q4', item1: 8432, item2: 5713}
          ],
          xkey: 'y',
          ykeys: ['item1', 'item2'],
          labels: ['Item 1', 'Item 2'],
          lineColors: ['#a0d0e0', '#3c8dbc'],
          hideHover: 'auto'
        });

        // LINE CHART
        var line = new Morris.Line({
          element: 'line-chart',
          resize: true,
          data: [
            {y: '2014 Q1', item1: 2666},
            {y: '2014 Q2', item1: 2778},
            {y: '2014 Q3', item1: 4912},
            {y: '2014 Q4', item1: 3767},
            {y: '2015 Q1', item1: 6810},
            {y: '2015 Q2', item1: 5670},
            {y: '2015 Q3', item1: 4820},
            {y: '2015 Q4', item1: 15073},
            {y: '2016 Q1', item1: 10687},
            {y: '2016 Q2', item1: 8432},
            {y: '2016 Q3', item1: 10687},
            {y: '2016 Q4', item1: 8432}
          ],
          xkey: 'y',
          ykeys: ['item1'],
          labels: ['Item 1'],
          lineColors: ['#3c8dbc'],
          hideHover: 'auto'
        });

        //DONUT CHART
        var donut = new Morris.Donut({
          element: 'sales-chart',
          resize: true,
          colors: ["#3c8dbc", "#f56954", "#00a65a"],
          data: [
            {label: "Financiamiento EPT", value: 33},
            {label: "Financiamiento OBPP", value: 33},
            {label: "Financiamiento Otras", value: 33},

          ],
          hideHover: 'auto'
        });
        //BAR CHART
        var bar = new Morris.Bar({
          element: 'bar-chart',
          resize: true,
          data: [
            {y: '2010', a: 50, b: 55},
            {y: '2011', a: 60, b: 65},
            {y: '2012', a: 70, b: 80},
            {y: '2013', a: 75, b: 65},
            {y: '2014', a: 50, b: 40},
            {y: '2015', a: 85, b: 90},
            {y: '2016', a: 100, b: 100}
          ],
          barColors: ['#00a65a', '#f56954'],
          xkey: 'y',
          ykeys: ['a', 'b'],
          labels: ['Proyectos Aprobados', 'Proyectos Financiados'],
          hideHover: 'auto'
        });
      });