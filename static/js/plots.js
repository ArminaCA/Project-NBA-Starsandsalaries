// Which positions are most scorer in NBA
d3.json("http://127.0.0.1:5000/Stats").then((data) => {
  formatted_response = {};
  avg_ppg = [];

  for (let i = 0; i < data.length; i++) {
    if (data[i].PPG != null) {
      if (formatted_response.hasOwnProperty(data[i].POSITION)) {
        formatted_response[data[i].POSITION].push(data[i].PPG);
      } else {
        formatted_response[data[i].POSITION] = [data[i].PPG];
      }
    }
  }

  Object.keys(formatted_response).forEach(function (key) {
    let sum = 0;
    for (let i = 0; i < formatted_response[key].length; i++) {
      sum += formatted_response[key][i];
    }
    avg_ppg.push(sum / formatted_response[key].length);
  });

  let trace1 = {
    x: ["Center", "Guard-Forward", "Forward-Center", "Forward", "Guard", "Forward-Guard", "Center-Forward"],
    y: avg_ppg,
    name: "positions",
    type: "bar",
  };

  let data_trace = [trace1];

  let layout = {
    title: "Average Score by Position",
  };

  Plotly.newPlot("avgppgperpos", data_trace, layout);
});

// Top Ten Scorers by Position
d3.json("http://127.0.0.1:5000/TopScorebyPosition").then((data) => {
  let trace1 = {
    x: data["C"].NAME,
    y: data["C"].PPG,
    name: "Center",
    type: "bar"
  };

  let trace2 = {
    x: data["C-F"].NAME,
    y: data["C-F"].PPG,
    name: "Center-Foward",
    type: "bar"
  };

  let trace3 = {
    x: data["F"].NAME,
    y: data["F"].PPG,
    name: "Foward",
    type: "bar",
  };

  let trace4 = {
    x: data["F-C"].NAME,
    y: data["F-C"].PPG,
    name: "Foward-Center",
    type: "bar",
  };
  
  let trace5 = {
    x: data["F-G"].NAME,
    y: data["F-G"].PPG,
    name: "Foward-Guard",
    type: "bar",
  };

  
  let trace6 = {
    x: data["G"].NAME,
    y: data["G"].PPG,
    name: "Guard",
    type: "bar",
  };

  let trace7 = {
    x: data["G-F"].NAME,
    y: data["G-F"].PPG,
    name: "Guard-Foward",
    type: "bar",
  };

  let data_trace = [trace1, trace2, trace3, trace4, trace5, trace6, trace7];

  let layout = {
    title: "Top Five Points Per Game by Position",
    barmode: "stack"
  };

  Plotly.newPlot("topfivescores", data_trace, layout);
});

// Top Ten Scorers by Position
d3.json("http://127.0.0.1:5000/TopSalary").then((data) => {
  let trace1 = {
    x: data["C"].NAME,
    y: data["C"].SALARY,
    name: "Center",
    type: "bar"
  };

  let trace2 = {
    x: data["C-F"].NAME,
    y: data["C-F"].SALARY,
    name: "Center-Foward",
    type: "bar"
  };

  let trace3 = {
    x: data["F"].NAME,
    y: data["F"].SALARY,
    name: "Foward",
    type: "bar",
  };

  let trace4 = {
    x: data["F-C"].NAME,
    y: data["F-C"].SALARY,
    name: "Foward-Center",
    type: "bar",
  };
  
  let trace5 = {
    x: data["F-G"].NAME,
    y: data["F-G"].SALARY,
    name: "Foward-Guard",
    type: "bar",
  };

  
  let trace6 = {
    x: data["G"].NAME,
    y: data["G"].SALARY,
    name: "Guard",
    type: "bar",
  };

  let trace7 = {
    x: data["G-F"].NAME,
    y: data["G-F"].SALARY,
    name: "Guard-Foward",
    type: "bar",
  };

  let data_trace = [trace1, trace2, trace3, trace4, trace5, trace6, trace7];

  let layout = {
    title: "Top Five Salaries by Position",
    barmode: "stack"
  };

  Plotly.newPlot("topfivesalary", data_trace, layout);
});

// Distribution of positions in the NBA
fetch("http://127.0.0.1:5000/PositionCounts")
  .then(response => response.json())
  .then(data => {

    const labels = data.map (d => d.POSITION);
    const values = data.map (d => d.COUNT);
  
    // Here we generate a set of random colors for each segment.
    const backgroundColors = data.map(() => `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.5)`);

    // Get the canvas context
    var ctx = document.getElementById('myPieChart').getContext('2d');

    var myPieChart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: backgroundColors
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          }
        }
      }
    });
  });

  /*
  // Top10 highest paid players by their position
  fetch("http://127.0.0.1:5000/TopSalary")
  .then(response => response.json())
  .then(data => {

    const labels = data.map(player => `${player.NAME} (${player.POSITION})`);
  
    const values = data.map(player => player.SALARY);

    // Generate a set of random colors for each bar.
    const backgroundColors = data.map(() => `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.5)`);

    var ctx = document.getElementById('top10SalaryChart').getContext('2d');

  
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Salary',
          data: values,
          backgroundColor: backgroundColors,
          borderColor: 'rgba(75, 192, 192, 1)', 
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          x: {
            beginAtZero: true
          }
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
          }
        }
      }
    });
  });
*/

var map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);

var franchiseStats = {};

// Demonstrate states on the map by their stats. (Total scores and team value)
fetch("http://127.0.0.1:5000/FranchiseStats")
    .then(response => response.json())
    .then(data => {
        // Convert data into an object
        data.forEach(item => {
            franchiseStats[item.FRANCHISE] = {
                TotalSalary: item.TotalSalary,
                AvgPPG: item.AvgPPG
            };
            // marker for each franchise to the map using the provided coordinates
            if (item.coordinates) {
                const marker = L.marker(item.coordinates).addTo(map);
                marker.bindPopup(`
                    <strong>${item.FRANCHISE}</strong><br>
                    Total Salary: ${item.TotalSalary}<br>
                    Avg PPG: ${item.AvgPPG}
                `);
            }
        });
    });