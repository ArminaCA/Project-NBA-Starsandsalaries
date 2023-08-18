d3.json('http://127.0.0.1:5000/Stats').then(data => {
  formatted_response = {};
  avg_ppg = [];

 for (let i=0; i<data.length; i++){
  if(Object.prototype.hasOwnProperty(formatted_response, data[i].POSITION)){
    formatted_response[data[i].POSITION].push(data[i].PPG);
  }else{
    formatted_response[data[i].POSITION] = [data[i].PPG]
  }
 }
 
 Object.keys(formatted_response).forEach(function(key) {
  let sum = 0;
  for (let i=0; i< formatted_response[key].length; i++){
    sum += formatted_response[key][i];
  }
  avg_ppg.push(sum/formatted_response[key].length);
  
});

let trace1 = {
  x: Object.keys(formatted_response),
  y: avg_ppg,
  type: 'bar'
};

let data_trace = [trace1];

let layout = {
  title: "Score by Position"
};

Plotly.newPlot("plot", data_trace, layout);} )

