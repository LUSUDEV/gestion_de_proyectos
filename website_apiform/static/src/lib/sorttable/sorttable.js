$.fn.sortTable = function(type, options)
{

var defaults = {
reverse : false,
column : 1
}

var options = $.extend(defaults, options);

id = "#"+this.attr("id");

var row = new Array();
$(id+" tr").each(function(i){
row[i] = [];
$(id+" tr:eq("+i+") td").each(function(index){
row[i][index] = $(this).text();
});
});

row.shift();

columna = defaults.column;
columna = columna - 1;

array_columna = new Array();
for (x=0; x <row.length; x++)
{
array_columna[x] = row[x][columna];
}

if (type == "number")
{
array_columna.sort(function (a,b){return a-b;});
}
else if(type == "letter")
{
function case_insensitive_comp(strA, strB) {
    return strA.toLowerCase().localeCompare(strB.toLowerCase());
}
array_columna.sort( case_insensitive_comp );
}
else if (type == "both")
{
function natSort(as, bs){
    var a, b, a1, b1, i= 0, L, rx=  /(\d+)|(\D+)/g, rd=  /\d/;
    if(isFinite(as) && isFinite(bs)) return as - bs;
    a= String(as).toLowerCase();
    b= String(bs).toLowerCase();
    if(a=== b) return 0;
    if(!(rd.test(a) && rd.test(b))) return a> b? 1: -1;
    a= a.match(rx);
    b= b.match(rx);
    L= a.length> b.length? b.length: a.length;
    while(i < L){
        a1= a[i];
        b1= b[i++];
        if(a1!== b1){
            if(isFinite(a1) && isFinite(b1)){
                if(a1.charAt(0)=== "0") a1= "." + a1;
                if(b1.charAt(0)=== "0") b1= "." + b1;
                return a1 - b1;
            }
            else return a1> b1? 1: -1;
        }
    }
    return a.length - b.length;
}
array_columna.sort( natSort );
}
else
{
array_columna.sort();
}

if (defaults.reverse == true)
{
array_columna.reverse();
}

registros_ordenados = new Array();

for (x=0; x<array_columna.length; x++)
{
for (y=0; y<row.length; y++)
{
for (v=0; v<row[0].length; v++)
{
if (array_columna[x] == row[y][v]){
for (n=0; n<row[0].length; n++)
{
registros_ordenados.push(row[y][n]);
}
}
}
}
}

$(id + " tr td").each(function(index){
$(this).text(registros_ordenados[index]);
});

};
