// Which positions are most scorer in NBA
d3.json("http://127.0.0.1:5000/Stats").then((data) => {
  formatted_response = {};
  avg_ppg = [];

  for (let i = 0; i < data.length; i++) {
    if (Object.prototype.hasOwnProperty(formatted_response, data[i].POSITION)) {
      formatted_response[data[i].POSITION].push(data[i].PPG);
    } else {
      formatted_response[data[i].POSITION] = [data[i].PPG];
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
    x: Object.keys(formatted_response),
    y: avg_ppg,
    type: "bar",
  };

  let data_trace = [trace1];

  let layout = {
    title: "Score by Position",
  };

  Plotly.newPlot("plot", data_trace, layout);
});

// Top scorers by positions and ages between 2018-2023
fetch("http://127.0.0.1:5000/TopScorers")
  .then(response => response.json())
  .then(data => {

    const labels = data.map(d => d.NAME);
    const values = data.map(d => d.AGE);

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
      type: 'line',
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





