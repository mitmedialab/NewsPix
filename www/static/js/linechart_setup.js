var data = [{date: '2015-11-13', close: 20}, {date: '2015-11-15', close: 30}, {date: '2015-11-18', close: 4}, {date: '2015-12-1', close: 5}, {date: '2015-12-13', close: 25}, {date: '2015-12-25', close: 100} ]


function linechart(data){

  var today = new Date();
  var todayDateString = today.getFullYear() + '-' + (String(today.getMonth() + 1).length == 1 ? "0" + today.getMonth() + 1 : today.getMonth() + 1) + '-' + (String(today.getDate()).length == 1 ? "0" + today.getDate() : today.getDate());

  // Make sure chart projected to current date
  if (data[data.length - 1]['date'] != todayDateString){
    data.push({date: todayDateString, close: 0});
  }

  // Set the dimensions of the canvas / graph
  var margin = {top: 40, right: 50, bottom: 40, left: 50},
    width = 650 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

  // Parse the date / time
  var parseDate = d3.time.format("%Y-%m-%d").parse;

  // Set the ranges
  var x = d3.time.scale().range([0, width]);
  var y = d3.scale.linear().range([height, 0]);

  // Define the axes
  var xAxis = d3.svg.axis().scale(x)
      .orient("bottom").ticks(5);

  var yAxis = d3.svg.axis().scale(y)
      .orient("left").ticks(5);

  // Define the line
  var valueline = d3.svg.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.close); });
      
  // Adds the svg canvas
  var svg = d3.select("#svg_div")
      .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
      .append("g")
          .attr("transform", 
                "translate(" + margin.left + "," + margin.top + ")");

  data.forEach(function(d) {
        d.date = parseDate(d.date);
        d.close = +d.close;
    });

    

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.date}));
    y.domain([0, d3.max(data, function(d) { return d.close; })]);

    // Add the valueline path.
    svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));

    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    // Chart title
    svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .style("text-decoration", "underline")  
        .text("Total Chrome Installations");

    // x-axis label
    svg.append("text")
        .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom) + ")")
        .style("text-anchor", "middle")
        .text("Date");

    // y-axis label
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("# Installs");

    svg.selectAll("circle.line")
      .data(data)
      .enter().append("svg:circle")
      .attr("class", "line")
      .attr("cx", function(d) { return x(d.date)})
      .attr("cy", function(d) { return y(d.close)})
      .attr("r", 4);
}

$(document).ready(function(){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/analytics/installations", true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {
      var response = JSON.parse(xhr.responseText);
      linechart(response);
    }
  }
  xhr.send();
})
     
